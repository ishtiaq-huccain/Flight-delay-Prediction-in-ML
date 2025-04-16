import pandas as pd
import os

train_file = "./MergeTrainCsv/merged_train.csv"
train_df = pd.read_csv(train_file)

weather_folder = "./WeatherCsv"
weather_files = [os.path.join(weather_folder, f) for f in os.listdir(weather_folder) if f.endswith(".csv")]

weather_df = pd.concat([pd.read_csv(file) for file in weather_files], ignore_index=True)

print("Training Data Sample:")
print(train_df.columns)

print("\nWeather Data Sample:")
print(weather_df.columns)
