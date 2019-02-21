"""
Created on Sun Feb 10 12:25:12 2019

@author: David Paipa
"""
import numpy as np
import matplotlib.pyplot as plt
import collections as cl
from mpl_toolkits.axes_grid1 import make_axes_locatable

DIV=np.load("div_test.npy")
PERT_W=np.load("pert_test.npy")
PERT_V=np.load("pert_voronoi.npy")

n_side=PERT_W.shape[0]

min_div=np.amin(DIV)
max_div=np.amax(DIV)
min_node=np.amin(PERT_W)
max_node=np.amax(PERT_W)

print("Generando grficas comparativas watershed - voronoi ...")

for i in range (n_side):
    print(i)
  
    
    fig = plt.figure(figsize=(30, 10))
    #fig.suptitle("Z = "+str(i)+"/"+str(n_side),fontsize=25)
    ax1 = fig.add_subplot(131)
    im1 = ax1.imshow((DIV[:,:,i]),cmap="nipy_spectral",vmax=max_div,vmin=min_div)
    plt.title("Divergence map")
    
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im1, cax=cax, orientation='vertical')
    
    ax2 = fig.add_subplot(132)
    im2 = ax2.imshow(PERT_W[:,:,i],cmap="gist_ncar",vmax=max_node,vmin=min_node)
    plt.title("Watershed map")
    
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im2, cax=cax, orientation='vertical')
    
    
    ax3 = fig.add_subplot(133)
    im3 = ax3.imshow(PERT_V[:,:,i],cmap="gist_ncar",vmax=max_node,vmin=min_node)
    plt.title("Voronoi map")
    
    divider = make_axes_locatable(ax3)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im3, cax=cax, orientation='vertical')
    
    
    
    
    fig.savefig("zsweep_comp_"+str(i)+".png")
    plt.close()
