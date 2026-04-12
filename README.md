# DriftTune — Music Recommendation System

## Problem Statement
DriftTune detects how user music preferences change over time using Last.fm 
listening history and Spotify audio features. Users are classified into 
High, Medium, or Low drift categories based on how much their listening 
behaviour shifted between early and late periods.

## Pipeline Diagram
Data Loading → Preprocessing → Feature Engineering → Drift Scoring → 
ML Models (LR, RF, DT, SVM) → Deep Learning (MLP Neural Network) → 
Evaluation and Comparison

## Dataset Details
- dataset.csv — 114,000 Spotify songs with 21 audio features
- Last.fm_data.csv — 166,153 user listening history records
- usersha1-profile.csv — 359,346 user profiles
- Source: Kaggle Spotify Dataset + Last.fm public dataset

## Models Used
ML Models:
- Logistic Regression — 34.4% accuracy
- Random Forest — 98.9% accuracy
- Decision Tree — 100% accuracy (overfitting)
- SVM — 66.7% accuracy

Deep Learning:
- Neural Network MLP — 84.4% accuracy
- Architecture: 128 → 64 → 32 → 3 (softmax)
- Optimizations: BatchNormalization, Dropout, EarlyStopping, Adam

## Steps to Run
1. Open DriftTune.ipynb in Google Colab
2. Mount Google Drive
3. Upload all CSV files to /content/drive/MyDrive/DriftTune/
4. Run all cells from top to bottom

## Dependencies
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- tensorflow
- xgboost

## Sample Output
- Model Performance Comparison chart
- Confusion matrices for all 5 models
- Neural Network accuracy and loss curves
- Feature importance chart
- Drift classification distribution

## Team Members
- Poornaa shree praveenraj 24BCS202
- Pranusree A S 24BCS206
- Raksha S V 24BCS219
- Rithy R 24BCS227
