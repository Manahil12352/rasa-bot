import pandas as pd
import yaml

# Load the dataset
df = pd.read_parquet("massive_ur_train.parquet")

# Get unique intents with their numbers
print("All intents found:")
print(df[['intent', 'scenario']].drop_duplicates().sort_values('intent').to_string())
