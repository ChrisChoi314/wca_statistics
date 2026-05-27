import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from correlation_data import (
    FIGURES_DIR,
    calculate_percentile_correlation,
    latest_cubingcontests_export_dir,
    latest_wca_export_dir,
    load_cubingcontests_fto_single_ranks,
    load_wca_single_ranks,
)


def save_heatmap(matrix: np.ndarray, labels: list[str], output_path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(17, 14))
    vmin = float(np.nanmin(matrix))
    vmax = float(np.nanmax(matrix))
    cmap = plt.get_cmap("magma")
    image = ax.imshow(matrix, cmap=cmap, vmin=vmin, vmax=vmax)
    colorbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    colorbar.ax.tick_params(labelsize=11)

    ax.set_xticks(np.arange(len(labels)), labels=labels, rotation=90, fontsize=12)
    ax.set_yticks(np.arange(len(labels)), labels=labels, fontsize=12)
    ax.set_title(title, fontsize=16, pad=16)

    for row_index in range(matrix.shape[0]):
        for col_index in range(matrix.shape[1]):
            value = matrix[row_index, col_index]
            normalized = 0.5 if vmax == vmin else (value - vmin) / (vmax - vmin)
            red, green, blue, _ = cmap(normalized)
            luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
            ax.text(
                col_index,
                row_index,
                f"{value:.3f}",
                ha="center",
                va="center",
                color="black" if luminance > 0.55 else "white",
                fontsize=10,
            )

    ax.set_xticks(np.arange(matrix.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(matrix.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)
    ax.tick_params(which="minor", bottom=False, left=False)
    fig.tight_layout()
    fig.savefig(output_path)
    fig.savefig(output_path.with_suffix(".png"), dpi=300)
    plt.close(fig)


def print_matrix(labels: list[str], matrix: np.ndarray) -> None:
    print("\t" + "\t".join(labels))
    for label, row in zip(labels, matrix):
        print(label + "\t" + "\t".join(f"{value:.6f}" for value in row))


def main() -> None:
    wca_export_dir = latest_wca_export_dir()
    cubingcontests_export_dir = latest_cubingcontests_export_dir()

    wca_results = load_wca_single_ranks(wca_export_dir)
    fto_results = load_cubingcontests_fto_single_ranks(cubingcontests_export_dir)
    fto_person_ids = {str(row["personId"]) for row in fto_results}
    wca_results = [row for row in wca_results if str(row["personId"]) in fto_person_ids]
    results = wca_results + fto_results

    labels, people, corrmat, _ = calculate_percentile_correlation(results)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    date_label = cubingcontests_export_dir.name.replace("CubingContests_export_v1_", "")[:10]
    title = f"Event Percentile Rank Correlation + FTO (n = {len(people)})"
    save_heatmap(corrmat, labels, FIGURES_DIR / "correlation_fto.pdf", title)
    save_heatmap(corrmat, labels, FIGURES_DIR / f"correlation_fto_{date_label}.pdf", title)

    print(f"Loaded WCA export: {wca_export_dir}")
    print(f"Loaded CubingContests export: {cubingcontests_export_dir}")
    print(f"Matched FTO solvers with WCA IDs: {len(fto_person_ids)}")
    print(f"People in correlation matrix: {len(people)}")
    print("Correlation Matrix:")
    print_matrix(labels, corrmat)


if __name__ == "__main__":
    main()
