# -*- coding: utf-8 -*-

"""
Package ns234
=======================================

Top-level package for ns234.
"""

__version__ = "0.0.0"

import numpy as np
from datetime import datetime


def rodrigues(b, a, theta, left=False):
    """Right rotate vector b around vector a (axis) over angle theta.

    if left is True, does a left rotation
    """
    if left:
        theta *= -1

    if isinstance(b,list):
        b = np.array(b,dtype=float)
        b = np.array(b,None)

    if isinstance(a,list):
        a = np.array(a,dtype=float)
        a = np.array(a, None)
    a /= np.linalg.norm(a)

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    brot = np.outer(b, cos_theta) + np.outer(np.cross(a,b), sin_theta) + np.dot(a,b)  * np.outer(a, (1 - cos_theta))

    if left: # reset theta
        theta *= -1

    return brot


def orientations(latitude, beta, num = 10):
    """
    """
    alpha = np.deg2rad(90 - latitude)
    beta  = np.deg2rad(beta)

    a = [-np.sin(alpha), 0, np.cos(alpha)]
    b = [np.cos(alpha + beta), 0, np.sin(alpha + beta)]

    theta = np.linspace(start=-np.pi, stop=np.pi, num=101)
    # num must be odd to include theta = 0
    brot = rodrigues(b, a, theta, left=True)
    above_horizon = np.where(brot[2,:]>0)
    brot = brot[:,above_horizon[0]]
    theta = theta[above_horizon[0]]
    return brot, theta


def theta2hour(theta):
    """Convert angle theta (degrees) to (sun) hour.

    0 degrees corresponds to 12 o'clock, when the sun is highest.
    """
    hour = theta * 12/np.pi + 12
    return hour


def hour2theta(hour):
    """Inverse of theta2hour.
    """
    theta = (hour - 12)*(np.pi/12)
    return theta


def date2beta(d=None):
    year = 365.242
    zero = datetime(2022,3,21) # begin of spring (equinox)
    if d is None:
        d = datetime.today()
    t = (d - zero).days * (2*np.pi/year)
    beta = 23.5 * np.sin(t)
    return beta


class Sun:
    """

    Based on http://notesfromnoosphere.blogspot.com/2012/05/simple-geometry-of-sun-paths.html
    """
    def __init__(self, latitude='leuven'):
        if latitude == 'leuven':
            latitude = 50.87959
        self.latitude = latitude


def distance(t0,t1):
    return np.linalg.norm(np.array(t1) - np.array(t0))
