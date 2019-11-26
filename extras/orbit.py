from pyorbital.orbital import Orbital
from datetime import datetime
from datetime import timedelta  

import pytz


def plot_map(service = 'World_Physical_Map', epsg = 4269, xpixels = 5000):
    # note, you need change the epsg for different region, 
    #US is 4269, and you can google the region you want
    plt.figure(figsize = (8, 8))
    m = Basemap(projection='mill',llcrnrlon=-123. ,llcrnrlat=37,
        urcrnrlon=-121 ,urcrnrlat=39, resolution = 'l', epsg = epsg)
    
    # xpixels controls the pixels in x direction, and if you leave ypixels
    # None, it will choose ypixels based on the aspect ratio
    m.arcgisimage(service=service, xpixels = xpixels, verbose= False)
    
    plt.show()



def get_latlon_corners(direction, satellite, duration, date):

    latlon_corners = 0


    return latlon_corners

duracion = 10.01*60
satelite = "noaa 19"
orb = Orbital(satelite)


#now = datetime.utcnow()
local_tz = pytz.timezone("America/Montevideo")
UTC_dif = 3
dtobj = datetime(2019,1,5,18+UTC_dif,19,18)
dtobj2= dtobj + timedelta(seconds=duracion)  


#aget_latlon_corners(direction, satellite, duracion, dtobj):


lon, lat, alt = orb.get_lonlatalt(dtobj)
lon2, lat2, alt2 = orb.get_lonlatalt(dtobj2)


print "Position:",  orb.get_position(dtobj)
print "Print lon:", lon
print "Print lon:", lat
print "Print lon:", alt
print "Print lon:", lon2
print "Print lon:", lat2
print "Print lon:", alt2

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# create new figure, axes instances.
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
#m = Basemap(width=12000000,height=9000000, projection='mill',
#            resolution='c',lat_1=0.,lat_2=55,lat_0=50,lon_0=-50.)

m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution=None,lat_0=-34.90328,lon_0=-56.18816)     
# draw a boundary around the map, fill the background.
# this background will end up being the ocean color, since
# the continents will be drawn on top.
#m.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
#m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
# label parallels on right and top
# meridians on bottom and left
parallels = np.arange(0.,81,10.)
# labels = [left,right,top,bottom]
m.drawparallels(parallels,labels=[False,True,True,False])
meridians = np.arange(10.,351.,20.)
m.drawmeridians(meridians,labels=[True,False,False,True])

# convert to map projection coords.
# Note that lon,lat can be scalars, lists or numpy arrays.
xpt,ypt = m(lon,lat)
xpt2,ypt2 = m(lon2,lat2)
print "Print lat:", xpt
print "Print lon:", ypt
print "Print lat:", xpt2
print "Print lon:", ypt2


# convert back to lat/lon
lonpt, latpt = m(xpt,ypt,inverse=True)
lonpt2, latpt2 = m(xpt2,ypt2,inverse=True)


m.plot(xpt,ypt,'bo')  # plot a blue dot there
m.plot(xpt2,ypt2,'bo')  # plot a blue dot there


m.drawgreatcircle(lonpt, latpt, lonpt2, latpt2, 
                  linewidth=2, color='b')
#m.warpimage(image='/home/gonzalo/Escritorio/imagen.png', scale = True)

# put some text next to the dot, offset a little bit
# (the offset is in map projection coordinates)
plt.text(xpt+100000,ypt+100000,'Inicio de captura (%5.1fW,%3.1fN)' % (lonpt,latpt))
plt.text(xpt2+100000,ypt2+100000,'Fin de captura (%5.1fW,%3.1fN)' % (lonpt2,latpt2))
plt.show()


