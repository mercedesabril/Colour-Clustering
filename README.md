# Color Clustering 

The objective of this project is to create a tool that given a set of pictures, is capable of determining the principal color present in each one, and use the principal color to sort the images, achieving a smooth transition between them.

The work was divided in three parts:

1. Obtain each picture's principal color using k-nearest neighbors
2. Sort the images by color
3. Upload the sorted pictures 

**Disclaimer: none of the images or pictures used are my property unless stated**

## 1. Obtain the principal color

An initial analysis of the RGB (Red, Green and Blue) contributions in the image is useful to understand how the colors are distributed.

Then, using sciḱit-learn k-nearest neighbors the principal color (or colors) for each picture is determined. The number of clusters can vary from picture to picture and this can be determined with a knee algorithm, or use a fix number. While using the knee algorithm, the clusters represent the images more accurately, but it also introduces more variability and noise, difficulting the process to define the principal color. In the end, it was better to use a fixed number of clusters (3 clusters).

Color clustering with knee algorithm:

![Image of dataset collage](https://github.com/mercedesabril/Colour-Clustering/blob/master/ColorPalette_withKnee/ColorPalette_pan.jpg)


Also, it was found that the clustering algorithm works better cropping the images by 10%, since this reduces noise.

## 2. Sort the images by color

Several ways of sorting colors where tested, and it was determined that the best approach was the * *step sorting* * using 9 steps ans HSV color space. The number of steps can vary from dataset to dataset.

![Image of dataset collage](https://github.com/mercedesabril/Colour-Clustering/blob/master/collage/collage_resized10p_enhanced_9steps_lumfix.jpg)


The colors luminosity plays an important role in the sorting process, not only the step sorting algorithm implements it, but also it's a helpful tool to reduce noise. For that reason, the best sorting results were obtained when enhancing the images' color contrast.

Color clustering using a fix number of clusters (3 clusters), image resized by 10% and with contrast enhancement:

![Image of dataset collage](https://github.com/mercedesabril/Colour-Clustering/blob/master/ColorPalette_enhanced10p/ColorPalette_pan.jpg)


## 3. Upload the sorted pictures

For this part, a Tumblr blog was created to host the sorted pictures (https://sorting-colors.tumblr.com/). The images were uploaded using Tumblr's API, which requires to create an API client. 

The usefulness of Tumblr in this project is:

1) Tumblr allows to configure the blogs themes, so you can choose a grid one which displays the results of the sorting code better.

2) It's possible to edit the date of publication of a post (while it isn't a date in the future, or an impossible date like the 56th of May), and the posts in the tumblr blog will appear ordered by this dates. So, the posts can have whatever order needed, in particular the order found by the sorting code: each post (an image from the dataset) will be associated with a date, so they will be published in a certain order. In the case of adding new elements to the dataset, the image order will change, but it's easy to fix that just editing the posting date.

