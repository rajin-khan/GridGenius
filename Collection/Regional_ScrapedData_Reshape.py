import pandas as pd

df = pd.read_csv('bpdb_area_demand_full.csv')

# Optionally, rename columns for easier use
df.columns = [c.strip() for c in df.columns]  # remove spaces

# Pivot for Demand
demand_wide = df.pivot(index='Date', columns='Zone', values='Demand (MW)')
demand_wide = demand_wide.add_suffix('_Demand')

# Pivot for Load Shed
load_wide = df.pivot(index='Date', columns='Zone', values='Load Shed (MW)')
load_wide = load_wide.add_suffix('_LoadShed')

# Combine
result = pd.concat([demand_wide, load_wide], axis=1).reset_index()

# Sort columns 
cols = ['Date'] + sorted([c for c in result.columns if c != 'Date'])
result = result[cols]

# Save as new CSV 
result.to_csv('Regional_Demand_Load_Iter1.csv', index=False)

print("Saved!")
