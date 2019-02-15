all:  watershed plot voronoi compare
watershed: 
	python grid_div.py

plotdiv: 
	python plot_pert.py


imdir: plotdiv
	mkdir newimages

plot: imdir
	mv *.png newimages/


c_vor_in: voronoi_c.c
	gcc -o exec voronoi_c.c -lm

c_vor: c_vor_in
	./exec

c_run: c_vor
	rm exec

voronoi: c_run
	python new_vor.py

compare: watershed voronoi
	python compare.py
	python vol_comp.py








