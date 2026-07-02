import math
import os
import tempfile
import numpy as np
import pytest
from core.stats import compute_mean, compute_median, compute_std, compute_percentiles, summarize
from core.histogram import compute_histogram, render_ascii
from core.loader import load_column


# A small, hand-computable dataset. Small on purpose — you should be
# able to verify every expected value below with a calculator, not
# trust that it's right because NumPy said so.
SAMPLE = np.array([55, 62, 70, 74, 78, 82, 85, 90, 95, 100])


def test_mean():
    # (55+62+70+74+78+82+85+90+95+100) / 10 = 791 / 10
    assert compute_mean(SAMPLE) == pytest.approx(79.1)


def test_median_even_length():
    # n=10 (even) -> average of sorted[4] and sorted[5] -> (78+82)/2
    assert compute_median(SAMPLE) == pytest.approx(80.0)


def test_median_odd_length():
    # n=5 (odd) -> exact middle value, no averaging
    odd_sample = np.array([10, 20, 30, 40, 50])
    assert compute_median(odd_sample) == pytest.approx(30.0)


def test_std_sample_vs_population():
    sample_std = compute_std(SAMPLE, sample=True)
    population_std = compute_std(SAMPLE, sample=False)

    # sample std (divides by n-1) is always >= population std (divides by n)
    # for the same data, since n-1 < n makes the divisor smaller
    assert sample_std > population_std
    assert sample_std == pytest.approx(14.28, abs=0.01)
    assert population_std == pytest.approx(13.55, abs=0.01)


def test_percentiles():
    result = compute_percentiles(SAMPLE, (25, 50, 75))
    assert result[50] == pytest.approx(80.0)          # median should match p50
    assert result[25] == pytest.approx(71.0, abs=0.01)  # 70 + 0.25*(74-70) = 71.0
    assert result[75] == pytest.approx(88.75, abs=0.01)  # 85 + 0.75*(90-85) = 88.75


def test_percentile_25_50_75_ordering():
    # sanity check that applies to ANY dataset: percentiles should
    # always come out in ascending order
    result = compute_percentiles(SAMPLE, (25, 50, 75))
    assert result[25] <= result[50] <= result[75]


def test_summarize_returns_all_keys():
    stats = summarize(SAMPLE)
    expected_keys = {"n", "mean", "median", "std_sample", "std_population",
                      "p25", "p50", "p75", "min", "max"}
    assert set(stats.keys()) == expected_keys
    assert stats["n"] == 10
    assert stats["min"] == 55
    assert stats["max"] == 100


def test_histogram_counts_sum_to_n():
    # every value must land in exactly one bin -> counts must sum to n
    counts, bin_edges = compute_histogram(SAMPLE, bins=5)
    assert counts.sum() == len(SAMPLE)
    assert len(bin_edges) == 6  # n bins -> n+1 edges


def test_histogram_ascii_renders_without_error():
    counts, bin_edges = compute_histogram(SAMPLE, bins=5)
    output = render_ascii(counts, bin_edges)
    assert isinstance(output, str)
    assert len(output) > 0


def test_single_value_array_std_is_zero_population():
    # edge case: one value has zero spread, population std must be 0
    single = np.array([50.0])
    assert compute_std(single, sample=False) == 0.0


def test_single_value_array_std_is_nan_sample():
    # edge case: sample std of a single observation is undefined (n-1 = 0)
    single = np.array([50.0])
    result = compute_std(single, sample=True)
    assert math.isnan(result)


def test_empty_array_raises_valueerror():
    # edge case: functions should fail loudly on empty input with a
    # clear ValueError, not crash with a cryptic AssertionError
    with pytest.raises(ValueError, match="must not be empty"):
        compute_mean(np.array([]))


def test_loader_drops_nan_values():
    # Write a CSV with a missing value and verify the loader drops it
    csv_content = "name,score\nAlice,85\nBob,\nCharlie,90\n"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        f.write(csv_content)
        tmp_path = f.name

    try:
        result = load_column(tmp_path, "score")
        assert len(result) == 2           # Bob's missing value is dropped
        assert 85.0 in result
        assert 90.0 in result
    finally:
        os.remove(tmp_path)


def test_loader_missing_column_raises():
    csv_content = "name,score\nAlice,85\n"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        f.write(csv_content)
        tmp_path = f.name

    try:
        with pytest.raises(ValueError, match="not found"):
            load_column(tmp_path, "nonexistent")
    finally:
        os.remove(tmp_path)


def test_loader_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_column("this_file_does_not_exist.csv", "score")