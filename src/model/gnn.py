import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATv2Conv


class FraudDetector(nn.Module):
    def __init__(
        self,
        input_dim: int = 182,  # shape of features without txId, Time step and User
        hidden_dim: int = 128,
        output_dim: int = 1,
        heads: int = 2,
        dropout: float = 0.5,
    ):
        """
        Attention-based Graph Neural Network model for fraud detection.
        """
        super(FraudDetector, self).__init__()
        self.conv1 = GATv2Conv(input_dim, hidden_dim, heads=heads)
        self.conv2 = GATv2Conv(heads * hidden_dim, hidden_dim, heads=heads)

        self.post_mp = nn.Sequential(
            nn.Linear(heads * hidden_dim, hidden_dim),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, output_dim),
            nn.Sigmoid(),
        )
        self.dropout = dropout

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=self.dropout, training=self.training)

        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=self.dropout, training=self.training)

        x = self.post_mp(x)
        return x
