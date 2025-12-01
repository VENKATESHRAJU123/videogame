# ============================================
# Load Data into SQL Server
# ============================================

import pandas as pd
import os
from sqlalchemy import create_engine, text
import urllib.parse

print("\n" + "="*70)
print("LOADING DATA INTO SQL SERVER")
print("="*70 + "\n")

# ============================================
# STEP 1: Database Connection
# ============================================

print("STEP 1: Connecting to SQL Server")
print("-" * 70)

# Connection parameters
server = 'localhost\\SQLEXPRESS'  # Change if your instance is different
database = 'VideoGameAnalysis'
driver = 'ODBC Driver 17 for SQL Server'

# Build connection string
params = urllib.parse.quote_plus(
    f'DRIVER={{{driver}}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

connection_string = f'mssql+pyodbc:///?odbc_connect={params}'

# Try to connect
try:
    engine = create_engine(connection_string)
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT @@VERSION"))
        version = result.fetchone()[0]
    print("✅ Connected to SQL Server successfully!")
    print(f"   Server: {server}")
    print(f"   Database: {database}")
    print()
except Exception as e:
    print(f"❌ Connection failed!")
    print(f"   Error: {e}")
    print()
    print("Troubleshooting:")
    print("  1. Check if SQL Server is running")
    print("  2. Verify server name (might be just 'localhost' or different instance)")
    print("  3. Make sure Windows Authentication is enabled")
    print()
    print("To find your server name:")
    print("  - Open SSMS")
    print("  - Look at the server name when you connect")
    print("  - Use that exact name in the 'server' variable above")
    exit()

# ============================================
# STEP 2: Load CSV Files
# ============================================

print("STEP 2: Loading Cleaned CSV Files")
print("-" * 70)

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
cleaned_folder = os.path.join(project_root, 'data', 'cleaned')

games_file = os.path.join(cleaned_folder, 'games_cleaned.csv')
sales_file = os.path.join(cleaned_folder, 'vgsales_cleaned.csv')
merged_file = os.path.join(cleaned_folder, 'merged_games_sales.csv')

# Load games
try:
    games = pd.read_csv(games_file)
    print(f"✅ Loaded games_cleaned.csv - {len(games)} rows")
except Exception as e:
    print(f"❌ Error loading games: {e}")
    exit()

# Load sales
try:
    sales = pd.read_csv(sales_file)
    print(f"✅ Loaded vgsales_cleaned.csv - {len(sales)} rows")
except Exception as e:
    print(f"❌ Error loading sales: {e}")
    exit()

# Load merged
try:
    merged = pd.read_csv(merged_file)
    print(f"✅ Loaded merged_games_sales.csv - {len(merged)} rows")
except Exception as e:
    print(f"❌ Error loading merged: {e}")
    exit()

print()

# ============================================
# STEP 3: Prepare Data for SQL
# ============================================

print("STEP 3: Preparing Data for SQL Import")
print("-" * 70)

# Prepare Games table data
games_columns = ['Title', 'Rating', 'Genres', 'Plays', 'Backlogs', 
                 'Wishlist', 'Release Date', 'Release_Year', 'Platform', 'Team']

# Select only columns that exist
games_cols_exist = [col for col in games_columns if col in games.columns]
games_sql = games[games_cols_exist].copy()

# Rename to match SQL table
rename_map = {
    'Release Date': 'ReleaseDate',
    'Release_Year': 'ReleaseYear',
    'Team': 'Developer'
}
games_sql = games_sql.rename(columns={k: v for k, v in rename_map.items() if k in games_sql.columns})

print(f"✅ Prepared Games table - {len(games_sql)} rows")

# Prepare Sales table data
sales_columns = ['Name', 'Platform', 'Year', 'Genre', 'Publisher',
                 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']

sales_cols_exist = [col for col in sales_columns if col in sales.columns]
sales_sql = sales[sales_cols_exist].copy()

# Rename to match SQL table
sales_rename = {
    'Name': 'GameName',
    'Year': 'ReleaseYear'
}
sales_sql = sales_sql.rename(columns={k: v for k, v in sales_rename.items() if k in sales_sql.columns})

print(f"✅ Prepared Sales table - {len(sales_sql)} rows")

# Prepare GameAnalysis table data
analysis_columns = ['Title', 'Rating', 'Genre', 'Platform', 'Developer', 
                    'Publisher', 'Year', 'Plays', 'Wishlist', 'Backlogs',
                    'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']

# Map column names from merged dataset
merged_rename = {
    'Game_Name': 'Title',
    'Year': 'ReleaseYear'
}
merged_renamed = merged.rename(columns={k: v for k, v in merged_rename.items() if k in merged.columns})

analysis_cols_exist = [col for col in analysis_columns if col in merged_renamed.columns]
merged_sql = merged_renamed[analysis_cols_exist].copy()

# Ensure ReleaseYear column exists
if 'ReleaseYear' in merged_sql.columns:
    pass
elif 'Year' in merged.columns:
    merged_sql['ReleaseYear'] = merged['Year']

print(f"✅ Prepared GameAnalysis table - {len(merged_sql)} rows")
print()

# ============================================
# STEP 4: Upload to SQL Server
# ============================================

print("STEP 4: Uploading Data to SQL Server")
print("-" * 70)
print("This may take 1-5 minutes depending on data size...")
print()

# Upload Games table
print("📤 Uploading to Games table...")
try:
    games_sql.to_sql('Games', engine, if_exists='append', index=False, method='multi', chunksize=500)
    print(f"✅ Uploaded {len(games_sql)} rows to Games table")
except Exception as e:
    print(f"❌ Error uploading Games: {e}")

print()

# Upload Sales table
print("📤 Uploading to Sales table...")
try:
    sales_sql.to_sql('Sales', engine, if_exists='append', index=False, method='multi', chunksize=500)
    print(f"✅ Uploaded {len(sales_sql)} rows to Sales table")
except Exception as e:
    print(f"❌ Error uploading Sales: {e}")

print()

# Upload GameAnalysis table
print("📤 Uploading to GameAnalysis table...")
try:
    merged_sql.to_sql('GameAnalysis', engine, if_exists='append', index=False, method='multi', chunksize=500)
    print(f"✅ Uploaded {len(merged_sql)} rows to GameAnalysis table")
except Exception as e:
    print(f"❌ Error uploading GameAnalysis: {e}")

print()

# ============================================
# STEP 5: Verify Upload
# ============================================

print("STEP 5: Verifying Data in SQL Server")
print("-" * 70)

verification_query = """
SELECT 'Games' AS TableName, COUNT(*) AS RowCount FROM Games
UNION ALL
SELECT 'Sales', COUNT(*) FROM Sales
UNION ALL
SELECT 'GameAnalysis', COUNT(*) FROM GameAnalysis;
"""

try:
    result = pd.read_sql(verification_query, engine)
    print("\n📊 ROW COUNTS IN SQL SERVER:")
    print(result.to_string(index=False))
    print()
except Exception as e:
    print(f"❌ Error verifying: {e}")

# ============================================
# STEP 6: Sample Data Check
# ============================================

print("\nSTEP 6: Checking Sample Data")
print("-" * 70)

# Check Games table
try:
    sample_games = pd.read_sql("SELECT TOP 3 * FROM Games", engine)
    print("\n📋 SAMPLE FROM GAMES TABLE:")
    print(sample_games)
    print()
except Exception as e:
    print(f"❌ Error reading Games: {e}")

# Check GameAnalysis table
try:
    sample_analysis = pd.read_sql(
        "SELECT TOP 5 Title, Genre, Platform, Global_Sales, Rating FROM GameAnalysis ORDER BY Global_Sales DESC",
        engine
    )
    print("\n🏆 TOP 5 GAMES BY SALES:")
    print(sample_analysis.to_string(index=False))
    print()
except Exception as e:
    print(f"❌ Error reading GameAnalysis: {e}")

# ============================================
# FINAL SUMMARY
# ============================================

print("="*70)
print("✅ DATA LOADING COMPLETE!")
print("="*70)
print()
print("WHAT WAS DONE:")
print("  ✅ Connected to SQL Server")
print("  ✅ Loaded 3 CSV files")
print("  ✅ Uploaded data to 3 SQL tables")
print("  ✅ Verified data in database")
print()
print("NEXT STEPS:")
print("  1. Open SQL Server Management Studio")
print("  2. Refresh the Tables folder")
print("  3. Right-click each table → Select Top 1000 Rows")
print("  4. Verify data looks correct")
print("  5. Move on to Power BI dashboard creation")
print()
print("="*70)
