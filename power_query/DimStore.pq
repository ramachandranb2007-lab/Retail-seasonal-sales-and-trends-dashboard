// ============================================================================
// Power Query M Script: DimStore
// Description: Cleans and validates the Store geographic dimension
// ============================================================================

let
    // 1. Ingest source CSV file
    Source = Csv.Document(
        File.Contents(SourceFilePath & "\DimStore.csv"),
        [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),

    // 2. Promote headers
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    // 3. Strongly type fields
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"StoreKey", Int64.Type},
        {"StoreName", type text},
        {"City", type text},
        {"State", type text},
        {"Region", type text},
        {"StoreType", type text}
    }),

    // 4. Clean whitespace
    #"Trimmed Text" = Table.TransformColumns(#"Changed Type", {
        {"StoreName", Text.Trim, type text},
        {"City", Text.Trim, type text},
        {"State", Text.Trim, type text},
        {"Region", Text.Trim, type text}
    }),

    // 5. Deduplicate primary key
    #"Removed Duplicates" = Table.Distinct(#"Trimmed Text", {"StoreKey"}),

    // 6. Ensure non-null records
    #"Filtered Rows" = Table.SelectRows(#"Removed Duplicates", each 
        [StoreKey] <> null and 
        [StoreName] <> "" and 
        [Region] <> ""
    )
in
    #"Filtered Rows"
