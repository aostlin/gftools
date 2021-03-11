"""3D simple cubic lattice.

:half_bandwidth: The half_bandwidth corresponds to a nearest neighbor hopping
                 of `t=D/6`

"""
import numpy as np

from numpy.lib.scimath import sqrt
from mpmath import mp

from gftool._util import _u_ellipk


def gf_z(z, half_bandwidth=1):
    r"""Local Green's function of 3D simple cubic lattice.

    Has a van Hove singularity (continuous but not differentiable) at
    `abs(z) = D/3`.

    Implements equations (1.24 - 1.26) from [delves2001]_.

    Parameters
    ----------
    z : complex np.ndarray or complex
        Green's function is evaluated at complex frequency `z`.
    half_bandwidth : float
        Half-bandwidth of the DOS of the simple cubic lattice.
        The `half_bandwidth` corresponds to the nearest neighbor hopping
        :math:`t=D/6`.

    Returns
    -------
    gf_z : complex np.ndarray or complex
        Value of the simple cubic Green's function at complex energy 'z'.

    References
    ----------
    .. [economou2006] Economou, E. N. Green's Functions in Quantum Physics.
       Springer, 2006.
    .. [delves2001] Delves, R. T. and Joyce, G. S., Ann. Phys. 291, 71 (2001).
       https://doi.org/10.1006/aphy.2001.6148

    Examples
    --------
    >>> ww = np.linspace(-1.1, 1.1, num=500)
    >>> gf_ww = gt.lattice.simplecubic.gf_z(ww)

    >>> import matplotlib.pyplot as plt
    >>> _ = plt.axhline(0, color='black', linewidth=0.8)
    >>> _ = plt.axvline(-1/3, color="black", linewidth=0.8)
    >>> _ = plt.axvline(+1/3, color="black", linewidth=0.8)
    >>> _ = plt.plot(ww.real, gf_ww.real, label=r"$\Re G$")
    >>> _ = plt.plot(ww.real, gf_ww.imag, label=r"$\Im G$")
    >>> _ = plt.ylabel(r"$G*D$")
    >>> _ = plt.xlabel(r"$\omega/D$")
    >>> _ = plt.xlim(left=ww.min(), right=ww.max())
    >>> _ = plt.legend()
    >>> plt.show()

    """
    D_inv = 3 / half_bandwidth
    z = D_inv * z
    z_sqr = z**-2
    xi = sqrt(1 - sqrt(1 - z_sqr)) / sqrt(1 + sqrt(1 - 9*z_sqr))
    denom_inv = 1 / ((1 - xi)**3 * (1 + 3*xi))
    k2 = 16 * xi**3 * denom_inv
    gf_z = (1 - 9*xi**4) * (2 / np.pi * _u_ellipk(k2))**2 * denom_inv / z
    return D_inv * gf_z

def dos_mp(eps, half_bandwidth=1):
    r"""Multi-precision DOS of non-interacting 3D simple cubic lattice.

    Has a van Hove singularity (continuous but not differentiable) at
    `abs(t) = D/3`.

    Implements Eq. 7.37 from [joyce1973] for the special case of eps == 0, otherwise calls gf_z_mp.

    Parameters
    ----------
    eps : float ndarray or float
        DOS is evaluated at points `eps`.

    Returns
    -------
    dos_mp : float ndarray or float
        The value of the DOS.

    Examples
    --------
    >>> eps = np.linspace(-1.1, 1.1, num=500)
    >>> with.workdps(15):
    >>>     dos_mp = [gt.lattice.simplecubic.dos_mp(ee, half_bandwidth=1) for ee in eps]
    >>> dos_mp = np.array(dos_mp, dtype=np.float64)

    >>> import matplotlib.pyplot as plt
    >>> _ = plt.plot(eps, dos_mp)
    >>> _ = plt.xlabel(r"$\epsilon/D$")
    >>> _ = plt.ylabel(r"DOS * $D$")
    >>> _ = plt.axvline(1/3, color="black", linestyle="--")
    >>> _ = plt.axvline(0, color='black', linewidth=0.8)
    >>> _ = plt.ylim(bottom=0)
    >>> _ = plt.xlim(left=eps.min(), right=eps.max())
    >>> plt.show()

    References
    ----------
    .. [economou2006] Economou, E. N. Green's Functions in Quantum Physics.
       Springer, 2006.
    .. [joyce1973] G. S. Joyce, Phil. Trans. of the Royal Society of London A, 273, 583 (1973).
    .. [katsura1971] S. Katsura et al., J. Math. Phys., 12, 895 (1971).

    """
    D_inv = 3 / half_bandwidth
    eps = mp.fabs(eps)
    if eps == 0:
        km2 = 0.25 * (2 - mp.sqrt(3))
        return D_inv * (2 / mp.pi**2) * mp.ellipk(km2) * mp.ellipk(1 - km2) / mp.pi
    return - mp.im( gf_z_mp(eps, half_bandwidth) ) / mp.pi

def gf_z_mp(z, half_bandwidth=1):
    r"""Multi-precision Green's function of non-interacting 3D simple cubic lattice.

    Has a van Hove singularity (continuous but not differentiable) at
    `abs(z) = D/3`.

    Implements equations (1.24 - 1.26) from [delves2001]_.

    Parameters
    ----------
    z : mpmath.mpc or mpc_like
        Green's function is evaluated at complex frequency `z`.
    half_bandwidth : mp.mpf or mpf_like
        Half-bandwidth of the DOS of the simple cubic lattice.
        The `half_bandwidth` corresponds to the nearest neighbor hopping
        :math:`t=D/6`.

    Returns
    -------
    gf_z : mpmath.mpc
        Value of the Green's function at complex energy 'z'.

    References
    ----------
    .. [economou2006] Economou, E. N. Green's Functions in Quantum Physics.
       Springer, 2006.
    .. [delves2001] Delves, R. T. and Joyce, G. S., Ann. Phys. 291, 71 (2001).
       https://doi.org/10.1006/aphy.2001.6148

    Examples
    --------
    >>> ww = np.linspace(-1.1, 1.1, num=500)
    >>> gf_ww = np.array([gt.lattice.simplecubic.gf_z_mp(wi) for wi in ww])

    >>> import matplotlib.pyplot as plt
    >>> _ = plt.axhline(0, color='black', linewidth=0.8)
    >>> _ = plt.axvline(-1/3, color="black", linewidth=0.8)
    >>> _ = plt.axvline(+1/3, color="black", linewidth=0.8)
    >>> _ = plt.plot(ww.real, gf_ww.astype(complex).real, label=r"$\Re G$")
    >>> _ = plt.plot(ww.real, gf_ww.astype(complex).imag, label=r"$\Im G$")
    >>> _ = plt.ylabel(r"$G*D$")
    >>> _ = plt.xlabel(r"$\omega/D$")
    >>> _ = plt.xlim(left=ww.min(), right=ww.max())
    >>> _ = plt.legend()
    >>> plt.show()

    """
    D_inv = 3 / half_bandwidth
    z = D_inv * mp.mpc(z)
    z_sqr = 1 / z**2
    xi = mp.sqrt(1 - mp.sqrt(1 - z_sqr)) / mp.sqrt(1 + mp.sqrt(1 - 9*z_sqr))
    k2 = 16 * xi**3 / ((1 - xi)**3 * (1 + 3*xi))
    green = (1 - 9*xi**4) * (2 * mp.ellipk(k2) / mp.pi)**2 / ((1 - xi)**3 * (1 + 3*xi)) / z

    return D_inv * green
