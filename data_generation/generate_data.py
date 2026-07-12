
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
Faker.seed(42)

plants = ["Frankfurt", "Cologne", "Hamburg"]
machine_types = ["CNC Mill", "Injection Molder", "Assembly Robot", "Packaging Unit"]

machines = []
machine_id = 1
for plant in plants:
    for i in range(1, 5):
        if machine_id > 10:
            break
        machines.append({
            "machine_id": machine_id,
            "machine_name": f"{plant[:3].upper()}-M{i}",
            "plant": plant,
            "production_line": random.randint(1, 3),
            "machine_type": random.choice(machine_types),
            "capacity_per_hour": random.randint(50, 200)
        })
        machine_id += 1

df_machines = pd.DataFrame(machines)
print(df_machines)
print(f"\nTotal machines: {len(df_machines)}")

# ---------------------------
# 2. PRODUCTS
# ---------------------------
categories = ["Hardware", "Software", "Services"]
channels = ["Direct", "Distributor", "OEM"]
markets = ["Germany", "EU", "International"]

products = []
for i in range(1, 6):  # 5 SKUs
    category = random.choice(categories)
    unit_cost = round(random.uniform(20, 300), 2)
    products.append({
        "product_id": i,
        "product_name": f"Product-{i:02d}",
        "category": category,
        "SKU": f"SKU-{1000+i}",
        "unit_cost": unit_cost,
        "unit_price": round(unit_cost * random.uniform(1.3, 2.2), 2),  # markup
        "channel": random.choice(channels),
        "market": random.choice(markets)
    })

df_products = pd.DataFrame(products)
print(df_products)
print(f"\nTotal products: {len(df_products)}")

# ---------------------------
# 3. SHIFTS
# ---------------------------
shift_defs = [
    ("Morning", "06:00", "14:00"),
    ("Afternoon", "14:00", "22:00"),
    ("Night", "22:00", "06:00")
]

shifts = []
shift_id = 1
for plant in plants:
    for shift_name, start, end in shift_defs:
        shifts.append({
            "shift_id": shift_id,
            "shift_name": shift_name,
            "start_time": start,
            "end_time": end,
            "plant": plant,
            "supervisor": fake.name()
        })
        shift_id += 1

df_shifts = pd.DataFrame(shifts)
print(df_shifts)
print(f"\nTotal shifts: {len(df_shifts)}")

# ---------------------------
# 4. COST CENTRES
# ---------------------------
departments = ["Production", "Sales", "Finance", "Controlling", "Logistics"]

cost_centres = []
cc_id = 1
for plant in plants:
    for dept in departments:
        cost_centres.append({
            "cc_id": cc_id,
            "cost_centre_name": f"{plant[:3].upper()}-{dept[:4].upper()}",
            "department": dept,
            "plant": plant,
            "budget_owner": fake.name()
        })
        cc_id += 1

df_costcentres = pd.DataFrame(cost_centres)
print(df_costcentres)
print(f"\nTotal cost centres: {len(df_costcentres)}")

# ---------------------------
# 5. DATE RANGE (2 years)
# ---------------------------
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_list = pd.date_range(start_date, end_date, freq='D')

print(f"\nDate range: {date_list[0].date()} to {date_list[-1].date()} ({len(date_list)} days)")

# ---------------------------
# 6. FACT: PRODUCTION
# ---------------------------
production_records = []
production_id = 1

for date in date_list:
    # not every machine runs every shift every day — simulate ~70% activity rate
    for machine in machines:
        for shift in [s for s in shifts if s["plant"] == machine["plant"]]:
            if random.random() > 0.3:  # 70% chance this machine/shift combo produced today
                product = random.choice(products)
                capacity_available = machine["capacity_per_hour"] * 8  # 8-hour shift
                units_produced = int(capacity_available * random.uniform(0.6, 0.98))
                units_defect = int(units_produced * random.uniform(0.0, 0.08))
                downtime_mins = random.randint(0, 120)
                cost_actual = round(units_produced * product["unit_cost"] * random.uniform(0.9, 1.1), 2)

                production_records.append({
                    "production_id": production_id,
                    "date_id": date.strftime("%Y-%m-%d"),
                    "machine_id": machine["machine_id"],
                    "shift_id": shift["shift_id"],
                    "product_id": product["product_id"],
                    "units_produced": units_produced,
                    "units_defect": units_defect,
                    "downtime_mins": downtime_mins,
                    "cost_actual": cost_actual,
                    "capacity_available": capacity_available
                })
                production_id += 1

df_production = pd.DataFrame(production_records)
print(f"\nTotal production records: {len(df_production)}")
print(df_production.head())

# ---------------------------
# 7. FACT: SALES
# ---------------------------
sales_records = []
sale_id = 1

for date in date_list:
    # simulate 3-8 sales transactions per day
    num_sales_today = random.randint(3, 8)
    for _ in range(num_sales_today):
        product = random.choice(products)
        cc = random.choice([c for c in cost_centres if c["department"] == "Sales"])
        units_sold = random.randint(5, 200)
        discount_pct = round(random.uniform(0, 0.15), 3)
        revenue = round(units_sold * product["unit_price"] * (1 - discount_pct), 2)
        cost_of_goods = round(units_sold * product["unit_cost"], 2)
        gross_margin = round(revenue - cost_of_goods, 2)

        sales_records.append({
            "sale_id": sale_id,
            "date_id": date.strftime("%Y-%m-%d"),
            "product_id": product["product_id"],
            "cc_id": cc["cc_id"],
            "channel": product["channel"],
            "units_sold": units_sold,
            "revenue": revenue,
            "discount_pct": discount_pct,
            "cost_of_goods": cost_of_goods,
            "gross_margin": gross_margin
        })
        sale_id += 1

df_sales = pd.DataFrame(sales_records)
print(f"\nTotal sales records: {len(df_sales)}")
print(df_sales.head())

# ---------------------------
# 8. FACT: BUDGET (monthly, 24 months)
# ---------------------------
budget_records = []
budget_id = 1
scenarios = ["Budget", "Forecast"]

months = pd.date_range(start_date, end_date, freq='MS')  # month start dates

for month in months:
    for cc in cost_centres:
        for product in products:
            budget_revenue = round(random.uniform(20000, 150000), 2)
            budget_cost = round(budget_revenue * random.uniform(0.5, 0.8), 2)
            # forecast is budget +/- some variance to simulate deviation
            forecast_revenue = round(budget_revenue * random.uniform(0.85, 1.15), 2)
            forecast_cost = round(budget_cost * random.uniform(0.85, 1.15), 2)

            budget_records.append({
                "budget_id": budget_id,
                "date_id": month.strftime("%Y-%m-%d"),
                "cc_id": cc["cc_id"],
                "product_id": product["product_id"],
                "budget_revenue": budget_revenue,
                "budget_cost": budget_cost,
                "forecast_revenue": forecast_revenue,
                "forecast_cost": forecast_cost,
                "scenario": "Actual"
            })
            budget_id += 1

df_budget = pd.DataFrame(budget_records)
print(f"\nTotal budget records: {len(df_budget)}")
print(df_budget.head())

# ---------------------------
# 9. SAVE ALL TO CSV
# ---------------------------
import os

os.makedirs("data", exist_ok=True)

df_machines.to_csv("data/machines.csv", index=False)
df_products.to_csv("data/products.csv", index=False)
df_shifts.to_csv("data/shifts.csv", index=False)
df_costcentres.to_csv("data/costcentres.csv", index=False)
df_production.to_csv("data/production.csv", index=False)
df_sales.to_csv("data/sales.csv", index=False)
df_budget.to_csv("data/budget.csv", index=False)

print("\n✅ All CSV files saved to /data folder")