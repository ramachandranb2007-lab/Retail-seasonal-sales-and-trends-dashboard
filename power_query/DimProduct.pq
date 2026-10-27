// ============================================================================
// Power Query M Script: DimProduct
// Description: Cleans, deduplicates, and validates the Product dimension
// ============================================================================

let
    // 1. Ingest source CSV file
    Source = Csv.Document(
        File.Contents(SourceFilePath & "\DimProduct.csv"),
        [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),

    // 2. Promote first row to column headers
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    // 3. Strongly type all fields
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"ProductKey", Int64.Type},
        {"ProductID", type text},
        {"ProductName", type text},
        {"Category", type text},
        {"SubCategory", type text},
        {"UnitCost", type number},
        {"UnitPrice", type number}
    }),

    // 4. Clean text whitespace
    #"Trimmed Text" = Table.TransformColumns(#"Changed Type", {
        {"ProductName", Text.Trim, type text},
        {"Category", Text.Trim, type text},
        {"SubCategory", Text.Trim, type text}
    }),

    // 5. Ensure primary key uniqueness
    #"Removed Duplicates" = Table.Distinct(#"Trimmed Text", {"ProductKey"}),

    // 6. Filter null or invalid records
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each 
        [ProductKey] <> null and 
        [ProductName] <> "" and 
        [UnitPrice] >= 0
    )
in
    #"Filtered Rows"
