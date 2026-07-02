import sys
import math
import argparse
from core.loader import load_column
from core.stats import summarize
from core.histogram import compute_histogram, render_ascii, render_matplotlib


def _fmt(value):
    """Format a numeric value, handling NaN gracefully."""
    if isinstance(value, float) and math.isnan(value):
        return "N/A (undefined)"
    return f"{value:.2f}"


def print_summary(column_name, stats):
    """Pretty-print the stats dict from summarize()."""
    print(f"\nSummary for '{column_name}'")
    print("-" * 40)
    print(f"{'Count':<20}{stats['n']}")
    print(f"{'Mean':<20}{_fmt(stats['mean'])}")
    print(f"{'Median':<20}{_fmt(stats['median'])}")
    print(f"{'Std dev (sample)':<20}{_fmt(stats['std_sample'])}")
    print(f"{'Std dev (population)':<20}{_fmt(stats['std_population'])}")
    print(f"{'Min':<20}{_fmt(stats['min'])}")
    print(f"{'25th percentile':<20}{_fmt(stats['p25'])}")
    print(f"{'50th percentile':<20}{_fmt(stats['p50'])}")
    print(f"{'75th percentile':<20}{_fmt(stats['p75'])}")
    print(f"{'Max':<20}{_fmt(stats['max'])}")
    print("-" * 40)


def main():
    parser = argparse.ArgumentParser(description="Compute stats on a CSV column using only NumPy")
    parser.add_argument("csv_path", help="Path to the CSV file")
    parser.add_argument("--column", required=True, help="Name of the column to analyze")
    parser.add_argument("--bins", type=int, default=10, help="Number of histogram bins")
    parser.add_argument("--plot", action="store_true", help="Also show a matplotlib histogram")
    args = parser.parse_args()

    try:
        scores = load_column(args.csv_path, args.column)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    stats = summarize(scores)
    print_summary(args.column, stats)

    counts, bin_edges = compute_histogram(scores, bins=args.bins)
    print(f"\nDistribution ({args.bins} bins)")
    print("-" * 40)
    print(render_ascii(counts, bin_edges))
    print("-" * 40)

    if args.plot:
        render_matplotlib(scores, bins=args.bins, column_name=args.column)


if __name__ == "__main__":
    main()

