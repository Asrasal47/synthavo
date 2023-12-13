import pandas as pd
import sys

# Read the Excel/CSV file into a pandas DataFrame
def read_data(file_path):
	try:
		data = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
		return data
	except Exception as e:
		print(f"Error reading the file: {e}")
		sys.exit(1)


