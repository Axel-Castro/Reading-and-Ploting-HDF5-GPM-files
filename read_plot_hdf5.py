import h5py 
import glob
import numpy as np
import matplotlib.pylab as plt
import cartopy.crs as ccrs   
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

from mpl_toolkits.basemap import Basemap, cm
def read(filename):
    dset=h5py.File(filename,"r")
    lat=dset["Grid/lat"][:]
    lon=dset["Grid/lon"][:]
    rain=dset["Grid/precipitationCal"][:]
    rain[rain==-9999.9]=np.nan
    fecha=filename.split("/")
    fecha=fecha[-1].split(".")
    return lat,lon,rain,fecha[3]+"_"+fecha[4]+"_"+fecha[5]+"_"+fecha[6]
    
#######################################################

def colorbarprecip():
        import matplotlib 
        colors=['#ffffff','#00fae9','#00d553','#acea00','#f8fd00','#ff6800','#fe071d','#f92db4','#bf32ff','#5f30ff','#3131c3','#202053',
                 '#4d4d4d','#adadad','#e7dace','#e4bd9a','#c5a385','#824f1d','#0e0700']

        lvs=[0.1,0.5,1,2.5,5,7.5,10,15,20,30,45,65,85,110,150,250,350,500]
        cmap,norm=matplotlib.colors.from_levels_and_colors(lvs,colors,extend="both")
        return cmap,norm,lvs




def read_precip(lat,lon,rain,fecha,path):
   
    fig=plt.figure(figsize=(12,9))
    
    
    lon,lat=np.meshgrid(lon,lat)
    
    Lat_cond= (lat> 15.) & (lat< 30.)
    Lon_cond= (lon> -87.) & (lon < -71.)
    
    lat_lon=Lat_cond & Lon_cond
    num_lat=np.where(Lat_cond[:,0]==True)
    num_lon=np.where(Lon_cond[0,:]==True)
    
    dim_lat,dim_lon=len(num_lat[0]),len(num_lon[0])
   
    rain=rain.T
    lat=lat[lat_lon].reshape((dim_lat,dim_lon))
    lon=lon[lat_lon].reshape((dim_lat,dim_lon))
    rain=rain[lat_lon].reshape((dim_lat,dim_lon))
    
    
    cmap = cm.s3pcpn_l
    clevs = np.array([0.1, 0.6, 1, 2, 4, 6, 8, 12, 17, 21, 25, 33, 40, 50, 65, 80])   
    crs = ccrs.PlateCarree()
    ax=plt.subplot(111,projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.6)
    ax.add_feature(cfeature.STATES, linewidth=0.6)
    
    cf = ax.contourf(lon, lat, rain,clevs,cmap=cmap,transform=ccrs.PlateCarree(), extend='both')
    ax.set_extent([np.min(lon),np.max(lon),np.min(lat),np.max(lat)], crs=ccrs.PlateCarree())
    paso_h=5
    cbposition='vertical'
    unit="mm"
        
    cb = fig.colorbar(cf, orientation=cbposition, aspect=40,shrink=0.6,pad=0.06)
    cb.set_label(unit, size='small')

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=3, color='gray', alpha=0.2, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_left = True
    gl.ylabels_right = False
    gl.xlines = True

    lons=np.arange(np.ceil(lon.min())-paso_h,np.ceil(lon.max()+paso_h),paso_h)
    gl.xlocator = mticker.FixedLocator(lons)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 15, 'color': 'gray'}
    gl.xlabel_style = {'color': 'black'}
    plt.savefig(path_output+"Rain_cartopy_"+fecha+".png",dpi=600.)
   
    plt.close()
        
    np.savetxt(path+"lat/"+str(fecha)+"_lat.txt",lat)
    np.savetxt(path+"lon/"+str(fecha)+"_lon.txt",lon)
    np.savetxt(path+"rain/"+str(fecha)+"_rain.txt",rain)
    
path="GPM/20161004/"
path_output="GPM_NEW/"

lista=glob.glob(path+"*.HDF5")
lista.sort()
for i in lista:
    print (i)
    lat,lon,rain,fecha=read(i)
    read_precip(lat,lon,rain,fecha,path_output)
#    plot_basemap(lat,lon,rain,fecha,path_output)
    
