# ============================================
# Test Script - Check if Everything Works
# ============================================

print("="*60)
print("TESTING PROJECT SETUP")
print("="*60)
print()

# Step 1: Test Python
print("Step 1: Testing Python...")
print("✅ Python is working!")
print()

# Step 2: Test pandas
print("Step 2: Testing pandas library...")
try:
    import pandas as pd
    print("✅ pandas is installed!")
    print(f"   Version: {pd.__version__}")
except ImportError:
    print("❌ pandas is NOT installed!")
    print("   Run this command in terminal: pip install pandas")
print()

# Step 3: Test file paths
print("Step 3: Testing file paths...")
import os

# Get current script location
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"📂 This script is at: {script_dir}")

# Get project root (one level up from scripts)
project_root = os.path.dirname(script_dir)
print(f"📂 Project root is at: {project_root}")

# Build path to data/raw folder
data_raw_folder = os.path.join(project_root, 'data', 'raw')
print(f"📂 Looking for CSV files at: {data_raw_folder}")
print()

# Step 4: Check if CSV files exist
print("Step 4: Checking for CSV files...")

games_file = os.path.join(data_raw_folder, 'games.csv')
vgsales_file = os.path.join(data_raw_folder, 'vgsales.csv')

print(f"Looking for: games.csv")
if os.path.exists(games_file):
    print(f"✅ FOUND: {games_file}")
    file_size = os.path.getsize(games_file) / 1024  # Size in KB
    print(f"   Size: {file_size:.2f} KB")
else:
    print(f"❌ NOT FOUND: {games_file}")
    print("   Please put games.csv in the data/raw folder")
print()

print(f"Looking for: vgsales.csv")
if os.path.exists(vgsales_file):
    print(f"✅ FOUND: {vgsales_file}")
    file_size = os.path.getsize(vgsales_file) / 1024  # Size in KB
    print(f"   Size: {file_size:.2f} KB")
else:
    print(f"❌ NOT FOUND: {vgsales_file}")
    print("   Please put vgsales.csv in the data/raw folder")
print()

# Step 5: Try to load the files
print("Step 5: Trying to load CSV files...")

if os.path.exists(games_file):
    try:
        import pandas as pd
        games = pd.read_csv(games_file)
        print(f"✅ Successfully loaded games.csv!")
        print(f"   Rows: {len(games)}")
        print(f"   Columns: {len(games.columns)}")
        print(f"   Column names: {list(games.columns)}")
    except Exception as e:
        print(f"❌ Error loading games.csv: {e}")
else:
    print("⏭️  Skipping games.csv (file not found)")
print()

if os.path.exists(vgsales_file):
    try:
        import pandas as pd
        sales = pd.read_csv(vgsales_file)
        print(f"✅ Successfully loaded vgsales.csv!")
        print(f"   Rows: {len(sales)}")
        print(f"   Columns: {len(sales.columns)}")
        print(f"   Column names: {list(sales.columns)}")
    except Exception as e:
        print(f"❌ Error loading vgsales.csv: {e}")
else:
    print("⏭️  Skipping vgsales.csv (file not found)")
print()

print("="*60)
print("TEST COMPLETE")
print("="*60)
print()

# Summary
print("SUMMARY:")
print("--------")
if os.path.exists(games_file) and os.path.exists(vgsales_file):
    print("✅ All checks passed! You're ready to start the project.")
else:
    print("⚠️  Some files are missing. Please:")
    print("   1. Download the CSV files")
    print("   2. Place them in: data/raw/")
    print("   3. Run this script again")
