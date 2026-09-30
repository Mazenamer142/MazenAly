# 05 | Business rules

| ID | Rule | Reason / effect |
|---|---|---|
| BR-01 | Profit for a sale line = units x (unit price - unit cost) | One consistent definition across every view |
| BR-02 | Cost and price are cleaned from text (e.g. `"$9.99 "`) to numbers before use | The source stores them as text with a $ sign and trailing space |
| BR-03 | Margin % is always Profit / Revenue on the selected slice, never an average of margins | Averages of percentages give the wrong answer |
| BR-04 | Like-for-like comparisons use the same calendar months in both years (Jan-Sep) | The data ends 30 Sep 2023, so full-year vs part-year would mislead |
| BR-05 | A store x product pair is **out of stock** when stock on hand = 0 | Simple, testable definition |
| BR-06 | Estimated profit at risk uses the pair's average daily profit over the last 90 days of data (3 Jul - 30 Sep 2023) | Recent rate is the best available proxy |
| BR-07 | A pair is **slow stock** when stock on hand covers more than 180 days at the recent rate | Threshold is a proposal for Inventory to confirm |
| BR-08 | The store city "Cuidad de Mexico" is standardised to "Ciudad de Mexico" | Source spells it two ways; otherwise Mexico City splits into two groups |
| BR-09 | Store x product pairs missing from inventory are reported as a data gap, not as zero stock | Missing is not the same as out of stock |
| BR-10 | Profit per store divides by the number of stores in the group (not by active days) | Fair comparison between location types with different store counts |
