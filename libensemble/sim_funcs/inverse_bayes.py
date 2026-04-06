"""
Simulator computing a proxy likelihood function for inverse Bayesian inference
testing. Evaluates the six_hump_camel function as a stand-in likelihood,
returning the result in the ``"like"`` output field. Used with the
``persistent_inverse_bayes`` generator in calibration tests.
"""

__all__ = ["likelihood_calculator"]

import numpy as np

from libensemble.sim_funcs.six_hump_camel import six_hump_camel_func


def likelihood_calculator(H, persis_info, sim_specs, _):
    """
    Evaluates likelihood
    """
    H_o = np.zeros(len(H["x"]), dtype=sim_specs["out"])
    for i, x in enumerate(H["x"]):
        H_o["like"][i] = six_hump_camel_func(x)

    return H_o, persis_info, "custom_status"
