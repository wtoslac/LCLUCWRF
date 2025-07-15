def MonthTimeSeries(Time, Vals, Title, Labels, Show=False):
    import numpy as np
    import matplotlib.pyplot as plt
    # Ensure Vals has at least one series
    n_vals = len(Vals)
    assert 1 <= n_vals <= 5, "Vals must contain between 1 and 5 elements."

    # === Compute Mean Differences, RMSD, and IOA relative to the first series ===
    mean_diffs = []
    rmsds = []
    ioas = []
    ref = np.array(Vals[0])

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
        # Setup the figure and axes
        fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=False)

        colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange']
        markers = ['.k'] + colors  # First is the observed data in black

        # === Top Subplot ===
        axs[0].plot(Time[0:359], Vals[0][0:359], '.k', label=Labels[0])
        for i in range(1, n_vals):
            axs[0].plot(Time[0:359], Vals[i][0:359], linewidth=2+(4-i), 
                        label=Labels[i], color=colors[i-1])
        axs[0].set_ylabel(Labels[0])
        axs[0].set_title(Title)
        axs[0].grid(True)
        axs[0].legend()

        # === Bottom Subplot ===
        axs[1].plot(Time[359:718], Vals[0][359:718], '.k', label=Labels[0])
        for i in range(1, n_vals):
            axs[1].plot(Time[359:718], Vals[i][359:718], linewidth=2+(4-i), 
                        label=Labels[i], color=colors[i-1])
        axs[1].set_ylabel(Labels[0])
        axs[1].grid(True)
        axs[1].legend()

        # Add statistics to the plot (split into two columns)
        mean_text = "\n".join([f"MeanBias {Labels[i]}: {mean_diffs[i-1]:.2f}" for i in range(1, n_vals)])
        rmsd_text = "\n".join([f"RMSD     {Labels[i]}: {rmsds[i-1]:.2f}" for i in range(1, n_vals)])
        ioa_text = "\n".join([f"IOA     {Labels[i]}: {ioas[i-1]:.2f}" for i in range(1, n_vals)])

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

