######################################################
##													##
##	To perform color analysis on multiple images	##
##													##
######################################################

from color_analysis import multiple_images, rgb_histogram, rgb_image, colors_plot, elbow_curve, color_clustering, save_clusters_info, ImageAnalizer
import os
from os import walk

folder = "Imgs"

f = []
for (dirpath, dirnames, filenames) in walk(folder):
    for file in filenames:
        if file.endswith(".jpg"):
            f.extend([file])

for i in f:
    print(i)
    fullpath = os.path.join(dirpath, i)
    Imagen = ImageAnalizer(fullpath)
    #Imagen.RGB_composite()
    #Imagen.RGB_graph()
    maxclusters = 30
    clusters = elbow_curve(maxclusters, Imagen.pixel_values)
    #clusters = 3
    Imagen.Color_palette(clusters)
    save_clusters_info(Imagen.name, Imagen.colors, Imagen.pixel_label, Imagen.total_pixels)

