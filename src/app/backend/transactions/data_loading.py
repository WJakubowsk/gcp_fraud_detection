import numpy as np
import pandas as pd
from django.contrib.auth.models import User
from tqdm.auto import tqdm
from .models import BitcoinTransaction
from django.db import transaction

import warnings

warnings.filterwarnings("ignore")

# BitcoinTransaction.objects.all().delete()

csv_file_path = "transactions/txs_features_engineered2.csv"
df = pd.read_csv(csv_file_path)

df.amount = df.amount.astype(np.float64, errors='ignore')

for i in range(1, 94):
    df[f"Local_feature_{i}"] = df[f"Local_feature_{i}"].astype(np.float64, errors='ignore')

for i in range(1, 73):
    df[f"Aggregate_feature_{i}"] = df[f"Aggregate_feature_{i}"].astype(np.float64, errors='ignore')

for col in ['txId', 'in_txs_degree', 'out_txs_degree', 'num_input_addresses', 'num_output_addresses']:
    df[col] = df[col].astype(np.int32, errors='ignore')
for col in ["total_BTC", "fees", "size", "in_BTC_min", "in_BTC_max", "in_BTC_mean", "in_BTC_median",
            "in_BTC_total", "out_BTC_min", "out_BTC_max", "out_BTC_mean", "out_BTC_median", "out_BTC_total"]:
    df[col] = df[col].astype(np.float64, errors='ignore')

df.rename(columns={'txId': 'tx_id'}, inplace=True)

user_dict = {user.id: user for user in User.objects.all()}

batch_size = 250
num_rows = len(df)
num_batches = (num_rows + batch_size - 1) // batch_size

for batch_num in tqdm(range(num_batches)):
    start_index = batch_num * batch_size
    end_index = min((batch_num + 1) * batch_size, num_rows)

    transactions = []

    for index in range(start_index, end_index):
        row = df.iloc[index]
        user_id = row.pop('User')
        date = row.pop('Time step')

        row_transaction = BitcoinTransaction(
            user=user_dict.get(user_id),
            date=date,
            **row,
        )
        transactions.append(row_transaction)

    with transaction.atomic():
        BitcoinTransaction.objects.bulk_create(transactions)

print("CSV data has been loaded into the Django database.")
