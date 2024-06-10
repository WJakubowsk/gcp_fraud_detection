import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from torch_geometric.data import Data


def load_data(
    DATA_PATH: str = "C:/studia/sem_8/Cloud/gcp_fraud_detection/data/",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Loads three datasets: features, edgelist and classes.
    """
    df_features = pd.read_csv(DATA_PATH + "txs_features.csv")
    df_edges = pd.read_csv(DATA_PATH + "txs_edgelist.csv")
    df_classes = pd.read_csv(DATA_PATH + "txs_classes.csv")
    return df_features, df_edges, df_classes


def map_feature_data(
    df_features: pd.DataFrame,
    year: int = 2023,
) -> pd.DataFrame:
    """
    Cleanses the feature data by generating users and mapping time steps to dates.
    """
    np.random.seed(0)
    # generate users for transactions
    df_features["User"] = np.random.randint(0, 1000, df_features.shape[0])
    # map time step to date
    df_features["Time step"] = pd.to_datetime(
        df_features["Time step"].astype(str) + "-" + str(year) + "-1",
        format="%W-%Y-%w",
    )
    # apply generating random day for each transaction
    df_features["Time step"] = df_features["Time step"] + pd.to_timedelta(
        np.random.randint(0, 7, df_features.shape[0]), unit="D"
    )
    # add amount information to the transactions
    df_features["Amount"] = np.round(
        np.random.uniform(1, 10000, df_features.shape[0]), 2
    )

    return df_features


def preprocess_data(
    df_features: pd.DataFrame, df_edges: pd.DataFrame, df_classes: pd.DataFrame
) -> tuple[Data, pd.Index, pd.Index]:
    """
    Applies preprocessing steps to the data.
    Returns a PyTorch Geometric Data object with the indexes for the classified
    and unclassified nodes.
    """
    df_features = map_feature_data(df_features)

    df_classes["class"] = df_classes["class"].map({3: -1, 1: 1, 2: 0})
    df = (
        df_features.merge(df_classes, how="left", on="txId")
        .sort_values("txId")
        .reset_index(drop=True)
    )

    nodes = df["txId"].values
    map_id = {j: i for i, j in enumerate(nodes)}
    edges = df_edges.copy()
    edges.txId1 = edges.txId1.map(map_id)
    edges.txId2 = edges.txId2.map(map_id)
    edges = edges.astype(int)
    edge_index = np.array(edges.values).T
    edge_index = torch.tensor(edge_index, dtype=torch.int32).contiguous()
    weights = torch.tensor([1] * edge_index.shape[1], dtype=torch.float32)
    labels = df["class"].values
    node_features = df.drop(["txId"], axis=1).copy()

    classified_idx = node_features["class"].loc[node_features["class"] != -1].index
    unclassified_idx = node_features["class"].loc[node_features["class"] == -1].index
    classified_illicit_idx = (
        node_features["class"].loc[node_features["class"] == 1].index
    )
    classified_licit_idx = node_features["class"].loc[node_features["class"] == 0].index

    node_features = node_features.drop(columns=["User", "Time step", "class", "Amount"])
    node_features = node_features.fillna(node_features.mean())

    node_features_t = torch.tensor(
        np.array(node_features.values, dtype=np.float32), dtype=torch.float32
    )

    train_idx, valid_idx = train_test_split(classified_idx.values, test_size=0.15)

    data_train = Data(
        x=node_features_t,
        edge_index=edge_index,
        edge_attr=weights,
        y=torch.tensor(labels, dtype=torch.float32),
    )
    data_train.train_idx = train_idx
    data_train.valid_idx = valid_idx
    data_train.test_idx = unclassified_idx

    return data_train, classified_licit_idx, classified_illicit_idx
