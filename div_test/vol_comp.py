"""
Created on Wed Feb 13 16:13:48 2019

@author: David Paipa
"""
import numpy as np
import matplotlib.pyplot as plt
import collections as cl
from mpl_toolkits.axes_grid1 import make_axes_locatable
#from astropy.convolution import Gaussian2DKernel,convolve
#import scipy.linalg as linalg
#from mpl_toolkits.mplot3d import Axes3D

PERT_W=np.load("pert_test.npy")
PERT_V=np.load("pert_voronoi.npy")
n_side=PERT_W.shape[0]

l_w=PERT_W.reshape([n_side**3])
l_v=PERT_V.reshape([n_side**3])


cnt_w=cl.Counter(l_w)
CW=[]
for k_w in cnt_w.keys():
  CW.append([k_w,cnt_w[k_w]])  


cnt_v=cl.Counter(l_v)
CV=[]
for k_v in cnt_v.keys():
  CV.append([k_v,cnt_v[k_v]])
  

CV=np.array(CV)
CW=np.array(CW)

x_w=CW[:,1]
y_v=CV[:,1]


plt.figure(figsize=[10,3])
plt.hist(np.log10(x_w/y_v),bins=60,ec="k")
plt.xlabel("$Log_{10}(V_{w}/V_{v})$",fontsize=15)
plt.ylabel("$N_{clusters}$",fontsize=15)
plt.savefig("log_vol_comp.png")
plt.close()

fig=plt.figure(figsize=[12,6])

#fig.suptitle("Z = "+str(i)+"/"+str(n_side),fontsize=25)
ax1 = fig.add_subplot(121)
im1 = ax1.scatter(x_w,y_v,s=5,c=np.arange(1562),cmap="jet")
divider = make_axes_locatable(ax1)
cax = divider.append_axes('bottom', size='5%', pad=0.6)
ax1.set_xlabel("$V_{Watershed}$",fontsize=15)
ax1.set_ylabel("$V_{Voronoi}$",fontsize=15)
cb = fig.colorbar(im1, cax=cax, orientation='horizontal')
cb.set_label("ID number")


ax2 = fig.add_subplot(122)
im2 = ax2.hist2d(x_w,y_v,bins=[16,16],cmap="nipy_spectral")

divider = make_axes_locatable(ax2)
cax = divider.append_axes('bottom', size='5%', pad=0.6)
ax2.set_xlabel("$V_{Watershed}$",fontsize=15)
ax2.set_ylabel("$V_{Voronoi}$",fontsize=15)
cb = fig.colorbar(im2[3], cax=cax, orientation='horizontal')
cb.set_label("count")

fig.savefig("vol_comp.png")
plt.close()



