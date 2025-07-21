import numpy as np
import matplotlib.pyplot as plt

def MonthTimeSeries(Time, Vals, Title, Labels, Show=False):
    # Ensure Vals has at least one series
    n_vals = len(Vals)
    assert 1 <= n_vals <= 5, "Vals must contain between 1 and 5 elements."

    # Convert Vals[0] to np.array for masking
    ref = np.array(Vals[0])
    
    # === Compute Mean Differences, RMSD, and IOA relative to the first series ===
    mean_diffs = []
    rmsds = []
    ioas = []

    for i in range(1, n_vals):
        model = np.array(Vals[i])
        diff = model - ref
        mean_diffs.append(np.mean(diff))
        rmsds.append(np.sqrt(np.mean(diff ** 2)))
        
        # Index of Agreement (Willmott 1981)
        numerator = np.sum((model - ref) ** 2)
        denominator = np.sum((np.abs(model - np.mean(ref)) + np.abs(ref - np.mean(ref))) ** 2)
        ioa = 1 - numerator / denominator if denominator != 0 else np.nan
        ioas.append(ioa)

    if Show:
        fig, axs = plt.subplots(2, 1, figsize=(16, 12), sharex=False)

        colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange']
        markers = ['.k'] + colors  # First is the observed data in black

        # === Top Subplot ===
        # Apply mask to Vals[0] for -9999
        t_top = np.array(Time[0:359])
        v0_top = np.array(Vals[0][0:359])
        mask_top = v0_top != -9999
        axs[0].plot(t_top[mask_top], v0_top[mask_top], '.k', label=Labels[0])
        for i in range(1, n_vals):
            axs[0].plot(Time[0:359], Vals[i][0:359], linewidth=1+(4-i),
                        label=Labels[i], color=colors[i-1])

        axs[0].set_ylabel(Labels[0])
        axs[0].set_title(Title)
        axs[0].grid(True)
        axs[0].legend()

        # === Bottom Subplot ===
        t_bot = np.array(Time[359:718])
        v0_bot = np.array(Vals[0][359:718])
        mask_bot = v0_bot != -9999
        axs[1].plot(t_bot[mask_bot], v0_bot[mask_bot], '.k', label=Labels[0])
        for i in range(1, n_vals):
            axs[1].plot(Time[359:718], Vals[i][359:718], linewidth=1+(4-i),
                        label=Labels[i], color=colors[i-1])

        axs[1].set_ylabel(Labels[0])
        axs[1].grid(True)
        axs[1].legend()

        # Add statistics to the plot
        mean_text = "\n".join([f"MeanBias: {Labels[i]}: {mean_diffs[i-1]:.2f}" for i in range(1, n_vals)])
        rmsd_text = "\n".join([f"RMSD:     {Labels[i]}: {rmsds[i-1]:.2f}" for i in range(1, n_vals)])
        ioa_text = "\n".join([f"IOA:     {Labels[i]}: {ioas[i-1]:.2f}" for i in range(1, n_vals)])

        axs[0].text(0.01, -0.1, mean_text,
                    transform=axs[0].transAxes,
                    fontsize=14,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

        axs[0].text(0.35, -0.1, rmsd_text,
                    transform=axs[0].transAxes,
                    fontsize=14,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        axs[0].text(0.69, -0.1, ioa_text,
                    transform=axs[0].transAxes,
                    fontsize=14,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

        plt.tight_layout()
        plt.show()

    return [mean_diffs, rmsds, ioas]

from netCDF4 import Dataset
from wrf import getvar, to_np, ll_to_xy, ALL_TIMES
from glob import glob

def MonthGlob(folders, Var, lat_point, lon_point, offset = 0):
    """
    Extract time series data from multiple WRF output folders for a specified variable and location.

    Args:
        folders (list of str): Paths to WRF output folders or file globs.
        Var (str): Variable to extract (e.g., 'T2').
        lat_point (float): Latitude of point.
        lon_point (float): Longitude of point.

    Returns:
        Time_all (np.ndarray): Time values (from the first dataset).
        Vals (list of np.ndarray): Extracted variable values for each folder.
    """
    Vals = []
    Time = []

    # Use the first file of the first folder to find the grid index
    sample_files = sorted(glob(folders[0]))
    sample_ds = Dataset(sample_files[0])
    x_idx, y_idx = map(int, ll_to_xy(sample_ds, lat_point, lon_point, as_int=True))

    # Loop through all folders / file globs
    for folder in folders:
        files = sorted(glob(folder))
        thisVal = []

        for f in files:
            ds = Dataset(f)
            var_data = getvar(ds, Var, timeidx=ALL_TIMES)
            thisVal.extend(to_np([var_data[y_idx, x_idx] + offset]))  # Kelvin to Celsius

            # Time info: only take once from the first folder
            if len(Time)<30*24:
                Time.append(var_data.Time.values)

        Vals.append(np.array(thisVal))

    return Time, Vals