// ============================================================================
// Power Query M Script: FactSales
// Description: Imports and cleans raw sales transactions
// Transformations: Type conversions, duplicate removal, status filtering,
//                 outlier exclusion, and primary/foreign key validation.
// ============================================================================

let
    // 1. Ingest source CSV file
    Source = Csv.Document(
        File.Contents(SourceFilePath & "\FactSales.csv"),
        [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),

    // 2. Promote first row to column headers
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    // 3. Strongly type all fields for optimal tabular engine compression
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"OrderID", type text},
        {"DateKey", Int64.Type},
        {"ProductKey", Int64.Type},
        {"StoreKey", Int64.Type},
        {"SeasonKey", Int64.Type},
        {"Quantity", Int64.Type},
        {"Revenue", type number},
        {"Discount", type number},
        {"Profit", type number},
        {"OrderStatus", type text}
    }),

    // 4. Remove duplicate order rows if any exist
    #"Removed Duplicates" = Table.Distinct(#"Changed Type", {"OrderID"}),

    // 5. Filter out cancelled orders and invalid transactions as per PRD requirements
    #"Filtered Valid Status" = Table.SelectRows(#"Removed Duplicates", each ([OrderStatus] = "Completed")),

    // 6. Data Quality & Outlier check: Filter positive values and non-null keys
    #"Filtered Clean Data" = Table.SelectRows(#"Filtered Valid Status", each 
        [DateKey] <> null and 
        [ProductKey] <> null and 
        [StoreKey] <> null and 
        [Quantity] > 0 and 
        [Revenue] >= 0
    ),

    // 7. Add surrogate Gross Revenue column if needed for margin reconciliation
    #"Added GrossSales" = Table.AddColumn(#"Filtered Clean Data", "GrossSales", each 
        if [Discount] < 1 then [Revenue] / (1 - [Discount]) else [Revenue], 
        type number
    ),

    // 8. Reorder and select final model columns
    #"Reordered Columns" = Table.SelectColumns(#"Added GrossSales", {
        "OrderID", 
        "DateKey", 
        "ProductKey", 
        "StoreKey", 
        "SeasonKey", 
        "Quantity", 
        "Revenue", 
        "Discount", 
        "Profit", 
        "OrderStatus",
        "GrossSales"
    })
in
    #"Reordered Columns"
