#################################################################
##                                                             ##
##      Functions to analize color composition of pictures     ##
##                                                             ##
#################################################################

from PIL import Image #Python Imaging Library

import sys
import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from sklearn.cluster import KMeans
from kneed import KneeLocator


def multiple_images(images, outputname):
    '''
    Multiple Images
    
    - Description:
        Combines several images side by side.
    
    - Paramaters:
        images: images data
        outputname: output file name
    '''
    
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    
    new_im = Image.new('RGB', (total_width, max_height))
    
    x_offset = 0
    
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
        new_im.save(outputname +'.jpg')


def elbow_curve(max_clusters, X, min_clusters = 2):
    '''
    Elbow Curve
    
    - Description:
        Plots the score for different numbers of clusters, helping the user to determine the ideal cluster quantity
    
    - Parameters:
        min_clusters: minimum number of clusters to test
        max_clusters: maximum numbert of clusters to test
        X: the dataset
    
    '''
    Nc = range(min_clusters, max_clusters)
    kmeans = [KMeans(n_clusters=i) for i in Nc]
    score = [kmeans[i].fit(X).score(X) for i in range(len(kmeans))]
    
    x = range(1, len(score)+1)
    kn = KneeLocator(x, score, curve = 'concave', direction = 'increasing', online = True)
    
    plt.figure(figsize=(5,5))
    plt.plot(Nc,score)
    plt.vlines(kn.knee, plt.ylim()[0], plt.ylim()[1], linestyles='dashed')
    plt.xlim([min_clusters-1,max_clusters])
    plt.xlabel('Number of Clusters')
    plt.ylabel('Score')
    plt.title('Elbow Curve')
    plt.grid()
    plt.show()
    return(kn.knee)

def color_clustering(pixel_values, clusters):
    '''
    Color Clustering
    
    - Description:
        Using K-means clustering extracts from the image as many principals colors as clusters stated.
        Used random_state = 42
        Returns the centroids of the clusters and the label for each pixel (i.e., the value of the centroid for each pixel)
        
    - Parameters:
        pixel_values: image RGB data for every pixel
        clusters: number of desired clusters
    '''
    X = np.array(pixel_values)
    
    kmeans = KMeans(n_clusters=clusters, random_state=42).fit(X)
    
    centroids = kmeans.cluster_centers_
    centroids = np.around(centroids)
    centroids = centroids.astype(int)
    centroids = tuple(map(tuple, centroids))
    
    labels = kmeans.predict(X)
    
    return(centroids, labels)

class ImageAnalizer(object):
    
    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[1].split(".", 1)[0]
        self.img = Image.open(path)
        self.pix = self.img.load()
        self.size = self.img.size
        self.total_pixels = self.size[0]*self.size[1]
        self.pixel_values = list(self.img.getdata())
        self.colors = np.NaN
        self.pixel_label = np.NaN
    
    def rgb_histogram(self):
        '''
        RGB Histogram
    
        - Description:
            Creates an histogram for the frequency of RGB contributions in the image 
            using the RGB values for each pixel in the image and saves the figure.
        '''
    
        if not os.path.isdir("histograms"):
            os.makedirs("histograms")
        
        plt.figure(figsize=(15,10))
        plt.grid()
        color = ('firebrick','mediumseagreen','royalblue')
        for i,col in enumerate(color):
            plt.hist(np.array(self.pixel_values)[:,i], color = col, histtype = 'stepfilled', 
                     bins = 256, alpha = 0.6)
        plt.xlim([0,256])
        plt.title("RGB contributions for "+ self.name)
        plt.ylabel("Frequency")
        plt.xlabel("Contribution to the pixels")
    
        plt.savefig("histograms/RGB_contribution_" + self.name + ".png")
    
    def rgb_composite(self):
        '''
        RGB Image
    
        - Description:
            Creates a composite side by side of the image and its RGB contributions.
        '''
    
        if not os.path.isdir("RGBcomposites"):
            os.makedirs("RGBcomposites")
        
        r = [(d[0], 0, 0) for d in self.pixel_values]
        g = [(0, d[1], 0) for d in self.pixel_values]
        b = [(0, 0, d[2]) for d in self.pixel_values]
    
        width, height = self.size
    
        new_im1 = Image.new('RGB', (width, height))
        new_im2 = Image.new('RGB', (width*3, height))
        x_offset = 0
        for j in [r, g, b]:
            new_im1.putdata(j)
            new_im2.paste(new_im1, (x_offset,0))
            x_offset = x_offset + width
        
        I = [self.img, new_im2]
        final = multiple_images(I, "RGBcomposites/RGB_composite_" + self.name)
        return(final)
    
    def color_palette(self, num_clusters, folder):
        '''
        Palette plotter
    
        - Description:
            Using a clustering function, it extracts the n desired RGB centroids. Then, given 
            those RGB values, plots side by side three images: the original picture, a sample of
            the RGB centroids and the picture using the centroids instead the original pixel values.
        
        - Parameters:
            num_clusters: the desired number of clusters
            folder: the name of the destination folder
        '''
        
        self.colors, self.pixel_label = color_clustering(self.pixel_values, num_clusters)  
    
        if not os.path.isdir(folder):
            os.makedirs(folder)
    
        # Making the sample colors
        sample = []
        number = len(self.colors)
        width, height = self.size
    
        for c in self.colors:
            sample = sample + ([c] * (round(width*height/number)-1))
        
        new_img = Image.new('RGB', (width, height))
        new_img.putdata(sample)
    
        # Making the image using the sample colors
        new_img2 = Image.new('RGB', (width, height))
        A = self.pixel_label.tolist()
        for i in range(0, len(A)):
            for j in range(0, len(self.colors)):
                if A[i] == j:
                    A[i] = self.colors[j]
        new_img2.putdata(A)
    
        # Put everything together side by side
        images = [self.img, new_img, new_img2]
        final = multiple_images(images, folder +'/ColorPalette_' + self.name)
        
    def clusters_info(self, file_name):
    	'''
    	Save clusters information

    	- Description:
    		Saves two .csv files, one containing the RGB centroids aand the other the 
    		percentage of pixel corresponding to each centroid.

    	- Parameters:
    		file_name: the output files name

    	'''
        
        if os.path.exists(file_name + "Percentage.csv") & os.path.exists(file_name + "RGB.csv"):
            df1 = pd.read_csv(file_name + "Percentage.csv")
            df2 = pd.read_csv(file_name + "RGB.csv")
            
            if df1.shape[0]<len(self.colors):
                R = abs(df1.shape[0]-len(self.colors))
                for i in range(0, R):
                    df1.append(pd.Series(), ignore_index=True)
                    df2.append(pd.Series(), ignore_index=True)
                
        else:
            df1 = pd.DataFrame()
            df2 = pd.DataFrame()
    
        # working out the percentage of pixels for each principal color
    
        percentage = []
        for i in range(0, len(self.colors)):
            A = round((np.sum(self.pixel_label==i)/self.total_pixels)*100)
            percentage = percentage + [A]
    
        add = []
        if len(percentage)<df1.shape[0]:
            remain = df1.shape[0]-len(percentage)
            add = [np.NaN]*remain
        percentage = percentage + add
    
        df1[self.name] = percentage
        df1.to_csv(file_name +'Percentage.csv', index = False)
    
        # writing the csv file with the principal colors in RGB
        
        Colors = self.colors
        add = []
        if len(self.colors)<df2.shape[0]:
            remain = df2.shape[0]-len(self.colors)
            add = [np.NaN]*remain
        Colors = Colors + tuple(add)
    
        df2[self.name] = Colors
        df2.to_csv(file_name + 'RGB.csv', index = False)