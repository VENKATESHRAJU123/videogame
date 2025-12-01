# ============================================
# Clean Sales Dataset
# ============================================

import pandas as pd
import numpy as np
import os

print("\n" + "="*70)
print("CLEANING SALES DATASET")
print("="*70 + "\n")

# ============================================
# LOAD DATA
# ============================================

print("📂 Loading vgsales.csv...")

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
input_file = os.path.join(project_root, 'data', 'raw', 'vgsales.csv')
output_folder = os.path.join(project_root, 'data', 'cleaned')

# Create folder if needed
os.makedirs(output_folder, exist_ok=True)

# Load data
sales = pd.read_csv(input_file)
print(f"✅ Loaded {len(sales)} rows\n")

original_rows = len(sales)

# ============================================
# STEP 1: Remove Duplicates
# ============================================

print("STEP 1: Removing Duplicates")
print("-" * 70)

duplicates_before = sales.duplicated().sum()
print(f"Found {duplicates_before} duplicate rows")

sales = sales.drop_duplicates()

duplicates_removed = original_rows - len(sales)
print(f"✅ Removed {duplicates_removed} duplicates")
print(f"   Remaining rows: {len(sales)}\n")

# ============================================
# STEP 2: Clean Year Column
# ============================================

print("STEP 2: Cleaning Year Column")
print("-" * 70)

# Remove 'N/A' values
if 'Year' in sales.columns:
    before = len(sales)
    sales = sales[sales['Year'].notna()]
    sales = sales[sales['Year'] != 'N/A']
    removed = before - len(sales)
    print(f"Removed {removed} rows with missing/invalid years")
    
    # Convert to integer
    sales['Year'] = sales['Year'].astype(int)
    print(f"✅ Converted Year to integer")
    print(f"   Year range: {sales['Year'].min()} to {sales['Year'].max()}\n")

# ============================================
# STEP 3: Clean Text Fields
# ============================================

print("STEP 3: Cleaning Text Fields")
print("-" * 70)

# Clean each text column
if 'Name' in sales.columns:
    sales['Name'] = sales['Name'].str.strip().str.title()
    print("✅ Cleaned 'Name' column")

if 'Platform' in sales.columns:
    sales['Platform'] = sales['Platform'].str.strip().str.upper()
    print("✅ Cleaned 'Platform' column")

if 'Genre' in sales.columns:
    sales['Genre'] = sales['Genre'].str.strip().str.title()
    print("✅ Cleaned 'Genre' column")

if 'Publisher' in sales.columns:
    sales['Publisher'] = sales['Publisher'].str.strip().str.title()
    print("✅ Cleaned 'Publisher' column")

print()

# ============================================
# STEP 4: Validate Sales Columns
# ============================================

print("STEP 4: Validating Sales Figures")
print("-" * 70)

sales_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']

for col in sales_columns:
    if col in sales.columns:
        # Convert to numeric, replace errors with 0
        sales[col] = pd.to_numeric(sales[col], errors='coerce').fillna(0)
        print(f"✅ Validated '{col}'")

print()

# ============================================
# STEP 5: Remove Invalid Records
# ============================================

print("STEP 5: Removing Invalid Records")
print("-" * 70)

if 'Global_Sales' in sales.columns:
    before = len(sales)
    sales = sales[sales['Global_Sales'] > 0]
    removed = before - len(sales)
    print(f"Removed {removed} games with zero sales\n")

# ============================================
# STEP 6: Save Cleaned Data
# ============================================

print("STEP 6: Saving Cleaned Data")
print("-" * 70)

output_file = os.path.join(output_folder, 'vgsales_cleaned.csv')
sales.to_csv(output_file, index=False)

print(f"✅ Saved to: {output_file}")
print(f"✅ Final dataset: {len(sales)} rows, {len(sales.columns)} columns\n")

# ============================================
# SUMMARY
# ============================================

print("="*70)
print("CLEANING SUMMARY")
print("="*70)
print(f"Original rows: {original_rows}")
print(f"Final rows: {len(sales)}")
print(f"Columns: {len(sales.columns)}")
print()

print("Column names:")
for i, col in enumerate(sales.columns, 1):
    print(f"  {i}. {col}")
print()

print("First 5 rows:")
print(sales.head())
print()

if 'Global_Sales' in sales.columns:
    print("SALES STATISTICS:")
    print(f"  Total Global Sales: ${sales['Global_Sales'].sum():.2f}M")
    print(f"  Average per Game: ${sales['Global_Sales'].mean():.2f}M")
    print(f"  Highest Selling Game: ${sales['Global_Sales'].max():.2f}M")
    print()
    
    print("TOP 5 BEST-SELLING GAMES:")
    top5 = sales.nlargest(5, 'Global_Sales')[['Name', 'Platform', 'Year', 'Global_Sales']]
    print(top5.to_string(index=False))

print()
print("✅ SALES DATASET CLEANING COMPLETE!")
print("="*70)
