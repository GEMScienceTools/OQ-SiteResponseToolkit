# =============================================================================
#
# Copyright (C) 2010-2017 GEM Foundation
#
# This file is part of the OpenQuake's Site Response Toolkit (OQ-SRTK)
#
# OQ-SRTK is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# OQ-SRTK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# with this download. If not, see <http://www.gnu.org/licenses/>
#
# Author: Valerio Poggi
#
# =============================================================================
"""
The module contains several functions to derive and manipulate average
soil parameters, such as travel-time average velocity and site kappa.
"""

import numpy as _np
import scipy.optimize as _spo


# =============================================================================

def depth_weighted_average(thickness, soil_prop, depth):
    """
    Compute the weighted average of a soil property at
    arbitrary depth.

    :param numpy.array tickness:
        array of layer's thicknesses in meters (half-space is 0.)

    :param numpy.array soil_prop:
        array of soil properties (e.g. slowness, density)

    :param float depth:
        averaging depth in meters

    :return float mean_value:
        the weighted mean of the given soil property
    """

    mean_value = 0
    total_depth = 0

    for tk, sp in zip(thickness[:-1], soil_prop[:-1]):
        if (tk + total_depth) < depth:
            mean_value += tk*sp/depth
        else:
            mean_value += (depth - total_depth)*sp/depth
            break
        total_depth += tk

    if total_depth == _np.sum(thickness[:-1]):
        mean_value += (depth - total_depth)*soil_prop[-1]/depth

    return mean_value


# =============================================================================

def compute_site_kappa(thickness, s_velocity, s_quality, depth=[]):
    """
    This function calucalte the site attenuation parameter Kappa(0)
    for a given soil profile down to an arbitrary depth.

    :param numpy.array tickness:
        array of layer's thicknesses in meters (half-space is 0.)

    :param numpy.array s_velocity:
        array of layer's shear-wave velocities in m/s

    :param numpy.array s_quality:
        array of layer's shear-wave quality factors (adimensional)

    :param float depth:
        averaging depth in meters; if depth is not specified,
        the last layer interface is used instead
    """

    # If depth not given, using the whole profile
    if not depth:
        depth = _np.sum(thickness)

    # Kappa vector
    layer_kappa = depth/(s_velocity*s_quality)

    # Computing the average kappa of the profile
    kappa0 = depth_weighted_average(thickness, layer_kappa, depth)

    return kappa0