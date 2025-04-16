import pandas as pd
import numpy as np
import os


def process_weather_file(file_path):
    """Process a single weather Excel file and return a cleaned DataFrame."""
    # Load the Excel file
    data = pd.ExcelFile(file_path)
    
    # Parse the first sheet
    sheet1_data = data.parse("Sheet1")
    
    # Extract the first row (contains all data)
    raw_data = sheet1_data.iloc[0]
    
    # Split each column into separate elements
    split_data = {col: raw_data[col].split() for col in raw_data.index}
    
    # Extract the "Time" column
    time_column = split_data["Time"]
    
    # Process other columns
    cleaned_columns = {}
    for col, values in split_data.items():
        if col == "Time":
            continue
        try:
            # Reshape into blocks of three (Max, Avg, Min)
            reshaped_values = np.array(values).reshape(-1, 3)
            cleaned_columns[f"{col} Max"] = reshaped_values[:, 0]
            cleaned_columns[f"{col} Avg"] = reshaped_values[:, 1]
            cleaned_columns[f"{col} Min"] = reshaped_values[:, 2]
        except ValueError:
            # If reshaping fails, keep raw values for further inspection
            cleaned_columns[col] = values
    
    # Combine into a cleaned DataFrame
    cleaned_data = pd.DataFrame({
        "Time": time_column,
        **cleaned_columns
    })
    
    # Convert numeric columns where possible
    for col in cleaned_data.columns[1:]:
        cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors="coerce")
    
    return cleaned_data


def clean_and_rename_columns(data):
    """Clean and rename the 'Time' column based on the month name in the first row."""
    # Check if the first row contains only the month name in the 'Time' column
    if data.iloc[0, 0] and data.iloc[0, 0].isalpha() and len(data.columns) > 1:
        # The first row contains a month name, so remove it
        month_name = data.iloc[0, 0]
        data = data.drop(index=0)
        
        # Rename 'Time' column by adding the month name as a prefix
        data.columns = [f"Time ({month_name})" if col == 'Time' else col for col in data.columns]
    
    return data


def process_weather_folder(folder_path, output_folder, num_files=13):
    """Process the first 13 weather Excel files in a folder and save each as a CSV."""
    os.makedirs(output_folder, exist_ok=True)

    for i in range(1, num_files + 1):
        file_name = f"{i}.xlsx"
        file_path = os.path.join(folder_path, file_name)
        output_file_path = os.path.join(output_folder, f"{i}.csv")

        if os.path.exists(file_path):
            print(f"Processing {file_name}...")
            try:
                # Process and clean each file
                cleaned_data = process_weather_file(file_path)
                cleaned_data = clean_and_rename_columns(cleaned_data)
                cleaned_data.to_csv(output_file_path, index=False)
                print(f"Saved {output_file_path}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
        else:
            print(f"{file_name} not found in {folder_path}.")


# Specify the folder containing the weather Excel files and output folder
weather_folder = "./Weather"
output_folder = "./WeatherCsv"

# Process the first 13 files and save each to a separate CSV
process_weather_folder(weather_folder, output_folder)
