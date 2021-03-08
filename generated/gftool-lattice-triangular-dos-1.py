eps = np.linspace(-1.5, 1.5, num=500)
dos = gt.lattice.triangular.dos(eps, half_bandwidth=1)

import matplotlib.pyplot as plt
_ = plt.plot(eps, dos)
_ = plt.axvline(-2/3, color='black', linewidth=0.8)
_ = plt.axvline(+4/3, color='black', linewidth=0.8)
_ = plt.xlabel(r"$\epsilon/D$")
_ = plt.ylabel(r"DOS * $D$")
_ = plt.axvline(0, color='black', linewidth=0.8)
_ = plt.ylim(bottom=0)
_ = plt.xlim(left=eps.min(), right=eps.max())
plt.show()
