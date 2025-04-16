# Flight Delay Prediction Project

# Overview
This project predicts flight delays using integrated flight and weather data. It employs machine learning to perform:
- **Binary Classification**: Predicts whether a flight is delayed (On-time vs. Delayed).
- **Multi-Class Classification**: Categorizes delays into No Delay, Short Delay, Moderate Delay, or Long Delay.
- **Regression**: Predicts the exact delay duration in minutes.

The pipeline processes raw data, performs exploratory data analysis (EDA), and trains models using Python with libraries like Pandas, Scikit-learn, Matplotlib, and Seaborn.

# Dataset
- **Flight Data**: Contains flight details (e.g., scheduled time, actual time, airline info) in `merged_train.csv` and `merged_test.csv`.
- **Weather Data**: Includes meteorological data (e.g., temperature, humidity, wind speed) in Excel files (`1.xlsx` to `13.xlsx`) and a merged CSV (`merged_weather.csv`).
- **Integrated Data**: Combines flight and weather data with calculated delay durations.

# Project Structure
The project is divided into five phases:

## Phase 1: Data Preprocessing
- **Scripts**:
  - `weather.py`: Converts weather Excel files to CSV and cleans data.
  - `preprocessed.py`: Handles missing values, encodes categorical variables, and scales numerical features for flight data.
  - `preprocessed.ipynb`: Additional preprocessing, including datetime conversions and column removal.
  - Integration script: Merges flight and weather data by nearest timestamp and calculates delays.
- **Outputs**:
  - `WeatherCsv/*.csv`: Processed weather data per month.
  - `MergeTrainCsv/preprocessed_train.csv`: Preprocessed training flight data.
  - `MergeTestCsv/preprocessed_test.csv`: Preprocessed testing flight data.
  - `MergeCsvWeather/preprocessed_weather.csv`: Preprocessed weather data.
  - `MergeTrainCsv/integrated_train.csv`: Integrated train data.
  - `MergeTestCsv/integrated_test.csv`: Integrated test data.

## Phase 2: Exploratory Data Analysis (EDA)
- **Script**: `eda_visualizations` function.
- **Purpose**: Visualizes delay distributions, temporal patterns (hour/day), airline-specific delays, and correlations.
- **Outputs**: Plots (e.g., histograms, line plots, boxplots, heatmaps).

## Phase 3: Model Development
- **Binary Classification**:
  - Uses RandomForestClassifier to predict On-time vs. Delayed.
  - Script: Preprocesses data, trains model, and evaluates metrics (accuracy, precision, recall, F1).
- **Multi-Class Classification**:
  - Categorizes delays into four classes using RandomForestClassifier.
  - Script: Preprocesses data, trains model, and evaluates metrics.
- **Regression**:
  - Uses RandomForestRegressor to predict delay duration.
  - Script: Preprocesses data, trains model, and evaluates MAE and RMSE.
- **Outputs**:
  - `preprocessed_binary_train.csv`, `preprocessed_binary_test.csv`
  - `preprocessed_multi_train.csv`, `preprocessed_multi_test.csv`

## Phase 4: Model Optimization
- **Scripts**: Apply GridSearchCV to tune hyperparameters for RandomForest models (binary and multi-class) and LinearRegression.
- **Outputs**: Optimized model performance metrics.

## Phase 5: Final Predictions
- **Scripts**: Use trained models to predict on test data.
- **Outputs**:
  - `submission_binary_classification.csv`: Binary classification predictions.
  - `submission_multi_class_classification.csv`: Multi-class classification predictions.
  - `submission_regression.csv`: Regression predictions.

# Requirements
- Python 3.8+
- Libraries:
  ```bash
  pandas
  numpy
  scikit-learn
  matplotlib
  seaborn
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

# Setup and Execution
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Organize data in the following structure:
   ```
   ML-Proj-Dataset/
   ├── MergeTrainCsv/
   │   ├── merged_train.csv
   ├── MergeTestCsv/
   │   ├── merged_test.csv
   ├── Weather/
   │   ├── 1.xlsx ... 13.xlsx
   ├── MergeCsvWeather/
   │   ├── merged_weather.csv
   ```
4. Run scripts in order:
   - Phase 1: `weather.py`, `preprocessed.py`, `preprocessed.ipynb`, integration script.
   - Phase 2: EDA script.
   - Phase 3: Binary, multi-class, and regression scripts.
   - Phase 4: Optimization scripts.
   - Phase 5: Prediction scripts to generate submission CSVs.

# Usage
- To preprocess data: Run `weather.py` and `preprocessed.py` with appropriate file paths.
- To perform EDA: Execute the EDA script with integrated train/test CSVs.
- To train models: Run the respective scripts for binary, multi-class, or regression tasks.
- To generate predictions: Run Phase 5 scripts to produce submission files.

# Results
- **Binary Classification**: Achieves ~81% accuracy on validation data.
- **Multi-Class Classification**: Achieves ~79% accuracy with challenges in imbalanced classes.
- **Regression**: MAE ~0.03, RMSE ~0.53 on validation data.

# Notes
- Ensure consistent file paths in scripts.
- Handle datetime parsing warnings by specifying formats if needed.
- Imbalanced classes in multi-class classification may require techniques like SMOTE.

# License
This project is licensed under the MIT License.

# Contact
For questions, contact the project maintainer at [your-email@example.com].
