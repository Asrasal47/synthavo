import pandas as pd
import requests
import json
import sys
from datetime import datetime

# Read the Excel/CSV file into a pandas DataFrame
def read_data(file_path):
	try:
		data = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
		return data
	except Exception as e:
		print(f"Error reading the file: {e}")
		sys.exit(1)

# Make a POST request to the API endpoint
def send_to_api(api_url, json_data):
	try:
		response = requests.post(api_url, json=json_data)
		response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
		print("Data sent successfully to the API.")
	except requests.exceptions.RequestException as e:
		print(f"Error sending data to the API: {e}")
		sys.exit(1)

def process_data(data):
	json_data = {}

	for _, row in data.iterrows():
		assembly_index = row['Assembly-Index']
		if not pd.isna(row['Assembly-Name']):
			assembly_name = row['Assembly-Name']
			if not pd.isna(row['replaced by']):
				assembly_name = row['replaced by']
		assembly_part = row['Assembly-Part']
		if not pd.isna(row['replaced by']):
			assembly_part = row['replaced by']
		valid_from = row['Valid from']
		valid_to = row['Valid to']
		replaced_by = row['replaced by']

		# Skip rows with empty Assembly-Part
		if pd.isna(assembly_part):
			continue
		# Convert date strings to datetime objects for comparison
		valid_from_date = datetime.strptime(valid_from, "%m/%d") if not pd.isna(valid_from) else None
		valid_to_date = datetime.strptime(valid_to, "%m/%d") if not pd.isna(valid_to) else None

		# Check if the part is valid based on date range
		current_date = datetime.now()
		if valid_from_date and valid_to_date and (current_date < valid_from_date or current_date > valid_to_date):
			continue

		# Check if the part is replaced by a newer version
		if not pd.isna(replaced_by):
			continue  # Skip, as it's replaced by a newer version

		# Add part information to the JSON object
		if assembly_part not in json_data:
			json_data[assembly_part] = {'assembly_names': []}
		if assembly_name not in json_data[assembly_part]['assembly_names']:
			json_data[assembly_part]['assembly_names'].append(assembly_name)

	return json_data

if __name__ == "__main__":
	# Check if the file path is provided as a command-line argument
	if len(sys.argv) != 2:
		print("Usage: python script.py <file_path>")
		sys.exit(1)

	# API endpoint
	api_endpoint = "http://<base-url>/addPartInformation"

	# Read data from the provided file
	file_path = sys.argv[1]
	input_data = read_data(file_path)

	# Process the data and create the JSON object
	json_data = process_data(input_data)

	# Send the JSON object to the API endpoint
	send_to_api(api_endpoint, json_data)


#Existing issues: Last Assembly name is missing from the 1st part of the last assembly because it was replaced by another part and i could have fixed this with some more time.
# also I would definitely worked more in readability of the final data if i had more time and experience with python.