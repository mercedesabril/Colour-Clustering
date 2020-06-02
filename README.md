# Color Clustering 

The objective of this project is to create a tool that given a set of pictures, is capable of determining the principal color present in each one, and use the principal color to sort the images, achieving a smooth transition between them.

The work was divided in three parts:

1. Obtain each picture's principal color using k-nearest neighbors
2. Sort the images by color
3. Upload the sorted pictures 

**Disclaimer: none of the images or pictures used are my property unless stated**

## 1. Obtain the principal color

An initial analysis of the RGB (Red, Green and Blue) contributions in the image is useful to understand how the colors are distributed.

Then, using sciḱit-learn k-nearest neighbors the principal color (or colors) for each picture is determined. The number of clusters can vary from picture to picture and this can be determine with a knee algorithm, or the number can be fixed. While using the knee algorithm, the clusters represent the images more accurately, but it also introduces more variability and noise, difficulting the process to define the principal color. In the end, it was better to use a fixed number of clusters (3 clusters).

Also, it was found that the clustering algorithm works better cropping the images by 10%, since this reduces noise.

## 2. Sort the images by color

Several ways of sorting colors where tested, and it was determined that the best approach was the * *step sorting* * using 9 steps ans HSV color space. The number of steps can vary from dataset to dataset.

![Image of dataset collage](poner link)


The colors luminosity plays an important role in the sorting process, not only the step sorting algorithm implements it, but also it's a helpful tool to reduce noise. For that reason, the best sorting results were obtained when enhancing the images' color contrast.

## 3. Upload the sorted pictures

For this part, a Tumblr blog was created to host the sorted pictures (https://sorting-colors.tumblr.com/). The images were uploaded using Tumblr's API, which requires to create an API client. 

This website was particularly useful for the purposes of this project because Tumblr's blogs can be configured to have a grid layout to display the images.