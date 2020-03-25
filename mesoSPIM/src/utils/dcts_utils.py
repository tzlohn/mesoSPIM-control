'''
Utility functions for measuring image quality using a DCTS (Shannon Entropy 
of the Discrete Cosine transform )

'''

from numba import jit
import numpy as np
from scipy.fftpack import dct

def dct2D(image, dct_cutoff_range=150):
    '''
    Discrete cosine transform of an image

    Args:
        image (np.ndarray): 2D numpy array representing an image
        dct_cutoff_range (int): Max number of X and Y coefficients to calculate

    Returns:
        np.ndarray: 2D numpy array, DCT of the input

    '''
    y=dct(image, type=2, n=dct_cutoff_range, axis=1, norm='ortho')
    return dct(y, type=2, n=dct_cutoff_range, axis=0, norm='ortho')

def l2_image(image):
    '''
    L2 (Fröbenius) norm of an image matrix: Square root of the sum of the absolute 
    squares of its elements

    Args:
        image (np.ndarray): 2D numpy array representing an image
    
    Returns:
        numpy.float64: 

    '''
    return np.linalg.norm(image)

@jit(nopython=True)
def entropy(dct_norm_image, cutoff_range=150):
    '''
    Custom image entropy measure to allow a simplified calculation of the DCTS.
    See Royer et al, Nat Biotech (2016), for a Java example, see here:

    https://github.com/MicroscopeAutoPilot/autopilot/blob/master/src/java/autopilot/measures/dcts/dcts3d/DCTS3D.java

    To speed up the processing, this entropy measure allows to specify a cutoff - max number of 
    x and y values (pixels) in the DCT that should be included in the calculation. This restricts 
    the iteration range to fewer elements. 

    Args:
        image (np.ndarray): 2D numpy array representing an image
        cutoff_range (int): Maximum x and y range to be included for the entropy calculation
    
    Returns:
        numpy.float64: 

    '''

    entropy = 0
    for x in range(cutoff_range):
        for y in range(cutoff_range):
            value = dct_norm_image[x,y]
            if value>0:
                entropy += np.abs(value)*np.log(value)
            elif value<0:
                entropy += np.abs(value)*np.log(-value)
            else:
                pass
            
    return -entropy

def dcts(image, dct_cutoff_range=150, entropy_cutoff_range=150):
    '''
    Custom dcts measure based on a simplified calculation of the entropy.
    See Royer et al, Nat Biotech (2016), for a Java example, see here:

    https://github.com/MicroscopeAutoPilot/autopilot/blob/master/src/java/autopilot/measures/dcts/dcts3d/DCTS3D.java

    To speed up the processing, this entropy measure allows to specify a cutoff - max number of 
    x and y values (pixels) in the DCT that should be included in the calculation. This restricts 
    the iteration range to fewer elements. 

    Args:
        image (np.ndarray): 2D numpy array representing an image
        dct_cutoff_range (int): Maximum DCT coefficients to calculate
        entropy_cutoff_range (int): Maximum DCT coefficients to include in the entropy calculation
    
    Returns:
        numpy.float64: 

    '''
    dct_result = dct2D(image, dct_cutoff_range)
    dct_norm_image = np.divide(dct_result, l2_image(dct_result)) # Divide by the L2 norm
    return entropy(dct_norm_image, entropy_cutoff_range)