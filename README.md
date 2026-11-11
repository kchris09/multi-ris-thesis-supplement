# Multi-RIS thesis supplementary material

Supplementary summary data for **Geometry-Aware Multi-RIS Index Modulation for mmWave Communications: Modeling, Optimization, and a 28 GHz Experimental Proof of Concept**.

**Thesis author:** Kyriakos Christodoulides, University of Cyprus.

The author carried out the work under the supervision and guidance of Professor Ioannis Krikidis and Elio Faddoul. Related research is reported in the coauthored manuscript *Multi-RIS-enabled Index Modulation for mmWave Communications* by Kyriakos Christodoulides, Elio Faddoul, and Ioannis Krikidis (2026).

## Scope

This package contains saved numerical summaries and a plotting helper that redraws two reported comparisons. The original CSV bytes are preserved. The plotting helper supplied with this package reads those values without rerunning simulations. Figure typography may differ from the thesis while the plotted summary values are the same.

The package does not contain all individual channel realizations, the complete original simulation code, raw experimental detector readings, or the numerical arrays behind the supplementary SNR heatmaps. It therefore supports figure reproduction rather than an independent rerun of the complete research campaign.

## Contents

- `data/detection_summary.csv`: independent-panel comparison, 44 rows (four methods at 11 SNR settings).
- `data/detection_selection_summary.csv`: shared-ray selection-subset comparison, 55 rows (five methods at 11 SNR settings).
- `plot_figures.py`: plotting helper for both comparisons.
- `requirements.txt`: plotting dependencies.
- `figures/`: example PDF and PNG outputs from the plotting helper.
- `RELEASE_NOTES.md`: proposed text for the first GitHub release.
- `SHA256SUMS.txt`: checksums of the two unchanged CSVs.

## Figure correspondence

| CSV | Figure in the current thesis | Output file stem |
|---|---|---|
| `detection_summary.csv` | Figure 6.4, independent-panel index detection | `independent_panel_detection` |
| `detection_selection_summary.csv` | Figure 6.5, restricted detection-aware selection | `shared_ray_configuration_selection` |

Figure numbering refers to the final-draft structure with eight chapters. The descriptive figure titles remain the identifying reference if pagination or numbering changes.

## CSV columns

### `detection_summary.csv`

| Column | Meaning |
|---|---|
| `scheme` | Saved placement-method identifier |
| `rhoDb` | Transmit-SNR parameter in dB, from 0 to 50 in steps of 5 |
| `meanPe` | Mean conditional index-error probability over the independent-panel ensemble |
| `ci95Lower`, `ci95Upper` | Saved pointwise 95% interval endpoints for that method mean |
| `matchedMeanMC` | Observation-level Monte Carlo mean on the matched detector-check subset |
| `matchedAnalyticalPe` | Analytical mean on that same matched subset |

The matched detector check uses a smaller channel subset than the full placement comparison. Its matched analytical mean is therefore compared with `matchedMeanMC`, rather than with the full-ensemble `meanPe`.

### `detection_selection_summary.csv`

| Column | Meaning |
|---|---|
| `method` | Saved method identifier |
| `rhoDb` | Transmit-SNR parameter in dB |
| `meanError` | Mean conditional index-error probability on the shared-ray selection subset |
| `ci95Lower`, `ci95Upper` | Saved pointwise 95% interval endpoints for that method mean |

### Method identifiers

| Identifier | Meaning |
|---|---|
| `Algorithm1` | SNR-oriented alternating optimization (AO) |
| `Predetermined` | Center placement in this comparison |
| `DistanceProduct` | Feasible placement minimizing the two-hop distance product |
| `RandomPlacement` | Uniform feasible-grid random placement |
| `DetectionSelection` | Detection-aware selection among saved configuration pairs |

The fixed-position baselines also optimize their transmit beam and RIS phases. Their comparison does not use arbitrary unoptimized phases.

## Interpretation

The first CSV uses 100,000 channel realizations with independently sampled panel parameters. The second uses a matched 100,000-realization subset with shared corresponding ray parameters across panels. They are separate ensembles and should not be pooled or treated as interchangeable observations.

In the selection benchmark, four saved configurations per panel produce 16 binary pairs. The detector-error criterion selects one pair at 20 dB transmit SNR for each realization. The selected pair remains fixed across the evaluated SNR sweep, while detector thresholds are recomputed at each operating SNR.

The ordinate is index-error probability. For the binary index it equals index-bit error probability under an explicit one-bit labeling. It does not measure conventional-symbol BER or joint throughput.

The supplied intervals concern individual method means. They are not paired method-difference intervals or multiplicity-adjusted contrast intervals. Subtracting separate interval endpoints does not recover the paired contrasts reported in the thesis.

Some approximate high-SNR interval lower endpoints are negative. The original CSV values are retained. The plotting helper clips only the displayed shaded bands to the visible probability range of the logarithmic axes. This display rule does not create replacement confidence intervals.

## Reproduce the figures

From the directory containing `plot_figures.py`:

```bash
python3 -m pip install -r requirements.txt
python3 plot_figures.py
```

On Windows, `python` may be the appropriate command instead of `python3`. The script saves two PDF figures and two PNG previews in `figures/`.

To choose a different output directory:

```bash
python3 plot_figures.py --output-dir regenerated_figures
```

The helper was checked with NumPy 2.3.5 and Matplotlib 3.10.8. Its direct dependencies are listed in `requirements.txt`.

## First GitHub release

Upload the extracted package contents at the repository root so that this README is visible on the main repository page. Create a tag named `v1.0` after the files are committed. Use `RELEASE_NOTES.md` as the release description. Cite the specific release URL in the thesis after the release is published.

This package does not assume a GitHub username, repository URL, or DOI. Those identifiers should be added only after they exist.
