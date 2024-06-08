import json
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
DATA = torch.load("graph.pth")
MAP_DICT = json.load(open("map_id.json"))

model = FraudDetector()
model_state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
model.load_state_dict(model_state_dict)
model.to(DEVICE)
model.eval()


class DataModel(BaseModel):
    """
    list of transaction ids to predict fraud for
    """

    indices: list


@app.post("/predict")
async def predict(input_data: DataModel):
    try:
        indices = [int(MAP_DICT[str(idx)]) for idx in input_data.indices]
        with torch.no_grad():
            output = model(DATA.to(DEVICE))
        predictions = [torch.round(output).squeeze().tolist()[idx] for idx in indices]

        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
