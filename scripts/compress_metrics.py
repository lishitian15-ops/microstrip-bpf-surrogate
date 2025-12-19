import pandas as pd
import numpy as np
from pathlib import Path

# paths
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
INPUT = DATA / "S11_S21_merged.csv"
OUTPUT = DATA / "design_metrics.csv"

# columns
COL_FREQ = "Freq [GHz]"
COL_S11  = "S11_dB"
COL_S21  = "S21_dB"
GEOM_COLS = ["dg1 [um]", "dg_feed [um]", "L1 [um]", "L2 [um]"]


def extract_metrics(g: pd.DataFrame) -> pd.Series:
    g = g.sort_values(COL_FREQ)
    f   = g[COL_FREQ].to_numpy(float)
    s11 = g[COL_S11].to_numpy(float)
    s21 = g[COL_S21].to_numpy(float)

    if len(f) < 5:
        return pd.Series({
            "fc [GHz]": np.nan,
            "BW_3dB [GHz]": np.nan,
            "S11min_inband [dB]": np.nan,
            "S21peak [dB]": np.nan,
            "fL_3dB [GHz]": np.nan,
            "fH_3dB [GHz]": np.nan,
        })

    peak_idx = int(np.nanargmax(s21))
    s21_peak = float(s21[peak_idx])
    mask = s21 >= (s21_peak - 3.0)

    if not np.any(mask):
        return pd.Series({
            "fc [GHz]": np.nan,
            "BW_3dB [GHz]": np.nan,
            "S11min_inband [dB]": np.nan,
            "S21peak [dB]": s21_peak,
            "fL_3dB [GHz]": np.nan,
            "fH_3dB [GHz]": np.nan,
        })

    left = peak_idx
    while left - 1 >= 0 and mask[left - 1]:
        left -= 1
    right = peak_idx
    while right + 1 < len(mask) and mask[right + 1]:
        right += 1

    fL, fH = float(f[left]), float(f[right])
    if not (np.isfinite(fL) and np.isfinite(fH) and fH > fL):
        return pd.Series({
            "fc [GHz]": np.nan,
            "BW_3dB [GHz]": np.nan,
            "S11min_inband [dB]": np.nan,
            "S21peak [dB]": s21_peak,
            "fL_3dB [GHz]": fL,
            "fH_3dB [GHz]": fH,
        })

    return pd.Series({
        "fc [GHz]": 0.5 * (fL + fH),
        "BW_3dB [GHz]": fH - fL,
        "S11min_inband [dB]": float(np.nanmin(s11[left:right + 1])),
        "S21peak [dB]": s21_peak,
        "fL_3dB [GHz]": fL,
        "fH_3dB [GHz]": fH,
    })


def main():
    df = pd.read_csv(INPUT)
    df.columns = [c.strip() for c in df.columns]

    for c in GEOM_COLS + [COL_FREQ, COL_S11, COL_S21]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    metrics = (
        df.groupby(GEOM_COLS, sort=False)
          .apply(extract_metrics)
          .reset_index()
          .sort_values(GEOM_COLS)
    )

    DATA.mkdir(exist_ok=True)
    metrics.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    print(f"Saved: {OUTPUT}  |  designs = {len(metrics)}")


if __name__ == "__main__":
    main()
