00 - Set up project environment -- .venv

01 - Load and verify data

   Loaded results/races/status from Kaggle rohanrao F1 dataset.
      Source | Formula 1 World Championship (1950-2024), Kaggle, published by Rohan Rao 
      URL | https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020
      Derived from | the Ergast motor racing database
      Downloaded | 09/25/2026
      Files used | 'results.csv', 'races.csv', 'status.csv'
      License / restrictions | public, free, no login; no proprietary or personal data beyond publicly published competitor names
   Ergast export uses '\N' for nulls; loaded with 'na_values=['\\N']'. Without this, 'position' parses as text and every retirement becomes the string ''\N''.
   'position' is null for retirements, so 'positionOrder' is the outcome variable.
   26,759 result rows loaded; 86 of the 2009+ entries had grid == 0.

02 - Data preparation
   
   | step                      |   rows |   removed | note                      |
   |:--------------------------|-------:|----------:|:--------------------------|
   | loaded results            |  26759 |         0 |                           |
   | joined races (year)       |  26759 |         0 |                           |
   | joined status             |  26759 |         0 |                           |
   | filtered to 2009+         |   6776 |     19983 | pre-2009 out of scope     |
   | dropped grid == 0         |   6690 |        86 | 86 pit-lane starts        |
   | kept classified finishers |   5494 |      1196 | 1,196 retirements removed |
    
    Join results to races on raceId to attach year.
    Join results to status on statusId to attach the readable status.
    Both are left joins, each followed by an assertion that no row came back null.
       A left join plus an assertion fails loudly; an inner join would drop unmatched rows silently.
    Filter to 2009 onward - Scope: 2009+ only. Earlier seasons differ in field size, scoring and data completeness.
    Four eras on regulation boundaries: 2009-10 pre-DRS, 2011-13 DRS with V8, 2014-21 hybrid, 2022-24 ground effect.
       Boundaries corroborated against the Wikipedia 'History of Formula One regulations' year-by-year entries.
    Dropped 86 pit-lane starts (grid == 0) - not a grid position, and they break the zero-sum validation check.
    Classified finishers = 'Finished' + '+N Lap(s)', built observed status list. Disqualified treated as NOT classified.
    Zero-sum check pre-filter: mean gained = 0.0000 (join verified).
    Post-filter mean positive as expected because retired cars carry large negative values.
    Kept a second dataset with retirements for the sensitivity test.

03 - Analysis
   
   | era                      |    n |   mean |   median |    sd |   min |   max |
   |:-------------------------|-----:|-------:|---------:|------:|------:|------:|
   | 1. Pre-DRS (2009-10)     |  608 |  1.76  |        1 | 4.121 |   -13 |    18 |
   | 2. DRS, V8 (2011-13)     | 1117 |  1.726 |        1 | 4.025 |   -15 |    21 |
   | 3. Hybrid (2014-21)      | 2635 |  1.402 |        1 | 3.848 |   -14 |    19 |
   | 4. Ground effect (2022+) | 1134 |  0.984 |        1 | 3.828 |   -18 |    16 |

   Homogeneity of variance - Levene's test: W = 2.5529, p = 0.0537
      p is above 0.05, so the null of equal variances is not rejected and the standard one-way ANOVA is the primary test.
      The result is marginal (p = 0.054), so Welch's ANOVA was also run as a robustness check; both agree.

   Normality - Shapiro-Wilk and Q-Q plots
      Shapiro rejects in every era, which is expected at these sample sizes, where the test detects trivial departures.
      Q-Q plots are near-linear through the body of each distribution, and with n per era in the hundreds to thousands the central limit theorem protects the F test.
      Recorded as a limitation rather than treated as satisfied.

   Independence
      Violated in a known way.
      Driver-races within a season share cars, regulations, and conditions, so observations are not strictly independent.
      Not testable from this data; recorded as a limitation.

   Analysis results
      One-way ANOVA (primary): F = 8.5224, p = 0.000012 --> reject H0 at α = 0.05
      Welch's ANOVA (robustness): F = 8.4332, p = 0.000014 - same conclusion
      Effect size: eta-squared = 0.00464 - era explains 0.46% of the variance in positions gained

      Tukey HSD (FWER = 0.05):
 
         | group1                   | group2                   | meandiff | p-adj  | lower   | upper   | reject |
         |:-------------------------|:-------------------------|---------:|-------:|--------:|--------:|:-------|
         | 1. Pre-DRS (2009-10)     | 2. DRS, V8 (2011-13)     |  -0.0338 | 0.9982 | -0.5404 |  0.4727 | False  |
         | 1. Pre-DRS (2009-10)     | 3. Hybrid (2014-21)      |  -0.3576 | 0.1763 | -0.8098 |  0.0946 | False  |
         | 1. Pre-DRS (2009-10)     | 4. Ground effect (2022+) |  -0.7757 | 0.0005 | -1.2810 | -0.2705 | True   |
         | 2. DRS, V8 (2011-13)     | 3. Hybrid (2014-21)      |  -0.3238 | 0.0939 | -0.6826 |  0.0351 | False  |
         | 2. DRS, V8 (2011-13)     | 4. Ground effect (2022+) |  -0.7419 | 0.0000 | -1.1656 | -0.3182 | True   |
         | 3. Hybrid (2014-21)      | 4. Ground effect (2022+) |  -0.4182 | 0.0140 | -0.7751 | -0.0612 | True   |
 
         Three of six pairs differ significantly, and every one of them involves the ground-effect era.
         No pair among the first three eras differs. 
         The era effect is entirely a 2022-24 effect, not a steady decline across all four eras.

      Supporting regression — per-era slope of finish on grid

         | era                      |   slope |   ci_low |   ci_high |   r_squared |    n |
         |:-------------------------|--------:|---------:|----------:|------------:|-----:|
         | 1. Pre-DRS (2009-10)     |  0.6256 |   0.5844 |    0.6668 |      0.5946 |  608 |
         | 2. DRS, V8 (2011-13)     |  0.688  |   0.6584 |    0.7177 |      0.6504 | 1117 |
         | 3. Hybrid (2014-21)      |  0.6472 |   0.6266 |    0.6679 |      0.5887 | 2635 |
         | 4. Ground effect (2022+) |  0.6757 |   0.6409 |    0.7105 |      0.562  | 1134 |

         The slopes show no trend and every pair of confidence intervals overlaps.
         The grid-to-finish relationship has been effectively constant since 2009. 
         Since the regression is the more direct test of whether starting position has become more decisive, this does NOT support the original hypothesis.

      Robustness — finisher definition

         | definition                  |    n |   welch_F |           p | reject_H0   |
         |:----------------------------|-----:|----------:|------------:|:------------|
         | Finished + lapped (primary) | 5494 |    8.4332 | 1.44106e-05 | True        |
         | Finished only (strict)      | 3497 |    3.0584 | 0.0273905   | True        |
         | Top 10 grid slots only      | 2769 |    0.6925 | 0.556729    | False       |

    The conclusion is sensitive.
         Restricted to the top 10 grid slots the test fails to reject (p = 0.557). 
         The era effect exists only when backmarkers are included, which matters because the stated client is a midfield team.

04 - Deviations from the plan

   Primary test switched from Welch's to standard ANOVA.
      The plan assumed unequal variances; Levene's test did not support that. 
      Both were run.

   Sensitivity check redesigned.
      The plan was to re-run the ANOVA with retirements included. 
      That is degenerate: positions gained is zero-sum within a race, so including every car forces each era's mean to exactly zero and the test becomes a near-identity. 
      Replaced with a finisher-definition robustness check across three definitions.

   Era 4 shortened to 2022–2024 because the dataset ends at 2024.

05 - Limitations discovered during analysis

   Confound: retirement rate and field size

      Derived from this project's own dataset:

      | era                        |   retirement_rate |   field_size |   mean_positions_gained |
      |:---------------------------|------------------:|-------------:|------------------------:|
      | 1. Pre-DRS (2009-10)       |            0.2352 |         22.1 |                   1.76  |
      | 2. DRS, V8 (2011-13)       |            0.1714 |         23.2 |                   1.726 |
      | 3. Hybrid (2014-21)        |            0.1837 |         20.2 |                   1.402 |
      | 4. Ground effect (2022-24) |            0.1403 |         19.4 |                   0.984 |

   Retirement rate correlates +0.77 with mean positions gained across the four eras, and mean field size fell from 22.1 to 19.4. 
   Both mechanically limit how many places a finisher can gain: fewer retirements frees up fewer places, and a smaller grid leaves less room to move. 
   The decline in positions gained may therefore reflect improved reliability and smaller fields rather than harder overtaking. 
   This is the most significant limitation of the analysis and must be stated plainly in parts F1 and F2.

06 - Other limitations

   Observational, not causal. Eras are compared; the regulations themselves are not isolated as a cause.

   No race context. The dataset carries no weather, safety-car, tyre or reliability detail, so confounders cannot be controlled for directly.

   Non-independence of driver-races within a season.

   Unequal era lengths — 2, 3, 8 and 3 seasons. The hybrid era carries disproportionate weight in the pooled test.
