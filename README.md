[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/poornaashreepraveenraj/Detecting-Behavioral-Drift-in-Long-Term-Music-Streaming-Users/blob/main/DriftTune.ipynb)

# DriftTune — Detecting Behavioral Drift in Long-Term Music Streaming User

## Problem Statement
DriftTune detects how user music preferences change over time using Last.fm 
listening history and Spotify audio features. Users are classified into 
High, Medium, or Low drift categories based on how much their listening 
behaviour shifted between early and late periods.

## Pipeline
Data Loading → Preprocessing → Feature Engineering → Drift Scoring → 
KMeans Clustering → ML Models → Deep Learning (MLP Neural Network) → 
Evaluation and Comparison

## Dataset Details
- dataset.csv — 114,000 Spotify songs with 21 audio features (Kaggle)
- Last.fm_data.csv — 166,153 user listening history records (Last.fm public)
- usersha1-profile.csv — 359,346 user profiles

## Models Used

### ML Models (Review 2)
| Model | Accuracy |
|---|---|
| Logistic Regression | 34.4% |
| Random Forest | 98.9% |
| Decision Tree | 100% (overfitting) |
| SVM | 66.7% |

### Deep Learning (Review 3)
| Model | Accuracy |
|---|---|
| Neural Network MLP | 84.4% |

Architecture: Input(8) → Dense(128) → BatchNorm → Dropout(0.3) → 
Dense(64) → BatchNorm → Dropout(0.2) → Dense(32) → Dense(3, softmax)

Optimizations: BatchNormalization, Dropout, EarlyStopping, Adam optimizer

## Steps to Run
1. Open DriftTune.ipynb in Google Colab
2. Mount Google Drive when prompted
3. Upload all CSV files to /content/drive/MyDrive/DriftTune/
4. Run all cells from top to bottom

## Dependencies
pandas
numpy
matplotlib
seaborn
scikit-learn
tensorflow
xgboost

## Sample Output
- Neural Network accuracy: 84.4%
- Random Forest accuracy: 98.9%
- Confusion matrices for all 5 models
- Neural Network training loss and accuracy curves
- Feature importance chart
- Drift classification distribution pie chart

## Team Members
- Poornaa Shree Praveenraj — 24BCS202
- Pranusree A S — 24BCS206
- Raksha S V — 24BCS219
- Rithy R — 24BCS227
