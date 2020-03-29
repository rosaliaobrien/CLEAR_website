import pandas as pd
import numpy as np
import csv
from sklearn import neighbors

def dist(i, arr):

	#use sklearn to find distance to each object is to each other
	tree = neighbors.BallTree(arr, leaf_size=2)
	dist, ind = tree.query(arr[[i]], k=2)

	return dist

def create_data(field, sc=None):
    
    #read field .cat file that has all necessary info
    data = pd.read_csv('/Users/rosaliaobrien/research/website/website_data/'+field+'.cat', sep=' ')

    #create array that only contains the x and y pos's of each object
    arr = data.to_numpy()
    arr = np.delete(arr, 0, 1)
    arr = np.delete(arr, 0, 1)
    arr = np.delete(arr, 0, 1)
    arr = np.delete(arr, 2, 1)

    #define the id #'s
    gids=data['ids']

    #create empty arrays for indices of objects that are close, very close, and medium close
    #to one another (will define circle radius based off this)
    closeob = np.array([], dtype='int')
    veryclose = np.array([], dtype='int')
    medclose = np.array([], dtype='int')
    farob = np.array([], dtype='int')

    #let a distance (defined by dist function) less than 30 be "close, 
    #less than 15 be "medium close" and less than 10 be "very close"
    for i, v in enumerate(arr):
        if dist(i, arr)[0][1] < 60:
            farob = np.append(farob, int(i))
        if dist(i, arr)[0][1] < 30:
            closeob = np.append(closeob, int(i))
    #         print(i, dist(i))
        if dist(i, arr)[0][1] < 15:
            medclose = np.append(medclose, int(i))
    #         print(i, dist(i))
        if dist(i, arr)[0][1] < 10:
            veryclose = np.append(veryclose, int(i))
    #         print(i, dist(i))

    #define scale factor so circles adjust based on scale of image (all based GN1, where sc = 4)
    newsc = 4/sc

    #let the default circle radius be 5
    circrad = np.array([10*newsc]*len(data))
    
    #let close radius be 3
    newrad1 = np.array([3*newsc]*len(closeob))
    
    #let very close radius be 1
    newrad2 = np.array([1*newsc]*len(veryclose))
    
    #let medium close radius be 2
    newrad3 = np.array([2*newsc]*len(medclose))
    
    #let far away objects radius be 7
    newrad4 = np.array([5*newsc]*len(farob))
    
    #update circrad with varying radii
    perform4 = np.put(circrad, farob, newrad4)
    perform = np.put(circrad, closeob, newrad1)
    perform3 = np.put(circrad, medclose, newrad3)
    perform2 = np.put(circrad, veryclose, newrad2)

    #add circle variable radius to dataframe
    data['circrad'] = circrad
    
    return data

def circle_var(gidn, radius, field, show_circles):
    text1="var circle = L.circle(gid{0}, ".format(gidn)
    
    if show_circles == True:
        text2="{\n\
color: 'red',\n\
fillOpacity: 0,\n\
weight: 0.8,\n\
opacity: 3,\n"
        
    if show_circles == False:
        text2="{\n\
color: 'red',\n\
fillOpacity: 0,\n\
opacity: 0,\n"       

    text3="radius:{0}".format(radius)
    
    text4="}).addTo(map);"
    
    text5="circle.bindPopup('gid#{0}: ' + '<a href=".format(gidn)
    
    text6='"bio_pages/{1}_{0}.html" target="_blank">'.format(gidn, field)
    
    text7="BIO PAGE</a>')\n\
circle.on('mouseover', function (e) {"
    
    text8="circlegid='{0}';\n\
document.getElementById('circle_tracker').innerHTML=circlegid".format(gidn)
    
    text9="});\n\
circle.on('mouseout', function (e) {\n\
circlegid='Move cursor over object';\n\
document.getElementById('circle_tracker').innerHTML=circlegid\n\
});"
    
    return text1 + text2 + text3 + text4 + text5 +text6 + text7 + text8 + text9

def prnt_circstyle(gid, radii, field, show_circles):
    for i, r in zip(gid, radii):
            variables=circle_var(i,r,field, show_circles)
            print(variables)

#return object variable in the form of a string for each object
# "sc" refers to a "scale factor" used
def circle_pos(x_pos ,y_pos ,gidn):
    text='var gid{0} = xy({1}/sc, {2}/sc)'.format(gidn, x_pos, y_pos)
    return text

def prnt_circloc(field, y_len, adjustx, adjusty):
    data = pd.read_csv('/Users/rosaliaobrien/research/website/website_data/'+field+'.cat', sep=' ')
    
    gid = data['ids']
    xpos = data['x']*adjustx
    ypos = data['y']*adjusty

    for i, x, y in zip(gid, xpos, ypos):
            positions=circle_pos(x,np.abs(y - y_len),i)
            print(positions)

def prnt_both(field, gid, radii, y_len, show_circles=False, adjustx = 1, adjusty = 1):
    prnt_circloc(field, y_len, adjustx, adjusty)
    prnt_circstyle(gid, radii, field, show_circles)