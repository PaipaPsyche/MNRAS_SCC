"""
Created on Wed Feb 13 10:36:23 2019

@author: David Paipa
"""
import numpy as np
import matplotlib.pyplot as plt
#from astropy.convolution import Gaussian2DKernel,convolve
#import scipy.linalg as linalg
from mpl_toolkits.mplot3d import Axes3D
import sys

grupo=int(sys.argv[1])

PERT_W=np.load("pert_test.npy")
PERT_V=np.load("pert_voronoi.npy")

n_size=PERT_V.shape[0]
n_grupos=int(np.amax(PERT_V))
ex,ey,ez=[0,n_size-1],[0,n_size-1],[0,n_size-1]

#grupo=356

x1,y1,z1=np.where(PERT_W==grupo)
x2,y2,z2=np.where(PERT_V==grupo)

print(grupo)

fig=plt.figure(figsize=[16,10])
ax1=fig.add_subplot(121,projection="3d")
_=ax1.scatter(ex,ey,ez,c="k",s=0.1)
sc1=ax1.scatter(x1,y1,z1,c="r",s=1,alpha=0.4)


ax2=fig.add_subplot(122,projection="3d")
_=ax2.scatter(ex,ey,ez,c="k",s=0.1)
sc2=ax2.scatter(x2,y2,z2,c="b",s=1,alpha=0.4)
fig.savefig("grupo_"+str(grupo)+".png")
plt.close()
