## Loading the Libaries.
import numpy as np
import matplotlib.pyplot as plt

def MonthTimeSeries(Time,Vals,Vals_Label,Show):
    # === Add the Mean Difference ======= #
    MeanDiff0=np.mean(np.array(Vals[1]) - np.array(Vals[0]))
    MeanDiff1=np.mean(np.array(Vals[2]) - np.array(Vals[0]))
    
    # === Add RMS Deviation to the plot ===
    rmsd0=np.sqrt(np.mean((np.array(Vals[1]) - np.array(Vals[0])) ** 2))
    rmsd1=np.sqrt(np.mean((np.array(Vals[2]) - np.array(Vals[0])) ** 2))
    if(Show):
        #### Setup the figures and axes.
        fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=False)
        
        #### Top subplot (first half)
        axs[0].plot(Time[0:359], Vals[0][0:359], '.k', label=Vals_Label[0])
        axs[0].plot(Time[0:359], Vals[1][0:359],linewidth=4, label=Vals_Label[1], color='tab:blue')
        axs[0].plot(Time[0:359], Vals[2][0:359],linewidth=3,  label=Vals_Label[2], color='tab:red')
        axs[0].set_ylabel(Vals_Label[0])
        axs[0].set_title(Vals_Label[0])
        axs[0].grid(True)
        axs[0].legend()
        
        # Bottom subplot (second half)
        axs[1].plot(Time[359:718], Vals[0][359:718], '.k', label=Vals_Label[0])
        axs[1].plot(Time[359:718], Vals[1][359:718],linewidth=4, label=Vals_Label[1], color='tab:blue')
        axs[1].plot(Time[359:718], Vals[2][359:718],linewidth=3,  label=Vals_Label[2], color='tab:red')
        axs[1].set_ylabel(Vals_Label[0])
        axs[1].grid(True)
        axs[1].legend()
        axs[0].text(0.35, -0.15, 
                    f"RMSD Blue-Data: {rmsd0:.2f}\nRMSD Red-Data: {rmsd1:.2f}",
                    transform=axs[0].transAxes,
                    fontsize=16,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        axs[0].text(0.01, -0.15, 
                    f"MeanBias Blue-Data: {MeanDiff0:.2f}\nMeanBias  Red-Data: {MeanDiff1:.2f}",
                    transform=axs[0].transAxes,
                    fontsize=16,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.show()

    return [[MeanDiff0,MeanDiff1],[rmsd0,rmsd1]]