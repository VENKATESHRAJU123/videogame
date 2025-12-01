# ============================================
# Data Exploration Script
# ============================================

import pandas as pd
import os

print("\n" + "="*70)
print("VIDEO GAME DATA EXPLORATION")
print("="*70 + "\n")

# ============================================
# STEP 1: Load the Data
# ============================================

print("STEP 1: Loading CSV Files...")
print("-" * 70)

# Build file paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_folder = os.path.join(project_root, 'data', 'raw')

games_file = os.path.join(data_folder, 'games.csv')
sales_file = os.path.join(data_folder, 'vgsales.csv')

# Load games data
try:
    games = pd.read_csv(games_file)
    print(f"✅ Loaded games.csv - {len(games)} rows")
except Exception as e:
    print(f"❌ Error loading games.csv: {e}")
    exit()

# Load sales data
try:
    sales = pd.read_csv(sales_file)
    print(f"✅ Loaded vgsales.csv - {len(sales)} rows")
except Exception as e:
    print(f"❌ Error loading vgsales.csv: {e}")
    exit()

print()

# ============================================
# STEP 2: Examine Games Dataset
# ============================================

print("STEP 2: GAMES DATASET OVERVIEW")
print("-" * 70)
print()

print("📊 BASIC INFO:")
print(f"   Total rows: {len(games)}")
print(f"   Total columns: {len(games.columns)}")
print()

print("📋 COLUMN NAMES:")
for i, col in enumerate(games.columns, 1):
    print(f"   {i}. {col}")
print()

print("🔤 DATA TYPES:")
print(games.dtypes)
print()

print("👀 FIRST 5 ROWS:")
print(games.head())
print()

print("📈 STATISTICAL SUMMARY (Numbers only):")
print(games.describe())
print()

print("❓ MISSING VALUES:")
missing = games.isnull().sum()
print(missing[missing > 0])  # Only show columns with missing values
if missing.sum() == 0:
    print("   ✅ No missing values!")
print()

# ============================================
# STEP 3: Examine Sales Dataset
# ============================================

print("\n" + "="*70)
print("STEP 3: SALES DATASET OVERVIEW")
print("-" * 70)
print()

print("📊 BASIC INFO:")
print(f"   Total rows: {len(sales)}")
print(f"   Total columns: {len(sales.columns)}")
print()

print("📋 COLUMN NAMES:")
for i, col in enumerate(sales.columns, 1):
    print(f"   {i}. {col}")
print()

print("🔤 DATA TYPES:")
print(sales.dtypes)
print()

print("👀 FIRST 5 ROWS:")
print(sales.head())
print()

print("📈 STATISTICAL SUMMARY:")
print(sales.describe())
print()

print("❓ MISSING VALUES:")
missing = sales.isnull().sum()
print(missing[missing > 0])
if missing.sum() == 0:
    print("   ✅ No missing values!")
print()

# ============================================
# STEP 4: Quick Analysis
# ============================================

print("\n" + "="*70)
print("STEP 4: QUICK INSIGHTS")
print("-" * 70)
print()

# For games dataset
if 'Rating' in games.columns:
    print("🎮 GAMES - RATINGS:")
    print(f"   Average rating: {games['Rating'].mean():.2f}")
    print(f"   Highest rating: {games['Rating'].max():.2f}")
    print(f"   Lowest rating: {games['Rating'].min():.2f}")
    print()

if 'Platform' in games.columns:
    print("🎮 GAMES - PLATFORMS:")
    print(f"   Unique platforms: {games['Platform'].nunique()}")
    print("   Top 5 platforms:")
    print(games['Platform'].value_counts().head())
    print()

# For sales dataset
if 'Global_Sales' in sales.columns:
    print("💰 SALES - GLOBAL SALES:")
    print(f"   Total global sales: ${sales['Global_Sales'].sum():.2f} million")
    print(f"   Average per game: ${sales['Global_Sales'].mean():.2f} million")
    print()

if 'Genre' in sales.columns:
    print("💰 SALES - TOP 5 GENRES:")
    print(sales['Genre'].value_counts().head())
    print()

if 'Platform' in sales.columns:
    print("💰 SALES - TOP 5 PLATFORMS:")
    print(sales['Platform'].value_counts().head())
    print()

# Top selling games
if 'Name' in sales.columns and 'Global_Sales' in sales.columns:
    print("🏆 TOP 10 BEST-SELLING GAMES:")
    top_games = sales.nlargest(10, 'Global_Sales')[['Name', 'Platform', 'Year', 'Global_Sales']]
    for idx, row in top_games.iterrows():
        print(f"   {row['Name']} ({row['Platform']}, {row['Year']}) - ${row['Global_Sales']}M")
    print()

print("="*70)
print("✅ EXPLORATION COMPLETE!")
print("="*70)
