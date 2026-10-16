# Has qualifying become more decisive in Formula 1?

WGU D502 Data Analytics Capstone.

## The question

A midfield Formula 1 team splits a capped development budget between one-lap
qualifying pace and race pace. If overtaking has become harder under current
regulations, a grid position is worth more than it used to be and the budget
should shift toward qualifying. Nobody has quantified how much.

**Research question.** Does the relationship between starting grid position and
finishing position differ significantly across Formula 1 regulation eras?

**H0.** Mean positions gained from grid to flag is equal across all four eras.
**H1.** At least one era differs.

## Method

| | |
|---|---|
| Dependent variable | `positions_gained = grid - positionOrder` |
| Primary test | One-way ANOVA across four regulation eras, alpha 0.05 |
| Post-hoc | Tukey HSD |
| Supporting model | Linear regression of finishing position on grid, with an era interaction |
| Effect size | Eta-squared, plus per-era regression slopes |

### Eras

| Era | Seasons | Boundary |
|---|---|---|
| Pre-DRS | 2009–2010 | New aero rules, no DRS |
| DRS, V8 | 2011–2013 | DRS introduced |
| Hybrid | 2014–2021 | V6 turbo-hybrid formula |
| Ground effect | 2022–2025 | Ground-effect cars |

## Running it

```bash
python -m venv .venv
# Windows:  .venv\Scripts\Activate.ps1
# macOS:    source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
python verify_setup.py
```

Then get the data (see `data/README.md`) and run the notebooks in order:

| Notebook | What it does |
|---|---|
| `01_load_and_verify.ipynb` | Loads the three source files, asserts the schema, surveys the status values |
| `02_data_preparation.ipynb` | Joins, filters, assigns eras, builds the dependent variable, writes the analysis dataset |
| `03_analysis.ipynb` | Assumption checks, ANOVA, Tukey HSD, regression, figures |

## Outputs

- `out/analysis_dataset.csv` — one row per classified finisher, the analysis set
- `out/analysis_dataset_with_retirements.csv` — the same before the retirement filter, for the sensitivity check
- `out/preparation_audit.csv` — every filtering step and how many rows it removed
- `out/*.png` — figures

## Scope

Covered: 2009 onward, classified finishers, four regulation eras.

Not covered: pre-2009 seasons, qualifying lap times, per-circuit modelling, and
any causal claim that the regulations themselves *caused* a change. This is an
observational comparison of eras.

## Data

Formula 1 World Championship (1950–2024), published on Kaggle by Rohan Rao,
derived from the Ergast database. Not redistributed here — see `data/README.md`.
