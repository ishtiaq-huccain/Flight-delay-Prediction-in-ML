import pandas as pd
import os
from calendar import month_abbr

filename_to_month = {
    "1.csv": 7,   # July
    "2.csv": 8,   # August
    "3.csv": 9,   # September
    "4.csv": 10,  # October
    "5.csv": 11,  # November
    "6.csv": 12,  # December
    "7.csv": 1,   # January
    "9.csv": 3,   # March
    "10.csv": 4,  # April
    "11.csv": 5,  # May
    "12.csv": 6,  # June
}

def preprocess_weather_file(file_path, month, year):
    try:
        weather_data = pd.read_csv(file_path, encoding='ISO-8859-1')
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

    weather_data.columns = [col.strip() for col in weather_data.columns]

    print(f"Columns in {file_path}: {weather_data.columns.tolist()}")

    month_name = month_abbr[month]
    time_column = [col for col in weather_data.columns if f"Time ({month_name})" in col]

    if not time_column:
        print(f"Time column for '{month_name}' not found in {file_path}")
        return None
    time_column = time_column[0]

    print(f"Sample Time values in {file_path}: {weather_data[time_column].head()}")

    try:
        weather_data['datetime'] = pd.to_datetime(
            weather_data[time_column].astype(str) + f"-{month:02d}-{year}",
            format='%d-%m-%Y',
            errors='coerce'
        )
    except Exception as e:
        print(f"Error creating datetime column in {file_path}: {e}")
        return None

    weather_data.drop(columns=[time_column], inplace=True)

    return weather_data

def merge_weather_data(weather_folder, year):
    weather_files = [os.path.join(weather_folder, file) for file in os.listdir(weather_folder) if file.endswith('.csv')]
    combined_data = pd.DataFrame()

    for file_path in weather_files:
        file_name = os.path.basename(file_path)
        print(f"Processing file: {file_name}")

        month = filename_to_month.get(file_name, None)
        if month is None:
            print(f"Month could not be identified for file: {file_name}")
            continue

        weather_data = preprocess_weather_file(file_path, month, year)
        if weather_data is not None:
            combined_data = pd.concat([combined_data, weather_data], ignore_index=True)
        else:
            print(f"Skipping file due to errors: {file_name}")

    return combined_data

weather_folder = "./WeatherCsv"
output_file = "./MergeCsvWeather/merged_weather.csv"
year = 2023

os.makedirs(os.path.dirname(output_file), exist_ok=True)

merged_weather_data = merge_weather_data(weather_folder, year)

if not merged_weather_data.empty:
    merged_weather_data.to_csv(output_file, index=False)
    print(f"Weather data merged and saved to {output_file}")
else:
    print("No valid data to save.")
