#!/usr/bin/env python3

"""
6.101 Lab 1:
Image Processing
"""

import math

from PIL import Image

# NO ADDITIONAL IMPORTS ALLOWED!
#% is remainder. // is floor division (how many times it goes in)

def get_pixel(image, colx, rowy, boundary_behavior= "None"):
    """Considers all three boundary behaviors through simplified booleans"""
    wx =colx not in range(image["width"])
    hy =rowy not in range(image["height"])
    if wx or hy:
        if boundary_behavior== "zero":    
            return 0
        if boundary_behavior== "wrap":
            if wx:
                colx = colx % int(image["width"])
            if hy:
                rowy = rowy % int(image["height"])
        if boundary_behavior== "extend":

            if wx:
                if colx<0:
                    colx = 0
                if colx> int(image["width"])-1:
                    colx = int(image["width"]-1)    
            if hy:
                if rowy<0:
                    rowy= 0
                if rowy> int(image["height"]-1):
                    rowy= int(image["height"]-1)  
    index = rowy*int(image["width"]) + colx
    return image["pixels"][index]


def set_pixel(image, colx, rowy, color):
    """Goes to image dictionary and sets the proper pixel values"""
    index = rowy*int(image["width"]) + colx
    image["pixels"].insert(index, color)


def apply_per_pixel(image, func):
    """piecewise processing, applying function to each new pixel value in image square"""
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [],
    }
    for rowy in range(int(image["height"])):
        for colx in range(int(image["width"])):
            color = get_pixel(image, colx, rowy)
            new_color = func(color)
            set_pixel(result, colx, rowy, new_color)
    return result


def inverted(image):
    """takes in image and sets function thorugh lambda inversion"""
    return apply_per_pixel(image, lambda color: 255-color)


# HELPER FUNCTIONS

def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of "zero", "extend", or "wrap", return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with "height", "width", and "pixels" keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE:
    Let kernel input simply be a list of number values. Nothing fancy.
    """
    if boundary_behavior is None:
        return None
    kern_leg= int(math.sqrt(len(kernel)))
    backtrack= kern_leg//2
    bb= boundary_behavior
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [],
    }
    for rowy in range(int(image["height"])):
        for colx in range(int(image["width"])):
            # allows for control of kernel linear combination through superimposed kernel and hypothetical pixel values outside range
            print(kernel)
            lin_combo = [get_pixel(image, int(colx-backtrack+x), int(rowy-backtrack+y), bb)* kernel[y*kern_leg + x] for y in range(kern_leg) for x in range(kern_leg)]
            color= sum(lin_combo)
            set_pixel(result, colx, rowy, color)
    return result
def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    # processes the pixel lists to ensure values are rounded and remain in 0-255 range
    dots= [round(val) for val in image["pixels"]]
    for ind in range(len(dots)):
        if dots[ind]>255:
            dots[ind]=255
        if dots[ind]<0:
            dots[ind]= 0   
    return {
        "height": image["height"],
        "width": image["width"],
        "pixels": dots
    }


# FILTERS
def make_blurredkern(n):
    """helper function to create a uniformly distributed matrix"""
    return [1/n**2 for i in range(n**2)]
    
    
def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    kernel = make_blurredkern(kernel_size)
    # ensures correlation matrix from uniform kernel superimposed to image, giving blur
    return round_and_clip_image(correlate(image, kernel, boundary_behavior= 'extend'))


def sharpened(image, n):
    """applies a matrix subtraction from twice image dictionary pixels, take away the values of blurred matrix"""
    B = blurred(image, n)
    # zip allows for corresponding linear combination
    dots = [(2*i)-b for i,b in zip(image["pixels"], B["pixels"] )]
    result= {
        "height": image["height"],
        "width": image["width"],
        "pixels": dots
    }
    return round_and_clip_image(result)
def edges(image):
    """edge behavior from two specific kernel correlations"""
    kern_1= [-1, -2, -1, 0,  0,  0, 1, 2,  1]
    kern_2= [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    O_1 = correlate(image, kern_1, boundary_behavior= 'extend')
    O_2 = correlate(image, kern_2, boundary_behavior= 'extend')
    # once more, zip allows for proper iiner product correspondence
    O_list = [round(math.sqrt(i**2 + j**2)) for i, j in zip(O_1["pixels"], O_2["pixels"])]
    result = {
        "height": image["height"],
        "width":  image["width"],
        "pixels": O_list
    }
    return round_and_clip_image(result)
    

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the "mode" parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    # fish = load_greyscale_image('C:/Users/gava1/Downloads/image_processing/image_processing/test_images/bluegill.png')
    # inter = inverted(fish)
    # save_greyscale_image(inter, 'C:/Users/gava1/Downloads/image_processing/image_processing/test_images/blue_solved.png' )
    # piggy = load_greyscale_image('C:/Users/gava1/Downloads/image_processing/image_processing/test_images/pigbird.png')
    # kernel= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
# 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # inter = round_and_clip_image(correlate(piggy, kernel, boundary_behavior= 'wrap'))
    # save_greyscale_image(inter, 'C:/Users/gava1/Downloads/image_processing/image_processing/test_images/piggy_wrap_solved.png')
    # cat = load_greyscale_image('C:/Users/gava1/Downloads/image_processing/image_processing/test_images/cat.png')
    # inter= blurred(cat, 13)
    # save_greyscale_image(inter, 'C:/Users/gava1/Downloads/image_processing/image_processing/test_images/cat_wrap_solved.png')
    # python = load_greyscale_image('C:/Users/gava1/Downloads/image_processing/image_processing/test_images/python.png')
    # inter= sharpened(python, 11)
    # save_greyscale_image(inter, 'C:/Users/gava1/Downloads/image_processing/image_processing/test_images/python_solved.png')
    construct = load_greyscale_image('C:/Users/gava1/Downloads/image_processing/image_processing/test_images/construct.png')
    # inter = edges(construct)
    # save_greyscale_image(inter, 'C:/Users/gava1/Downloads/image_processing/image_processing/test_images/construct_solved.png')