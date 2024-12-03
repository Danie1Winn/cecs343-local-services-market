import sqlite3

# Path to your SQLite database
db_path = "instance/local_services.db"

# Connect to the database
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Insert test data
cursor.execute("""
    INSERT INTO workers (id, name, zip_code, travel_distance, phone_number, password) 
    VALUES (105, 'Tim Smith', '90803', 1000, '546-432-6542', 'securepassword5')
""")





# Commit changes and close
connection.commit()
connection.close()

print("Test data inserted successfully!")
