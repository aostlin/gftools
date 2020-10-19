"""Functionality related or derived from the Fermi and Bose statistics.

Per default, the functions refer to Fermi statistics,
a tailing '_b' indicates Bose statistics instead.

"""
import numpy as np

from scipy import linalg
from scipy.special import expit, logit


def bose_fct(eps, beta):
    r"""Return the Bose function `1/(exp(βϵ)-1)`.

    Parameters
    ----------
    eps : complex or float or array_like
        The energy at which the Bose function is evaluated.
    beta : float
        The inverse temperature :math:`beta = 1/k_B T`.

    Returns
    -------
    bose_fct : complex of float np.ndarray
        The Bose function, same type as eps.

    """
    betaeps = np.asanyarray(beta*eps)
    res = np.empty_like(betaeps)
    small = betaeps < 700
    res[small] = 1./np.expm1(betaeps[small])
    # avoid overflows for big numbers using negative exponents
    res[~small] = -np.exp(-betaeps[~small])/np.expm1(-betaeps[~small])
    return res


def fermi_fct(eps, beta):
    r"""Return the Fermi function `1/(exp(βϵ)+1)`.

    For complex inputs the function is not as accurate as for real inputs.

    Parameters
    ----------
    eps : complex or float or ndarray
        The energy at which the Fermi function is evaluated.
    beta : float
        The inverse temperature :math:`beta = 1/k_B T`.

    Returns
    -------
    fermi_fct : complex of float or ndarray
        The Fermi function, same type as eps.

    See Also
    --------
    fermi_fct_inv : The inverse of the Fermi function for real arguments

    """
    z = eps*beta
    try:
        return expit(-z)  # = 0.5 * (1. + tanh(-0.5 * beta * eps))
    except TypeError:
        pass  # complex arguments not handled by expit
    z = np.asanyarray(z)
    pos = z.real > 0
    res = np.empty_like(z)
    res[~pos] = 1./(np.exp(z[~pos]) + 1)
    exp_m = np.exp(-z[pos])
    res[pos] = exp_m/(1 + exp_m)
    return res


def fermi_fct_d1(eps, beta):
    r"""Return the 1st derivative of the Fermi function.

    .. math:: -β\exp(βϵ)/{(\exp(βϵ)+1)}^2

    Parameters
    ----------
    eps : float or float ndarray
        The energy at which the Fermi function is evaluated.
    beta : float
        The inverse temperature :math:`beta = 1/k_B T`.

    Returns
    -------
    fermi_fct_d1 : float or float ndarray
        The Fermi function, same type as eps.

    See Also
    --------
    fermi_fct

    """
    fermi = fermi_fct(eps, beta=beta)
    return -beta*fermi*(1-fermi)


def fermi_fct_inv(fermi, beta):
    """Inverse of the Fermi function.

    This is e.g. useful for integrals over the derivative of the Fermi function.

    Parameters
    ----------
    fermi : float or float ndarray
        The values of the Fermi function
    beta : float
        The inverse temperature :math:`beta = 1/k_B T`.

    Returns
    -------
    fermi_fct_inv : float or float ndarray
        The inverse of the Fermi function `fermi_fct(fermi_fct_inv, beta)=fermi`.

    See Also
    --------
    fermi_fct

    """
    return -logit(fermi)/beta


def matsubara_frequencies(n_points, beta):
    r"""Return *fermionic* Matsubara frequencies :math:`iω_n` for the points `n_points`.

    Parameters
    ----------
    n_points : int array_like
        Points for which the Matsubara frequencies :math:`iω_n` are returned.
    beta : float
        The inverse temperature :math:`beta = 1/k_B T`.

    Returns
    -------
    matsubara_frequencies : complex ndarray
        Array of the imaginary Matsubara frequencies

    Examples
    --------
    >>> gt.matsubara_frequencies(range(1024), beta=1)
    array([0.+3.14159265e+00j, 0.+9.42477796e+00j, 0.+1.57079633e+01j, ...,
           0.+6.41827379e+03j, 0.+6.42455698e+03j, 0.+6.43084016e+03j])

    """
    n_points = np.asanyarray(n_points).astype(dtype=int, casting='safe')
    return 1j * np.pi / beta * (2*n_points + 1)


def matsubara_frequencies_b(n_points, beta):
    r"""Return *bosonic* Matsubara frequencies :math:`iν_n` for the points `n_points`.

    Parameters
    ----------
    n_points : int ndarray
        Points for which the Matsubara frequencies :math:`iν_n` are returned.
    beta : float
        The inverse temperature :math:`beta = 1/k_B T`.

    Returns
    -------
    matsubara_frequencies : complex ndarray
        Array of the imaginary Matsubara frequencies

    Examples
    --------
    >>> gt.matsubara_frequencies_b(range(1024), beta=1)
    array([0.+0.00000000e+00j, 0.+6.28318531e+00j, 0.+1.25663706e+01j, ...,
           0.+6.41513220e+03j, 0.+6.42141538e+03j, 0.+6.42769857e+03j])

    """
    n_points = np.asanyarray(n_points).astype(dtype=int, casting='safe')
    return 2j * np.pi / beta * n_points


def pade_frequencies(num: int, beta):
    """Return `num` *fermionic* Padé frequencies :math:`iz_p`.

    The Padé frequencies are the poles of the approximation of the Fermi
    function with `2*num` poles [ozaki2007]_.
    This gives an non-equidistant mesh on the imaginary axis.

    Parameters
    ----------
    num : int
        Number of positive Padé frequencies.
    beta : float
        The inverse temperature :math:`beta = 1/k_B T`.

    Returns
    -------
    izp : (num) complex np.ndarray
        Positive Padé frequencies.
    resids : (num) float np.ndarray
        Residue of the Fermi function corresponding to `izp`. The residue is
        given relative to true residue of the Fermi function corresponding to
        the poles at Matsubara frequencies. This allows to use Padé frequencies
        as drop-in replacement.
        The actual residues would be `-resids/beta`.

    References
    ----------
    .. [ozaki2007] Ozaki, Taisuke. Continued Fraction Representation of the
       Fermi-Dirac Function for Large-Scale Electronic Structure Calculations.
       Physical Review B 75, no. 3 (January 23, 2007): 035123.
       https://doi.org/10.1103/PhysRevB.75.035123.

    .. [hu2010] J. Hu, R.-X. Xu, and Y. Yan, “Communication: Padé spectrum
       decomposition of Fermi function and Bose function,” J. Chem. Phys., vol.
       133, no. 10, p.  101106, Sep. 2010, https://doi.org/10.1063/1.3484491

    """
    num = 2*num
    a = -np.diagflat(range(1, 2*num, 2))
    b = np.zeros_like(a, dtype=np.float_)
    np.fill_diagonal(b[1:, :], 0.5)
    np.fill_diagonal(b[:, 1:], 0.5)
    eig, v = linalg.eig(a, b=b, overwrite_a=True, overwrite_b=True)
    sort = np.argsort(eig)
    izp = 1j/beta * eig[sort]
    resids = (0.25*v[0]*np.linalg.inv(v)[:, 0]*eig**2)[sort]
    assert np.allclose(-izp[:num//2][::-1], izp[num//2:])
    assert np.allclose(resids[:num//2][::-1], resids[num//2:])
    assert np.all(~np.iscomplex(resids))
    return izp[num//2:], resids.real[num//2:]
