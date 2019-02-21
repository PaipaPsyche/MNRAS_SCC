# README

## MAKE

### watershed
Barrer toda la grid de divergencia (div_test.npy) y clasificar con el algoritmo de waterhed
#### return
* crea archivo **NODOS.npy** con los nodos obtenidos (Python)
* crea archivo **pert_test.npy** con la grid de pertenencias de las mismas dimensiones de div_test.npy (Python)
* crea archivo **nodos.txt** con los nodos obtenidos (C)
* crea archivo **params.txt** con el numero de nodos hallados (C)


### voronoi
Usando **nodos.txt** y **params.txt** asigna a cada voxel del espacio un identificador por criterio de voronoi
#### return
* crea archivo **pert_voronoi.txt** con la coordenada y pertenencia de cada voxel (Python)
* crea archivo **pert_voronoi.npy** con la grid de pertenencias de voronoi (Python)
* Borra archivo **params.txt**



### compare
Usando **pert_voronoi.npy** y **pert_watershed.npy** muestra comparaciones cuantitativas entre ambos metodos.
#### return
* crea graficas.
* crea archivo **comp_volumenes.txt** con una lista de supercumulos de la forma *ID,vol_watershed,vol_voronoi,coef*

##### Nota:
*coef* es un coeficiente que se asigna para mirar la similitud en ordenes de magnitud. Cerca de 1 significa que ambos volumenes
son similares, mientras que cerca de 0 significa ordenes de magnitud muy diferentes.


### inertia
usando  **pert_voronoi.npy** y **pert_watershed.npy** y un archivo de masa (si no es proporcionado se usa m=1 para cada voxel) se hacen calculos de inercia.
* crea archivos **CALIBRACION_W.npy** y **CALIBRACION_V.npy** con los parametros de centrado para cada cumulo.
* crea archivos **INERCIA_W.npy** y **INERCIA_V.npy** con los valores de inercia calculados para watershed y voronoi.
* crea archivo **COORDS_REAL_V.npy** y **COORDS_REAL_W.npy** con las coordenadas reales de los centros de masa para cada cumulo.
* crea archivo **COORDS_CENT_V.npy** y **COORDS_CENT_W.npy** con las coordenadas de los centros de masa para cada cumulo UNA VEZ CENTRADO.


