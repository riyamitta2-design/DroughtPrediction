
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, LSTM, Conv1D, Dropout, MaxPooling1D, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

file_name = "data5000.csv"
length = 36
prediction = [6, 9, 12]
seeds = [42, 123, 456]
feature = ["spei_1", "spei_3", "spei_12", "month_sin", "month_cos"]
df = pd.read_csv(file_name)
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=["latitude", "longitude", "year", "month", "spei_1", "spei_3", "spei_12"]).copy()
df = df.sort_values(["latitude", "longitude", "year", "month"])
df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)
df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
df["drought"] = (df["spei_12"] <= -1).astype(int)
def create_sequence(df, p):
    X, y, years = [], [], []
    for _, group in df.groupby(["latitude", "longitude"], sort=False):
        group = group.sort_values(["year", "month"])
        v = group[feature].to_numpy(dtype=np.float32)
        dv = group["drought"].to_numpy(dtype=np.int32)
        yv = group["year"].to_numpy(dtype=np.int32)
        months = yv * 12 + group["month"].to_numpy(dtype=np.int32)
        for j in range(length, len(group) - p + 1):
            target = j - 1 + p
            if not np.all(np.diff(months[j-length:target+1]) == 1):
                continue
            X.append(v[j-length:j])
            y.append(dv[target])
            years.append(yv[target])
    return np.asarray(X, dtype=np.float32), np.asarray(y), np.asarray(years)


def create_cnn_model():
    model = Sequential([
        Input(shape=(length, len(feature))),
        Conv1D(64, 3, activation="relu"),
        Conv1D(32, 3, activation="relu"),
        MaxPooling1D(2), Flatten(),
        Dense(64, activation="relu"), Dropout(0.3),
        Dense(32, activation="relu"), Dropout(0.2),
        Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer=Adam(learning_rate=0.0005), loss="binary_crossentropy", metrics=["accuracy"])
    return model


def create_lstm_model():
    model = Sequential([
        Input(shape=(length, len(feature))),
        LSTM(64, return_sequences=True), Dropout(0.3),
        LSTM(32), Dropout(0.3),
        Dense(32, activation="relu"), Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer=Adam(learning_rate=0.0005), loss="binary_crossentropy", metrics=["accuracy"])
    return model


def findtreasure(y, prob):
    best, best_score = 0.5, -1
    for threshold in np.arange(0.1, 0.91, 0.01):
        score = f1_score(y, prob >= threshold, zero_division=0)
        if score > best_score:
            best, best_score = float(threshold), score
    return best


def evaluate(name, p, run, y_val, val_prob, y_test, test_prob):
    threshold = findtreasure(y_val, val_prob)
    pred = (test_prob >= threshold).astype(int)
    result = {
        "Horizon": p, "Model": name, "Run": run, "Threshold": threshold,
        "Accuracy": accuracy_score(y_test, pred),
        "Precision": precision_score(y_test, pred, zero_division=0),
        "Recall": recall_score(y_test, pred, zero_division=0),
        "F1": f1_score(y_test, pred, zero_division=0),
        "ROC_AUC": roc_auc_score(y_test, test_prob) if len(np.unique(y_test)) == 2 else np.nan
    }
    print(name, "horizon", p, "run", run, "F1", round(result["F1"], 3))
    return result


results = []
dataset_results = []

for p in prediction:
    print("\nPredicting", p, "months ahead")
    X, y, years = create_sequence(df, p)
    train = years <= 2010
    validation = (years >= 2011) & (years <= 2015)
    test = years >= 2016
    if not all(np.any(mask) for mask in [train, validation, test]):
        raise ValueError("A time split is empty. Check the years in the dataset.")

    X_train, X_val, X_test = X[train], X[validation], X[test]
    y_train, y_val, y_test = y[train], y[validation], y[test]
    if len(np.unique(y_train)) != 2:
        raise ValueError("Training data must contain both drought classes.")
    dataset_results.append({
        "Horizon": p, "Train": len(y_train), "Validation": len(y_val), "Test": len(y_test),
        "Train_Drought_%": 100*y_train.mean(),
        "Validation_Drought_%": 100*y_val.mean(), "Test_Drought_%": 100*y_test.mean()
    })
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train.reshape(-1, len(feature))).reshape(X_train.shape)
    X_val = scaler.transform(X_val.reshape(-1, len(feature))).reshape(X_val.shape)
    X_test = scaler.transform(X_test.reshape(-1, len(feature))).reshape(X_test.shape)
    train2d = X_train.reshape(len(X_train), -1)
    val2d = X_val.reshape(len(X_val), -1)
    test2d = X_test.reshape(len(X_test), -1)

    dummy = DummyClassifier(strategy="most_frequent")
    logistic = LogisticRegression(max_iter=1000, class_weight="balanced")
    forest = RandomForestClassifier(n_estimators=300, max_depth=15,
                                    random_state=30, n_jobs=-1, class_weight="balanced")

    for name, model in [("Dummy", dummy), ("Logistic Regression", logistic), ("Random Forest", forest)]:
        model.fit(train2d, y_train)
        val_prob = model.predict_proba(val2d)[:, list(model.classes_).index(1)]
        test_prob = model.predict_proba(test2d)[:, list(model.classes_).index(1)]
        results.append(evaluate(name, p, 1, y_val, val_prob, y_test, test_prob))

    weights = compute_class_weight("balanced", classes=np.array([0, 1]), y=y_train)
    class_weights = {0: float(weights[0]), 1: float(weights[1])}

    for name, builder in [("CNN", create_cnn_model), ("LSTM", create_lstm_model)]:
        for run, seed in enumerate(seeds, start=1):
            random.seed(seed)
            np.random.seed(seed)
            model = builder()
            early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
            history = model.fit(
                X_train, y_train, epochs=30, batch_size=512,
                validation_data=(X_val, y_val), class_weight=class_weights,
                callbacks=[early_stop], verbose=1
            )
            val_prob = model.predict(X_val, verbose=0).ravel()
            test_prob = model.predict(X_test, verbose=0).ravel()
            results.append(evaluate(name, p, run, y_val, val_prob, y_test, test_prob))

            if run == 1:
                plt.figure()
                plt.plot(history.history["loss"], label="Training")
                plt.plot(history.history["val_loss"], label="Validation")
                plt.xlabel("Epoch")
                plt.ylabel("Loss")
                plt.title(f"{name}: {p}-month forecast")
                plt.legend()
                plt.tight_layout()
                plt.savefig(f"{name}_{p}_loss.png", dpi=200)
                plt.close()

results_df = pd.DataFrame(results)
results_df.to_csv("results_all_runs.csv", index=False)
pd.DataFrame(dataset_results).to_csv("dataset_summary.csv", index=False)
summary = results_df.groupby(["Horizon", "Model"], as_index=False).agg(
    Accuracy_mean=("Accuracy", "mean"), Precision_mean=("Precision", "mean"),
    Recall_mean=("Recall", "mean"), F1_mean=("F1", "mean"),
    F1_std=("F1", "std"), ROC_AUC_mean=("ROC_AUC", "mean")
)
summary.to_csv("results_summary.csv", index=False)
print("\nPaper results:\n", summary.round(3).to_string(index=False))

# F1 comparison figure
plt.figure(figsize=(8, 5))
for name in ["Dummy", "Logistic Regression", "Random Forest", "CNN", "LSTM"]:
    data = summary[summary["Model"] == name].sort_values("Horizon")
    plt.errorbar(data["Horizon"], data["F1_mean"],
                 yerr=data["F1_std"].fillna(0), marker="o", capsize=3, label=name)
plt.xticks(prediction)
plt.xlabel("Forecast horizon (months)")
plt.ylabel("Test F1-score")
plt.title("Drought forecasting model comparison")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("f1_comparison.png", dpi=300)
plt.close()
print("Saved results_summary.csv, dataset_summary.csv, results_all_runs.csv and PNG figures")