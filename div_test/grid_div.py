"""
Created on Sat Feb  9 22:58:03 2019

@author: david
"""
import numpy as np
import matplotlib.pyplot as plt
from time import gmtime, strftime
import itertools as itt

#DATA=np.load("div_test.npy")
#
#n_side=DATA.shape[0]

#=========================FUNCIONES=======================
def vecinos3D(ii,jj,kk,tam_r):
    ii_a=(ii-1)%tam_r
    ii_b=(ii+1)%tam_r
    jj_a=(jj-1)%tam_r
    jj_b=(jj+1)%tam_r
    kk_a=(kk-1)%tam_r
    kk_b=(kk+1)%tam_r 
    xx=[ii_a,ii,ii_b]
    yy=[jj_a,jj,jj_b]
    zz=[kk_a,kk,kk_b]
    
    L=list(itt.product(*[xx,yy,zz]))
 
    L=np.array(L).T
#retorna las coordenadas de los 26 vecinos y si mismo   
    return L[0],L[1],L[2]


def revisarVecinos(ii,jj,kk,Pertenencia,tam_r):
    xx,yy,zz=vecinos3D(ii,jj,kk,tam_r)
    tam=len(xx)
    pert=[]
    for i in range (tam):#revisa las pertenencias de todos los vecionos 
        p_i=Pertenencia[xx[i],yy[i],zz[i]]
        pert.append(p_i)
    suma=np.sum(pert)
    if(suma==0):
        return 0
    else:
        pert=np.array(pert)
        pert=list(pert[pert!=0])
        return max(set(pert), key=pert.count) #el identificador de la mayoria
#define el identificador del voxel basado en sus vecinos

        



def darVacios(Pertenencia):
    return len(np.where(Pertenencia==0)[0])

#===================WATERSHED==============================

def watershed(filename,filename_out,d_tolerancia,vacios_tolerancia):
    DIV=np.load(filename)
    tam=np.shape(DIV)[0]
    
    div_max=round(np.amax(DIV)+5,-1)
    div_min=round(np.amin(DIV)-5,-1)
    N_intervalos=40*tam
    #se definen los limites del barrido y se hace un numero grande de cortes 
    #entre estos limites
    
    
    barridoA=np.linspace(div_min,div_max,N_intervalos)
    barrido=np.concatenate((barridoA,barridoA))
    
    #se hace eeste barrido 2 veces
    
    tam_b=len(barrido) #tamaño del barrido final
    delta=np.abs(barrido[0]-barrido[1])
    Pertenencia=np.zeros([tam,tam,tam])
    
    
    x_nodos=[]
    y_nodos=[]
    z_nodos=[]
    p_nodos=[]
    cont_nodos=1
    
    cont_iteraciones=0
    
    
    vacios=[]
    vacios.append(darVacios(Pertenencia))
    
    #El loop corre hasta que el numero de vacios es nulo
    while(vacios[-1]>vacios_tolerancia):
        print(str(round((100*vacios[-1]/(tam**3)),6)) + " % del espacio está vacio (En total son "+str(vacios[-1])+" voxeles)")   
        
        c=0
        
        for lev in barrido:
            if(c%300==0):
                print(str(round(c*100/tam_b,2))+" % evaluado ("+str(darVacios(Pertenencia))+" voxeles sin asignar)")
            c+=1
            cota_inf=lev
            cota_sup=lev+delta
            #se definen los limites del corte en los valores del campo
            aa=np.where((DIV<cota_sup)&(DIV>=cota_inf)&(Pertenencia==0))
            xx,yy,zz=aa[0],aa[1],aa[2]
            rec=len(xx)
            #se obtienen los voxeles sin asignar
            for i in range (rec):
                x,y,z=xx[i],yy[i],zz[i]
                pert=revisarVecinos(x,y,z,Pertenencia,tam)
                # se recorren y revisan sus vecinos...
                if(pert!=0):
                    Pertenencia[x,y,z]=pert
                else:
                    #si ninguno de sus 27 vecinos (incluyendose) esta asignado
                    #Se convierte en un nuev nodo

                    Pertenencia[x,y,z]=cont_nodos
                    p_nodos.append(cont_nodos)
                    cont_nodos+=1
                    x_nodos.append(x)
                    y_nodos.append(y)
                    z_nodos.append(z)
        #si no se cumple la condicion de voxeles vacios una vez recorrido el campo
        #se recorre de nuevo
        cont_iteraciones+=1
        vacios.append(darVacios(Pertenencia))

    np.save(filename_out,Pertenencia)
    print(str(np.amax(Pertenencia)) + " nodos encontrados con Watershed.")
    return tam,cont_nodos-1,cont_iteraciones,np.array([x_nodos,y_nodos,z_nodos,p_nodos]) 



#============Main======================================================
    
file_stats=open("STATS.csv","w")
file_stats.write("Parches,Iteraciones,VaciosTol,DistanciaTol,FileIN,FileOut,Time"+"\n")

name_in="div_test.npy"
name_out="pert_test.npy"

tol_vacios=0
DistanciaTol=1

n_side,nodos,it,NODOS=watershed(name_in,name_out,DistanciaTol,tol_vacios)

np.save("NODOS.npy",NODOS)





file_stats.write(str(nodos)+","+str(it)+","+str(tol_vacios)+","+str(DistanciaTol)+","+name_in+","+name_out+","+strftime("%Y.%m.%d-%H:%M:%S", gmtime())+"\n")
file_stats.close()

file_n=open("nodos.txt","w")
# se escriben los nodos y su id para so posterior
for N in range(len(NODOS[0])):
    file_n.write(str(NODOS[0][N])+" "+str(NODOS[1][N])+" "+str(NODOS[2][N])+" "+str(NODOS[3][N])+"\n")
file_n.close()


file_p=open("params.txt","w")
# se escriben los nodos y su id para so posterior
file_p.write(str(int(n_side))+"\n")
file_p.write(str(nodos)+"\n")
file_p.close()

