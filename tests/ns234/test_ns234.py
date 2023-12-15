# -*- coding: utf-8 -*-

"""Tests for ns234 package."""

import ns234

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

def test_coordinates():
    """Test converting coordinates.
    png_coordinates obtained by opening kadaster-ns234.png in gimp, and reading of the pixel coordinates.
    Pixel coordinates have the origin in the upper left corner, so the X-axis is correct, but the Y-axis is
    in the wrong direction.
    """
    png_coordinates = { 
        'A' : (316,544),
        'B' : (527,544),
        '0' : (633,486),
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
        '13' : (377,305),
        '14' : (476,334),
        '15' : (476,275),
        '16' : (637,278),
        '17' : (117,273),
        '18' : (139,173),
        '19' : (187,183),
        '20' : (185,197),
        '21' : (193,198),
        '22' : (174,285),
    }
    # z-coordinates in meter
    z0 = 0.10       # niveau berging/wasruimte/garage
    z1 = 1.00       # niveau keuken/sas/atelier/speelruimte/tv-ruimte/inkomhal
    z2 = z1 + 0.80  # niveau tuin

    z_coordinates = {
    'A':  0,
    'B':  0,
    '0':  0,
    '1':  z1,
    '2':  z1,
    '3':  z1,
    '4':  z1,
    '5':  z1,
    '6':  z1,
    '7':  z1,
    '8':  0,
    '9':  0,
    '10': z1,
    '11': z2,
    '12a': z2,
    '12b': z2,
    '13': z2,
    '14': z1,
    '15': 0,
    '16': 0,
    '17': z2,
    '18': z2,
    '19': z2,
    '20': z2,
    '21': z2,
    '22': z2,
    }
    # Converteer png coordinates naar meter
    coordinates = {}
    scale_factor = 20 / ns234.distance(png_coordinates['A'],png_coordinates['B'])
    print(f"{scale_factor=}")
    digits = 2
    origin = png_coordinates['0']
    for id,xy in png_coordinates.items():
        y = - round( scale_factor * (xy[0] - origin[0]), digits)
        x =   round(-scale_factor * (xy[1] - origin[1]), digits)
        coordinates[id] = (x,y)
        print(f"{id=} = ({x},{y})")

    # voeg twee punten toe voor het tuin niveau
    v34 = np.array(coordinates['4']) - np.array(coordinates['3'])
    l34 = np.linalg.norm(v34)
    u34 = v34/l34
    coordinates['11a'] = np.array(coordinates['2']) + (l34 + 2.20)*u34
    coordinates['13b'] = np.array(coordinates['6']) + (2.20)*u34
    print(f"11a = {coordinates['11a']}")
    print(f"13b = {coordinates['13b']}")
    # Maak lines
    lines = [['0','1','2','11','12a','12b','13','6','7','8','9','0']
            ,['2','3','4','5','6']
            ,['5','10','9']
            ,['14','15','16','8']
            ,['17','18','19','20','21','22','17']
            ,['11a','13b']                          # begin van tuinniveau
            ]
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect='equal')
    for line in lines:
        for i1 in range(1,len(line)):
            xy0 = coordinates[line[i1-1]]
            xy1 = coordinates[line[i1]]
            plt.plot([xy0[0],xy1[0]], [xy0[1],xy1[1]])
    # y0 = - coordinates['0'][0]
    # x0 =   coordinates['0'][1]
    #
    # plt.plot( [x0 + 0.5, x0 + 14],[-y0 + 15, -y0 + 15], '--')     # maximale diepte gelijkvloerse bouwlaag
    # plt.plot( [x0 - 12, x0 - 12], [y0 + 0.5, y0 + 13.5],'--')   # maximale diepte bouwlagen verdiepingen
    # plt.plot( [x0 - 9, x0 - 6], [y0, y0 + 12.5],'--')           # schuine lijn loodrecht op tuin

    v76 = np.array(coordinates['6']) - np.array(coordinates['7'])
    u76 = v76 / np.linalg.norm(v76)
    alpha76 = np.rad2deg( np.arccos(u76[0]) )
    cotg76 = v76[0] / v76[1]
    print(f'{u76=}, {alpha76=}, {cotg76=}')
    print(f'{5.5 * cotg76}')
    print(f'{2.5 * cotg76}')

    # plt.show()

def test_perspective():
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=[8, 14])
    ax1 = fig.add_subplot(211, projection='3d')
    ax2 = fig.add_subplot(212, projection='3d')

    x = np.linspace(-1, 1, 100)
    y = np.linspace(-1, 1, 100)

    ax1.plot(x, y, 0, 'b', lw=3)
    ax1.plot(x, y, 1, 'r', lw=3)

    ax2.plot(x, y, 0, 'b', lw=3)
    ax2.plot(x, y, 1, 'r', lw=3)

    ax1.view_init(90, 0)
    ax2.view_init(-90, 0)

    plt.show()

def test_rodrigues():

    alpha = np.deg2rad(90 - 51)
    beta = np.deg2rad(12)

    a = [-np.sin(alpha), 0, np.cos(alpha)]
    b = [np.cos(alpha + beta), 0, np.sin(alpha + beta)]

    theta = np.linspace(start=-np.pi, stop=np.pi, num=100)
    brot = ns234.rodrigues(b,a,theta)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.plot(brot[0,:], brot[1,:], brot[2,:], 'o')
    plt.show()

def test_rodrigues1():
    a = [0,0,1]
    b = [1,0,0]
    theta = 0
    brot = ns234.rodrigues(b,a,theta)
    print(brot)
    theta = np.pi/2
    brot = ns234.rodrigues(b,a,theta)
    print(brot)
    theta = np.pi
    brot = ns234.rodrigues(b,a,theta)
    print(brot)
    theta = 3*np.pi/2
    brot = ns234.rodrigues(b,a,theta)
    print(brot)

def test_rodrigues2():
    a = [0,0,1]
    b = [1,0,1]
    theta = 0
    brot = ns234.rodrigues(b,a,theta)
    print(brot)
    theta = np.pi/2
    brot = ns234.rodrigues(b,a,theta)
    print(brot)
    theta = np.pi
    brot = ns234.rodrigues(b,a,theta)
    print(brot)
    theta = 3*np.pi/2
    brot = ns234.rodrigues(b,a,theta)
    print(brot)

def test_rodrigues3():
    a = [0,0,1]
    b = [1,0,1]
    theta = [0, np.pi/2, np.pi, 3*np.pi/2]
    brot = ns234.rodrigues(b,a,theta)
    print(brot)

def test_rodrigues4():
    a = [1,0,1]
    b = [1,0,0]
    theta = [0, np.pi / 2, np.pi, 3 * np.pi / 2]
    theta = np.linspace(start=0, stop=2*np.pi, num=20)

    brot = ns234.rodrigues(b,a,theta)
    print(brot)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.plot(brot[0,:], brot[1,:], brot[2,:])
    plt.show()

def test_orientations():
    latitude = 51
    brot, theta = ns234.orientations(latitude,-12)
    hour = ns234.theta2hour(theta)
    for i in range(len(theta)):
        print(f"{hour[i]} {theta[i]}, {brot[:, i].transpose()}")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.plot(brot[0,:], brot[1,:], brot[2,:])
    plt.show()


def test_date2beta():
    for d in [datetime(2021,12,21), datetime(2022,3,21), datetime(2022,6,21), datetime(2022,9,21), ]:
        print( d, ns234.date2beta(d))


def test_date2beta():

    d0 = datetime(2022,1,1)
    for d in range(365):
        
        print( d, ns234.date2beta(d))



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