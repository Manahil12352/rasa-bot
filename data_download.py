import pandas as pd

url = "https://huggingface.co/datasets/AmazonScience/massive/resolve/f4917eeb708a6306fd8982a60b1bf36373830a0c/ur-PK/massive-train.parquet"

print("Downloading...")
df = pd.read_parquet(url)
print("Success! Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df[['utt', 'intent']].head(5))
