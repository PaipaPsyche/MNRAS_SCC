"""
Created on Wed Feb 13 11:44:18 2019

@author: David Paipa
"""
import numpy as np
import matplotlib.pyplot as plt
#from astropy.convolution import Gaussian2DKernel,convolve
#import scipy.linalg as linalg
#from mpl_toolkits.mplot3d import Axes3D

DATA=np.loadtxt("voronoi_3D.txt")

n_side=int(np.amax(DATA[:,0])+1)
PERT_V=np.zeros([n_side,n_side,n_side])

print("compilando resultados voronoi . . .")
for i in range (n_side**3):
    PERT_V[int(DATA[i,0]),int(DATA[i,1]),int(DATA[i,2])]=int(DATA[i,3])
np.save("pert_voronoi.npy",PERT_V)
