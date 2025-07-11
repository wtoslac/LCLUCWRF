## Loading the data for the whole month #############
# === Location of the EPA site===
lat_point = 38.593322
lon_point = -121.503795
## User Parameters
### Set the Variable you want to look at. ####
Var = "T2"
VarLabel = "Two-Meter Temperature [°C]"
 
# === Load all WRF output files ===
data_path0 = "/data/wto/WRFOUT/Sac_NDown_UCM1/"  # Update if needed
file_pattern0 = "wrfout_d01_2020-06-*"
files0 = sorted(glob(f"{data_path0}/{file_pattern0}"))
 
data_path1 = "/data/wto/WRFOUT/Sac_NDown_UCM1_PBL2_250710/"  # Update if needed
file_pattern1 = "wrfout_d01_2020-06-*"
files1 = sorted(glob(f"{data_path1}/{file_pattern1}"))
 
# === Use first file to find grid location ===
sample_ds = Dataset(files0[0])
xy_loc = ll_to_xy(sample_ds, lat_point, lon_point, as_int=True)
x_idx, y_idx = int(xy_loc[0]), int(xy_loc[1])
 
# === Extract and accumulate T2 at the target location ===
Var0_all = []
Var1_all = []
Time_all = []
 
for ifile in range(0,len(files0)):
 
    Var0 = getvar(Dataset(files0[ifile]), Var, timeidx=ALL_TIMES)  # May return 2D or 3D
    Var0_all.extend(to_np([Var0[y_idx, x_idx] - 273.15]))
    Time_all.append(Var0.Time.values)
    Var1 = getvar(Dataset(files1[ifile]), Var, timeidx=ALL_TIMES)  # May return 2D or 3D
    Var1_all.extend(to_np([Var1[y_idx, x_idx] - 273.15]))
 
 
#### Setup the figures and axes.
fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=False)
 
#### Top subplot (first half)
axs[0].plot(Time_all[0:359], EPAVar[0:359], '.k', label="T(°C) EPA Data")
axs[0].plot(Time_all[0:359], Var0_all[0:359],linewidth=4, label="WRF FDDA0", color='tab:blue')
axs[0].plot(Time_all[0:359], Var1_all[0:359],linewidth=3,  label="WRF FDDA1", color='tab:red')
axs[0].set_ylabel(VarLabel)
axs[0].set_title(VarLabel +" at 38.593322, -121.503795")
axs[0].grid(True)
axs[0].legend()
 
# Bottom subplot (second half)
axs[1].plot(Time_all[359:718], EPAVar[359:718], '.k', label="T(°C) EPA Data")
axs[1].plot(Time_all[359:718], Var0_all[359:718],linewidth=4, label="WRF FDDA0", color='tab:blue')
axs[1].plot(Time_all[359:718], Var1_all[359:718],linewidth=3,  label="WRF FDDA1", color='tab:red')
axs[1].set_ylabel(VarLabel)
#axs[1].set_title(VarLabel +" at 38.593322, -121.503795")
axs[1].grid(True)
axs[1].legend()
 
# === Add the Mean Difference ======= #
MeanDiff0=np.mean(np.array(Var0_all) - np.array(EPAVar))
MeanDiff1=np.mean(np.array(Var1_all) - np.array(EPAVar))
axs[0].text(0.01, -0.15, 
            f"AvgDiff WRF FDDA0: {MeanDiff0:.2f} °C\nAvgDiff  WRF FDDA1: {MeanDiff1:.2f} °C",
            transform=axs[0].transAxes,
            fontsize=16,
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
 
# === Add RMS Deviation to the plot ===
rmsd0=np.sqrt(np.mean((np.array(Var0_all) - np.array(EPAVar)) ** 2))
rmsd1=np.sqrt(np.mean((np.array(Var1_all) - np.array(EPAVar)) ** 2))
axs[0].text(0.35, -0.15, 
            f"RMSD WRF FDDA0: {rmsd0:.2f} °C\nRMSD WRF FDDA1: {rmsd1:.2f} °C",
            transform=axs[0].transAxes,
            fontsize=16,
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
 
plt.tight_layout()
plt.show()
