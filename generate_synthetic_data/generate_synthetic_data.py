

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Load the original data (first 1000 rows)
real_data = pd.read_csv("dataset.csv").head(1000)

# 2. Ensure columns are numeric where needed
numeric_columns = ["task_size", "cpu_demand", "memory_demand", "disk_usage", "io_operations"]
for col in numeric_columns:
    real_data[col] = pd.to_numeric(real_data[col], errors="coerce")

# Drop rows with missing required values
real_data_cleaned = real_data.dropna(subset=["task_size", "cpu_demand", "memory_demand", "disk_usage", "io_operations"])

# 3. Compute lambda for Poisson safely
lam_value = real_data_cleaned["io_operations"].mean()
if np.isnan(lam_value) or lam_value < 0:
    lam_value = 5  # fallback/default

# 4. Generate 1000 synthetic records
np.random.seed(42)
synthetic_data = pd.DataFrame({
    "task_size": np.random.normal(loc=real_data_cleaned["task_size"].mean(), scale=real_data_cleaned["task_size"].std(), size=1000),
    "cpu_demand": np.random.normal(loc=real_data_cleaned["cpu_demand"].mean(), scale=real_data_cleaned["cpu_demand"].std(), size=1000),
    "memory_demand": np.random.normal(loc=real_data_cleaned["memory_demand"].mean(), scale=real_data_cleaned["memory_demand"].std(), size=1000),
    "network_latency": np.random.randint(low=5, high=200, size=1000),
    "io_operations": np.random.poisson(lam=lam_value, size=1000),
    "disk_usage": np.random.normal(loc=real_data_cleaned["disk_usage"].mean(), scale=real_data_cleaned["disk_usage"].std(), size=1000),
    "num_connections": np.random.randint(low=1, high=20, size=1000),
    "priority_level": np.random.choice([0, 1], size=1000, p=[0.7, 0.3]),
    "target": np.random.choice(real_data["target"].dropna().unique(), size=1000),
    "timestamp": [datetime.now() - timedelta(minutes=np.random.randint(0, 10000)) for _ in range(1000)]
})

# 5. Clean up negative values
for col in ["task_size", "cpu_demand", "memory_demand", "disk_usage"]:
    synthetic_data[col] = synthetic_data[col].clip(lower=0)

# 6. Combine real + synthetic
combined_data = pd.concat([real_data, synthetic_data], ignore_index=True)

# 7. Save to CSV
combined_data.to_csv("dataset2.csv", index=False)
print("✅ Dataset saved as combined_dataset.csv with", len(combined_data), "rows.")



