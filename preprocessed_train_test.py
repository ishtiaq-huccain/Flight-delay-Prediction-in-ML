import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

merged_train_file = "./MergeTrainCsv/merged_train.csv"
preprocessed_train_file = "./MergeTrainCsv/preprocessed_train.csv"

merged_test_file = "./MergeTestCsv/merged_test.csv"
preprocessed_test_file = "./MergeTestCsv/preprocessed_test.csv"

categorical_columns = ['terminal', 'iataCode', 'icaoCode', 'name']

def preprocess_data(input_file, output_file, label_encoders=None, is_train=True):
    # Load the data
    data = pd.read_csv(input_file)
    print(f"\n--- Preprocessing {input_file} ---")
    
    # Handle missing values
    for column in data.columns:
        if data[column].dtype == 'object':  # Categorical columns
            data[column].fillna('Unknown', inplace=True)
        else:  # Numerical columns
            data[column].fillna(data[column].median(), inplace=True)
    
    # Encode categorical features
    if is_train:
        label_encoders = {}
        for col in categorical_columns:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            label_encoders[col] = le
    else:
        for col in categorical_columns:
            le = label_encoders[col]
            data[col] = data[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

    numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

    data.to_csv(output_file, index=False)
    print(f"Preprocessed data saved to {output_file}")
    
    return label_encoders

# Preprocess train data and save the encoders
label_encoders = preprocess_data(merged_train_file, preprocessed_train_file, is_train=True)

# Preprocess test data using the same encoders
preprocess_data(merged_test_file, preprocessed_test_file, label_encoders, is_train=False)


