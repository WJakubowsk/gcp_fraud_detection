from ts.torch_handler.base_handler import BaseHandler
import torch
from torch_geometric.data import Data


class GNNHandler(BaseHandler):
    def initialize(self, context):
        self.model = self.load_model()

    def preprocess(self, data):
        for row in data:
            # Assuming input data contains node_features, edge_index, and edge_attr in JSON format
            input_data = row.get("body")

            node_features = torch.tensor(
                input_data["node_features"], dtype=torch.float32
            )
            edge_index = torch.tensor(input_data["edge_index"], dtype=torch.long)
            edge_attr = torch.tensor(input_data["edge_attr"], dtype=torch.float32)

            graph_data = Data(
                x=node_features, edge_index=edge_index, edge_attr=edge_attr
            )
            return graph_data

    def inference(self, data):
        with torch.no_grad():
            output = self.model(data)
        return output

    def postprocess(self, inference_output):
        predictions = torch.round(inference_output).squeeze().tolist()
        return predictions

    def _load_model(self):
        # Load the saved GNN model
        model_path = "./model_weights.pth"
        model = torch.load(model_path)
        return model
