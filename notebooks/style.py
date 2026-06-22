"""Shared plot style and helpers for the matching pennies tutorial site."""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# -- Palette (matches matchingp) -----------------------------------------
CHOICE_COLORS = {"L": "#2A9DF4", "R": "#F45B69"}
STRATEGY_COLORS = {
    "biased": "#6366F1",
    "wsls": "#F59E0B",
    "perseverant": "#10B981",
}
STATE_COLORS = {
    0: "#2A9DF4",
    1: "#F45B69",
    2: "#6366F1",
    3: "#10B981",
}
MODEL_COLORS = {
    "GLM-HMM": "#2A9DF4",
    "Q-learning": "#F45B69",
    "Logistic Reg.": "#6366F1",
}

# -- Stylesheet -----------------------------------------------------------
def apply_style():
    style = {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.8,
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "axes.titleweight": "medium",
        "axes.labelcolor": "#333333",
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "figure.dpi": 150,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
    }
    mpl.rcParams.update(style)


# -- Choice raster (matchingp style) -------------------------------------
def plot_choices(df, shade_strategy=True, fig=None, ax=None):
    """Tick-mark choice plot.

    Left choices are drawn upward, right choices downward.  Filled circles
    mark rewarded trials.
    """
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=(12, 2.0))

    n = len(df)

    choice = df["choice"].values
    reward = (df["reward"].values > 0).astype(int)

    left_idx = np.where(choice == "L")[0]
    right_idx = np.where(choice == "R")[0]

    for idx in left_idx:
        ax.plot([idx, idx], [0, 1], color=CHOICE_COLORS["L"], lw=0.8, alpha=0.85)
    for idx in right_idx:
        ax.plot([idx, idx], [0, -1], color=CHOICE_COLORS["R"], lw=0.8, alpha=0.85)

    left_rew = np.where((choice == "L") & (reward == 1))[0]
    right_rew = np.where((choice == "R") & (reward == 1))[0]
    ax.scatter(left_rew, np.ones(len(left_rew)), color=CHOICE_COLORS["L"],
               s=8, lw=0, clip_on=False, zorder=3)
    ax.scatter(right_rew, -np.ones(len(right_rew)), color=CHOICE_COLORS["R"],
               s=8, lw=0, clip_on=False, zorder=3)

    ax.axhline(0, color="#333333", lw=1.2, zorder=2)

    # Strategy shading + legend
    if shade_strategy and "strategy" in df.columns:
        _shade_strategies(df, ax)
        from matplotlib.patches import Patch
        present = df["strategy"].unique()
        handles = [Patch(facecolor=STRATEGY_COLORS.get(s, "#CCCCCC"),
                         alpha=0.3, label=s)
                   for s in present if s in STRATEGY_COLORS]
        if handles:
            ax.legend(handles=handles, loc="upper right", fontsize=7, ncol=len(handles))

    ax.set_xlim(0, n)
    ax.set_ylim(-1.3, 1.55)
    ax.spines["left"].set_bounds(-1, 1)
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels([])
    ax.text(-0.01, 1.3, "L", transform=ax.get_yaxis_transform(),
            ha="right", va="center", fontsize=10, color=CHOICE_COLORS["L"],
            fontweight="bold")
    ax.text(-0.01, -1.3, "R", transform=ax.get_yaxis_transform(),
            ha="right", va="center", fontsize=10, color=CHOICE_COLORS["R"],
            fontweight="bold")
    ax.set_xlabel("Trial")

    return fig, ax


def _shade_strategies(df, ax):
    """Add light background shading by strategy label."""
    if "strategy" not in df.columns:
        return
    strategies = df["strategy"].values
    prev = strategies[0]
    start = 0
    for i in range(1, len(strategies)):
        if strategies[i] != prev or i == len(strategies) - 1:
            end = i if strategies[i] != prev else i + 1
            c = STRATEGY_COLORS.get(prev, "#CCCCCC")
            ax.axvspan(start, end, color=c, alpha=0.08, zorder=-1)
            start = i
            prev = strategies[i]
