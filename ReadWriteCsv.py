from docx import Document
import pandas as pd
import os
import json


def flatten_json(nested_json):
    """Flattens a nested JSON object recursively."""
    out = {}

    def flatten(element, name=''):
        if isinstance(element, dict):
            for key in element:
                flatten(element[key], name + key + '.')
        elif isinstance(element, list):
            for i, item in enumerate(element):
                flatten(item, name + str(i) + '.')
        else:
            out[name[:-1]] = element

    flatten(nested_json)
    return out


def parse_json_string(json_string):
    """Safely parse a JSON string into a dictionary."""
    if isinstance(json_string, str):
        try:
            return json.loads(json_string.replace("'", '"'))  # Replace single quotes for valid JSON
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {json_string}")
            return {}
    return json_string if isinstance(json_string, dict) else {}


def process_json_entry(entry):
    """Flatten and process a single JSON entry."""
    flat_entry = {}
    for key, value in entry.items():
        if isinstance(value, (dict, str)):
            parsed_value = parse_json_string(value)
            flat_entry.update(flatten_json(parsed_value))
        else:
            flat_entry[key] = value
    return flat_entry


def process_docx(file_path):
    """Extract JSON data from a Word document and process it."""
    doc = Document(file_path)
    extracted_data = []

    for paragraph in doc.paragraphs:
        paragraph_text = paragraph.text.strip()  # Remove extra spaces
        if not paragraph_text:  # Skip empty paragraphs
            continue

        try:
            # Parse JSON data
            json_data = json.loads(paragraph_text)
            if isinstance(json_data, list):  # Expecting a JSON array
                for entry in json_data:
                    if isinstance(entry, dict):  # Process only valid JSON objects
                        flattened_entry = process_json_entry(entry)
                        extracted_data.append(flattened_entry)
                    else:
                        print(f"Skipping non-dict entry: {entry}")
            else:
                print(f"Skipping non-list JSON: {paragraph_text}")

        except json.JSONDecodeError:
            print(f"Skipping non-JSON paragraph: {paragraph_text}")
    return extracted_data


def save_to_csv(data, output_path):
    """Save processed data to a CSV file."""
    if data:
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
    else:
        print(f"No data to save for {output_path}")


def process_docx_folder(folder_path, output_folder):
    """Process all DOCX files in a folder and save to CSV."""
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".docx"):
            file_path = os.path.join(folder_path, file_name)
            output_file_path = os.path.join(output_folder, file_name.replace(".docx", ".csv"))

            try:
                data = process_docx(file_path)
                save_to_csv(data, output_file_path)
            except Exception as e:
                print(f"Error processing {file_name}: {e}")


# Specify input and output folders
input_train_folder = "./Train"
output_train_folder = "./TrainCsv"
input_test_folder = "./Test"
output_test_folder = "./TestCsv"

# Process Train and Test folders
process_docx_folder(input_train_folder, output_train_folder)
process_docx_folder(input_test_folder, output_test_folder)
