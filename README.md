# Microstrip Filter Dataset (HFSS → S-Params → Metrics)

This repository contains a dataset generated from Ansys HFSS parametric sweeps for a microstrip bandpass filter.

## Files

### 1) Point-level dataset (merged S-parameters)
- `S11_S21_merged.csv`
- Columns:
  - `dg1 [um]`, `dg_feed [um]`, `L1 [um]`, `L2 [um]` (geometry parameters)
  - `Freq [GHz]` (frequency samples)
  - `S11_dB` (dB(St(T1,T1)) [])
  - `S21_dB` (dB(St(T2,T1)) [])

Each row corresponds to one frequency sample of one design.

### 2) Design-level dataset (compressed metrics)
- `design_metrics.csv`
- Columns:
  - Inputs: `dg1 [um]`, `dg_feed [um]`, `L1 [um]`, `L2 [um]`
  - Targets: `fc [GHz]`, `BW_3dB [GHz]`, `S11min_inband [dB]`
  - Extra: `S21peak [dB]`, `fL_3dB [GHz]`, `fH_3dB [GHz]`

Each row corresponds to one design (one geometry parameter combination).

## Metric definitions
- `fc [GHz]`: at the midpoint of the frequency of `S21_dB` −3 dB passband: `fc = (fL + fH)/2`.
- `BW_3dB [GHz]`: bandwidth where `S21_dB >= (S21_peak - 3 dB)`, using the continuous passband region containing the peak
- `S11min_inband [dB]`: minimum `S11_dB` within the -3 dB passband region

## Notes
- Data is exported from HFSS terminal S-parameter reports and post-processed by Python scripts.
- Units: geometry in `um`, frequency in `GHz`, S-parameters in `dB`.


