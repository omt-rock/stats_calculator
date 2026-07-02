import warnings
import numpy as np


def _validate_input(arr, func_name):
    """Raise ValueError on empty arrays — fail loudly, not silently."""
    if len(arr) == 0:
        raise ValueError(f"{func_name}: input array must not be empty.")


def compute_mean(arr):
    """Average value. Manual version confirms it's just sum / count."""
    _validate_input(arr, "compute_mean")

    numpy_result = np.mean(arr)
    manual_result = np.sum(arr) / len(arr)
    assert np.isclose(numpy_result, manual_result)
    return numpy_result


def compute_median(arr):
    """
    Middle value of sorted data.
    Manual version shows exactly what NumPy does internally:
    sort, then pick the middle (or average the two middles if n is even).
    """
    _validate_input(arr, "compute_median")

    numpy_result = np.median(arr)

    sorted_arr = np.sort(arr)
    n = len(sorted_arr)
    mid = n // 2
    if n % 2 == 0:
        manual_result = (sorted_arr[mid - 1] + sorted_arr[mid]) / 2
    else:
        manual_result = sorted_arr[mid]

    assert np.isclose(numpy_result, manual_result)
    return numpy_result


def compute_std(arr, sample=True):
    """
    Standard deviation.
    sample=True  -> divides by (n-1), Bessel's correction, use for real datasets
    sample=False -> divides by n, population std, use only if arr IS the whole population

    Edge case: a single-element array has no spread.
    - population std is 0 (the one value IS the mean)
    - sample std is undefined (dividing by n-1 = 0), returned as NaN
    """
    _validate_input(arr, "compute_std")

    n = len(arr)
    ddof = 1 if sample else 0

    if sample and n == 1:
        # sample std of a single observation is mathematically undefined
        warnings.warn(
            "Sample standard deviation is undefined for a single value; returning NaN."
        )
        return float('nan')

    numpy_result = np.std(arr, ddof=ddof)

    mean = np.mean(arr)
    squared_deviations = (arr - mean) ** 2
    divisor = n - ddof
    manual_result = np.sqrt(np.sum(squared_deviations) / divisor)

    assert np.isclose(numpy_result, manual_result)
    return numpy_result


def compute_percentiles(arr, percentiles=(25, 50, 75)):
    """
    Percentile values using linear interpolation (NumPy's default method).
    Returns a dict like {25: ..., 50: ..., 75: ...}
    """
    _validate_input(arr, "compute_percentiles")

    results = {}
    sorted_arr = np.sort(arr)
    n = len(sorted_arr)

    for p in percentiles:
        numpy_result = np.percentile(arr, p)

        # manual linear interpolation, matching NumPy's default 'linear' method
        pos = (p / 100) * (n - 1)
        lo = int(np.floor(pos))
        hi = int(np.ceil(pos))
        frac = pos - lo
        manual_result = sorted_arr[lo] + frac * (sorted_arr[hi] - sorted_arr[lo])

        assert np.isclose(numpy_result, manual_result)
        results[p] = numpy_result

    return results


def summarize(arr):
    """Bring it all together into one summary dict."""
    _validate_input(arr, "summarize")

    p = compute_percentiles(arr, (25, 50, 75))
    return {
        "n": len(arr),
        "mean": compute_mean(arr),
        "median": compute_median(arr),
        "std_sample": compute_std(arr, sample=True),
        "std_population": compute_std(arr, sample=False),
        "p25": p[25],
        "p50": p[50],
        "p75": p[75],
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }