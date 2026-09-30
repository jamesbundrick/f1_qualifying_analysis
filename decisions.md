
00 - Set up project environment -- .venv

01 - Load and verify data
   Loaded results/races/status from Kaggle rohanrao F1 dataset.
   Ergast export uses \N for nulls; loaded with na_values=['\\N'].
   'position' is null for retirements, so positionOrder is the outcome variable.
   N rows total, N with grid == 0.

02 - Data preparation
    Join results to races on raceId to attach year
    Join results to status on statusI dto attach the readable status
    Filter to 2009 onward - Scope: 2009+ only. Four erras on regulation boundaries.
    Dropped N pit-lane starts (grid == 0).
    Classified finishers = 'Finished' + '+N Lap(s)', built observed status list. Disqualified treated as NOT classified.
    Zero-sum check pre-filter: mean gained = 0.0000 (join verified).
    Post-filter mean positive as expected because retired cars carry large negative values.
    Kept a second dataset with retirements for the sensitivity test.

03 - Analysis
   Levene p < .001 -> variances unequal -> Welch's ANOVA is the primary test; standard ANOVA reported alongside
   Limitation - Shapiro rejects in every era, but n is large and Q-Q plots are near-linear; relying on CLT
   Limitation - Independence violated (drive-races share a season)
   Dropped the 'include retirements' sesitivity check - zero-sum within race makes it degenerate
   Replaced with a finisher-definition robustness check across three definitions