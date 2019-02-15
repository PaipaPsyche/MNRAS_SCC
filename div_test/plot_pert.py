"""
Created on Sat Feb  9 23:28:10 2019

@author: david
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable

PERT=np.load("pert_test.npy")
DIV=np.load("div_test.npy")

n_side=DIV.shape[0]

min_div=np.amin(DIV)
max_div=np.amax(DIV)
min_node=np.amin(PERT)
max_node=np.amax(PERT)


for i in range(n_side):
    print(i)
  
    
    fig = plt.figure(figsize=(20, 10))
    fig.suptitle("Z = "+str(i)+"/"+str(n_side),fontsize=25)
    ax1 = fig.add_subplot(121)
    im1 = ax1.imshow((DIV[:,:,i]),cmap="nipy_spectral",vmax=max_div,vmin=min_div)
    
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im1, cax=cax, orientation='vertical')
    
    ax2 = fig.add_subplot(122)
    im2 = ax2.imshow(PERT[:,:,i],cmap="gist_ncar",vmax=max_node,vmin=min_node)
    
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im2, cax=cax, orientation='vertical')
    
    fig.savefig("zsweep_"+str(i)+".png")
    plt.close()