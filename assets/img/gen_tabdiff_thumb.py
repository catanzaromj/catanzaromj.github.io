"""
Generate thumbnail for the tabular diffusion project.
Shows the reverse diffusion process: noisy samples -> structured tabular distribution.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
from scipy.stats import gaussian_kde

rng = np.random.default_rng(42)

# --- Simulate a 2D projection of tabular data at different noise levels ---
# True data: mixture of Gaussians (represents realistic tabular marginals)
n = 600
centers = np.array([[-1.5, -1.0], [1.5, -1.0], [0.0, 1.5]])
weights = [0.35, 0.35, 0.30]
samples = []
for i, (c, w) in enumerate(zip(centers, weights)):
    k = int(n * w)
    samples.append(rng.multivariate_normal(c, [[0.18, 0.0], [0.0, 0.18]], k))
x_clean = np.vstack(samples)

# Noise schedule: linear, from t=1 (noisy) to t=0 (clean)
timesteps = [1.0, 0.65, 0.30, 0.0]
labels = [r"$t = T$", r"$t = 0.65T$", r"$t = 0.3T$", r"$t = 0$"]
signal_scale = [0.0, 0.45, 0.78, 1.0]   # how much clean signal
noise_scale  = [1.0, 0.55, 0.22, 0.0]   # how much noise remains

fig = plt.figure(figsize=(7.5, 2.2), facecolor="#0f1117")
gs = gridspec.GridSpec(1, 4, figure=fig, wspace=0.12,
                       left=0.02, right=0.98, top=0.82, bottom=0.05)

cmap_pts  = "#7ec8e3"   # light blue for points
cmap_bg   = "#0f1117"   # dark background

for col, (sig, nse, lbl) in enumerate(zip(signal_scale, noise_scale, labels)):
    ax = fig.add_subplot(gs[col])
    ax.set_facecolor(cmap_bg)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor("#333344")

    # Interpolate between pure noise and clean data
    noise = rng.normal(0, 1.2, x_clean.shape)
    pts = sig * x_clean + nse * noise

    # Scatter
    alpha = 0.18 + 0.55 * sig   # more opaque as we approach clean
    size  = 4 + 8 * sig
    ax.scatter(pts[:, 0], pts[:, 1],
               s=size, c=cmap_pts, alpha=alpha, linewidths=0)

    # KDE contour only for cleaner timesteps
    if sig > 0.3:
        try:
            kde = gaussian_kde(pts.T, bw_method=0.35)
            grid_x = np.linspace(-3.5, 3.5, 80)
            grid_y = np.linspace(-3.5, 3.5, 80)
            xx, yy = np.meshgrid(grid_x, grid_y)
            zz = kde(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
            ax.contour(xx, yy, zz, levels=4, colors=["#4a9eca"],
                       linewidths=0.7, alpha=0.6)
        except Exception:
            pass

    ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5)
    ax.set_title(lbl, color="#ccddee", fontsize=9, pad=3,
                 fontfamily="monospace")

# Arrow between panels (drawn in figure coords)
for x_pos in [0.255, 0.505, 0.755]:
    fig.patches.append(
        FancyArrowPatch(
            (x_pos - 0.005, 0.46), (x_pos + 0.025, 0.46),
            transform=fig.transFigure,
            arrowstyle="->, head_width=0.3, head_length=0.3",
            color="#5588aa", linewidth=1.2,
            mutation_scale=10,
        )
    )

# Title
fig.text(0.5, 0.94, "Reverse Diffusion on Tabular Data",
         ha="center", va="center", color="#aabbcc",
         fontsize=10, fontfamily="monospace")

out = "tabular_diffusion_thumb.png"
plt.savefig(out, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved {out}")
plt.close()
