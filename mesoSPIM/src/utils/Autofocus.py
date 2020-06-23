import numpy as np

def get_width_in_k(self,image):

    k_spectrum = np.fft.fft2(image)
    k_spectrum = np.fft.fftshift(k_spectrum)
    k_spectrum = np.abs(k_spectrum)
    k_spectrum = np.multiply(k_spectrum,k_spectrum)

    mass = np.sum(k_spectrum)
    prob = k_spectrum/mass

    y_list = np.asmatrix(range(image.shape[0]))
    x_list = np.asmatrix(range(image.shape[1]))
    mean_x = np.sum(np.dot(prob, np.transpose(x_list)))
    mean_y = np.sum(np.dot(y_list,prob))
    width_x = np.sum(np.multiply(prob,np.transpose(np.multiply(x_list,x_list))))
    width_x = np.sqrt(width_x-mean_x*mean_x)
    width_y = np.sum(np.multiply(np.multiply(x_list,x_list),prob))
    width_y = np.sqrt(width_y-mean_y*mean_y)
    return (width_x + width_y)/2

def autofocus(self):
    '''
    # function 1: get the size of the image in k-space
    # input: image
    # process: FFT, second moment(standard deviation)
    # output: standard deviation
#   
    # function 2: push button for autofocus 
    # input: step size  
    # determination:
    # 1) move positive, get std
    # 2) move negative, get std
    # 3) move toward the direction with larger std
    # 4) while loop: while new std > current std
    #       move stage toward the same direction
    #       take images
    #       send image to function 1, get new std
    '''
    # magic number
    f_step = 2
    ##############

    current_f = self.parent.state['position']['f_pos']
    new_f = current_f + f_step
    self.sig_move_absolute.emit({'f_abs':new_f})
    self.open_shutters()  

    self.snap_image()
    image = self.camera_worker.camera.get_image()
    image = np.rot90(image)  
    width_positive = self.get_width_in_k(image) 

    new_f = current_f - f_step
    self.sig_move_absolute.emit({'f_abs':new_f})
    self.snap_image()
    image = self.camera_worker.camera.get_image()
    image = np.rot90(image) 
    width_negative = self.get_width_in_k(image)

    if width_negative > width_positive:
        f_step = f_step*-1
        current_width = width_negative
    else:
        current_width = width_positive
    new_width = current_width
    n = 0
    
    while current_width-new_width < 0 and n != 0:
        current_width = new_width
        current_f = new_f
        new_f = current_f + f_step
        self.sig_move_absolute.emit({'f_abs':new_f})
        self.snap_image()
        image = self.camera_worker.camera.get_image()
        image = np.rot90(image)
        new_width = self.get_width_in_k(image)
        n = n+1
    
    self.self.sig_move_absolute.emit({'f_abs':new_f})
    self.close_shutters()
    print(current_f)