// ============================================================================
// Power Query M Script: DimSeason
// Description: Master Season dimension for seasonal trend analysis
// ============================================================================

let
    // 1. Ingest source CSV file
    Source = Csv.Document(
        File.Contents(SourceFilePath & "\DimSeason.csv"),
        [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),

    // 2. Promote headers
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    // 3. Strongly type fields
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"SeasonKey", Int64.Type},
        {"SeasonName", type text},
        {"SeasonCode", type text},
        {"StartDate", type date},
        {"EndDate", type date},
        {"Description", type text}
    }),

    // 4. Deduplicate primary key
    #"Removed Duplicates" = Table.Distinct(#"Changed Type", {"SeasonKey"}),

    // 5. Filter null records
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each [SeasonKey] <> null)
in
    #"Filtered Rows"
