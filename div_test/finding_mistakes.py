"""
Created on Fri Feb 15 13:53:30 2019

@author: David Paipa
"""
import numpy as np
import matplotlib.pyplot as plt
import collections as cl
from operator import itemgetter
#from astropy.convolution import Gaussian2DKernel,convolve
#import scipy.linalg as linalg
#from mpl_toolkits.mplot3d import Axes3D
PERT_V=np.load("pert_voronoi.npy")
PERT_W=np.load("pert_test.npy")

n_side=PERT_W.shape[0]
n_cumulos=np.amax(PERT_W)

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
  
CV=sorted(CV,key=itemgetter(0))
CW=sorted(CW,key=itemgetter(0))

CV=np.array(CV)
CW=np.array(CW)