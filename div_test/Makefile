all:  watershed voronoi compare inertia
watershed: 
	python grid_div.py

plotdiv: compare
	python plot_pert.py
	


imdir: plotdiv
	mkdir images_watershed/

plot: imdir
	mv *.png images_watershed/


c_vor_in: voronoi_c.c
	gcc -o exec voronoi_c.c -lm

c_vor: c_vor_in
	./exec

c_run: c_vor
	rm exec

voronoi: c_run
	python new_vor.py
	rm params.txt


compare_gen: watershed voronoi
	python vol_comp.py

compare: compare_gen
	mkdir images_comp/
	mv *.png images_comp/


inertia_gen:
	python inertia.py

inertia_stat: inertia_gen
	python stats_inertia.py

inertia: inertia_stat
	mv *.png images_comp/



