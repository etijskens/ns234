# -*- coding: utf-8 -*-

"""Tests for ns234 package."""

import ns234

import numpy as np

def test_coordinates():
    """Test converting coordinates.
    png_coordinates obtained by opening kadaster-ns234.png in gimp, and reading of the pixel coordinates.
    Pixel coordinates have the origin in the upper left corner, so the X-axis is correct, but the Y-axis is
    in the wrong direction.
    """
    png_coordinates = { 
        'A' : (316,544),
        'B' : (527,544),
        '0' : (633,468),
        '1' : (533,484),
        '2' : (444,461),
        '3' : (453,431),
        '4' : (398,416),
        '5' : (412,368),
        '6' : (426,319),
        '7' : (534,350),
        '8' : (635,353),
        '9' : (635,406),
        '10' : (534,405),
        '11' : ( 84,372),
        '12a': (136,149),
        '12b': (145,122),
        # '13' : (,),
        # '14' : (,),
        # '15' : (,),
        # '16' : (,),
        # '17' : (,),
        # '18' : (,),
        # '19' : (,),
        # '20' : (,),
        # '21' : (,),
        # '22' : (,),
    }
    coordinates = {}
    scale_factor = 20 / ns234.distance(png_coordinates['A'],png_coordinates['B'])
    print(f"{scale_factor=}")
    digits = 2
    for id,xy in png_coordinates.items():
        x = round( scale_factor * xy[0], digits)
        y = round(-scale_factor * xy[1], digits)
        coordinates[id] = (x,y)
        print(f"{id=} = ({x},{y})")



# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_coordinates

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')

# eof