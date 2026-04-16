import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import time

def train_and_evaluate():
    print("--- Phase 1: Data Preparation ---")
    df = pd.read_csv('processed_dataset.csv')
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Consistent Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "Decision Tree": DecisionTreeClassifier(max_depth=10),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, n_jobs=-1),
        "AdaBoost": AdaBoostClassifier(n_estimators=50)
    }
    
    results = []
    
    print("\n--- Phase 2: Model Training & Cross-Validation ---")
    for name, model in models.items():
        print(f"Evaluating {name}...")
        start_time = time.time()
        
        # Cross-validation
        cv_results = cross_validate(model, X, y, cv=5, scoring=['accuracy', 'precision', 'recall', 'f1'])
        
        # Fit on training set for specific prediction metrics
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        elapsed = time.time() - start_time
        
        results.append({
            "Model": name,
            "CV Accuracy": np.mean(cv_results['test_accuracy']),
            "CV Precision": np.mean(cv_results['test_precision']),
            "CV Recall": np.mean(cv_results['test_recall']),
            "CV F1-Score": np.mean(cv_results['test_f1']),
            "Holdout Accuracy": accuracy_score(y_test, y_pred),
            "Time (s)": elapsed
        })

    # Summary Table
    results_df = pd.DataFrame(results)
    print("\n--- Phase 3: Evaluation Summary ---")
    print(results_df.sort_values(by="CV F1-Score", ascending=False).to_string(index=False))
    
    # Save Report
    results_df.to_csv('model_evaluation_results.csv', index=False)
    
    print("\nModel training and evaluation complete. Results saved to 'model_evaluation_results.csv'.")
    
    # Best Model Justification
    best_model = results_df.iloc[results_df['CV F1-Score'].idxmax()]
    print(f"\nRecommended Model: {best_model['Model']}")
    print(f"Reasoning: Highest F1-Score ({best_model['CV F1-Score']:.4f}) indicates the best balance between precision and recall for energy classification.")

if __name__ == "__main__":
    train_and_evaluate()
