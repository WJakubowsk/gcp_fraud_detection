import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, f1_score
from torch_geometric.data import Data


def calculate_metrics(
    pred_scores: np.array, target_labels: np.array, threshold: float = 0.5
):
    """
    Calculates metrics for a given set of predictions and target labels.
    """
    metrics = {}
    metrics["accuracy"] = accuracy_score(target_labels, pred_scores > threshold)
    metrics["f1"] = f1_score(target_labels, pred_scores > threshold, average="micro")
    return metrics


def get_best_metric(output: dict, metric: str, mode: str = "val"):
    """
    Returns the best results for a given metric and mode.
    Args:
        output (dict): Dictionary containing the metrics, returned by calculate_metrics() func.
        metric (str): Metric to consider.
        mode (str): Mode to consider (train, val).
    """
    best_results = {}
    i = np.array(output[mode][metric]).argmax()
    for m in output[mode].keys():
        best_results[m] = output[mode][m][i]
    return best_results


def save_metrics(metrics: dict, save_name: str, path: str = "./results/"):
    """
    Saves the metrics dictionary to a CSV file. Appends if the file already exists.
    """
    # create dir if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)
    df = pd.DataFrame(metrics, columns=metrics.keys(), index=[0])
    if os.path.exists(path + save_name):
        df.to_csv(path + save_name, mode="a", header=False, index=False)
    else:
        df.to_csv(path + save_name, index=False)


def save_model(model, save_name: str, path: str = "./results/"):
    """
    Saves the model to a given path.
    """
    # create dir if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)
    torch.save(model.state_dict(), path + save_name)


def visualize_predictions(
    predictions: dict,
    time_period: int,
    df_merge: pd.DataFrame,
    classified_illicit_idx: pd.Index,
    classified_licit_idx: pd.Index,
    data: Data,
    path: str = "./results/",
    plot_name: str = "network_graph_with_predictions.png",
):
    """
    Visualizes and saves the graph of predictions for a given time period.
    """
    sub_node_list = df_merge[df_merge["Time step"] == time_period].index.tolist()

    edge_tuples = [
        (row[0], row[1])
        for row in data.edge_index.cpu().numpy().T
        if row[0] in sub_node_list or row[1] in sub_node_list
    ]

    node_color = []
    for node_id in sub_node_list:
        if node_id in classified_illicit_idx:
            label = "red"
        elif node_id in classified_licit_idx:
            label = "green"
        else:
            label = "yellow" if predictions["pred_labels"][node_id] else "blue"
        node_color.append(label)

    G = nx.Graph()
    G.add_edges_from(edge_tuples)

    plt.figure(figsize=(16, 16))
    plt.title("Graph network of BTC transactions from period: " + str(time_period))
    nx.draw_networkx(
        G, nodelist=sub_node_list, node_color=node_color, node_size=6, with_labels=False
    )
    plt.legend(["Illicit", "Licit", "Unclassified"], loc="upper right")

    os.makedirs(path, exist_ok=True)

    plt.savefig(os.path.join(path, plot_name))
    plt.show()
