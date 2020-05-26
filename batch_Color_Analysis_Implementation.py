######################################################
##													##
##	To perform color analysis on multiple images	##
##													##
######################################################

from color_analysis2 import multiple_images, elbow_curve, color_clustering, ImageAnalizer
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
    Imagen.rgb_composite()
    Imagen.rgb_histogram()
    maxclusters = 30
    clusters = elbow_curve(maxclusters, Imagen.pixel_values)
    Imagen.color_palette(clusters, "ColorPalette_withKnee")
    Imagen.clusters_info("ColorCluster_withKnee_")

