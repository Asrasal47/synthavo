import pandas as pd
import requests
import sys

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
