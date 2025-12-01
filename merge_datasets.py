# ============================================
# MERGE GAMES AND SALES DATASETS
# ============================================

import pandas as pd
import os

print("\n" + "="*80)
print("MERGING GAMES AND SALES DATASETS")
print("="*80 + "\n")

# ============================================
# LOAD CLEANED DATA
# ============================================

print("STEP 1: Loading Cleaned Datasets")
print("-" * 80)

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
cleaned_folder = os.path.join(project_root, 'data', 'cleaned')

games_file = os.path.join(cleaned_folder, 'games_cleaned.csv')
sales_file = os.path.join(cleaned_folder, 'vgsales_cleaned.csv')

try:
    games = pd.read_csv(games_file)
    print(f"✅ Loaded games_cleaned.csv - {len(games):,} rows")
except Exception as e:
    print(f"❌ Error: {e}")
    print("   Did you run 02_clean_games.py first?")
    exit()

try:
    sales = pd.read_csv(sales_file)
    print(f"✅ Loaded vgsales_cleaned.csv - {len(sales):,} rows")
except Exception as e:
    print(f"❌ Error: {e}")
    print("   Did you run 03_clean_sales.py first?")
    exit()

print()

# ============================================
# IDENTIFY MATCHING COLUMNS
# ============================================

print("STEP 2: Identifying Matching Columns")
print("-" * 80)

# Find title columns
title_col_games = None
for col in ['Title', 'title', 'Name', 'name']:
    if col in games.columns:
        title_col_games = col
        break

name_col_sales = None
for col in ['Name', 'name', 'Title', 'title']:
    if col in sales.columns:
        name_col_sales = col
        break

# Find platform columns
platform_col_games = None
for col in ['Platform', 'platform', 'Console']:
    if col in games.columns:
        platform_col_games = col
        break

platform_col_sales = None
for col in ['Platform', 'platform', 'Console']:
    if col in sales.columns:
        platform_col_sales = col
        break

print(f"Games title column: {title_col_games}")
print(f"Sales name column: {name_col_sales}")
print(f"Games platform column: {platform_col_games}")
print(f"Sales platform column: {platform_col_sales}")
print()

# ============================================
# PREPARE FOR MERGE
# ============================================

print("STEP 3: Preparing for Merge")
print("-" * 80)

if not title_col_games or not name_col_sales:
    print("❌ Cannot find title columns!")
    exit()

# Create normalized matching columns
games['Match_Title'] = games[title_col_games].str.lower().str.strip()
sales['Match_Name'] = sales[name_col_sales].str.lower().str.strip()

print("✅ Created normalized matching columns")

# Determine merge strategy
if platform_col_games and platform_col_sales:
    print("   Strategy: Match on TITLE + PLATFORM")
    merge_left = ['Match_Title', platform_col_games]
    merge_right = ['Match_Name', platform_col_sales]
else:
    print("   Strategy: Match on TITLE only")
    merge_left = ['Match_Title']
    merge_right = ['Match_Name']

print()

# ============================================
# PERFORM MERGE
# ============================================

print("STEP 4: Merging Datasets")
print("-" * 80)

try:
    merged = pd.merge(
        games,
        sales,
        left_on=merge_left,
        right_on=merge_right,
        how='inner'
    )
    
    print(f"✅ Merge successful!")
    print(f"   Games: {len(games):,} rows")
    print(f"   Sales: {len(sales):,} rows")
    print(f"   Merged: {len(merged):,} rows")
    
    if len(games) > 0:
        match_rate = (len(merged) / len(games)) * 100
        print(f"   Match rate: {match_rate:.1f}%")
    
except Exception as e:
    print(f"❌ Merge failed: {e}")
    exit()

print()

# ============================================
# CLEAN MERGED DATA
# ============================================

print("STEP 5: Cleaning Merged Dataset")
print("-" * 80)

# Remove temporary columns
merged = merged.drop(['Match_Title', 'Match_Name'], axis=1)
print("✅ Removed temporary columns")

# Remove duplicates
before = len(merged)
merged = merged.drop_duplicates()
after = len(merged)
print(f"✅ Removed {before - after:,} duplicates")

print()

# ============================================
# SAVE MERGED DATA
# ============================================

print("STEP 6: Saving Merged Dataset")
print("-" * 80)

output_file = os.path.join(cleaned_folder, 'merged_games_sales.csv')
merged.to_csv(output_file, index=False)

print(f"✅ Saved to: {output_file}")
print(f"   Size: {len(merged):,} rows × {len(merged.columns)} columns")
print()

# ============================================
# SHOW RESULTS
# ============================================

print("STEP 7: Merged Dataset Overview")
print("-" * 80)
print()

print("COLUMNS:")
for i, col in enumerate(merged.columns, 1):
    print(f"   {i:2}. {col}")
print()

if len(merged) > 0:
    print("FIRST 3 ROWS:")
    print(merged.head(3).to_string())
    print()
    
    # Quick stats
    if 'Global_Sales' in merged.columns:
        print("QUICK STATISTICS:")
        print(f"   Total Sales: ${merged['Global_Sales'].sum():,.2f}M")
        print(f"   Average Sales: ${merged['Global_Sales'].mean():,.2f}M")
        print()
        
        print("TOP 5 GAMES:")
        top5 = merged.nlargest(5, 'Global_Sales')
        for i, (idx, row) in enumerate(top5.iterrows(), 1):
            name = row.get(name_col_sales, row.get(title_col_games, 'Unknown'))
            sales = row['Global_Sales']
            print(f"   {i}. {name} - ${sales:.2f}M")

print()
print("="*80)
print("✅ MERGE COMPLETE!")
print("="*80)
