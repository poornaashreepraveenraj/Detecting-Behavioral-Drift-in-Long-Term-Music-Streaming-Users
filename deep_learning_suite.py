import pandas as pd
import numpy as np
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import time

def train_deep_learning_model():
    print("--- Phase 1: Data Loading ---")
    try:
        df = pd.read_csv('processed_dataset.csv')
    except FileNotFoundError:
        print("Error: processed_dataset.csv not found. Please run data_pipeline.py first.")
        return

    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("\n--- Phase 2: Building Deep Learning Model (MLP) ---")
    # Architecture: 3 Hidden Layers (64, 32, 16)
    # MLPClassifier is scikit-learn's implementation of a Multi-Layer Perceptron (Neural Network)
    # We use 'adam' optimizer and 'relu' activation which are deep learning standards.
    mlp = MLPClassifier(
        hidden_layer_sizes=(64, 32, 16),
        activation='relu',
        solver='adam',
        max_iter=500,
        random_state=42,
        verbose=True,
        early_stopping=True,
        validation_fraction=0.1
    )
    
    print("Training neural network...")
    start_time = time.time()
    mlp.fit(X_train, y_train)
    elapsed = time.time() - start_time
    
    print(f"\nTraining complete in {elapsed:.2f} seconds.")
    
    print("\n--- Phase 3: Evaluation ---")
    y_pred = mlp.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    with open('deep_learning_model.pkl', 'wb') as f:
        pickle.dump(mlp, f)
    
    # Save metrics to txt
    with open('dl_metrics.txt', 'w') as f:
        f.write("Deep Learning (MLP) Model Results\n")
        f.write("="*50 + "\n")
        f.write(f"Architecture: (64, 32, 16) Hidden Layers\n")
        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall: {recall:.4f}\n")
        f.write(f"F1-Score: {f1:.4f}\n")
        f.write("\nClassification Report:\n")
        f.write(classification_report(y_test, y_pred))

    print("\nModel saved as 'deep_learning_model.pkl' and metrics saved to 'dl_metrics.txt'.")

if __name__ == "__main__":
    train_deep_learning_model()
