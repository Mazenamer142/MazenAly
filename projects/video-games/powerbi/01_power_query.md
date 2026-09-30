# 01 | Power Query (Get data)

In Power BI Desktop: **Home > Get data > Blank query > Advanced editor**. Make a text parameter first: **Manage parameters > New**, name `DataFolder`, value the folder with the unzipped file, ending with a backslash, e.g. `C:\Data\VideoGames\`.

## publisher_map (small lookup table, typed in)
```m
let
    Rows = {
        {"EA Sports", "Electronic Arts"}, {"EA Sports BIG", "Electronic Arts"},
        {"Namco", "Bandai Namco"}, {"Namco Bandai", "Bandai Namco"}, {"Namco Bandai Games", "Bandai Namco"}, {"Bandai", "Bandai Namco"},
        {"Warner Bros. Interactive", "Warner Bros"}, {"Warner Bros. Interactive Entertainment", "Warner Bros"},
        {"2K Sports", "2K"}, {"2K Games", "2K"},
        {"Microsoft Game Studios", "Microsoft"}, {"Microsoft Studios", "Microsoft"},
        {"Konami Digital Entertainment", "Konami"}},
    T = #table(type table [raw_name = text, clean_name = text], Rows)
in
    T
```

## platform_map (console to platform family)
```m
let
    Fam = {
        {"PlayStation", {"PS", "PS2", "PS3", "PS4", "PSP", "PSV", "PSN"}},
        {"Xbox", {"XB", "X360", "XOne", "XBL"}},
        {"Nintendo", {"NES", "SNES", "N64", "GC", "Wii", "WiiU", "NS", "GB", "GBC", "GBA", "DS", "3DS", "VC"}},
        {"Sega", {"GEN", "SAT", "DC", "SCD", "GG"}},
        {"PC", {"PC", "OSX"}}},
    Rows = List.Combine(List.Transform(Fam, (f) => List.Transform(f{1}, (c) => {c, f{0}}))),
    T = #table(type table [console = text, platform_family = text], Rows)
in
    T
```

## fact_games
```m
let
    Source = Csv.Document(File.Contents(DataFolder & "vgchartz-2024.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"critic_score", type number}, {"total_sales", type number}, {"na_sales", type number}, {"jp_sales", type number},
        {"pal_sales", type number}, {"other_sales", type number}}, "en-US"),
    OnlyWithSales = Table.SelectRows(Typed, each [total_sales] <> null),
    Dropped = Table.RemoveColumns(OnlyWithSales, {"img", "last_update"}),
    MergedPub = Table.NestedJoin(Dropped, {"publisher"}, publisher_map, {"raw_name"}, "pm", JoinKind.LeftOuter),
    PubExpanded = Table.ExpandTableColumn(MergedPub, "pm", {"clean_name"}, {"clean_name"}),
    PubClean = Table.AddColumn(PubExpanded, "publisher_clean", each if [clean_name] = null then [publisher] else [clean_name], type text),
    NoPubHelper = Table.RemoveColumns(PubClean, {"clean_name", "publisher"}),
    MergedPlat = Table.NestedJoin(NoPubHelper, {"console"}, platform_map, {"console"}, "pf", JoinKind.LeftOuter),
    PlatExpanded = Table.ExpandTableColumn(MergedPlat, "pf", {"platform_family"}, {"platform_family"}),
    PlatFilled = Table.ReplaceValue(PlatExpanded, null, "Other", Replacer.ReplaceValue, {"platform_family"}),
    ZeroRegions = Table.ReplaceValue(PlatFilled, null, 0, Replacer.ReplaceValue, {"na_sales", "jp_sales", "pal_sales", "other_sales"}),
    Year = Table.AddColumn(ZeroRegions, "release_year", each try Number.From(Text.Start([release_date], 4)) otherwise null, Int64.Type),
    Band = Table.AddColumn(Year, "score_band", each
        if [critic_score] = null then "No score"
        else if [critic_score] <= 6 then "6 or less"
        else if [critic_score] <= 7 then "6 to 7"
        else if [critic_score] <= 8 then "7 to 8"
        else if [critic_score] <= 9 then "8 to 9"
        else "over 9", type text),
    BandOrder = Table.AddColumn(Band, "band_order", each
        if [score_band] = "6 or less" then 1 else if [score_band] = "6 to 7" then 2 else if [score_band] = "7 to 8" then 3
        else if [score_band] = "8 to 9" then 4 else if [score_band] = "over 9" then 5 else 0, Int64.Type),
    AddId = Table.AddIndexColumn(BandOrder, "game_id", 1, 1, Int64.Type)
in
    AddId
```
Keep only rows with a sales number (that is what the analysis does). If you want the "data limits" page to show coverage by year, load a second copy of the file without the `OnlyWithSales` step and name it `fact_all_rows`.

## fact_region (one row per game and region, so one region slicer drives every chart)
```m
let
    Source = Table.SelectColumns(fact_games, {"game_id", "na_sales", "pal_sales", "jp_sales", "other_sales"}),
    Unpivoted = Table.UnpivotOtherColumns(Source, {"game_id"}, "region_col", "sales"),
    Named = Table.AddColumn(Unpivoted, "region", each
        if [region_col] = "na_sales" then "North America"
        else if [region_col] = "pal_sales" then "Europe & Africa"
        else if [region_col] = "jp_sales" then "Japan" else "Other", type text),
    Cleaned = Table.RemoveColumns(Named, {"region_col"}),
    Typed = Table.TransformColumnTypes(Cleaned, {{"sales", type number}})
in
    Typed
```

## Model view
1. `fact_games[game_id]` (one) to `fact_region[game_id]` (many), single direction: a genre or year slicer filters the region rows.
2. Sort `fact_games[score_band]` by `band_order`.
3. The region slicer uses `fact_region[region]`. It drives the region measures. If you want it to filter the game-level visuals too, set the relationship to **Both** directions (only if you need it: it is slower and can create ambiguity).
4. Hide `game_id` and the four region columns of `fact_games`.
