# -*- coding: utf-8 -*-

"""
Package ns234
=======================================

Top-level package for ns234.
"""

__version__ = "0.0.0"

import numpy as np

def distance(p,q):
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    d = np.sqrt(dx*dx + dy*dy)
    return d
