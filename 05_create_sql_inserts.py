# ============================================
# CREATE SQL INSERT SCRIPTS
# ============================================

import pandas as pd
import os

print("\n" + "="*80)
print("CREATING SQL INSERT SCRIPTS")
print("="*80 + "\n")

# ============================================
# LOAD DATA
# ============================================

print("STEP 1: Loading CSV Files")
print("-" * 80)

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
cleaned_folder = os.path.join(project_root, 'data', 'cleaned')
sql_folder = os.path.join(project_root, 'sql')

os.makedirs(sql_folder, exist_ok=True)

# Load games
games_file = os.path.join(cleaned_folder, 'games_cleaned.csv')
try:
    games = pd.read_csv(games_file)
    print(f"✅ Loaded games_cleaned.csv - {len(games):,} rows")
except Exception as e:
    print(f"❌ Error: {e}")
    exit()

# Load sales
sales_file = os.path.join(cleaned_folder, 'vgsales_cleaned.csv')
try:
    sales = pd.read_csv(sales_file)
    print(f"✅ Loaded vgsales_cleaned.csv - {len(sales):,} rows")
except Exception as e:
    print(f"❌ Error: {e}")
    exit()

# Load merged
merged_file = os.path.join(cleaned_folder, 'merged_games_sales.csv')
try:
    merged = pd.read_csv(merged_file)
    print(f"✅ Loaded merged_games_sales.csv - {len(merged):,} rows")
except Exception as e:
    print(f"❌ Error: {e}")
    exit()

print()

# ============================================
# FUNCTION TO CREATE INSERT STATEMENTS
# ============================================

def clean_value(val):
    """Clean a value for SQL insertion"""
    if pd.isna(val):
        return 'NULL'
    elif isinstance(val, str):
        # Escape single quotes
        val_clean = val.replace("'", "''")
        return f"N'{val_clean}'"
    elif isinstance(val, (int, float)):
        return str(val)
    else:
        return f"N'{str(val)}'"

def create_insert_script(df, table_name, column_map, output_file, max_rows=1000):
    """
    Create SQL INSERT script
    df: DataFrame to export
    table_name: SQL table name
    column_map: dict mapping DataFrame columns to SQL columns
    output_file: where to save SQL script
    max_rows: limit number of rows (for testing)
    """
    
    # Limit rows if dataset is large
    if len(df) > max_rows:
        print(f"   ⚠️  Limiting to first {max_rows:,} rows (dataset has {len(df):,})")
        df = df.head(max_rows)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write(f"USE VideoGameAnalysis;\n")
        f.write(f"GO\n\n")
        f.write(f"PRINT 'Loading {table_name}...';\n")
        f.write(f"PRINT '';\n\n")
        
        # Get columns
        sql_cols = list(column_map.values())
        df_cols = list(column_map.keys())
        
        # Filter to only existing columns
        existing_cols = [col for col in df_cols if col in df.columns]
        sql_cols_filtered = [column_map[col] for col in existing_cols]
        
        # Create inserts in batches
        batch_size = 100
        total = len(df)
        
        for i in range(0, total, batch_size):
            batch = df.iloc[i:i+batch_size]
            
            for idx, row in batch.iterrows():
                # Build values
                values = [clean_value(row.get(col)) for col in existing_cols]
                
                # Create INSERT
                cols_str = ', '.join(sql_cols_filtered)
                vals_str = ', '.join(values)
                
                f.write(f"INSERT INTO {table_name} ({cols_str})\n")
                f.write(f"VALUES ({vals_str});\n\n")
            
            # Add GO every 100 rows
            f.write("GO\n\n")
            
            # Progress
            if (i + batch_size) % 500 == 0:
                f.write(f"PRINT '{i + batch_size:,} rows inserted...';\n\n")
        
        # Footer
        f.write(f"PRINT 'Completed: {len(df):,} rows inserted into {table_name}';\n")
        f.write(f"GO\n")

# ============================================
# CREATE GAMES INSERT SCRIPT
# ============================================

print("STEP 2: Creating Games Insert Script")
print("-" * 80)

# Map DataFrame columns to SQL columns
games_map = {}

# Try to find and map each column
if 'Title' in games.columns:
    games_map['Title'] = 'Title'
elif 'title' in games.columns:
    games_map['title'] = 'Title'

if 'Rating' in games.columns:
    games_map['Rating'] = 'Rating'

if 'Genres' in games.columns:
    games_map['Genres'] = 'Genres'
elif 'Genre' in games.columns:
    games_map['Genre'] = 'Genres'

if 'Plays' in games.columns:
    games_map['Plays'] = 'Plays'

if 'Backlogs' in games.columns:
    games_map['Backlogs'] = 'Backlogs'

if 'Wishlist' in games.columns:
    games_map['Wishlist'] = 'Wishlist'

if 'ReleaseYear' in games.columns:
    games_map['ReleaseYear'] = 'ReleaseYear'
elif 'Release_Year' in games.columns:
    games_map['Release_Year'] = 'ReleaseYear'

if 'Platform' in games.columns:
    games_map['Platform'] = 'Platform'

if 'Developer' in games.columns:
    games_map['Developer'] = 'Developer'
elif 'Team' in games.columns:
    games_map['Team'] = 'Developer'

games_script = os.path.join(sql_folder, '02_insert_games.sql')
create_insert_script(games, 'Games', games_map, games_script, max_rows=1000)

print(f"✅ Created: {games_script}")
print()

# ============================================
# CREATE SALES INSERT SCRIPT
# ============================================

print("STEP 3: Creating Sales Insert Script")
print("-" * 80)

sales_map = {}

if 'Name' in sales.columns:
    sales_map['Name'] = 'GameName'

if 'Platform' in sales.columns:
    sales_map['Platform'] = 'Platform'

if 'Year' in sales.columns:
    sales_map['Year'] = 'ReleaseYear'

if 'Genre' in sales.columns:
    sales_map['Genre'] = 'Genre'

if 'Publisher' in sales.columns:
    sales_map['Publisher'] = 'Publisher'

if 'NA_Sales' in sales.columns:
    sales_map['NA_Sales'] = 'NA_Sales'

if 'EU_Sales' in sales.columns:
    sales_map['EU_Sales'] = 'EU_Sales'

if 'JP_Sales' in sales.columns:
    sales_map['JP_Sales'] = 'JP_Sales'

if 'Other_Sales' in sales.columns:
    sales_map['Other_Sales'] = 'Other_Sales'

if 'Global_Sales' in sales.columns:
    sales_map['Global_Sales'] = 'Global_Sales'

sales_script = os.path.join(sql_folder, '03_insert_sales.sql')
create_insert_script(sales, 'Sales', sales_map, sales_script, max_rows=1000)

print(f"✅ Created: {sales_script}")
print()

# ============================================
# CREATE GAMEANALYSIS INSERT SCRIPT
# ============================================

print("STEP 4: Creating GameAnalysis Insert Script")
print("-" * 80)

analysis_map = {}

# Find title
for col in ['Title', 'title', 'Game_Name', 'Name']:
    if col in merged.columns:
        analysis_map[col] = 'Title'
        break

# Other columns
if 'Rating' in merged.columns:
    analysis_map['Rating'] = 'Rating'

if 'Genre' in merged.columns:
    analysis_map['Genre'] = 'Genre'

if 'Platform' in merged.columns:
    analysis_map['Platform'] = 'Platform'

if 'Developer' in merged.columns:
    analysis_map['Developer'] = 'Developer'

if 'Publisher' in merged.columns:
    analysis_map['Publisher'] = 'Publisher'

if 'Year' in merged.columns:
    analysis_map['Year'] = 'ReleaseYear'
elif 'ReleaseYear' in merged.columns:
    analysis_map['ReleaseYear'] = 'ReleaseYear'

if 'Plays' in merged.columns:
    analysis_map['Plays'] = 'Plays'

if 'Wishlist' in merged.columns:
    analysis_map['Wishlist'] = 'Wishlist'

if 'Backlogs' in merged.columns:
    analysis_map['Backlogs'] = 'Backlogs'

if 'NA_Sales' in merged.columns:
    analysis_map['NA_Sales'] = 'NA_Sales'

if 'EU_Sales' in merged.columns:
    analysis_map['EU_Sales'] = 'EU_Sales'

if 'JP_Sales' in merged.columns:
    analysis_map['JP_Sales'] = 'JP_Sales'

if 'Other_Sales' in merged.columns:
    analysis_map['Other_Sales'] = 'Other_Sales'

if 'Global_Sales' in merged.columns:
    analysis_map['Global_Sales'] = 'Global_Sales'

merged_script = os.path.join(sql_folder, '04_insert_gameanalysis.sql')
create_insert_script(merged, 'GameAnalysis', analysis_map, merged_script, max_rows=1000)

print(f"✅ Created: {merged_script}")
print()

# ============================================
# INSTRUCTIONS
# ============================================

print("="*80)
print("✅ SQL INSERT SCRIPTS CREATED!")
print("="*80)
print()
print("FILES CREATED:")
print(f"   1. {games_script}")
print(f"   2. {sales_script}")
print(f"   3. {merged_script}")
print()
print("NEXT STEPS:")
print("   1. Open SQL Server Management Studio")
print("   2. Connect to your server")
print("   3. Make sure 'VideoGameAnalysis' database is selected")
print("   4. Open and execute each SQL file in order:")
print("      a) File → Open → File → select 02_insert_games.sql → Execute")
print("      b) File → Open → File → select 03_insert_sales.sql → Execute")
print("      c) File → Open → File → select 04_insert_gameanalysis.sql → Execute")
print()
print("   Each script will take 30 seconds - 2 minutes to run")
print()
print("NOTE: Scripts are limited to 1,000 rows for faster testing.")
print("      To load all data, change max_rows parameter to higher number.")
print()
print("="*80)
