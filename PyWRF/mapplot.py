from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import get_cmap

from wrf import getvar, interplevel, to_np, get_basemap, latlon_coords

# Open the NetCDF file
#ncfile = Dataset("wrfout_d01_2025-01-02_00:00:00")
#ncfile = Dataset("../WRFOUT/wrfout_d01_2025-01-01_23:00:00")
ncfile = Dataset(" /data/wto/WRFOUT/run_CONUS_20250214/wrfout_d01_2025-01-01_00:00:00")

# Extract the pressure, geopotential height, and wind variables
p = getvar(ncfile, "pressure")
z = getvar(ncfile, "z", units="dm")
ua = getvar(ncfile, "ua", units="kt")
va = getvar(ncfile, "va", units="kt")
wspd = getvar(ncfile, "wspd_wdir", units="kts")[0,:]

# Interpolate geopotential height, u, and v winds to 500 hPa
ht_500 = interplevel(z, p, 500)
u_500 = interplevel(ua, p, 500)
v_500 = interplevel(va, p, 500)
wspd_500 = interplevel(wspd, p, 500)

# Get the lat/lon coordinates
lats, lons = latlon_coords(ht_500)

# Get the basemap object
bm = get_basemap(ht_500)

# Create the figure
fig = plt.figure(figsize=(12,9))
ax = plt.axes()

# Convert the lat/lon coordinates to x/y coordinates in the projection space
x, y = bm(to_np(lons), to_np(lats))

# Add the 500 hPa geopotential height contours
levels = np.arange(520., 580., 6.)
contours = bm.contour(x, y, to_np(ht_500), levels=levels, colors="black")
plt.clabel(contours, inline=1, fontsize=10, fmt="%i")

# Add the wind speed contours
levels = [25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120]
wspd_contours = bm.contourf(x, y, to_np(wspd_500), levels=levels,
                            cmap=get_cmap("rainbow"))
plt.colorbar(wspd_contours, ax=ax, orientation="horizontal", pad=.05)

# Add the geographic boundaries
bm.drawcoastlines(linewidth=0.25)
bm.drawstates(linewidth=0.25)
bm.drawcountries(linewidth=0.25)

# Add the 500 hPa wind barbs, only plotting every 125th data point.
bm.barbs(x[::125,::125], y[::125,::125], to_np(u_500[::125, ::125]),
         to_np(v_500[::125, ::125]), length=6)

plt.title("500 MB Height (dm), Wind Speed (kt), Barbs (kt)")

plt.show()
