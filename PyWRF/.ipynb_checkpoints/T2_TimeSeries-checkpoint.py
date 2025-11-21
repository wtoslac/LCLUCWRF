## Loading the Libaries.
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import getvar, to_np, get_cartopy, latlon_coords, ll_to_xy, vertcross, interplevel,ALL_TIMES
import cartopy as cp
from glob import glob


def T2_TimeSeries(data_csv,model_pattern0,model_pattern1):
    ### Set the Variable you want to look at. ####
    Var = "T2"
    VarLabel = "Two-Meter Temperature [°C]"
    EPAVar = (np.loadtxt(data_csv, delimiter=',',usecols=[13])-32)*5/9
    ## Loading the data for the whole month #############
    files0 = sorted(glob(model_pattern0))
    files1 = sorted(glob(model_pattern1))
    
    # === Location of the EPA site===
    lat_point = 38.593322
    lon_point = -121.503795
    
    # === Use first file to find grid location ===
    sample_ds = Dataset(files0[0])
    xy_loc = ll_to_xy(sample_ds, lat_point, lon_point, as_int=True)
    x_idx, y_idx = int(xy_loc[0]), int(xy_loc[1])
    
    # === Extract and accumulate T2 at the target location ===
    Var0_all = []
    Var1_all = []
    Time_all = []
    
    for ifile in range(0,len(files0)):
    
        Var0 = getvar(Dataset(files0[ifile]), Var, timeidx=ALL_TIMES) 
        Var0_all.extend(to_np([Var0[y_idx, x_idx] - 273.15]))
        Time_all.append(Var0.Time.values)
        
        Var1 = getvar(Dataset(files1[ifile]), Var, timeidx=ALL_TIMES) 
        Var1_all.extend(to_np([Var1[y_idx, x_idx] - 273.15]))
    
    
    #### Setup the figures and axes.
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=False)
    
    #### Top subplot (first half)
    axs[0].plot(Time_all[0:359], EPAVar[0:359], '.k', label="T(°C) EPA Data")
    axs[0].plot(Time_all[0:359], Var0_all[0:359],linewidth=4, label="WRF FDDA0PBL2", color='tab:blue')
    axs[0].plot(Time_all[0:359], Var1_all[0:359],linewidth=3,  label="WRF FDDA1PBL2", color='tab:red')
    axs[0].set_ylabel(VarLabel)
    axs[0].set_title(VarLabel +" at 38.593322, -121.503795")
    axs[0].grid(True)
    axs[0].legend()
    
    # Bottom subplot (second half)
    axs[1].plot(Time_all[359:718], EPAVar[359:718], '.k', label="T(°C) EPA Data")
    axs[1].plot(Time_all[359:718], Var0_all[359:718],linewidth=4, label="WRF FDDA0PBL2", color='tab:blue')
    axs[1].plot(Time_all[359:718], Var1_all[359:718],linewidth=3,  label="WRF FDDA1PBL2", color='tab:red')
    axs[1].set_ylabel(VarLabel)
    #axs[1].set_title(VarLabel +" at 38.593322, -121.503795")
    axs[1].grid(True)
    axs[1].legend()
    
    # === Add the Mean Difference ======= #
    MeanDiff0=np.mean(np.array(Var0_all) - np.array(EPAVar))
    MeanDiff1=np.mean(np.array(Var1_all) - np.array(EPAVar))
    axs[0].text(0.01, -0.15, 
                f"MeanBias Blue-DATA: {MeanDiff0:.2f} °C\nMeanBias  Red-DATA: {MeanDiff1:.2f} °C",
                transform=axs[0].transAxes,
                fontsize=16,
                verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # === Add RMS Deviation to the plot ===
    rmsd0=np.sqrt(np.mean((np.array(Var0_all) - np.array(EPAVar)) ** 2))
    rmsd1=np.sqrt(np.mean((np.array(Var1_all) - np.array(EPAVar)) ** 2))
    axs[0].text(0.35, -0.15, 
                f"RMSD Blue-Data: {rmsd0:.2f} °C\nRMSD Red-Data: {rmsd1:.2f} °C",
                transform=axs[0].transAxes,
                fontsize=16,
                verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.show()