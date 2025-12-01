import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Check ORIGINAL games.csv
print("="*70)
print("ORIGINAL GAMES.CSV")
print("="*70)
games_raw = os.path.join(project_root, 'data', 'raw', 'games.csv')
try:
    df = pd.read_csv(games_raw, nrows=5)
    print("Columns:", list(df.columns))
    print("\nFirst row:")
    print(df.head(1).to_string())
except Exception as e:
    print(f"Error: {e}")

print("\n")

# Check ORIGINAL vgsales.csv
print("="*70)
print("ORIGINAL VGSALES.CSV")
print("="*70)
sales_raw = os.path.join(project_root, 'data', 'raw', 'vgsales.csv')
try:
    df = pd.read_csv(sales_raw, nrows=5)
    print("Columns:", list(df.columns))
    print("\nFirst row:")
    print(df.head(1).to_string())
except Exception as e:
    print(f"Error: {e}")
