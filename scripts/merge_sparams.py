import pandas as pd

S11_PATH = r"E:\射频电子学\S12.csv"   # dB(St(T1,T1)) []
S21_PATH = r"E:\射频电子学\S21.csv"   # dB(St(T2,T1)) []
OUT_PATH = r"E:\射频电子学\S11_S21_merged.csv"

df11 = pd.read_csv(S11_PATH, engine="python")
df21 = pd.read_csv(S21_PATH, engine="python")

df11.columns = [c.strip() for c in df11.columns]
df21.columns = [c.strip() for c in df21.columns]

df11 = df11.rename(columns={"dB(St(T1,T1)) []": "S11_dB"})
df21 = df21.rename(columns={"dB(St(T2,T1)) []": "S21_dB"})

KEYS = ["dg1 [um]", "dg_feed [um]", "L1 [um]", "L2 [um]", "Freq [GHz]"]

merged = pd.merge(
    df11,
    df21[KEYS + ["S21_dB"]],
    on=KEYS,
    how="inner"
)

merged = merged[
    ["dg1 [um]", "dg_feed [um]", "L1 [um]", "L2 [um]", "Freq [GHz]", "S11_dB", "S21_dB"]
].sort_values(["dg1 [um]", "dg_feed [um]", "L1 [um]", "L2 [um]", "Freq [GHz]"], kind="mergesort")

merged.to_csv(OUT_PATH, index=False, encoding="utf-8-sig")
print("✅ merged saved to:", OUT_PATH, " rows=", len(merged))
