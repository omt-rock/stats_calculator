import numpy as np


def compute_histogram(arr, bins=10):
    """
    Bucket the data into bins and count values in each.
    Returns (counts, bin_edges) — pure NumPy, no display logic here.
    """
    counts, bin_edges = np.histogram(arr, bins=bins)
    return counts, bin_edges


def render_ascii(counts, bin_edges, width=40):
    """
    Turn (counts, bin_edges) into a printable ASCII bar chart string.
    Kept separate from compute_histogram so you can swap this out
    for a matplotlib version without touching the binning logic.
    """
    max_count = counts.max() if counts.max() > 0 else 1
    lines = []
    for i in range(len(counts)):
        low, high = bin_edges[i], bin_edges[i + 1]
        bar_len = int((counts[i] / max_count) * width)
        bar = "#" * bar_len
        lines.append(f"{low:6.1f}-{high:6.1f} | {bar} ({counts[i]})")
    return "\n".join(lines)


def render_matplotlib(arr, bins=10, save_path=None, column_name="value"):
    """
    Optional: render an actual histogram image using matplotlib.
    Only called if the user passes --plot; keeps matplotlib an
    optional dependency rather than a hard requirement.
    """
    import matplotlib.pyplot as plt  # imported here, not at module top

    fig, ax = plt.subplots()
    ax.hist(arr, bins=bins, edgecolor="black")
    ax.set_xlabel(column_name)
    ax.set_ylabel("Frequency")
    ax.set_title(f"Distribution of {column_name}")

    if save_path:
        fig.savefig(save_path)
        print(f"Histogram saved to {save_path}")
    else:
        plt.show()

    plt.close(fig)