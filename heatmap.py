"""
Accessibility UX Design – Publication Heatmap
==============================================
Generates a polished heatmap: Year × Document Type, coloured by
publication count, with average citations annotated in each cell.

Usage:
    python heatmap.py                           # uses default CSV path
    python heatmap.py path/to/your_file.csv     # custom path
"""

import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import LinearSegmentedColormap

warnings.filterwarnings("ignore")

# ── 1. Load data ────────────────────────────────────────────────────────────
CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else "accessibbility_UX_design.csv"

df = pd.read_csv(CSV_PATH)
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Cited by"] = pd.to_numeric(df["Cited by"], errors="coerce").fillna(0)

# Keep only years with at least 2 papers (removes sparse early outliers)
year_counts = df["Year"].value_counts()
valid_years = sorted(year_counts[year_counts >= 2].index)
df = df[df["Year"].isin(valid_years)]

# ── 2. Build pivot tables ────────────────────────────────────────────────────
# Order document types by overall frequency (most common → top)
doc_order = (
    df["Document Type"]
    .value_counts()
    .index.tolist()
)

pivot_count = (
    df.pivot_table(
        index="Document Type",
        columns="Year",
        values="Title",
        aggfunc="count",
        fill_value=0,
    )
    .reindex(doc_order)
    .reindex(columns=valid_years, fill_value=0)
)

pivot_citations = (
    df.pivot_table(
        index="Document Type",
        columns="Year",
        values="Cited by",
        aggfunc="mean",
        fill_value=0,
    )
    .reindex(doc_order)
    .reindex(columns=valid_years, fill_value=0)
)

# ── 3. Colour palette ────────────────────────────────────────────────────────
ACCENT   = "#6C63FF"   # indigo-violet
BG       = "#0F0F1A"   # near-black
CELL_BG  = "#1A1A2E"   # dark navy
TEXT_LT  = "#E8E8F0"
TEXT_DIM = "#8888AA"
GRID_COL = "#2A2A44"

cmap = LinearSegmentedColormap.from_list(
    "pub_heat",
    ["#1A1A2E", "#2D2B6B", "#5A52C4", "#9B8FFF", "#D4B8FF", "#FFE8A3"],
)

# ── 4. Figure layout ─────────────────────────────────────────────────────────
n_rows, n_cols = pivot_count.shape

fig_w = max(14, n_cols * 0.72 + 3)
fig_h = max(5,  n_rows * 0.95 + 3)

fig, ax = plt.subplots(figsize=(fig_w, fig_h))
fig.patch.set_facecolor(BG)
ax.set_facecolor(CELL_BG)

# ── 5. Draw heatmap ──────────────────────────────────────────────────────────
data = pivot_count.values.astype(float)
vmax = data.max()

im = ax.imshow(
    data,
    cmap=cmap,
    aspect="auto",
    vmin=0,
    vmax=vmax,
    interpolation="nearest",
)

# ── 6. Annotate cells ────────────────────────────────────────────────────────
for r in range(n_rows):
    for c in range(n_cols):
        count = int(pivot_count.iloc[r, c])
        if count == 0:
            continue
        avg_cit = pivot_citations.iloc[r, c]

        # Brightness of cell determines text colour
        norm_val = count / vmax if vmax > 0 else 0
        txt_col = TEXT_LT if norm_val > 0.35 else TEXT_DIM

        # Publication count – large
        ax.text(
            c, r, str(count),
            ha="center", va="center",
            fontsize=9.5, fontweight="bold",
            color=txt_col,
        )
        # Average citations – small, below
        if avg_cit > 0:
            ax.text(
                c, r + 0.30,
                f"({avg_cit:.1f}✦)",
                ha="center", va="center",
                fontsize=6.5,
                color=txt_col,
                alpha=0.80,
            )

# ── 7. Axes labels & ticks ───────────────────────────────────────────────────
ax.set_xticks(range(n_cols))
ax.set_xticklabels(
    [str(y) for y in valid_years],
    rotation=45, ha="right", fontsize=9, color=TEXT_LT,
)

ax.set_yticks(range(n_rows))
ax.set_yticklabels(pivot_count.index, fontsize=9, color=TEXT_LT)

ax.tick_params(colors=TEXT_LT, length=0)

# Grid lines between cells
ax.set_xticks(np.arange(-0.5, n_cols, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n_rows, 1), minor=True)
ax.grid(which="minor", color=GRID_COL, linewidth=0.8)
ax.tick_params(which="minor", length=0)

for spine in ax.spines.values():
    spine.set_edgecolor(GRID_COL)

# ── 8. Colour-bar ────────────────────────────────────────────────────────────
cbar = fig.colorbar(im, ax=ax, pad=0.015, fraction=0.03)
cbar.set_label("Number of Publications", color=TEXT_LT, fontsize=9, labelpad=8)
cbar.ax.yaxis.set_tick_params(color=TEXT_LT, labelsize=8)
cbar.outline.set_edgecolor(GRID_COL)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT_LT)

# ── 9. Titles & footnote ─────────────────────────────────────────────────────
ax.set_title(
    "Accessibility & UX Design Research",
    color=TEXT_LT, fontsize=15, fontweight="bold", pad=14,
)
ax.set_xlabel("Publication Year", color=TEXT_LT, fontsize=10, labelpad=8)
ax.set_ylabel("Document Type",   color=TEXT_LT, fontsize=10, labelpad=8)

fig.text(
    0.012, 0.01,
    "Cell: publication count  ·  (n.n✦) = avg citations  ·  years with <2 papers excluded",
    color=TEXT_DIM, fontsize=7, ha="left",
)

# ── 10. Save & show ──────────────────────────────────────────────────────────
plt.tight_layout(rect=[0, 0.03, 1, 1])
OUT = "accessibility_UX_heatmap.png"
plt.savefig(OUT, dpi=180, bbox_inches="tight", facecolor=BG)
print(f"✓  Saved → {OUT}")
plt.show()
