"""
Created on Tue Feb 19 16:16:58 2019

@author: David Paipa
"""
import numpy as np
import matplotlib.pyplot as plt
#from astropy.convolution import Gaussian2DKernel,convolve
#import scipy.linalg as linalg
#from mpl_toolkits.mplot3d import Axes3D
INERCIA_W=np.load("INERCIA_W.npy")
INERCIA_V=np.load("INERCIA_V.npy")
VOLS=np.load("VOLS.npy")
#importando datos


#escala logaritmica
INERCIA_W_l=np.log10(INERCIA_W+1)
INERCIA_V_l=np.log10(INERCIA_V+1)

#------------separando constantes----------
I_x_w=INERCIA_W_l[:,6]
I_y_w=INERCIA_W_l[:,7]
I_z_w=INERCIA_W_l[:,8]

l1l2_w=INERCIA_W[:,9]
l2l3_w=INERCIA_W[:,10]

I_x_v=INERCIA_V_l[:,6]
I_y_v=INERCIA_V_l[:,7]
I_z_v=INERCIA_V_l[:,8]

l1l2_v=INERCIA_V[:,9]
l2l3_v=INERCIA_V[:,10]
#--------------------


#--------------- limpiando los ceros------------
I_x_w = [x for x in I_x_w if x != 0]
I_y_w = [x for x in I_y_w if x != 0]
I_z_w = [x for x in I_z_w if x != 0]
l1l2_w = [x for x in l1l2_w if (x != 0 and x<1E6)]
l2l3_w = [x for x in l2l3_w if (x != 0 and x<1E6)]

I_x_v = [x for x in I_x_v if x != 0]
I_y_v = [x for x in I_y_v if x != 0]
I_z_v = [x for x in I_z_v if x != 0]
l1l2_v = [x for x in l1l2_v if (x != 0 and x<1E6)]
l2l3_v = [x for x in l2l3_v if (x != 0 and x<1E6)]
#----------------------------------------------

l1l2_w = np.array(l1l2_w)
l2l3_w = np.array(l2l3_w)
I_x_w=np.array(I_x_w)+2 # cada vozel aporta 100Mpc2
I_y_w=np.array(I_y_w)+2 # cada vozel aporta 100Mpc2
I_z_w=np.array(I_z_w)+2 # cada vozel aporta 100Mpc2

l1l2_v = np.array(l1l2_v)
l2l3_v = np.array(l2l3_v)
I_x_v=np.array(I_x_v)+2 # cada vozel aporta 100Mpc2
I_y_v=np.array(I_y_v)+2 # cada vozel aporta 100Mpc2
I_z_v=np.array(I_z_v)+2 # cada vozel aporta 100Mpc2



#-----plotting-------------------
print("Graficando stats de inercia . . .")


#-----------------plot histogramas--------------------
sigma=2
n_bins=int(48.6*np.exp(-0.105*sigma)) # formula empírica
ALPHA=0.5


plt.figure(figsize=[17,5])
#plt.suptitle(r"$\sigma_{Vox} = $"+str(sigma))
plt.subplot(1,3,1)
plt.hist(np.log10(l1l2_w),bins=n_bins,alpha=ALPHA,color="orange",label="Waterhed")
plt.hist(np.log10(l1l2_v),bins=n_bins,alpha=ALPHA,color="blue",label="Voronoi")
plt.xlabel(r'$Log_{10}(\lambda_1 / \lambda_2)$',fontsize=13)
plt.ylabel("# Superclusters",fontsize=13)
plt.legend()
#    plt.xlim(np.amin(l1l2)-1,np.amax(l1l2)+1)


plt.subplot(1,3,2)
plt.hist(np.log10(l2l3_w),bins=n_bins,alpha=ALPHA,color="green",label="Waterhed")
plt.hist(np.log10(l2l3_v),bins=n_bins,alpha=ALPHA,color="red",label="Voronoi")
plt.xlabel(r'$Log_{10}(\lambda_2 / \lambda_3)$',fontsize=13)
plt.ylabel("# Superclusters",fontsize=13)
plt.legend()
#    plt.xlim(np.amin(l2l3)-1,np.amax(l2l3)+1)

           
plt.subplot(1,3,3)
ALPHA=0.3
n_data_w=np.amin([len(l1l2_w),len(l2l3_w)])
plt.scatter(np.log10(l1l2_w[:n_data_w]),np.log10(l2l3_w[:n_data_w]),c="red",s=3,alpha=ALPHA,label="Watershed")
n_data_v=np.amin([len(l1l2_v),len(l2l3_v)])
plt.scatter(np.log10(l1l2_v[:n_data_v]),np.log10(l2l3_v[:n_data_v]),c="green",s=3,alpha=ALPHA,label="Voronoi")
plt.legend()
plt.xlabel(r'$ Log_{10}( \lambda_1 / \lambda_2)$',fontsize=13)
plt.ylabel(r'$ Log_{10}( \lambda_2 / \lambda_3)$',fontsize=13)           

plt.savefig("cocientes_inercia.png")
#-------------------------------------


#-----------------plot histograma 2D--------------------
L1_W=INERCIA_W[:,6]
L2_W=INERCIA_W[:,7]
L3_W=INERCIA_W[:,8]

L1_V=INERCIA_V[:,6]
L2_V=INERCIA_V[:,7]
L3_V=INERCIA_V[:,8]

jj_w=np.logical_and(np.logical_and(L1_W!=0,L2_W!=0),L3_W!=0)
jj_v=np.logical_and(np.logical_and(L1_V!=0,L2_V!=0),L3_V!=0)

L1_W=L1_W[jj_w]
L2_W=L2_W[jj_w]
L3_W=L3_W[jj_w]

L1_V=L1_V[jj_v]
L2_V=L2_V[jj_v]
L3_V=L3_V[jj_v]

col_w=VOLS[0][jj_w]
col_v=VOLS[0][jj_v]

DELTA=0.00001

C1_W=(L1_W-L2_W)/(L1_W+L2_W+L3_W+DELTA)
C2_W=(L2_W-L3_W)/(L1_W+L2_W+L3_W+DELTA)


C1_V=(L1_V-L2_V)/(L1_V+L2_V+L3_V+DELTA)
C2_V=(L2_V-L3_V)/(L1_V+L2_V+L3_V+DELTA)



fss=15
bins2d=50
plt.figure(figsize=[16,12])

plt.subplot(2,2,1)
plt.title("Watershed",fontsize=fss)
sc=plt.scatter(C1_W,C2_W,c=np.log10(col_w),cmap='jet',s=5)
cb=plt.colorbar(sc)
#cb.set_label(r"$Log_{10}$(V $[Mpc^3 h^{-3}]$)",fontsize=16)
cb.set_label(r"$Log_{10}$(M $[M_{\odot} h^{-1}]$)",fontsize=fss)
plt.grid()
plt.ylabel(r"($\lambda_2 - \lambda_3$)/ ($\lambda_1+\lambda_2+\lambda_3$)",fontsize=fss)
plt.xlabel(r"($\lambda_1 - \lambda_2$)/ ($\lambda_1+\lambda_2+\lambda_3$)",fontsize=fss)
plt.axhline(0,c="k",linestyle="--")
plt.axvline(0,c="k",linestyle="--")



plt.subplot(2,2,3)
HH=plt.hist2d(C1_W,C2_W,bins=bins2d,cmap='nipy_spectral')
cb=plt.colorbar()
cb.set_label(r"Number of superclsuters",fontsize=fss)

FS=30
#plt.text(0.01,0.02,"A",color="white",fontsize=FS)
#plt.text(0.01,0.25,"B",color="white",fontsize=FS)
#plt.text(0.3,0.02,"C",color="white",fontsize=FS)
#plt.text(0.2,0.2,"D",color="white",fontsize=FS)

plt.ylabel(r"($\lambda_2 - \lambda_3$)/ ($\lambda_1+\lambda_2+\lambda_3$)",fontsize=fss)
plt.xlabel(r"($\lambda_1 - \lambda_2$)/ ($\lambda_1+\lambda_2+\lambda_3$)",fontsize=fss)



plt.subplot(2,2,2)
plt.title("Voronoi",fontsize=fss)
sc=plt.scatter(C1_V,C2_V,c=np.log10(col_v),cmap='jet',s=5)
cb=plt.colorbar(sc)
#cb.set_label(r"$Log_{10}$(V $[Mpc^3 h^{-3}]$)",fontsize=16)
cb.set_label(r"$Log_{10}$(M $[M_{\odot} h^{-1}]$)",fontsize=fss)
plt.grid()
plt.ylabel(r"($\lambda_2 - \lambda_3$)/ ($\lambda_1+\lambda_2+\lambda_3$)",fontsize=fss)
plt.xlabel(r"($\lambda_1 - \lambda_2$)/ ($\lambda_1+\lambda_2+\lambda_3$)",fontsize=fss)
plt.axhline(0,c="k",linestyle="--")
plt.axvline(0,c="k",linestyle="--")



plt.subplot(2,2,4)
HH=plt.hist2d(C1_V,C2_V,bins=bins2d,cmap='nipy_spectral')
cb=plt.colorbar()
cb.set_label(r"Number of superclsuters",fontsize=fss)

FS=30
#plt.text(0.01,0.02,"A",color="white",fontsize=FS)
#plt.text(0.01,0.25,"B",color="white",fontsize=FS)
#plt.text(0.3,0.02,"C",color="white",fontsize=FS)
#plt.text(0.2,0.2,"D",color="white",fontsize=FS)

plt.ylabel(r"($\lambda_2 - \lambda_3$)/ ($\lambda_1+\lambda_2+\lambda_3$)",fontsize=fss)
plt.xlabel(r"($\lambda_1 - \lambda_2$)/ ($\lambda_1+\lambda_2+\lambda_3$)",fontsize=fss)

plt.savefig("hist_shape.png")



