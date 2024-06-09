import argparse

import torch
import torch.nn as nn
from torch_geometric.data import Data

from gnn import FraudDetector
from preprocessing import load_data, preprocess_data
from utils import calculate_metrics, save_metrics, save_model, visualize_predictions


def train(model, data_train: Data, optimizer, criterion, args: argparse.Namespace):
    """
    Trains the model on the given Geometric data.
    Args:
        model (torch.nn.Module): Model to train.
        data_train (Data): PyTorch Geometric Data object.
        optimizer (torch.optim): Optimizer to use.
        criterion (torch.nn): Loss function.
        args (argparse.Namespace): Arguments.
    """
    best_val_f1 = 0
    for epoch in range(args.num_epochs):
        model.train()
        optimizer.zero_grad()
        out = model(data_train)

        out = out.reshape((data_train.x.shape[0]))
        loss = criterion(out[data_train.train_idx], data_train.y[data_train.train_idx])

        target_labels = data_train.y.detach().cpu().numpy()[data_train.train_idx]
        pred_scores = out.detach().cpu().numpy()[data_train.train_idx]
        metrics = calculate_metrics(pred_scores, target_labels)
        train_acc, train_f1 = metrics["accuracy"], metrics["f1"]

        # training step
        loss.backward()
        optimizer.step()

        # validation data
        model.eval()
        target_labels = data_train.y.detach().cpu().numpy()[data_train.valid_idx]
        pred_scores = out.detach().cpu().numpy()[data_train.valid_idx]
        metrics = calculate_metrics(pred_scores, target_labels)
        val_acc, val_f1 = metrics["accuracy"], metrics["f1"]

        if epoch % 5 == 0:
            print(
                "epoch: {} - loss: {:.4f} - accuracy train: {:.4f} - accuracy valid: {:.4f} - train f1: {:.4f} - val f1: {:.4f}".format(
                    epoch, loss.item(), train_acc, val_acc, train_f1, val_f1
                )
            )

        result = {
            "epoch": epoch,
            "accuracy_train": train_acc,
            "accuracy_val": val_acc,
            "f1_train": train_f1,
            "f1_val": val_f1,
        }

        save_metrics(
            result,
            f"metrics_{args.num_heads}_heads_{args.hidden_dim}_hidden_dim_{args.lr}_lr_{args.num_epochs}_epochs.csv",
            path=args.output_path,
        )

        if val_f1 > best_val_f1:
            best_val_f1 = val_f1
            save_model(
                model,
                f"fraud_detector_{args.num_heads}_heads_{args.hidden_dim}_hidden_dim_{args.lr}_lr_{args.num_epochs}_epochs.pth",
                path=args.output_path,
            )


def predict(model, data_test: Data, threshold: float = 0.5) -> dict:
    """
    Performs inference on the given data by the model.
    Returns the predicted scores and labels.
    """
    with torch.no_grad():
        out = model(data_test)
        out = out.reshape((data_test.x.shape[0]))

    pred_scores = out.detach().cpu().numpy()

    pred_labels = pred_scores > threshold

    return {"pred_scores": pred_scores, "pred_labels": pred_labels}


def main(args):
    """
    Loads data, trains the model and saves the metrics. Visualizes the predictions.
    """
    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device: ", device)
    print("Loading data...")
    df_features, df_edges, df_classes = load_data(args.data_path)
    print("Preprocessing data...")
    data, classified_licit_idx, classified_illicit_idx = preprocess_data(
        df_features, df_edges, df_classes
    )
    data = data.to(device)

    model = FraudDetector(
        input_dim=data.x.shape[1],
        hidden_dim=args.hidden_dim,
        output_dim=1,
        heads=args.num_heads,
        dropout=args.dropout,
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    criterion = nn.BCELoss()
    print("Training model...")
    train(model, data, optimizer, criterion, args)

    # load best model
    best_model = FraudDetector(
        input_dim=data.x.shape[1],
        hidden_dim=args.hidden_dim,
        output_dim=1,
        heads=args.num_heads,
        dropout=args.dropout,
    ).to(device)

    best_model.load_state_dict(
        torch.load(
            args.output_path
            + f"fraud_detector_{args.num_heads}_heads_{args.hidden_dim}_hidden_dim_{args.lr}_lr_{args.num_epochs}_epochs.pth",
        )
    )

    # perform inference
    print("Predicting labels...")
    predictions = predict(best_model, data)

    # visualize predictions
    print("Visualizing predictions...")
    visualize_predictions(
        predictions,
        time_period=10,
        df_merge=df_features,
        classified_illicit_idx=classified_illicit_idx,
        classified_licit_idx=classified_licit_idx,
        data=data,
    )
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        type=str,
        default="C:/studia/sem_8/Cloud/gcp_fraud_detection/data/",
    )
    parser.add_argument("--num-epochs", type=int, default=100)
    parser.add_argument("--hidden-dim", type=int, default=128)
    parser.add_argument("--num-heads", type=int, default=2)
    parser.add_argument("--dropout", type=float, default=0.5)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--seed", type=int, default=420)
    parser.add_argument(
        "--output-path",
        type=str,
        default="C:/studia/sem_8/Cloud/gcp_fraud_detection/src/model/results/",
    )
    args = parser.parse_args()
    main(args)
