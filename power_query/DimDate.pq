// ============================================================================
// Power Query M Script: DimDate (Dedicated Date Dimension)
// Description: Dynamic calendar dimension spanning dataset history.
//              Generates complete time intelligence attributes, seasonal flags,
//              and retail festival indicators.
// ============================================================================

let
    // Set dynamic or static boundary dates spanning dataset history
    StartDate = #date(2023, 1, 1),
    EndDate = #date(2025, 12, 31),
    DayCount = Duration.Days(Duration.From(EndDate - StartDate)) + 1,

    // Generate continuous list of dates
    DateList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    #"Converted to Table" = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
    #"Changed Type Date" = Table.TransformColumnTypes(#"Converted to Table", {{"Date", type date}}),

    // Add DateKey (YYYYMMDD integer)
    #"Added DateKey" = Table.AddColumn(#"Changed Type Date", "DateKey", each 
        Date.Year([Date]) * 10000 + Date.Month([Date]) * 100 + Date.Day([Date]), 
        Int64.Type
    ),

    // Calendar attributes
    #"Added Year" = Table.AddColumn(#"Added DateKey", "Year", each Date.Year([Date]), Int64.Type),
    #"Added Quarter" = Table.AddColumn(#"Added Year", "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    #"Added Month" = Table.AddColumn(#"Added Quarter", "Month", each Date.MonthName([Date]), type text),
    #"Added MonthNo" = Table.AddColumn(#"Added Month", "MonthNo", each Date.Month([Date]), Int64.Type),
    #"Added Week" = Table.AddColumn(#"Added MonthNo", "Week", each Date.WeekOfYear([Date]), Int64.Type),
    #"Added DayOfWeek" = Table.AddColumn(#"Added Week", "DayOfWeek", each Date.DayOfWeekName([Date]), type text),
    #"Added IsWeekend" = Table.AddColumn(#"Added DayOfWeek", "IsWeekend", each 
        if Date.DayOfWeek([Date], Day.Monday) >= 5 then 1 else 0, 
        Int64.Type
    ),

    // Assign Season based on meteorological definition
    #"Added Season" = Table.AddColumn(#"Added IsWeekend", "Season", each 
        let m = [MonthNo] in
        if m = 3 or m = 4 or m = 5 then "Spring"
        else if m = 6 or m = 7 or m = 8 then "Summer"
        else if m = 9 or m = 10 or m = 11 then "Fall"
        else "Winter",
        type text
    ),

    #"Added SeasonKey" = Table.AddColumn(#"Added Season", "SeasonKey", each 
        if [Season] = "Spring" then 1
        else if [Season] = "Summer" then 2
        else if [Season] = "Fall" then 3
        else 4,
        Int64.Type
    ),

    // Festival and Retail Promotion Calendar assignment
    #"Added Festival" = Table.AddColumn(#"Added SeasonKey", "Festival", each 
        let 
            m = [MonthNo], 
            d = Date.Day([Date]),
            dw = Date.DayOfWeek([Date], Day.Monday) // 0 = Monday, 3 = Thursday, 4 = Friday
        in
        if m = 1 and d = 1 then "New Year's Day"
        else if m = 2 and d = 14 then "Valentine's Day"
        else if m = 5 and d >= 25 and dw = 0 then "Memorial Day Sale"
        else if m = 7 and d = 4 then "Independence Day Sale"
        else if m = 9 and d <= 7 and dw = 0 then "Labor Day / Back to School"
        else if m = 10 and d = 31 then "Halloween"
        else if m = 11 and d >= 22 and d <= 28 and dw = 3 then "Thanksgiving"
        else if m = 11 and d >= 23 and d <= 29 and dw = 4 then "Black Friday"
        else if m = 11 and d >= 26 and d <= 30 and dw = 0 then "Cyber Monday"
        else if m = 12 and (d = 1 or d = 2) then "Cyber Week"
        else if m = 12 and (d = 24 or d = 25) then "Christmas Holiday"
        else if m = 12 and d >= 26 and d <= 31 then "Year-End Mega Clearance"
        else "Regular Trading",
        type text
    )
in
    #"Added Festival"
