######################################################
##													##
##	To perform color analysis on multiple images	##
##													##
######################################################

from color_analysis import multiple_images, elbow_curve, color_clustering, ImageAnalizer
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
    Imagen = ImageAnalizer(fullpath, True, True)
    Imagen.rgb_composite()
    Imagen.rgb_histogram()
    maxclusters = 15
    clusters = elbow_curve(maxclusters, Imagen.pixel_values)
    #clusters = 3
    #maxclusters = clusters
    Imagen.color_palette(clusters, "ColorPalette_enhanced10p")
    Imagen.clusters_info("ColorCluster_enhanced10p_", maxclusters)

