# 04 | Page template: how every page is set up

The template makes every page look the same, and the theme makes every visual you add pick up the style on its own. Set it up once on page 1, then **duplicate the page** for the next pages.

**Files in this folder:** `theme.json`, `bg_page.png` (the page background), `layout_preview.png` (what the layout looks like).

## One-time setup
1. **View > Themes > Browse for themes** and pick `theme.json`.
2. Click an empty spot on the page. In the **Format** pane (paint roller) > **Page** > **Canvas settings**: Type = **Custom**, Width = **1280**, Height = **720**.
3. Format pane > **Canvas background**: Image > Browse > `bg_page.png`. Image fit = **Fit**, Transparency = **0%**.
4. Format pane > **Wallpaper**: colour `#D6E8F9`.
5. **Insert > Buttons > Navigator > Page navigator.** Put it on the dark sidebar at x=14, y=124, width 140, height 200. In its Format pane set layout to Vertical, and for the **Selected** state use fill `#4AA8FF` with text `#0C2340`. The theme already styles the other states.

## Grid (use Format > General > Properties for exact numbers)
| What | X | Y | Width | Height |
|---|---|---|---|---|
| Title (text box, 22 pt, bold, navy) | 190 | 16 | 540 | 44 |
| Store slicer (tile style) | 760 | 20 | 500 | 34 |
| KPI tile 1 | 190 | 70 | 251 | 100 |
| KPI tile 2 | 463 | 70 | 251 | 100 |
| KPI tile 3 | 736 | 70 | 251 | 100 |
| KPI tile 4 | 1009 | 70 | 251 | 100 |
| Big chart, left | 190 | 186 | 520 | 250 |
| Big chart, right | 732 | 186 | 528 | 250 |
| Bottom row, left | 190 | 452 | 340 | 248 |
| Bottom row, middle | 552 | 452 | 340 | 248 |
| Bottom row, right | 914 | 452 | 346 | 248 |

Everything stays 20 px away from the page edge and 22 px away from its neighbours.

## Rules so you do not need to adjust anything
- **Cards and multi-row cards** become KPI tiles by themselves: navy outline, hard shadow, big number, grey label. Only set the size and position.
- **All other visuals** get a white rounded panel with a soft blue border, the chart palette, and a left-aligned title. Do not change colours: if a visual looks wrong, press **Format > Reset to default** and the theme comes back.
- **Slicers** show as outlined tiles with no panel. Set the style to **Tile** once.
- **Tables and matrices** get a navy header with white text.
- Colour order in charts is always blue, orange, purple, teal. Keep the same store the same colour on every page.
- To use the template again on a new page: right-click the page tab > **Duplicate page**, then delete the visuals you do not need.

## If a style does not show up
Some theme settings are not supported in every Power BI version. If a visual ignores the theme (for example no shadow), set that one thing by hand: Format > Effects > Shadow, colour `#0C2340`, Distance 4, Angle 45, Blur 0 for KPI tiles. Tell me which one, so I can fix the theme file.
