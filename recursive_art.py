"""Generates random art!!"""

import random
import math
from PIL import Image


def random_function():
    '''returns a random function'''
    random_num = random.random()
    number_of_funcs = 8
    if random_num <= (1/number_of_funcs):
        return "prod"
    elif random_num <= (2/number_of_funcs):
        return "avg"
    elif random_num <= (3/number_of_funcs):
        return "cos_pi"
    elif random_num <= (4/number_of_funcs):
        return "sin_pi"
    elif random_num <= (5/number_of_funcs):
        return "geo_mean"
    elif random_num <= (6/number_of_funcs):
        return "square"
    elif random_num <= (7/number_of_funcs):
        return "x"
    else:
        return "y"


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    # base case: depth = 0, return either x or y
    if min_depth <= 0:
        random_num = random.randint(0, 1)
        if random_num:
            return "x"
        return "y"
    else:
        rand_func = random_function()
        return [rand_func, build_random_function(min_depth-1, max_depth),
                build_random_function(min_depth-1, max_depth)]


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0] == "x":
        return x
    elif f[0] == "y":
        return y
    else:
        x_local = evaluate_random_function(f[1], x, y)
        y_local = evaluate_random_function(f[2], x, y)
        if f[0] == "prod":
            return x_local*y_local
        elif f[0] == "avg":
            return (x + y)/2
        elif f[0] == "cos_pi":
            return math.cos(math.pi*x_local)
        elif f[0] == "sin_pi":
            return math.sin(math.pi*x_local)
        elif f[0] == "geo_mean":
            return math.sqrt((x_local**2)*(y_local**2))
        elif f[0] == "square":
            return x**2


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # input range as input_interval_end minus input_interval_start
    input_range = input_interval_end - input_interval_start
    # output range
    output_range = output_interval_end - output_interval_start
    # scale as output_range/input_range, used to find saled value
    scale = output_range/input_range

    # finds val (initially in input_range scale) in output_range scale)
    offset_val = val - input_interval_start
    mapped_val = offset_val*scale + output_interval_start

    return mapped_val


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
