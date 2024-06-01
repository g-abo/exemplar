#!/usr/bin/env python3

"""
6.101 Lab 2:
Image Processing 2
"""

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image


def get_pixel(image, colx, rowy, boundary_behavior="None"):
    """Returns pixel value at some col and row for image.
    Considers different return behavior for out of range"""
    wx = colx not in range(image["width"])
    hy = rowy not in range(image["height"])
    if wx or hy:
        if boundary_behavior == "zero":
            return 0
        if boundary_behavior == "wrap":
            if wx:
                colx = colx % int(image["width"])
            if hy:
                rowy = rowy % int(image["height"])
        if boundary_behavior == "extend":

            if wx:
                colx = max(0, min(colx, int(image["width"]) - 1))
            if hy:
                rowy = max(0, min(rowy, int(image["height"]) - 1))
    index = rowy * int(image["width"]) + colx
    return image["pixels"][index]


def set_pixel(image, colx, rowy, color):
    """Inserts a new color value at the colx and rowy of an image"""
    index = rowy * int(image["width"]) + colx
    image["pixels"].insert(index, color)


def apply_per_pixel(image, func):
    """applies the function of interest to color of each pixel
    without modifying the original"""
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
    """Each pixel is applied the inversion function for color"""
    return apply_per_pixel(image, lambda color: 255 - color)


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
    kern_leg = int(math.sqrt(len(kernel)))
    backtrack = kern_leg // 2
    bb = boundary_behavior
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [],
    }
    for rowy in range(int(image["height"])):
        for colx in range(int(image["width"])):
            lin_combo = [
                get_pixel(
                    image, int(colx - backtrack + x), int(rowy - backtrack + y), bb
                )
                * kernel[y * kern_leg + x]
                for y in range(kern_leg)
                for x in range(kern_leg)
            ]
            color = sum(lin_combo)
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
    # DO WE MUTATE IMAGE[PIXELS]?
    dots = [round(val) for val in image["pixels"]]
    for ind in range(len(dots)):
        if dots[ind] > 255:
            dots[ind] = 255
        if dots[ind] < 0:
            dots[ind] = 0
    return {"height": image["height"], "width": image["width"], "pixels": dots}


def make_blurredkern(n):
    """Helper function to instantiate uniform density array
    given leg size of a square: n"""
    return [1 / n**2 for i in range(n**2)]


def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    kernel = make_blurredkern(kernel_size)
    return round_and_clip_image(correlate(image, kernel, boundary_behavior="extend"))


def sharpened(image, n):
    """Applies the matrix calculation of twice the original, take away the
    blurred matrix"""
    blur = blurred(image, n)
    dots = [(2 * i) - b for i, b in zip(image["pixels"], blur["pixels"])]
    result = {"height": image["height"], "width": image["width"], "pixels": dots}
    return round_and_clip_image(result)


def edges(image):
    """Applies the matrix calculation of twice the first correlation, add
    the second distinct correlation"""
    kern_1 = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    kern_2 = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    o_1 = correlate(image, kern_1, boundary_behavior="extend")
    o_2 = correlate(image, kern_2, boundary_behavior="extend")
    o_list = [
        round(math.sqrt(i**2 + j**2)) for i, j in zip(o_1["pixels"], o_2["pixels"])
    ]
    result = {"height": image["height"], "width": image["width"], "pixels": o_list}
    return round_and_clip_image(result)


# ###################################################################################
# VARIOUS FILTERS


def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """

    def rgb_functer(color_image):
        """Takes in color image as dictionary format with rgb tuples in the pixels list.
        Outputs the proper color image of the same format, after applying the proper
        function enclosed in the outer function"""
        red = [pix[0] for pix in color_image["pixels"]]
        green = [pix[1] for pix in color_image["pixels"]]
        blue = [pix[2] for pix in color_image["pixels"]]
        rgb_lists = [red, green, blue]
        dicts_out = []
        for color_lists in rgb_lists:
            dict_in = {
                "height": color_image["height"],
                "width": color_image["width"],
                "pixels": color_lists,
            }
            dicts_out.append(filt(dict_in))
        return {
            "height": color_image["height"],
            "width": color_image["width"],
            "pixels": [
                (r, g, b)
                for r, g, b in zip(
                    dicts_out[0]["pixels"],
                    dicts_out[1]["pixels"],
                    dicts_out[2]["pixels"],
                )
            ],
        }

    return rgb_functer


def make_blur_filter(kernel_size):
    """Feeds kernel size to enclosure of the function that will be returned
    ,which itself can return a blur of an image"""
    k_size = kernel_size

    def one_arg_blur(image):
        """Given image, returns its blurred"""
        return blurred(image, k_size)

    return one_arg_blur


def make_sharpen_filter(kernel_size):
    """Feeds the kernel size to enclosure of the funcion that will be returned
    ,which itself can return a sharpened of image"""
    k_size = kernel_size

    def one_arg_sharpen(image):
        """Given image, returns its sharpen"""
        return sharpened(image, k_size)

    return one_arg_sharpen


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """

    def chaining(image):
        """function that takes in the list of functions to apply to an image
        the, in left to right order"""
        functions = filters
        photo = {
            "height": image["height"],
            "width": image["width"],
            "pixels": image["pixels"],
        }
        for func in functions:
            photo = func(photo)
        return photo

    return chaining


# SEAM CARVING


# Optional Helper Functions for Seam Carving


def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    return {
        "height": image["height"],
        "width": image["width"],
        "pixels": [
            round(0.299 * r + 0.587 * g + 0.114 * b) for r, g, b in image["pixels"]
        ],
    }


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def two_to_1d(image, colx, rowy):
    """Helper function to black-box the colx and rowy conversion
    to 1D index position of image"""
    return rowy * int(image["width"]) + colx


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    # inherits the energy values from the Energy matrix
    energy_values = [num for num in energy["pixels"]]
    dict_cum = {"height": energy["height"], "width": energy["width"], "pixels": []}
    # dynamic programming of minimum of top 3 adjacent minimum pixel values
    for rowy in range(int(dict_cum["height"])):
        for colx in range(int(dict_cum["width"])):
            index = two_to_1d(dict_cum, colx, rowy)
            if rowy == 0:
                dict_cum["pixels"].append(energy_values[index])
            else:
                left, up, right = colx - 1, colx, colx + 1
                directions = [left, up, right]
                if left < 0:
                    directions.pop(0)
                if right > int(dict_cum["width"]) - 1:
                    directions.pop(2)
                prevs = [
                    dict_cum["pixels"][two_to_1d(dict_cum, col, rowy - 1)]
                    for col in directions
                ]
                energy_val = energy_values[index] + min(prevs)
                set_pixel(dict_cum, colx, rowy, energy_val)
    return dict_cum


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    # Index to fill for scrapping
    indices_to_scrap = []
    index_start = two_to_1d(cem, 0, int(cem["height"]) - 1)
    index_end = two_to_1d(cem, int(cem["width"]) - 1, int(cem["height"]) - 1)
    # From the values of the cem, determines the index of the min value of last row
    minim_index, _ = min(
        [(i, val) for i, val in enumerate(cem["pixels"][index_start : index_end + 1])],
        key=lambda x: x[1],
    )
    s_rowy = int(cem["height"]) - 1
    minim_index += s_rowy * int(cem["width"])
    indices_to_scrap.append(minim_index)
    s_colx = minim_index - (s_rowy) * int(cem["width"])
    # From top to bottom, determine the index of the min values of the adjacencies
    for rowy in reversed(range(int(cem["height"]))):
        if rowy != s_rowy:
            left, up, right = s_colx - 1, s_colx, s_colx + 1
            directions = [left, up, right]
            if left < 0:
                directions.pop(0)
            if right > int(cem["width"]) - 1:
                directions.pop(2)
            min_index, _ = min(
                [
                    (
                        rowy * int(cem["width"]) + adj,
                        cem["pixels"][rowy * int(cem["width"]) + adj],
                    )
                    for adj in directions
                ],
                key=lambda x: x[1],
            )
            indices_to_scrap.append(min_index)
            s_rowy = rowy
            s_colx = min_index - (s_rowy) * int(cem["width"])
    return indices_to_scrap


def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    # returns an unmodified dictionary with the proper removed seams
    dict_copy = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"],
    }
    shrunk = []
    for pix_i in range(len(dict_copy["pixels"])):
        if pix_i not in seam:
            shrunk.append(dict_copy["pixels"][pix_i])
    # mindful enough to reduce the width by 1 after removal
    dict_copy["width"] = dict_copy["width"] - 1
    dict_copy["pixels"] = shrunk

    return dict_copy


def image_with_seam(image, seam):
    """Helper function to stretch out the Image,
    rather than shrinking, based on the minimal energy"""
    dict_copy = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"],
    }
    inflate = []
    for pix_i in range(len(dict_copy["pixels"])):
        if pix_i not in seam:
            inflate.append(dict_copy["pixels"][pix_i])
        if pix_i in seam:
            inflate.extend([dict_copy["pixels"][pix_i]] * 2)
    dict_copy["width"] = dict_copy["width"] + 1
    dict_copy["pixels"] = inflate

    return dict_copy


# Main Seam Carving Implementation


def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image. Returns a new image.
    """
    photo_repl = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"],
    }
    filters = [compute_energy, cumulative_energy_map, minimum_energy_seam]
    for _ in range(ncols):
        photo_in = greyscale_image_from_color_image(photo_repl)
        scrap_indices = filter_cascade(filters)(photo_in)
        photo_repl = image_without_seam(photo_repl, scrap_indices)
    return photo_repl


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES


def custom_feature(image, ncols):
    """Opposite of Seam carving"""
    photo_repl = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"],
    }
    filters = [compute_energy, cumulative_energy_map, minimum_energy_seam]
    for _ in range(ncols):
        photo_in = greyscale_image_from_color_image(photo_repl)
        extra_indices = filter_cascade(filters)(photo_in)
        photo_repl = image_with_seam(photo_repl, extra_indices)
    return photo_repl


def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
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
    by the 'mode' parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


# if __name__ == "__main__":
# filter1 = edges
# blur_format = make_blur_filter(5)
# color_format= color_filter_from_greyscale_filter(make_blur_filter(9))
# color_format= color_filter_from_greyscale_filter(make_sharpen_filter(7))
# code in this block will only be run when you explicitly run your script,
# and not when the tests are being run.  this is a good place for
# generating images, etc.
# twocats = load_color_image(
# inter = filter_cascade([filter1, filter1, blur_format, filter1])(frog)
# inter = custom_feature(twocats, 100)
# inter_1 = compute_energy(test)
# inter_2= cumulative_energy_map(inter_1)
# inter_3 = minimum_energy_seam(inter_2)
# print(inter_1, inter_2, inter_3)
