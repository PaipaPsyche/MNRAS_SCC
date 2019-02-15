"""
Created on Thu Feb 14 14:07:00 2019

@author: David Paipa
"""
import numpy as np
import matplotlib.pyplot as plt
#from astropy.convolution import Gaussian2DKernel,convolve
#import scipy.linalg as linalg
#from mpl_toolkits.mplot3d import Axes3D
CALIBRACION=1

#print(sigma," inicio")
PERT_W=np.load("pert_test.npy")
PERT_V=np.load("pert_voronoi.npy")
n_side=np.shape(PERT_W)[0]
MASS=np.ones([n_side,n_side,n_side])


n_cumulos=int(np.amax(PERT_W))


CALIBRACION=np.zeros([n_cumulos,3])

COORDS_CM=np.zeros([n_cumulos,3])

#print(sigma," doing ")
for i in range(1,n_cumulos+1):
    coords=np.array(np.where(PERTW==i))
    n_datos=len(coords[0])
    for dim in range(3):
        while((len(np.where((np.where(coords[dim]==(n_side-1)))or(coords[dim]==0))[0])!=0)and(CALIBRACION[sigma-1,i-1,dim]<n_side)):
            CALIBRACION[sigma-1,i-1,dim]=CALIBRACION[sigma-1,i-1,dim]+1
            coords[dim]=(coords[dim]+1)%n_side
            
            
            ##### HAY QUE ENCONTRAR:
            #parametros de centrado
            #coords CM
            #momoento inercia
            