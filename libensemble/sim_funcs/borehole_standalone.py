import numpy as np
import time
import sys
from libensemble.sim_funcs.cwpsim import bounds


def borehole_func(H):
    """This evaluates the Borehole function for n-by-8 input
    matrix x, and returns the flow rate through the Borehole. (Harper and Gupta, 1983)
    input:

    Parameters
    ----------
    theta: matrix of dimentsion (n, 6),
        theta[:,0]: Tu, transmissivity of upper aquifer (m^2/year)
        theta[:,1]: Tl, transmissivity of lower aquifer (m^2/year)
        theta[:,2]: Hu, potentiometric head of upper aquifer (m)
        theta[:,3]: Hl, potentiometric head of lower aquifer (m)
        theta[:,4]: r, radius of influence (m)
        theta[:,5]: Kw, hydraulic conductivity of borehole (m/year)

    x: matrix of dimension (n, 3), where n is the number of input configurations:
        .. code-block::
        x[:,0]: rw, radius of borehole (m)
        x[:,1]: L, length of borehole (m)
        x[:,2]: a in {0, 1}. type label for modification

    Returns
    -------

    vector of dimension (n, 1):
        flow rate through the Borehole (m^3/year)

    """

    thetas = H['thetas']
    xs = H['x']

    assert np.all(thetas >= bounds[:6, 0]) and \
        np.all(thetas <= bounds[:6, 1]) and \
        np.all(xs[:, :-1] >= bounds[6:, 0]) and \
        np.all(xs[:, :-1] <= bounds[6:, 1]), "Point not within bounds"

    taxis = 1
    if thetas.ndim == 1:
        taxis = 0
    (Tu, Tl, Hu, Hl, r, Kw) = np.split(thetas, 6, taxis)

    xaxis = 1
    if xs.ndim == 1:
        xaxis = 0
    (rw, L) = np.split(xs[:, :-1], 2, xaxis)

    numer = 2 * np.pi * Tu * (Hu - Hl)
    denom1 = 2 * L * Tu / (np.log(r/rw) * rw**2 * Kw)
    denom2 = Tu / Tl

    f = (numer / (np.log(r/rw) * (1 + denom1 + denom2))).reshape(-1)

    f[xs[:, -1] == 1] = f[xs[:, -1].astype(bool)] ** (1.5)

    return f


if __name__ == '__main__':
    if len(sys.argv) > 1:
        H = np.load(sys.argv[1])
    else:
        sys.exit('Need supply input file with H array')
    delay = None
    if len(sys.argv) > 2:
        delay = float(sys.argv[2])

    if delay is not None:
        time.sleep(delay)
    f = borehole_func(H)
    print(f[0])
