# 05 | Requirements, user stories and test cases

## Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Filter everything by release year range, genre, platform family and region | Must |
| FR-02 | Show total sales, games and average sales per game for the selection | Must |
| FR-03 | Show sales by genre with the average per game next to it | Must |
| FR-04 | Show a genre by region heat map (share of each region's sales) | Must |
| FR-05 | Show critic score bands and average sales | Should |
| FR-06 | Show sales by release year with a clear note that data stops in 2018 | Must |
| FR-07 | Show top publishers after the name clean-up | Should |
| FR-08 | A "data limits" page | Must |
| FR-09 | Compare two genres side by side | Could |
| FR-10 | Forecast next year's sales | Won't (data too incomplete) |

## User stories
| # | As a... | I want... | So that... |
|---|---|---|---|
| US-1 | Studio head | to see genre size and average sales together | I do not pick a big genre with weak games |
| US-2 | Finance lead | to see how concentrated sales are | I understand the risk of a miss |
| US-3 | Marketing lead | to switch region and see genre shares change | I can plan launches by region |
| US-4 | Creative director | to see the score bands | I can judge how much quality is worth |
| US-5 | Head of publishing | to compare platform families | I can pick where to launch |

## Acceptance test cases
| # | Test | Expected result |
|---|---|---|
| T-01 | No filters selected | Total sales 6,605.9M, 18,922 games |
| T-02 | Genre = Sports | 1,187.5M sales, 2,597 games, 0.46M per game |
| T-03 | Region = Japan, genre = Role-Playing | 19.0% share |
| T-04 | Critic band = over 9 | 194 games, 2.48M average |
| T-05 | Publisher = Electronic Arts | 1,157.3M sales after the merge (EA Sports included) |
| T-06 | Year slicer set to 2019+ | Dashboard shows the "little data" warning |
