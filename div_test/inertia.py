"""
Created on Thu Feb 14 14:07:00 2019

@author: David Paipa
"""
import numpy as np
import matplotlib.pyplot as plt
#from astropy.convolution import Gaussian2DKernel,convolve
import scipy.linalg as linalg
#from mpl_toolkits.mplot3d import Axes3D
CALIBRACION=1

##importando los datos
PERT_W=np.load("pert_test.npy")
PERT_V=np.load("pert_voronoi.npy")
n_side=np.shape(PERT_W)[0]
n_cumulos=int(np.amax(PERT_W))



CALIBRACION_W=np.zeros([n_cumulos,3]) # calibracion en x,y,z para cada cumulo(W)


CALIBRACION_V=np.zeros([n_cumulos,3]) # calibracion en x,y,z para cada cumulo(V)


#=====================CALIBRACION============
#SE BUSCAN PARAMETROS X,Y,Z QUE CORRESPONDAN A DESPLAZAMIENTOS
#EN LOS 3 EJES CON EL FIN DE CONTRARESTAR LAS CONDICIONES PERIODICAS
#Y EL EFECTO BORDE, CENTRANDO ASI EL OBJETO 
print("Generando parametros de calibración...")
for i in range(1,n_cumulos+1):
    if (i%70==0):
        print(int(i/n_cumulos *100),"%") #print selectivo
    coords_w=np.array(np.where(PERT_W==i)) #coordenadas voxeles del cumulo
    n_datos=len(coords_w[0]) #n_voxeles
    for dim in range(3): 
        while((len(np.where((np.where(coords_w[dim]==(n_side-1)))or(coords_w[dim]==0))[0])!=0)and(CALIBRACION_W[i-1,dim]<n_side)):
            CALIBRACION_W[i-1,dim]=CALIBRACION_W[i-1,dim]+1 
            coords_w[dim]=(coords_w[dim]+1)%n_side
        #se desplaza el cumulo en las tres dimensiones hasta que no cruce ninguna pared
            
    coords_v=np.array(np.where(PERT_V==i))
    n_datos=len(coords_v[0])
    for dim in range(3):
        while((len(np.where((np.where(coords_v[dim]==(n_side-1)))or(coords_v[dim]==0))[0])!=0)and(CALIBRACION_V[i-1,dim]<n_side)):
            CALIBRACION_V[i-1,dim]=CALIBRACION_V[i-1,dim]+1
            coords_v[dim]=(coords_v[dim]+1)%n_side


np.save("CALIBRACION_W.npy",CALIBRACION_W)
np.save("CALIBRACION_V.npy",CALIBRACION_V)
print("Parametros de calibración listos.")


#====================CENTRO DE MASA=================
#AHORA PARA CADA CUMULO SE QUIEREN LAS COORDENADAS X,Y,Z 
# DE SU CENTRO DE MASA


COORDS_W=np.zeros(np.shape(CALIBRACION_W)) #coordenadas centro de masa (Watershed) [una vez centrado el cumulo con sus parametros]
R_COORDS_W=np.zeros(np.shape(CALIBRACION_W)) # coordenadas centro de masa (Watershed)[sin cnetrar]
INERCIA_W=np.zeros([np.shape(CALIBRACION_W)[0],11]) # 11 valores para definir la inercia del cumulo


COORDS_V=np.zeros(np.shape(CALIBRACION_V))#coordenadas CM (Voronoi) [centrado]
R_COORDS_V=np.zeros(np.shape(CALIBRACION_V))#coordenadas CM (Voronoi) [sin centrar]
INERCIA_V=np.zeros([np.shape(CALIBRACION_V)[0],11]) # 11 valores para definir la inercia del cumulo




print("Calculando centro de masa e inercia ...")

M=np.ones([n_side,n_side,n_side]) #todos con misma masa
#M=np.load("Mass.npy")

for cumulo in range(1,n_cumulos+1):
    
    if (cumulo%70==0):
        print(int(cumulo/n_cumulos *100),"%") #print selectivo
    
    coords_w=np.array(np.where(PERT_W==cumulo)) #coordenadas voxeles del cumulo
    coords_w[0],coords_w[1],coords_w[2]=(coords_w[0]+CALIBRACION_W[cumulo-1,0])%n_side,(coords_w[1]+CALIBRACION_W[cumulo-1,1])%n_side,(coords_w[2]+CALIBRACION_W[cumulo-1,2])%n_side      #centrando ...
    
    coords_v=np.array(np.where(PERT_V==cumulo))
    coords_v[0],coords_v[1],coords_v[2]=(coords_v[0]+CALIBRACION_V[cumulo-1,0])%n_side,(coords_v[1]+CALIBRACION_V[cumulo-1,1])%n_side,(coords_v[2]+CALIBRACION_V[cumulo-1,2])%n_side
    

    C_w=np.zeros([3])
    C_v=np.zeros([3])

    for dim in range (3):
        C_w[dim]=np.sum(coords_w[dim][:]*M[coords_w[0][:],coords_w[1][:],coords_w[2][:]])/np.sum(M[PERT_W==cumulo])
        C_v[dim]=np.sum(coords_v[dim][:]*M[coords_v[0][:],coords_v[1][:],coords_v[2][:]])/np.sum(M[PERT_V==cumulo])
    COORDS_W[cumulo-1,:]=C_w[:] #coordenadas del centro de masa
    R_COORDS_W[cumulo-1,:]=(C_w[:]-CALIBRACION_W[cumulo-1,:])%n_side
    
    COORDS_V[cumulo-1,:]=C_v[:]
    R_COORDS_V[cumulo-1,:]=(C_v[:]-CALIBRACION_V[cumulo-1,:])%n_side
    
    #---------------CUANTIFICANDO LA INERCIA ----------------------------
    
    x_r_w,y_r_w,z_r_w=(coords_w[0]-C_w[0])%n_side,(coords_w[1]-C_w[1])%n_side,(coords_w[2]-C_w[2])%n_side
    x_r_w,y_r_w,z_r_w=np.array(x_r_w).astype("int")%n_side,np.array(y_r_w).astype("int")%n_side,np.array(z_r_w).astype("int")%n_side

    x_r_v,y_r_v,z_r_v=(coords_v[0]-C_v[0])%n_side,(coords_v[1]-C_v[1])%n_side,(coords_v[2]-C_v[2])%n_side
    x_r_v,y_r_v,z_r_v=np.array(x_r_v).astype("int")%n_side,np.array(y_r_v).astype("int")%n_side,np.array(z_r_v).astype("int")%n_side

    
    
    INERCIA_W[cumulo-1,0]=np.sum((y_r_w**2 + z_r_w**2)*M[x_r_w[:],y_r_w[:],z_r_w[:]])
    INERCIA_W[cumulo-1,1]=np.sum((x_r_w**2 + z_r_w**2)*M[x_r_w[:],y_r_w[:],z_r_w[:]])
    INERCIA_W[cumulo-1,2]=np.sum((y_r_w**2 + x_r_w**2)*M[x_r_w[:],y_r_w[:],z_r_w[:]])
    INERCIA_W[cumulo-1,3]=np.sum((y_r_w * x_r_w)*M[x_r_w[:],y_r_w[:],z_r_w[:]])
    INERCIA_W[cumulo-1,4]=np.sum((x_r_w * z_r_w)*M[x_r_w[:],y_r_w[:],z_r_w[:]])
    INERCIA_W[cumulo-1,5]=np.sum((y_r_w * z_r_w)*M[x_r_w[:],y_r_w[:],z_r_w[:]])
    
    INERCIA_V[cumulo-1,0]=np.sum((y_r_v**2 + z_r_v**2)*M[x_r_v[:],y_r_v[:],z_r_v[:]])
    INERCIA_V[cumulo-1,1]=np.sum((x_r_v**2 + z_r_v**2)*M[x_r_v[:],y_r_v[:],z_r_v[:]])
    INERCIA_V[cumulo-1,2]=np.sum((y_r_v**2 + x_r_v**2)*M[x_r_v[:],y_r_v[:],z_r_v[:]])
    INERCIA_V[cumulo-1,3]=np.sum((y_r_v * x_r_v)*M[x_r_v[:],y_r_v[:],z_r_v[:]])
    INERCIA_V[cumulo-1,4]=np.sum((x_r_v * z_r_v)*M[x_r_v[:],y_r_v[:],z_r_v[:]])
    INERCIA_V[cumulo-1,5]=np.sum((y_r_v * z_r_v)*M[x_r_v[:],y_r_v[:],z_r_v[:]])
    
    Ixx_w=INERCIA_W[cumulo-1,0]
    Iyy_w=INERCIA_W[cumulo-1,1]
    Izz_w=INERCIA_W[cumulo-1,2]
    Ixy_w=INERCIA_W[cumulo-1,3]
    Ixz_w=INERCIA_W[cumulo-1,4]
    Iyz_w=INERCIA_W[cumulo-1,5]
    
    Ixx_v=INERCIA_V[cumulo-1,0]
    Iyy_v=INERCIA_V[cumulo-1,1]
    Izz_v=INERCIA_V[cumulo-1,2]
    Ixy_v=INERCIA_V[cumulo-1,3]
    Ixz_v=INERCIA_V[cumulo-1,4]
    Iyz_v=INERCIA_V[cumulo-1,5]
    
    
    
    IMAT_w=np.array([[Ixx_w,Ixy_w,Ixz_w],[Ixy_w,Iyy_w,Iyz_w],[Ixz_w,Iyz_w,Izz_w]]) #matriz de inercia
    IMAT_v=np.array([[Ixx_v,Ixy_v,Ixz_v],[Ixy_v,Iyy_v,Iyz_v],[Ixz_v,Iyz_v,Izz_v]])
    
    w_w,v_w=linalg.eig(IMAT_w)
    w_v,v_v=linalg.eig(IMAT_v)
    
    cocientes_w=sorted([w_w[0],w_w[1],w_w[2]],reverse=True)
    cocientes_v=sorted([w_v[0],w_v[1],w_v[2]],reverse=True) #autovalores de la matriz de inercia
    
    
    INERCIA_W[cumulo-1,6]=cocientes_w[0]
    INERCIA_W[cumulo-1,7]=cocientes_w[1]
    INERCIA_W[cumulo-1,8]=cocientes_w[2]
    
    INERCIA_V[cumulo-1,6]=cocientes_v[0]
    INERCIA_V[cumulo-1,7]=cocientes_v[1]
    INERCIA_V[cumulo-1,8]=cocientes_v[2]
    
    

  
    INERCIA_W[cumulo-1,9]=cocientes_w[0]/(cocientes_w[1]+1E-4)
    INERCIA_W[cumulo-1,10]=cocientes_w[1]/(cocientes_w[2]+1E-4)
    
    INERCIA_V[cumulo-1,9]=cocientes_v[0]/(cocientes_v[1]+1E-4)  #cocientes entre valores propios
    INERCIA_V[cumulo-1,10]=cocientes_v[1]/(cocientes_v[2]+1E-4)
        
        
        
    
        
np.save("COORDS_CENT_W.npy",np.round(COORDS_W))
np.save("COORDS_REAL_W.npy",np.round(R_COORDS_W))
np.save("INERCIA_W.npy",INERCIA_W)
#guardando
np.save("COORDS_CENT_V.npy",np.round(COORDS_V))
np.save("COORDS_REAL_V.npy",np.round(R_COORDS_V))
np.save("INERCIA_V.npy",INERCIA_V)

print("Centro de masa e inercia listos.")
