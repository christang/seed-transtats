import matplotlib
from mpl_toolkits.basemap import Basemap


def plot_conus():
    """ Create a plot of the Continential US. """
    m = Basemap(
        llcrnrlon=-130.0,
        llcrnrlat=20.0,
        urcrnrlon=-60.0,
        urcrnrlat=55.0,
        projection='mill',
        resolution='c')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    return m


def plot_conus_precip(lats, lons, precip_in):
    m = plot_conus()
    cax = m.pcolormesh(lons, lats, precip_in, latlon=True, norm=norm,
                       cmap=precip_colormap)
    m.colorbar(cax)
    return m


# Colorbar with NSW Precip colors
nws_precip_colors = [
    "#04e9e7",  # 0.01 - 0.10 inches
    "#019ff4",  # 0.10 - 0.25 inches
    "#0300f4",  # 0.25 - 0.50 inches
    "#02fd02",  # 0.50 - 0.75 inches
    "#01c501",  # 0.75 - 1.00 inches
    "#008e00",  # 1.00 - 1.50 inches
    "#fdf802",  # 1.50 - 2.00 inches
    "#e5bc00",  # 2.00 - 2.50 inches
    "#fd9500",  # 2.50 - 3.00 inches
    "#fd0000",  # 3.00 - 4.00 inches
    "#d40000",  # 4.00 - 5.00 inches
    "#bc0000",  # 5.00 - 6.00 inches
    "#f800fd",  # 6.00 - 8.00 inches
    "#9854c6",  # 8.00 - 10.00 inches
    "#fdfdfd"   # 10.00+
]

levels = [0.01, 0.1, 0.25, 0.50, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0,
          6.0, 8.0, 10., 20.0]

norm = matplotlib.colors.BoundaryNorm(levels, 15)

precip_colormap = matplotlib.colors.ListedColormap(nws_precip_colors)

