import json

import numpy as np
import pandas as pd
import torch
from torch_geometric.data import Data
from ts.torch_handler.base_handler import BaseHandler

from gnn import FraudDetector


class GNNHandler(BaseHandler):
    def initialize(self, context):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.load_model()
        self.model.to(self.device)
        self.model.eval()

    def preprocess(self, data):
        node_features = torch.tensor([], dtype=torch.float32)
        edge_index = torch.tensor([], dtype=torch.long)

        input_data = json.loads(data[0]["body"].decode("utf-8"))

        try:
            node_features = torch.tensor(
                np.array(pd.DataFrame(input_data["features"]).values, dtype=np.float32),
                dtype=torch.float32,
            )
            edge_index = torch.tensor(
                np.array(pd.DataFrame(input_data["edges"]).values).T,
                dtype=torch.int32,
            ).contiguous()
        except KeyError as e:
            raise ValueError("Input data does not contain expected keys: {}".format(e))

        graph_data = Data(
            x=node_features,
            edge_index=edge_index,
        )
        return graph_data

    def inference(self, data):
        with torch.no_grad():
            output = self.model(data.to(self.device))
        predictions = [torch.round(output).squeeze().tolist()]
        return predictions

    def postprocess(self, inference_output):
        return [json.dumps(inference_output)]

    def load_model(self):
        model_path = "model_weights.pth"
        try:
            model_state_dict = torch.load(model_path, map_location=self.device)
            model = FraudDetector()
            model.load_state_dict(model_state_dict)
            print("Model loaded successfully")
            return model
        except Exception as e:
            print("Model loading failed")
            print(e)
