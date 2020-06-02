######################################################
##		Tools to upload the organized pictures 		##
##			   		on Tumblr						##
######################################################


import os
import pandas as pd

from PIL import Image, ImageOps

import pytumblr

def upload_post(folder_of_pictures, picture_name, blogname, picture_color, date_of, published_df, client):

    '''
    Upload Post

    - Description
        Tool to upload a new image post.

    - Parameters
        folder_of_pictures: the name of the folder which contains the pictures
        picturename: file name of the picture
        blogname: name of the Tumblr blog the pictures will be uploaded to
        picture_color: the principal color of the picture as a tuple of 3 (RGB)
        date_of: the publication date
        published_df: the dataframe where the upload info is going to be saved
        client: the Tumblr client
    '''

    img = Image.open(folder_of_pictures + '/' + picture_name + '.jpg')
    thumb = ImageOps.fit(img, (128, 128), Image.ANTIALIAS)
    display(thumb)

    print('\nEnter the tags for the image above separated by commas: \n')
    tags = input()
    tags = ['rgb', 'colors', 'python'] + ['rgb: ' + picture_color.replace(',', '')] + tags.split(sep = ',')
        
    upload = client.create_photo(blogname, state="published", tags = tags, 
        data = folder_of_pictures + '/'+ picture_name + '.jpg', date = date_of)
        
    tags = ','.join(tags)
        
    published_df = published_df.append({
        'name': picture_name,
        'post_id': 'id' + upload['id_string'],
        'post_date': date_of,
        'p_color': picture_color,
        'tags': tags
        }, ignore_index=True)
        
    print('\nPublished post!\n')

    return(published_df)


def edit_post(published_df, published_df_names_column, published_df_tags_column, published_df_id_column, picture_name, picture_color, blogname, date_of, client):

    '''
    Edit Post

    - Description
        Edits the date of publication of a preexistent Tumblr post

    - Parameters
        published_df: the dataframe with the uploaded post's data
        published_df_names_column: the name of the column of the dataframe containing the pictures' file names
        published_df_tags_column: the name of the column of the dataframe containing the publications' tags
        published_df_id_column: the name of the column of the dataframe containing the publications' idsas strings
        picture_name: the name of the image file
        picture_color: the principal color of the picture
        blogname: name of the Tumblr blog
        date_of: the new date of publication
        client: the Tumblr client

    '''

    row = published_df[published_df[published_df_names_column] == picture_name].index
            
    tags = published_df[published_df_tags_column][row[0]]
    tags = tags.split(sep = ',')
    tags = [tag for tag in tags if 'rgb' not in tag] + ['rgb: ' + picture_color.replace(',', '')]
                                    
    client.edit_post(blogname, id=published_df['post_id'][row[0]][2:], date = date_of, tags = tags)
                        
    published_df.loc[row, 'post_date'] = date_of
            
    tags = ','.join(tags)
    published_df.loc[row, 'tags'] = tags
            
    print('\nEdited post!\n')

    return(published_df)


def publisher(blogname, folder_of_pictures, picture_name, date_of, picture_color, csv_filename, client):

    '''
    Publisher Tool

    - Description
       Publishes an images or edits the publication date if it was already published.

    - Parameters
        blogname: name of the Tumblr blog
        folder_of_pictures: the name of the folder which contains the pictures
        picture_name: the name of the image file
        date_of: date of publication
        picture_color: the principal color of the image
        csv_filename: the csv file where the publications' info is stored
        client: the Tumblr client

    '''
    
    if os.path.exists(csv_filename + '.csv') == False:
        published = pd.DataFrame([], columns = ['name', 'post_id', 'post_date', 'p_color', 'tags'])
        published.to_csv(csv_filename + '.csv', index = False)
    
    published = pd.read_csv(csv_filename + '.csv')
    
    if picture_name not in published['name'].tolist():
        
        published = upload_post(folder_of_pictures, picture_name, blogname, picture_color, date_of, published, client)
        
    else:
        
        if picture_name in published['name'].tolist():
            
            published = edit_post(published, 'name', 'tags', 'post_id', picture_name, picture_color, blogname, date_of, client)
    
    row = published[published['name'] == picture_name].index
    print('Stats: \n\nblog name: ' + str(blogname) + '\nimage file: ' + str(published['name'][row[0]]) +
          '\npost id: ' + str(published['post_id'][row[0]][2:]) + '\ntags: ' + 
          str(published['tags'][row[0]]) + '\npost date: ' + 
          str(published['post_date'][row[0]]))
    
    published.sort_values(by=['post_date'], ascending = False)
    published.to_csv(csv_filename + '.csv', index = False) 
