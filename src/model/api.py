from fastapi import FastAPI, HTTPException
import numpy as np
import pandas as pd
from pydantic import BaseModel
import torch
from torch_geometric.data import Data
from gnn import FraudDetector

app = FastAPI()
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = "model_weights.pth"

model = FraudDetector()
model_state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
model.load_state_dict(model_state_dict)
model.to(DEVICE)
model.eval()


class DataModel(BaseModel):
    input_data: dict


@app.post("/predict")
async def predict(data_model: DataModel):
    try:
        features = pd.DataFrame(data_model.input_data["features"])
        edges = pd.DataFrame(data_model.input_data["edges"])

        node_features = torch.tensor(
            np.array(pd.DataFrame(features).values, dtype=np.float32),
            dtype=torch.float32,
        )
        edge_index = torch.tensor(
            np.array(pd.DataFrame(edges).values).T,
            dtype=torch.int32,
        ).contiguous()

        data = Data(
            x=node_features,
            edge_index=edge_index,
        )

        with torch.no_grad():
            output = model(data.to(DEVICE))
        predictions = [torch.round(output).squeeze().tolist()]

        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
