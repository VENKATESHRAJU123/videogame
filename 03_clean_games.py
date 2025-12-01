# ============================================
# CLEAN GAMES DATASET - COMPLETE VERSION
# ============================================

import pandas as pd
import numpy as np
import os

print("\n" + "="*80)
print("CLEANING GAMES DATASET")
print("="*80 + "\n")

# ============================================
# STEP 1: Load Data
# ============================================

print("STEP 1: Loading Data")
print("-" * 80)

# Get file paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
raw_folder = os.path.join(project_root, 'data', 'raw')
cleaned_folder = os.path.join(project_root, 'data', 'cleaned')

# Create cleaned folder if it doesn't exist
os.makedirs(cleaned_folder, exist_ok=True)

# Build path to games.csv
games_file = os.path.join(raw_folder, 'games.csv')

print(f"Looking for: {games_file}")

# Check if file exists
if not os.path.exists(games_file):
    print(f"❌ ERROR: File not found!")
    print(f"   Please make sure games.csv is in: {raw_folder}")
    exit()

# Load the file
try:
    games = pd.read_csv(games_file)
    print(f"✅ Loaded games.csv successfully")
    print(f"   Rows: {len(games):,}")
    print(f"   Columns: {len(games.columns)}")
    print(f"   Column names: {list(games.columns)}")
except Exception as e:
    print(f"❌ ERROR loading file: {e}")
    exit()

print()

# Save original row count
original_rows = len(games)

# ============================================
# STEP 2: Remove Duplicates
# ============================================

print("STEP 2: Removing Duplicates")
print("-" * 80)

# Find the title column
title_col = None
for col in ['Title', 'title', 'Name', 'name', 'Game']:
    if col in games.columns:
        title_col = col
        print(f"Found title column: '{col}'")
        break

if title_col:
    # Count duplicates
    duplicates_before = games.duplicated(subset=[title_col]).sum()
    print(f"Found {duplicates_before:,} duplicate rows")
    
    # Remove duplicates
    games = games.drop_duplicates(subset=[title_col], keep='first')
    
    print(f"✅ Removed {duplicates_before:,} duplicates")
    print(f"   Remaining rows: {len(games):,}")
else:
    print("⚠️  No title column found, skipping duplicate removal")

print()

# ============================================
# STEP 3: Convert K/M Values to Numbers
# ============================================

print("STEP 3: Converting K/M Values to Numbers")
print("-" * 80)

def convert_k_m_to_number(val):
    """
    Convert values like:
    - '17K' to 17000
    - '5.6K' to 5600
    - '2.3M' to 2300000
    """
    # Handle missing values
    if pd.isna(val):
        return 0
    
    # Already a number
    if isinstance(val, (int, float)):
        return int(val)
    
    # Convert to string and clean
    val_str = str(val).strip().upper()
    
    # Remove any commas
    val_str = val_str.replace(',', '')
    
    # Handle 'K' (thousands)
    if 'K' in val_str:
        try:
            number = float(val_str.replace('K', '').strip())
            return int(number * 1000)
        except:
            return 0
    
    # Handle 'M' (millions)
    if 'M' in val_str:
        try:
            number = float(val_str.replace('M', '').strip())
            return int(number * 1000000)
        except:
            return 0
    
    # Try direct conversion
    try:
        return int(float(val_str))
    except:
        return 0

# Find columns that might have K/M values
possible_count_cols = ['Plays', 'plays', 'Backlogs', 'backlogs', 
                       'Wishlist', 'wishlist', 'Backlog', 'backlog']

converted_cols = []

for col in games.columns:
    # Check if this is a count column
    if any(keyword in col for keyword in possible_count_cols):
        print(f"Processing column: '{col}'")
        
        # Show sample BEFORE conversion
        sample_before = games[col].head(5).tolist()
        print(f"   Sample before: {sample_before}")
        
        # Apply conversion
        games[col] = games[col].apply(convert_k_m_to_number)
        
        # Show sample AFTER conversion
        sample_after = games[col].head(5).tolist()
        print(f"   Sample after:  {sample_after}")
        
        print(f"   ✅ Converted '{col}' to numbers")
        print()
        
        converted_cols.append(col)

if converted_cols:
    print(f"✅ Converted {len(converted_cols)} columns from K/M notation")
else:
    print("ℹ️  No K/M columns found to convert")

print()

# ============================================
# STEP 4: Handle Missing Values
# ============================================

print("STEP 4: Handling Missing Values")
print("-" * 80)

print("Missing values count:")
missing_before = games.isnull().sum()
for col, count in missing_before[missing_before > 0].items():
    percent = (count / len(games)) * 100
    print(f"   {col:25} {count:6,} ({percent:.1f}%)")

if missing_before.sum() == 0:
    print("   ✅ No missing values found!")

print()

# Handle Rating column
rating_cols = [col for col in games.columns if 'rating' in col.lower()]

for col in rating_cols:
    print(f"Processing '{col}'...")
    
    # Convert to numeric (non-numeric become NaN)
    games[col] = pd.to_numeric(games[col], errors='coerce')
    
    # Get median
    median_val = games[col].median()
    
    # Fill missing values
    games[col].fillna(median_val, inplace=True)
    
    print(f"   ✅ Filled missing values with median: {median_val:.2f}")

# Fill other numeric columns with 0
for col in games.select_dtypes(include=[np.number]).columns:
    if col not in rating_cols:
        games[col].fillna(0, inplace=True)

print()

# ============================================
# STEP 5: Clean Text Columns
# ============================================

print("STEP 5: Cleaning Text Columns")
print("-" * 80)

text_cols = games.select_dtypes(include=['object']).columns

for col in text_cols:
    # Skip date columns
    if 'date' in col.lower():
        continue
    
    # Convert to string and strip spaces
    games[col] = games[col].astype(str).str.strip()
    
    # Replace 'nan' with empty string
    games[col] = games[col].replace('nan', '')
    
    # Standardize based on column type
    if 'title' in col.lower() or 'name' in col.lower():
        games[col] = games[col].str.title()
        print(f"✅ '{col}' → Title Case")
    elif 'platform' in col.lower() or 'console' in col.lower():
        games[col] = games[col].str.upper()
        print(f"✅ '{col}' → UPPERCASE")
    else:
        games[col] = games[col].str.title()
        print(f"✅ '{col}' → Cleaned")

print()

# ============================================
# STEP 6: Handle Date Columns
# ============================================

print("STEP 6: Processing Date Columns")
print("-" * 80)

date_cols = [col for col in games.columns if 'date' in col.lower()]

for col in date_cols:
    print(f"Processing '{col}'...")
    
    try:
        # Convert to datetime
        games[col] = pd.to_datetime(games[col], errors='coerce')
        print(f"   ✅ Converted to datetime")
        
        # Create year column
        year_col_name = col.replace('Date', 'Year').replace('date', 'Year')
        games[year_col_name] = games[col].dt.year
        print(f"   ✅ Created '{year_col_name}' column")
        
        # Fill missing years with mode (most common year)
        if games[year_col_name].isnull().sum() > 0:
            if len(games[year_col_name].mode()) > 0:
                mode_year = games[year_col_name].mode()[0]
                games[year_col_name].fillna(mode_year, inplace=True)
                print(f"   ✅ Filled missing years with mode: {int(mode_year)}")
            else:
                # If no mode, use 2020
                games[year_col_name].fillna(2020, inplace=True)
                print(f"   ✅ Filled missing years with 2020")
        
    except Exception as e:
        print(f"   ⚠️  Error: {e}")

print()

# ============================================
# STEP 7: Final Data Type Validation
# ============================================

print("STEP 7: Final Data Type Validation")
print("-" * 80)

# Ensure numeric columns are proper integers
for col in games.select_dtypes(include=[np.number]).columns:
    # Fill any remaining NaN with 0
    games[col].fillna(0, inplace=True)
    
    # Convert count columns to integers
    if any(keyword in col.lower() for keyword in ['plays', 'backlog', 'wishlist', 'year']):
        games[col] = games[col].astype(int)
        print(f"✅ '{col}' → Integer type")

print()

# ============================================
# STEP 8: Save Cleaned Data
# ============================================

print("STEP 8: Saving Cleaned Data")
print("-" * 80)

output_file = os.path.join(cleaned_folder, 'games_cleaned.csv')
games.to_csv(output_file, index=False)

print(f"✅ Saved to: {output_file}")
print(f"   Size: {len(games):,} rows × {len(games.columns)} columns")
print()

# ============================================
# SUMMARY
# ============================================

print("="*80)
print("CLEANING SUMMARY")
print("="*80)
print()

print(f"Original rows: {original_rows:,}")
print(f"Final rows: {len(games):,}")
print(f"Rows removed: {original_rows - len(games):,}")
print(f"Total columns: {len(games.columns)}")
print()

print("COLUMN DATA TYPES:")
for col in games.columns:
    dtype = games[col].dtype
    print(f"   {col:30} {dtype}")
print()

print("FIRST 3 ROWS OF CLEANED DATA:")
print(games.head(3).to_string())
print()

print("SAMPLE STATISTICS:")
print(games.describe().to_string())
print()

print("="*80)
print("✅ GAMES DATASET CLEANING COMPLETE!")
print("="*80)
