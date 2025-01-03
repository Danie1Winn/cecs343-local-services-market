from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from geopy.distance import geodesic
from sqlalchemy.orm import joinedload
from app.models.worker import Worker
from app.models.skill import Skill
import csv
import os

home_bp = Blueprint('home', __name__)

# Load ZIP code data globally
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

ZIP_TO_LAT_LON = load_zip_code_data()

# Function to get latitude and longitude for a ZIP code
def get_lat_lon_from_zip(zip_code):
    """Fetches latitude and longitude for a given ZIP code."""
    return ZIP_TO_LAT_LON.get(zip_code, (None, None))


@home_bp.route('/home')
def home():
    return render_template('index.html')


@home_bp.route('/')
def root():
    session.clear()
    return redirect(url_for('home.home'))


@home_bp.route('/search', methods=['GET'])
def search():
    zip_code = request.args.get('zip_code')
    service_type = request.args.get('service_type')

    # User's location based on input ZIP code
    user_location = get_lat_lon_from_zip(zip_code)

    # Dynamically fetch unique skills from the database
    all_skills = Skill.query.distinct(Skill.skill_name).all()
    skill_names = [skill.skill_name for skill in all_skills]

    # Fetch workers from the database with skills eagerly loaded
    workers = Worker.query.filter_by(is_online=True).all()

    # Filter results
    results = []
    for worker in workers:
        # Skip workers with the default ZIP code (00000)
        if worker.zip_code == "00000":
            continue

        # Calculate distance only for workers with valid ZIP codes
        worker_location = get_lat_lon_from_zip(worker.zip_code)
        if None in worker_location or None in user_location:
            continue 

        distance = geodesic(user_location, worker_location).miles

        # Include workers within their travel radius
        if distance <= worker.travel_distance:
            if service_type == "any" or any(
                service_type.lower() == skill.skill_name.lower() for skill in worker.skills
            ):
                results.append({
                    "id": worker.id,
                    "name": worker.name,
                    "skills": worker.skills,
                    "zip_code": worker.zip_code,
                    "distance": f"{distance:.1f} miles"
                })

    if not results:
        flash("No workers found matching your criteria.", "info")

    return render_template('worker_search.html', results=results, skills=skill_names)
