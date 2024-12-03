import csv
import os

def load_zip_code_data():
    """Loads ZIP code to latitude/longitude mapping from a CSV file."""
    zip_to_lat_lon = {}
    csv_path = os.path.join(os.path.dirname(__file__), "../static/data/zip_codes.csv")
    
    # Open and read the CSV
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            zip_to_lat_lon[row['zip']] = (float(row['lat']), float(row['lng']))
    return zip_to_lat_lon
