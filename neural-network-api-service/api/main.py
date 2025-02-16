from fastapi import FastAPI
from pydantic import BaseModel
import torch
import torch.nn as nn


# Define the same deep neural network architecture with dropout and batch normalization
class Net(nn.Module):
    def __init__(self, input_dim):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.dropout1 = nn.Dropout(0.3)

        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.dropout2 = nn.Dropout(0.3)

        self.fc3 = nn.Linear(64, 32)
        self.bn3 = nn.BatchNorm1d(32)
        self.dropout3 = nn.Dropout(0.3)

        self.fc4 = nn.Linear(32, 16)
        self.bn4 = nn.BatchNorm1d(16)
        self.dropout4 = nn.Dropout(0.3)

        self.fc5 = nn.Linear(16, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.dropout1(x)

        x = self.fc2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.dropout2(x)

        x = self.fc3(x)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.dropout3(x)

        x = self.fc4(x)
        x = self.bn4(x)
        x = self.relu(x)
        x = self.dropout4(x)

        x = self.fc5(x)
        return x


# Set the input dimension to match the number of features (adjust if necessary)
input_dim = 30

# Load the trained model
model = Net(input_dim)
model.load_state_dict(
    torch.load("model.pth", map_location=torch.device("cpu"))
)
model.eval()


# Define a request schema using Pydantic
class PredictionRequest(BaseModel):
    features: list[float]  # List of feature values


# Initialize FastAPI app
app = FastAPI()


@app.post("/predict")
async def predict(request: PredictionRequest):
    # Convert the incoming features to a tensor and add a batch dimension
    input_tensor = torch.tensor(
        request.features, dtype=torch.float32
    ).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor).squeeze(1)
        probability = torch.sigmoid(output).item()
        prediction = 1 if probability > 0.5 else 0
    return {"probability": probability, "prediction": prediction}


# Run the server when this file is executed directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("inference:app", host="0.0.0.0", port=8000, reload=True)
