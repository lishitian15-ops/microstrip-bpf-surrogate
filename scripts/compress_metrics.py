import pandas as pd
import numpy as np

INPUT_CSV  = r"E:\射频电子学\S11_S21_merged.csv"
OUTPUT_CSV = r"E:\射频电子学\design_metrics.csv"

COL_FREQ = "Freq [GHz]"
COL_S11  = "S11_dB"
COL_S21  = "S21_dB"
GEOM_COLS = ["dg1 [um]", "dg_feed [um]", "L1 [um]", "L2 [um]"]

def extract_metrics(group: pd.DataFrame) -> pd.Series:
    g = group.sort_values(COL_FREQ).copy()
    f   = g[COL_FREQ].to_numpy(dtype=float)
    s11 = g[COL_S11].to_numpy(dtype=float)
    s21 = g[COL_S21].to_numpy(dtype=float)

    if len(f) < 5:
        return pd.Series({
            "fc [GHz]": np.nan, "BW_3dB [GHz]": np.nan, "S11min_inband [dB]": np.nan,
            "S21peak [dB]": np.nan, "fL_3dB [GHz]": np.nan, "fH_3dB [GHz]": np.nan
        })

    peak_idx = int(np.argmax(s21))
    s21_peak = float(s21[peak_idx])
    fc = float(f[peak_idx])

    thr = s21_peak - 3.0
    mask = s21 >= thr
    if not np.any(mask):
        return pd.Series({
            "fc [GHz]": fc, "BW_3dB [GHz]": 0.0, "S11min_inband [dB]": np.nan,
            "S21peak [dB]": s21_peak, "fL_3dB [GHz]": np.nan, "fH_3dB [GHz]": np.nan
        })

    # continuous passband containing the peak
    left = peak_idx
    while left - 1 >= 0 and mask[left - 1]:
        left -= 1
    right = peak_idx
    while right + 1 < len(mask) and mask[right + 1]:
        right += 1

    fL = float(f[left])
    fH = float(f[right])
    BW = float(fH - fL)
    s11_min = float(np.min(s11[left:right + 1]))

    return pd.Series({
        "fc [GHz]": fc,
        "BW_3dB [GHz]": BW,
        "S11min_inband [dB]": s11_min,
        "S21peak [dB]": s21_peak,
        "fL_3dB [GHz]": fL,
        "fH_3dB [GHz]": fH,
    })

def main():
    df = pd.read_csv(INPUT_CSV, engine="python")
    df.columns = [c.strip() for c in df.columns]

    need = set(GEOM_COLS + [COL_FREQ, COL_S11, COL_S21])
    missing = [c for c in need if c not in df.columns]
    if missing:
        raise KeyError(f"Missing columns: {missing}\nColumns found: {list(df.columns)}")

    for c in GEOM_COLS + [COL_FREQ, COL_S11, COL_S21]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    metrics = (
        df.groupby(GEOM_COLS, dropna=False, sort=False)
          .apply(extract_metrics)
          .reset_index()
          .sort_values(GEOM_COLS, kind="mergesort")
    )

    metrics.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print("metrics saved to:", OUTPUT_CSV, " designs=", len(metrics))

if __name__ == "__main__":
    main()
