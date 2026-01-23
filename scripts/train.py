import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
import os

os.makedirs("model", exist_ok=True)

df = pd.read_csv("data/winequality-red.csv", sep=",")
df.columns = df.columns.str.strip().str.lower()

X = df.drop("quality", axis=1)
y = df["quality"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = Ridge(alpha=1.0)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse}")
print(f"R2: {r2}")

joblib.dump(model, "model/model.pkl")

metrics = {
    "mse": round(mse, 4),
    "r2": round(r2, 4)
}

with open("metrics.json", "w") as f:
    json.dump(metrics, f)

print("Training complete and metrics saved")
