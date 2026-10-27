import os
import csv
import random
import datetime

# Seed for reproducibility
random.seed(42)

DATA_DIR = os.path.join(os.getcwd(), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# 1. DimSeason
# Defining meteorological / retail seasons across years 2023-2025
seasons_def = [
    {"SeasonKey": 1, "SeasonName": "Spring", "Color": "#10B981", "Months": [3, 4, 5]},
    {"SeasonKey": 2, "SeasonName": "Summer", "Color": "#F59E0B", "Months": [6, 7, 8]},
    {"SeasonKey": 3, "SeasonName": "Fall", "Color": "#EA580C", "Months": [9, 10, 11]},
    {"SeasonKey": 4, "SeasonName": "Winter", "Color": "#3B82F6", "Months": [12, 1, 2]},
]

# Write DimSeason
dim_season_rows = []
for yr in [2023, 2024, 2025]:
    dim_season_rows.append({"SeasonKey": f"{yr}01", "SeasonName": "Winter", "StartDate": f"{yr}-01-01", "EndDate": f"{yr}-02-28" if yr != 2024 else f"{yr}-02-29", "Year": yr})
    dim_season_rows.append({"SeasonKey": f"{yr}02", "SeasonName": "Spring", "StartDate": f"{yr}-03-01", "EndDate": f"{yr}-05-31", "Year": yr})
    dim_season_rows.append({"SeasonKey": f"{yr}03", "SeasonName": "Summer", "StartDate": f"{yr}-06-01", "EndDate": f"{yr}-08-31", "Year": yr})
    dim_season_rows.append({"SeasonKey": f"{yr}04", "SeasonName": "Fall", "StartDate": f"{yr}-09-01", "EndDate": f"{yr}-11-30", "Year": yr})
    dim_season_rows.append({"SeasonKey": f"{yr}05", "SeasonName": "Winter", "StartDate": f"{yr}-12-01", "EndDate": f"{yr}-12-31", "Year": yr})

# Standard Master DimSeason (4 season dimensions for Star Schema relationship)
master_seasons = [
    {"SeasonKey": 1, "SeasonName": "Spring", "SeasonCode": "SPR", "StartDate": "2023-03-01", "EndDate": "2023-05-31", "Description": "March to May - Renewal, Garden & Apparel"},
    {"SeasonKey": 2, "SeasonName": "Summer", "SeasonCode": "SUM", "StartDate": "2023-06-01", "EndDate": "2023-08-31", "Description": "June to August - Outdoor, Travel & Clearance"},
    {"SeasonKey": 3, "SeasonName": "Fall", "SeasonCode": "FAL", "StartDate": "2023-09-01", "EndDate": "2023-11-30", "Description": "September to November - Back to School & Harvest"},
    {"SeasonKey": 4, "SeasonName": "Winter", "SeasonCode": "WIN", "StartDate": "2023-12-01", "EndDate": "2024-02-28", "Description": "December to February - Holiday Shopping & Winter Warmth"},
]

with open(os.path.join(DATA_DIR, 'DimSeason.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["SeasonKey", "SeasonName", "SeasonCode", "StartDate", "EndDate", "Description"])
    writer.writeheader()
    writer.writerows(master_seasons)

# 2. DimProduct
# Categories: Apparel, Electronics, Home & Garden, Sports & Outdoor, Beauty & Health
products_raw = [
    # Apparel
    {"ProductID": "PRD-APP-001", "ProductName": "Thermal Winter Parka", "Category": "Apparel", "SubCategory": "Outerwear", "UnitCost": 65.0, "UnitPrice": 149.99, "PeakSeason": "Winter"},
    {"ProductID": "PRD-APP-002", "ProductName": "Cashmere Knit Sweater", "Category": "Apparel", "SubCategory": "Knitwear", "UnitCost": 42.0, "UnitPrice": 99.50, "PeakSeason": "Fall"},
    {"ProductID": "PRD-APP-003", "ProductName": "Breathable Linen Shirt", "Category": "Apparel", "SubCategory": "Tops", "UnitCost": 18.0, "UnitPrice": 48.00, "PeakSeason": "Summer"},
    {"ProductID": "PRD-APP-004", "ProductName": "Floral Spring Sundress", "Category": "Apparel", "SubCategory": "Dresses", "UnitCost": 25.0, "UnitPrice": 69.90, "PeakSeason": "Spring"},
    {"ProductID": "PRD-APP-005", "ProductName": "Waterproof Trench Coat", "Category": "Apparel", "SubCategory": "Outerwear", "UnitCost": 55.0, "UnitPrice": 129.00, "PeakSeason": "Spring"},
    {"ProductID": "PRD-APP-006", "ProductName": "Classic Denim Jacket", "Category": "Apparel", "SubCategory": "Outerwear", "UnitCost": 35.0, "UnitPrice": 79.99, "PeakSeason": "Fall"},
    {"ProductID": "PRD-APP-007", "ProductName": "Quick-Dry Board Shorts", "Category": "Apparel", "SubCategory": "Swimwear", "UnitCost": 12.0, "UnitPrice": 34.50, "PeakSeason": "Summer"},

    # Electronics
    {"ProductID": "PRD-ELE-001", "ProductName": "UltraHD 4K Smart OLED TV", "Category": "Electronics", "SubCategory": "Home Entertainment", "UnitCost": 480.0, "UnitPrice": 899.99, "PeakSeason": "Winter"},
    {"ProductID": "PRD-ELE-002", "ProductName": "Noise-Cancelling Wireless Headphones", "Category": "Electronics", "SubCategory": "Audio", "UnitCost": 85.0, "UnitPrice": 199.99, "PeakSeason": "Winter"},
    {"ProductID": "PRD-ELE-003", "ProductName": "Smart Fitness Watch Pro", "Category": "Electronics", "SubCategory": "Wearables", "UnitCost": 70.0, "UnitPrice": 159.00, "PeakSeason": "Spring"},
    {"ProductID": "PRD-ELE-004", "ProductName": "Portable Bluetooth Speaker", "Category": "Electronics", "SubCategory": "Audio", "UnitCost": 28.0, "UnitPrice": 69.99, "PeakSeason": "Summer"},
    {"ProductID": "PRD-ELE-005", "ProductName": "Ergonomic Mechanical Keyboard", "Category": "Electronics", "SubCategory": "Computer Accessories", "UnitCost": 45.0, "UnitPrice": 109.99, "PeakSeason": "Fall"},
    {"ProductID": "PRD-ELE-006", "ProductName": "1080p Streaming Webcam", "Category": "Electronics", "SubCategory": "Computer Accessories", "UnitCost": 22.0, "UnitPrice": 59.50, "PeakSeason": "Fall"},

    # Home & Garden
    {"ProductID": "PRD-HOM-001", "ProductName": "Ceramic Space Heater 1500W", "Category": "Home & Garden", "SubCategory": "Climate Control", "UnitCost": 28.0, "UnitPrice": 69.99, "PeakSeason": "Winter"},
    {"ProductID": "PRD-HOM-002", "ProductName": "Duo Oscillating Tower Fan", "Category": "Home & Garden", "SubCategory": "Climate Control", "UnitCost": 24.0, "UnitPrice": 59.99, "PeakSeason": "Summer"},
    {"ProductID": "PRD-HOM-003", "ProductName": "Botanical Planter Set 3-Pack", "Category": "Home & Garden", "SubCategory": "Gardening", "UnitCost": 15.0, "UnitPrice": 39.99, "PeakSeason": "Spring"},
    {"ProductID": "PRD-HOM-004", "ProductName": "Heavy-Duty Cordless Lawnmower", "Category": "Home & Garden", "SubCategory": "Lawn Care", "UnitCost": 140.0, "UnitPrice": 299.00, "PeakSeason": "Spring"},
    {"ProductID": "PRD-HOM-005", "ProductName": "Decorative Holiday String Lights", "Category": "Home & Garden", "SubCategory": "Seasonal Decor", "UnitCost": 8.0, "UnitPrice": 29.99, "PeakSeason": "Winter"},
    {"ProductID": "PRD-HOM-006", "ProductName": "Autumn Scented Candle Collection", "Category": "Home & Garden", "SubCategory": "Home Fragrance", "UnitCost": 10.0, "UnitPrice": 26.50, "PeakSeason": "Fall"},

    # Sports & Outdoor
    {"ProductID": "PRD-SPO-001", "ProductName": "4-Person Camping Tent", "Category": "Sports & Outdoor", "SubCategory": "Camping", "UnitCost": 75.0, "UnitPrice": 169.99, "PeakSeason": "Summer"},
    {"ProductID": "PRD-SPO-002", "ProductName": "All-Mountain Snow Ski Goggles", "Category": "Sports & Outdoor", "SubCategory": "Winter Sports", "UnitCost": 30.0, "UnitPrice": 79.99, "PeakSeason": "Winter"},
    {"ProductID": "PRD-SPO-003", "ProductName": "Aluminum Road Bicycle 21-Speed", "Category": "Sports & Outdoor", "SubCategory": "Cycling", "UnitCost": 190.0, "UnitPrice": 420.00, "PeakSeason": "Spring"},
    {"ProductID": "PRD-SPO-004", "ProductName": "Insulated Hydro Canteen 32oz", "Category": "Sports & Outdoor", "SubCategory": "Hydration", "UnitCost": 11.0, "UnitPrice": 29.99, "PeakSeason": "Summer"},
    {"ProductID": "PRD-SPO-005", "ProductName": "Trekking Poles Carbon Fiber", "Category": "Sports & Outdoor", "SubCategory": "Hiking", "UnitCost": 22.0, "UnitPrice": 54.99, "PeakSeason": "Fall"},

    # Beauty & Health
    {"ProductID": "PRD-BEA-001", "ProductName": "Hydrating SPF 50 Sunscreen", "Category": "Beauty & Health", "SubCategory": "Sun Care", "UnitCost": 7.0, "UnitPrice": 22.00, "PeakSeason": "Summer"},
    {"ProductID": "PRD-BEA-002", "ProductName": "Intense Moisture Winter Lip Balm", "Category": "Beauty & Health", "SubCategory": "Skincare", "UnitCost": 3.0, "UnitPrice": 9.99, "PeakSeason": "Winter"},
    {"ProductID": "PRD-BEA-003", "ProductName": "Vitamin C Radiance Glow Serum", "Category": "Beauty & Health", "SubCategory": "Skincare", "UnitCost": 12.0, "UnitPrice": 38.00, "PeakSeason": "Spring"},
    {"ProductID": "PRD-BEA-004", "ProductName": "Exfoliating Coffee Body Scrub", "Category": "Beauty & Health", "SubCategory": "Personal Care", "UnitCost": 8.0, "UnitPrice": 24.50, "PeakSeason": "Fall"},
]

dim_product_rows = []
for idx, p in enumerate(products_raw, start=1):
    dim_product_rows.append({
        "ProductKey": idx,
        "ProductID": p["ProductID"],
        "ProductName": p["ProductName"],
        "Category": p["Category"],
        "SubCategory": p["SubCategory"],
        "UnitCost": round(p["UnitCost"], 2),
        "UnitPrice": round(p["UnitPrice"], 2),
        "PeakSeason": p["PeakSeason"]
    })

with open(os.path.join(DATA_DIR, 'DimProduct.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["ProductKey", "ProductID", "ProductName", "Category", "SubCategory", "UnitCost", "UnitPrice"])
    writer.writeheader()
    for row in dim_product_rows:
        writer.writerow({k: row[k] for k in ["ProductKey", "ProductID", "ProductName", "Category", "SubCategory", "UnitCost", "UnitPrice"]})

# 3. DimStore
stores_raw = [
    {"StoreKey": 1, "StoreName": "Metro Center Flagship", "City": "New York", "State": "NY", "Region": "East", "StoreType": "Flagship"},
    {"StoreKey": 2, "StoreName": "Boston Common Galleria", "City": "Boston", "State": "MA", "Region": "East", "StoreType": "Mall"},
    {"StoreKey": 3, "StoreName": "Philadelphia Liberty Center", "City": "Philadelphia", "State": "PA", "Region": "East", "StoreType": "Outlet"},
    {"StoreKey": 4, "StoreName": "Magnificent Mile Retail", "City": "Chicago", "State": "IL", "Region": "Central", "StoreType": "Flagship"},
    {"StoreKey": 5, "StoreName": "Twin Cities Mall of America", "City": "Minneapolis", "State": "MN", "Region": "Central", "StoreType": "Mall"},
    {"StoreKey": 6, "StoreName": "Detroit Metro Pavilion", "City": "Detroit", "State": "MI", "Region": "Central", "StoreType": "Outlet"},
    {"StoreKey": 7, "StoreName": "Atlanta Peachtree Square", "City": "Atlanta", "State": "GA", "Region": "South", "StoreType": "Mall"},
    {"StoreKey": 8, "StoreName": "Miami Biscayne Promenade", "City": "Miami", "State": "FL", "Region": "South", "StoreType": "Flagship"},
    {"StoreKey": 9, "StoreName": "Dallas Galleria Station", "City": "Dallas", "State": "TX", "Region": "South", "StoreType": "Mall"},
    {"StoreKey": 10, "StoreName": "Houston Space City Plaza", "City": "Houston", "State": "TX", "Region": "South", "StoreType": "Outlet"},
    {"StoreKey": 11, "StoreName": "San Francisco Union Square", "City": "San Francisco", "State": "CA", "Region": "West", "StoreType": "Flagship"},
    {"StoreKey": 12, "StoreName": "Los Angeles Beverly Centre", "City": "Los Angeles", "State": "CA", "Region": "West", "StoreType": "Mall"},
    {"StoreKey": 13, "StoreName": "Seattle Pike Place Market", "City": "Seattle", "State": "WA", "Region": "West", "StoreType": "Flagship"},
    {"StoreKey": 14, "StoreName": "Denver Rocky Mountain Mall", "City": "Denver", "State": "CO", "Region": "West", "StoreType": "Outlet"},
]

with open(os.path.join(DATA_DIR, 'DimStore.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["StoreKey", "StoreName", "City", "State", "Region", "StoreType"])
    writer.writeheader()
    writer.writerows(stores_raw)

# 4. DimDate (spanning 2023-01-01 to 2025-12-31)
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2025, 12, 31)

def get_season(month):
    if month in [3, 4, 5]:
        return ("Spring", 1)
    elif month in [6, 7, 8]:
        return ("Summer", 2)
    elif month in [9, 10, 11]:
        return ("Fall", 3)
    else:
        return ("Winter", 4)

def get_festival(d):
    # Fixed & floating holidays
    m, day = d.month, d.day
    if m == 1 and day == 1:
        return "New Year's Day"
    elif m == 2 and day == 14:
        return "Valentine's Day"
    elif m == 5 and day >= 25 and d.weekday() == 0:
        return "Memorial Day Sale"
    elif m == 7 and day == 4:
        return "Independence Day Sale"
    elif m == 9 and day <= 7 and d.weekday() == 0:
        return "Labor Day / Back to School"
    elif m == 10 and day == 31:
        return "Halloween"
    elif m == 11 and 22 <= day <= 28 and d.weekday() == 3:
        return "Thanksgiving"
    elif m == 11 and 23 <= day <= 29 and d.weekday() == 4:
        return "Black Friday"
    elif m == 11 and 26 <= day <= 30 and d.weekday() == 0:
        return "Cyber Monday"
    elif m == 12 and 1 <= day <= 2:
        # early dec cyber week
        return "Cyber Week"
    elif m == 12 and 24 <= day <= 25:
        return "Christmas Holiday"
    elif m == 12 and 26 <= day <= 31:
        return "Year-End Mega Clearance"
    return "Regular Trading"

curr = start_date
dim_date_rows = []
while curr <= end_date:
    date_key = int(curr.strftime("%Y%m%d"))
    date_str = curr.strftime("%Y-%m-%d")
    year = curr.year
    month_no = curr.month
    month_name = curr.strftime("%B")
    quarter = f"Q{(month_no - 1) // 3 + 1}"
    week_no = curr.isocalendar()[1]
    day_of_week = curr.strftime("%A")
    is_weekend = 1 if curr.weekday() >= 5 else 0
    season_name, season_key = get_season(month_no)
    festival = get_festival(curr)

    dim_date_rows.append({
        "DateKey": date_key,
        "Date": date_str,
        "Year": year,
        "Quarter": quarter,
        "Month": month_name,
        "MonthNo": month_no,
        "Week": week_no,
        "DayOfWeek": day_of_week,
        "IsWeekend": is_weekend,
        "Season": season_name,
        "SeasonKey": season_key,
        "Festival": festival
    })
    curr += datetime.timedelta(days=1)

with open(os.path.join(DATA_DIR, 'DimDate.csv'), 'w', newline='', encoding='utf-8') as f:
    fieldnames = ["DateKey", "Date", "Year", "Quarter", "Month", "MonthNo", "Week", "DayOfWeek", "IsWeekend", "Season", "SeasonKey", "Festival"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dim_date_rows)

print(f"DimDate generated: {len(dim_date_rows)} days")

# 5. FactSales
# Generate realistic seasonal sales with YoY growth, festival multipliers, product seasonal affinity
date_dict = {r["DateKey"]: r for r in dim_date_rows}
date_keys = [r["DateKey"] for r in dim_date_rows]

orders = []
order_id_counter = 100001

# Seasonal weights base
season_multipliers = {
    "Spring": 1.05,
    "Summer": 1.15,
    "Fall": 1.10,
    "Winter": 1.35   # Q4 holiday rush
}

# Yearly growth trend
year_multipliers = {
    2023: 1.00,
    2024: 1.12,  # +12% YoY
    2025: 1.25   # +11.6% YoY vs 2024
}

# Regional weights
store_weights = [1.3, 1.0, 0.8, 1.2, 0.9, 0.7, 1.0, 1.15, 1.05, 0.85, 1.25, 1.2, 1.1, 0.8]

# Target around 15,000 transactions
for d in dim_date_rows:
    dt = datetime.datetime.strptime(d["Date"], "%Y-%m-%d").date()
    dkey = d["DateKey"]
    yr = d["Year"]
    season = d["Season"]
    festival = d["Festival"]
    is_weekend = d["IsWeekend"]

    # Base orders per day
    base_n = 11
    if is_weekend:
        base_n += 4
    
    # Season multiplier
    s_mult = season_multipliers[season]
    y_mult = year_multipliers[yr]

    # Festival impact
    f_mult = 1.0
    f_discount_bias = 0.0
    if festival in ["Black Friday", "Cyber Monday"]:
        f_mult = 3.6
        f_discount_bias = 0.20
    elif festival in ["Year-End Mega Clearance", "Christmas Holiday"]:
        f_mult = 2.4
        f_discount_bias = 0.15
    elif festival in ["Memorial Day Sale", "Labor Day / Back to School", "Independence Day Sale"]:
        f_mult = 1.8
        f_discount_bias = 0.10
    elif festival == "Valentine's Day":
        f_mult = 1.5
        f_discount_bias = 0.08
    elif festival != "Regular Trading":
        f_mult = 1.3
        f_discount_bias = 0.05

    daily_orders = int(base_n * s_mult * y_mult * f_mult * random.uniform(0.85, 1.15))

    for _ in range(daily_orders):
        order_id = f"ORD-{order_id_counter}"
        order_id_counter += 1

        # Select store
        store_obj = random.choices(stores_raw, weights=store_weights, k=1)[0]
        store_key = store_obj["StoreKey"]

        # Select product based on seasonal affinity
        prod_weights = []
        for p in dim_product_rows:
            w = 1.0
            if p["PeakSeason"] == season:
                w *= 2.8  # Strong seasonal affinity
            elif (season == "Winter" and p["PeakSeason"] == "Summer") or (season == "Summer" and p["PeakSeason"] == "Winter"):
                w *= 0.35 # Off-season trough
            prod_weights.append(w)

        prod = random.choices(dim_product_rows, weights=prod_weights, k=1)[0]
        prod_key = prod["ProductKey"]

        # Quantity
        qty_weights = [0.55, 0.28, 0.10, 0.05, 0.02]
        qty = random.choices([1, 2, 3, 4, 5], weights=qty_weights, k=1)[0]

        # Discount
        if f_discount_bias > 0:
            discount_pct = min(0.40, round(random.choice([0.10, 0.15, 0.20, 0.25, 0.30]) + random.uniform(0, f_discount_bias * 0.5), 2))
        else:
            discount_pct = random.choices([0.0, 0.05, 0.10, 0.15, 0.20], weights=[0.45, 0.25, 0.15, 0.10, 0.05], k=1)[0]

        unit_price = prod["UnitPrice"]
        unit_cost = prod["UnitCost"]

        # Revenue = Quantity * UnitPrice * (1 - Discount)
        gross_rev = qty * unit_price
        discount_amount = round(gross_rev * discount_pct, 2)
        revenue = round(gross_rev - discount_amount, 2)
        total_cost = round(qty * unit_cost, 2)
        profit = round(revenue - total_cost, 2)

        # Status: 98% Completed, 1.5% Cancelled (to test Power Query cleaning requirements), 0.5% Outlier/Test
        status_rand = random.random()
        if status_rand < 0.015:
            status = "Cancelled"
        elif status_rand < 0.018:
            status = "Returned"
        else:
            status = "Completed"

        orders.append({
            "OrderID": order_id,
            "DateKey": dkey,
            "ProductKey": prod_key,
            "StoreKey": store_key,
            "SeasonKey": d["SeasonKey"],
            "Quantity": qty,
            "Revenue": revenue,
            "Discount": discount_pct,
            "Profit": profit,
            "OrderStatus": status
        })

print(f"Total sales generated: {len(orders)} transactions")

# Write FactSales
with open(os.path.join(DATA_DIR, 'FactSales.csv'), 'w', newline='', encoding='utf-8') as f:
    fieldnames = ["OrderID", "DateKey", "ProductKey", "StoreKey", "SeasonKey", "Quantity", "Revenue", "Discount", "Profit", "OrderStatus"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(orders)

# Also create cleaned FactSales (Completed only) as required by Power Query step
cleaned_orders = [o for o in orders if o["OrderStatus"] == "Completed"]
with open(os.path.join(DATA_DIR, 'FactSales_Cleaned.csv'), 'w', newline='', encoding='utf-8') as f:
    fieldnames = ["OrderID", "DateKey", "ProductKey", "StoreKey", "SeasonKey", "Quantity", "Revenue", "Discount", "Profit", "OrderStatus"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cleaned_orders)

# Export complete data payload for interactive web dashboard
import json
payload = {
    "products": dim_product_rows,
    "stores": stores_raw,
    "seasons": master_seasons,
    "dates": dim_date_rows,
    "orders": cleaned_orders,
    "metadata": {
        "generatedAt": datetime.datetime.now().isoformat(),
        "totalOrdersRaw": len(orders),
        "totalOrdersCleaned": len(cleaned_orders),
        "totalRevenue": round(sum(o["Revenue"] for o in cleaned_orders), 2),
        "totalProfit": round(sum(o["Profit"] for o in cleaned_orders), 2),
        "totalUnits": sum(o["Quantity"] for o in cleaned_orders),
        "years": [2023, 2024, 2025]
    }
}

with open(os.path.join(DATA_DIR, 'retail_dashboard_data.json'), 'w', encoding='utf-8') as f:
    json.dump(payload, f, indent=2)

# Also export as retail_dashboard_data.js (window.RETAIL_DATA = ...) for zero-config browser loading
with open(os.path.join(DATA_DIR, 'retail_dashboard_data.js'), 'w', encoding='utf-8') as f:
    f.write("window.RETAIL_DATA = " + json.dumps(payload) + ";\n")

print("Data generation and web payload export finished successfully!")
