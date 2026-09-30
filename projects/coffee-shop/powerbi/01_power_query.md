# 01 | Power Query (Get data)

Build three tables. In Power BI Desktop: **Home > Get data > Blank query**, open **Advanced editor**, paste each block, name the query as shown.

First make a parameter: **Home > Transform data > Manage parameters > New parameter**, name `DataFolder`, type Text, value the folder that holds the unzipped file, ending with a backslash, e.g. `C:\Data\CoffeeShop\`.

## fact_sales
```m
let
    Source = Excel.Workbook(File.Contents(DataFolder & "Coffee Shop Sales.xlsx"), null, true),
    Sheet = Source{[Item = "Transactions", Kind = "Sheet"]}[Data],
    Promoted = Table.PromoteHeaders(Sheet, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"transaction_id", Int64.Type}, {"transaction_date", type date}, {"transaction_time", type time},
        {"transaction_qty", Int64.Type}, {"store_id", Int64.Type}, {"store_location", type text},
        {"product_id", Int64.Type}, {"unit_price", type number}, {"product_category", type text},
        {"product_type", type text}, {"product_detail", type text}}),
    AddRevenue = Table.AddColumn(Typed, "revenue", each [transaction_qty] * [unit_price], type number),
    AddHour = Table.AddColumn(AddRevenue, "hour", each Time.Hour([transaction_time]), Int64.Type),
    AddSize = Table.AddColumn(AddHour, "size", each
        if Text.EndsWith([product_detail], " Sm") then "Small"
        else if Text.EndsWith([product_detail], " Rg") then "Regular"
        else if Text.EndsWith([product_detail], " Lg") then "Large"
        else "No size", type text)
in
    AddSize
```

## dim_date
```m
let
    Start = #date(2023, 1, 1),
    End = #date(2023, 6, 30),
    Days = List.Dates(Start, Duration.Days(End - Start) + 1, #duration(1, 0, 0, 0)),
    AsTable = Table.FromList(Days, Splitter.SplitByNothing(), {"date"}, null, ExtraValues.Error),
    Typed = Table.TransformColumnTypes(AsTable, {{"date", type date}}),
    AddMonth = Table.AddColumn(Typed, "month", each Date.ToText([date], "MMM"), type text),
    AddMonthNum = Table.AddColumn(AddMonth, "month_num", each Date.Month([date]), Int64.Type),
    AddWeekday = Table.AddColumn(AddMonthNum, "weekday", each Date.ToText([date], "ddd"), type text),
    AddWeekdayNum = Table.AddColumn(AddWeekday, "weekday_num", each Date.DayOfWeek([date], Day.Monday) + 1, Int64.Type)
in
    AddWeekdayNum
```

## dim_hour
```m
let
    Rows = {
        {6, "6am", "6am", 1}, {7, "7am", "7 to 10am", 2}, {8, "8am", "7 to 10am", 2}, {9, "9am", "7 to 10am", 2}, {10, "10am", "7 to 10am", 2},
        {11, "11am", "11am to 1pm", 3}, {12, "12pm", "11am to 1pm", 3}, {13, "1pm", "11am to 1pm", 3},
        {14, "2pm", "2 to 4pm", 4}, {15, "3pm", "2 to 4pm", 4}, {16, "4pm", "2 to 4pm", 4},
        {17, "5pm", "5 to 6pm", 5}, {18, "6pm", "5 to 6pm", 5}, {19, "7pm", "7 to 8pm", 6}, {20, "8pm", "7 to 8pm", 6}},
    T = #table(type table [hour = Int64.Type, label = text, block = text, block_order = Int64.Type], Rows)
in
    T
```

## Then, in Model view
1. `fact_sales[transaction_date]` to `dim_date[date]`: many to one, single direction.
2. `fact_sales[hour]` to `dim_hour[hour]`: many to one, single direction.
3. Column tools > **Sort by column**: `dim_date[month]` by `month_num`, `dim_date[weekday]` by `weekday_num`, `dim_hour[label]` by `hour`, `dim_hour[block]` by `block_order`.
4. Hide the columns you will not drag into visuals (`transaction_id`, `product_id`, `store_id`) and mark `dim_date` as a date table.
