# 01 | Business problem and decision

> **Scenario.** The data is a public video game sales file (VGChartz, 2024 version). The publisher and its decision are my own scenario for practising business analysis.

## Background
A mid-size publisher (I call it "Northgate Games") has budget for **three new games** over the next two years. The team is split on what to make: the safe big genres, or something smaller and cheaper. They want facts about what has sold in the past before they commit money.

## The decision
Which **genres** and **platforms** should the next three games target, and how much should the team trust review scores when picking?

## What the data covers
- 64,016 rows, one per game and console. Sales are recorded for **18,922** of them (30%).
- 12,992 unique titles have sales. Total recorded sales are about **6.6 billion copies**.
- Sales figures stop around 2018: games released in 2019 or later have almost no sales recorded (see the coverage chart).

## Options on the table
| Option | What it means |
|---|---|
| A. Big three | Sports, Action or Shooter: the biggest genres by total sales |
| B. Hit chance | Shooter or Action-Adventure: fewer games but a higher average per game |
| C. Regional | Role-Playing: small in the West, very strong in Japan |
| D. Low cost | Adventure or Simulation: cheaper to make, lower average sales |

## In scope
- Genre, platform family, publisher, region and critic score analysis for 1995 to 2018
- A Power BI market explorer (spec here, build separate)

## Out of scope
- Anything after 2018 (no sales data)
- Digital-only, mobile and free-to-play games (not covered by this source)
- Development cost, price and marketing budget (not in the data)

## Assumptions
- "Sales" means copies sold in millions, as in the data dictionary.
- A blank in a region column means no sales recorded there; the four regions add up to the total for every row.
- The past is a rough guide to the next few years, not a forecast.

## Success
The team can point to a genre and platform shortlist, and say in one line why each is on it, with the data limits stated.
