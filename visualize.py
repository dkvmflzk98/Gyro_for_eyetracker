import plotly.plotly as py
import numpy as np
from numpy import pi, sin, cos
from mpl_toolkits.basemap import Basemap


def degree2radians(degree):
    return degree*pi/180


def mapping_map_to_sphere(lon, lat, radius=1):
    # this function maps the points of coords (lon, lat) to points onto the  sphere of radius radius
    lon = np.array(lon, dtype=np.float64)
    lat = np.array(lat, dtype=np.float64)
    lon = degree2radians(lon)
    lat = degree2radians(lat)
    xs = radius * cos(lon) * cos(lat)
    ys = radius * sin(lon) * cos(lat)
    zs = radius * sin(lat)
    return xs, ys, zs


def sphere_heatmap(lon, lat, olr):
    print(lon.shape, lat.shape, olr.shape)

    tmp_lon = np.array([lon[n]-360 if l >= 180 else lon[n] for n, l in enumerate(lon)])

    i_east, = np.where(tmp_lon >= 0)
    i_west, = np.where(tmp_lon < 0)
    lon = np.hstack((tmp_lon[i_west], tmp_lon[i_east]))

    olr_ground = np.array(olr)
    olr = np.hstack((olr_ground[:, i_west], olr_ground[:, i_east]))

    # Make shortcut to Basemap object,
    # not specifying projection type for this example
    m = Basemap()

    colorscale = [[0.0, '#313695'],
     [0.07692307692307693, '#3a67af'],
     [0.15384615384615385, '#5994c5'],
     [0.23076923076923078, '#84bbd8'],
     [0.3076923076923077, '#afdbea'],
     [0.38461538461538464, '#d8eff5'],
     [0.46153846153846156, '#d6ffe1'],
     [0.5384615384615384, '#fef4ac'],
     [0.6153846153846154, '#fed987'],
     [0.6923076923076923, '#fdb264'],
     [0.7692307692307693, '#f78249'],
     [0.8461538461538461, '#e75435'],
     [0.9230769230769231, '#cc2727'],
     [1.0, '#a50026']]

    clons = np.array(lon.tolist()+[180], dtype=np.float64)
    clats = np.array(lat, dtype=np.float64)
    clons, clats = np.meshgrid(clons, clats)
    XS, YS, ZS = mapping_map_to_sphere(clons, clats)

    nrows, ncolumns = clons.shape
    OLR = np.zeros(clons.shape, dtype=np.float64)
    OLR[:, :ncolumns-1] = np.copy(np.array(olr,  dtype=np.float64))
    OLR[:, ncolumns-1] = np.copy(olr[:, 0])
    print(OLR)

    text = [['lon: '+'{:.2f}'.format(clons[i, j])+'<br>lat: '+'{:.2f}'.format(clats[i, j]) +
            '<br>W: '+'{:.2f}'.format(OLR[i][j]) for j in range(ncolumns)] for i in range(nrows)]

    sphere = dict(type='surface',
                x=XS,
                y=YS,
                z=ZS,
                colorscale=colorscale,
                surfacecolor=OLR,
                cmin=np.min(OLR),
                cmax=np.max(OLR),
                colorbar=dict(thickness=20, len=0.75, ticklen=4, title= 'W/m²'),
                text=text,
                hoverinfo='text')

    noaxis = dict(showbackground=False,
                  showgrid=False,
                  showline=False,
                  showticklabels=False,
                  ticks='',
                  title='',
                  zeroline=False)

    layout3d = dict(title='Outgoing Longwave Radiation Anomalies<br>Dec 2017-Jan 2018',
                    font=dict(family='Balto', size=14),
                    width=800,
                    height=800,
                    scene=dict(xaxis=noaxis,
                               yaxis=noaxis,
                               zaxis=noaxis,
                               aspectratio=dict(x=1,
                                                y=1,
                                                z=1),
                               camera=dict(eye=dict(x=1.15,
                                                    y=1.15,
                                                    z=1.15)
                                           )
                               ),
                    paper_bgcolor='rgba(235,235,235, 0.9)'
                    )

    fig = dict(data=[sphere], layout=layout3d)
    py.sign_in('yungkk87', 'hFD4gMKjr5YyORuEWCOz')
    py.plot(fig, filename='radiation-map2sphere')

