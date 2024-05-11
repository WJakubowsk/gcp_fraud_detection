import numpy as np
import pandas as pd
import torch
from torch_geometric.data import Data
from sklearn.model_selection import train_test_split


def load_data(
    DATA_PATH: str = "C:/studia/sem_8/Cloud/gcp_fraud_detection/data/",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ "
    Loads three datasets: features, edgelist and classes.
    """
    df_features = pd.read_csv(DATA_PATH + "txs_features.csv")
    df_edges = pd.read_csv(DATA_PATH + "txs_edgelist.csv")
    df_classes = pd.read_csv(DATA_PATH + "txs_classes.csv")
    return df_features, df_edges, df_classes


def preprocess_data(
    df_features: pd.DataFrame, df_edges: pd.DataFrame, df_classes: pd.DataFrame
) -> Data:
    """
    Applies preprocessing steps to the data.
    Returns a PyTorch Geometric Data object with the indexes for the classified
    and unclassified nodes.
    """
    df_classes["class"] = df_classes["class"].map({3: -1, 1: 1, 2: 0})
    df = (
        df_features.merge(df_classes, how="left", on="txId")
        .sort_values("txId")
        .reset_index(drop=True)
    )

    nodes = df[0].values
    map_id = {j: i for i, j in enumerate(nodes)}
    edges = df_edges.copy()
    edges.txId1 = edges.txId1.map(map_id)
    edges.txId2 = edges.txId2.map(map_id)
    edges = edges.astype(int)
    edge_index = np.array(edges.values).T
    edge_index = torch.tensor(edge_index, dtype=torch.long).contiguous()
    weights = torch.tensor([1] * edge_index.shape[1], dtype=torch.double)
    labels = df["class"].values
    node_features = df.drop(["txId"], axis=1).copy()

    classified_idx = node_features["class"].loc[node_features["class"] != -1].index
    unclassified_idx = node_features["class"].loc[node_features["class"] == -1].index
    classified_illicit_idx = (
        node_features["class"].loc[node_features["class"] == 1].index
    )
    classified_licit_idx = node_features["class"].loc[node_features["class"] == 0].index

    node_features = node_features.drop(columns=["Time step", "class"])
    node_features_t = torch.tensor(
        np.array(node_features.values, dtype=np.double), dtype=torch.double
    )

    train_idx, valid_idx = train_test_split(classified_idx.values, test_size=0.2)

    data_train = Data(
        x=node_features_t,
        edge_index=edge_index,
        edge_attr=weights,
        y=torch.tensor(labels, dtype=torch.double),
    )
    data_train.train_idx = train_idx
    data_train.valid_idx = valid_idx
    data_train.test_idx = unclassified_idx

    return data_train, classified_licit_idx, classified_illicit_idx
