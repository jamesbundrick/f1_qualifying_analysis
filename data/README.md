# Source data

The raw CSVs are deliberately not committed to this repository. They
belong to the dataset's publisher, and redistributing them here would be
both discourteous and unnecessary.

## How to obtain them

1. Download the *Formula 1 World Championship (1950–2024)* dataset from
   Kaggle: https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020
2. Unzip it into this folder.
3. Confirm you have at least `results.csv`, `races.csv` and `status.csv`.
4. Run `01_load_and_verify.ipynb` — its schema assertion will tell you
   immediately if anything is missing or has changed.

Downloaded on: 09/25/2026

## A quirk worth knowing

This dataset is exported from the Ergast MySQL database, which writes
missing values as the literal string `\N`. Always load with:

```python
pd.read_csv(path, na_values=["\\N"])
```

Without it, `position` is read as text and every retirement becomes the
string `'\N'` instead of a null.
