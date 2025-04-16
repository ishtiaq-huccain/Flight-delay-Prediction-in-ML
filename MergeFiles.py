import pandas as pd
import os

def merge_csv_files(input_folder, output_folder, output_file_name):

    os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist
    output_file_path = os.path.join(output_folder, output_file_name)

    csv_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.csv')]

    merged_data = pd.concat((pd.read_csv(file) for file in csv_files), ignore_index=True)

    merged_data.to_csv(output_file_path, index=False)
    print(f"Merged {len(csv_files)} files into {output_file_path}")

input_train_folder = "./TrainCsv"
output_train_folder = "./MergeTrainCsv"
input_test_folder = "./TestCsv"
output_test_folder = "./MergeTestCsv"

# Merge Train and Test CSV files
merge_csv_files(input_train_folder, output_train_folder, "merged_train.csv")
merge_csv_files(input_test_folder, output_test_folder, "merged_test.csv")
