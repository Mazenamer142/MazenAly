# Baby names: how America picked names for 30 years

A data analysis project on a public **US baby names** dataset: 2,212,361 rows (state x gender x year x name), 98.7 million babies, 22,240 names, 51 states (with DC), 1980 to 2009.
Baby names are not business data, so this project has **no business analysis or dashboard side**. It is not client work.

## The question
How did American naming habits change from 1980 to 2009, and where did the changes come from?

## What I found
- **Names got about 2.7 times more varied.** The effective number of names (1 / sum of squared shares) went from 136 to 354 for girls and from 90 to 256 for boys. The share of babies with a top-10 name fell from 19.4% to 10.6% (girls) and from 25.2% to 10.5% (boys).
- **The crown is worth less.** Michael was number one for 19 years in a row (1980 to 1998), then Jacob for 11. The number one name went from about 4% of babies to about 1.2 to 1.5%.
- **Girls' names churn faster.** Of 1980's top 100, 20 girls' names and 44 boys' names were still in the top 100 in 2009. None of the girls' top 10 survived; three of the boys' did.
- **Spikes.** Madison went from 0 girls in 1983 to 22,162 in 2001. Nevaeh went from 53 babies in 2000 to 6,803 in 2007. Ashanti had a one-year spike in 2002 (2,928 babies vs 253 the year before).
- **Sounds.** Boys with names ending in "n" went from 24.5% to 36.2%. The "-den" family (Jayden, Aiden, Hayden, Brayden...) went from 0.01% to 4.76% of boys. Average name length hardly changed (6.05 to 5.93 letters).
- **Gender.** 1,964 names are used for both genders. Some crossed over: Addison 5% girls to 94%, Kennedy 0% to 96%, Ashton 67% to 12%.
- **Regions.** New England leans Irish (Brendan 3.1 times as common as nationally), the Pacific leans Spanish, the South likes Bobby, Billy and Willie.

## Limits
- The file hides every name with fewer than 5 babies in a state: 42.5% of rows have under 10 babies but they are only 6.2% of the babies. Boys are 53.6% of the babies in the file; my explanation is that more girls fall under the cut, but the file cannot prove it.
- The regions table was missing Michigan (I put it in the Midwest) and wrote "New England" two ways.
- Only 1980 to 2009, two genders as recorded at birth, no other information about the babies or parents.

## What is in this folder
| Folder | What |
|---|---|
| `sql/` | Eight SQL scripts (SQLite): clean and model, overview, diversity, ranks and churn, rise and fall, gender, sounds, regions |
| `python/analysis.py` | Repeats the whole analysis in pandas, runs the SQL, and stops with an error if the two disagree. Writes `data/summary/` and `assets/data/baby-names.json` |
| `data/summary/` | The small result tables the portfolio charts are drawn from |

The name explorer on the portfolio page reads `assets/data/baby-names.json` (yearly babies for the 3,000 most used names, about 480 KB).

## Run it
```
pip install pandas numpy
python python/analysis.py --data "path/to/folder with names.csv and regions.csv"
```
The raw files are a public download and are not stored in this repo (`data/raw/` is git-ignored). The script needs a few minutes because of the 2.2 million rows.

AI note: I used AI to help brainstorm and to polish the writing and code in this project.
