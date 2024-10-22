# Service Marketplace Application

This is a service marketplace application that connects skilled workers with employers. Users can create profiles, manage job requests, and process payments within the application.

# Installation

## Prerequisites
- Python 3.x
    To install:
        Run in terminal:
            winget install python3
        Check version / verify installation (restart of VSCode may be required):
            python --version
- Git
    To install:
        Run in terminal: 
            winget install --id Git.Git -e --source winget
    To sign in:
        Run in terminal:
            git config --global user.name "Your Name"
            git config --global user.email "your_email@example.com"

## Install packages (*not used currently*)
pip install -r requirements.txt

## Contributing

### 1. Fork the repo
- Navigate to repo on GitHub
- Click on "Fork" in the top right corner to create your own copy of the project

### 2. Clone the Fork
- git clone https://github.com/YOUR_USERNAME/cecs343-local-services-market.git

### 3. Create a new branch
- Run in terminal:
    cd cecs343-local-services-market
    git checkout -b feature/your-feature-name

### 4. Make your changes to the code. Test locally before proceeding.

### 5. Commit your changes
- Run in terminal:
    git add .
    git commit -m "Describe your changes here"

### 6. Push changes to your fork
- Run in terminal:
    git push origin feature/your-feature-name

### 7. Create a pull request
- Go to your forked repo on GitHub
- You will be prompted to create a pull request for your recently pushed branch. Click "compare & pull request"
- Add a title and description for your pull request (describe any changes made)
- Click on "Create pull request"

### 8. Sync your fork
- Run in terminal:
    git remote add upstream https://github.com/Danie1Winn/cecs343-local-services-market.git
    git fetch upstream
    git checkout main
    git merge upstream/main
- You can also sync changes under "Source control" in VSCode

# Project Structure
service_marketplace/
├── app/
│   ├── __init__.py                 # Initializes the application package
│   ├── models/                     # Contains data models
│   │   ├── __init__.py
│   │   ├── user.py                 # User model for Workers and Employers
│   │   ├── worker.py               # Worker model, including skills and availability
│   │   ├── employer.py             # Employer model, including job requests
│   │   ├── contract.py             # Contract model linking workers and employers
│   │   └── review.py               # Review model for worker ratings
│   │
│   ├── routes/                     # Contains application routes for handling requests
│   │   ├── __init__.py
│   │   ├── auth.py                 # User authentication and registration routes
│   │   ├── worker_routes.py        # Routes related to workers and their profiles
│   │   └── employer_routes.py      # Routes related to employers and job requests
│   │
│   ├── services/                   # Contains business logic and service handling
│   │   ├── __init__.py
│   │   ├── payment_service.py      # Logic for processing payments
│   │   ├── notification_service.py # Manages user notifications
│   │   └── verification_service.py # Handles phone number verification
│   │
│   ├── templates/                  # HTML templates for rendering views
│   │   ├── base.html               # Base template for the application
│   │   ├── worker_profile.html     # Template for displaying worker profiles
│   │   └── employer_dashboard.html # Template for the employer dashboard
│   │
│   ├── static/                     # Static files (CSS, JavaScript, images)
│   │   ├── css/
│   │   │   └── styles.css          # Stylesheet for the application
│   │   ├── js/
│   │   │   └── scripts.js          # JavaScript for client-side functionality
│   │   └── images/                 # Directory for image assets
│   │
│   ├── forms.py                    # Defines forms for user input and validation
│   ├── config.py                   # Configuration settings for the application
│   ├── app.py                      # Main entry point of the application
│   └── utils.py                    # Utility functions used across the application
│
├── tests/                          # Directory for test cases and testing logic
│   ├── __init__.py
│   ├── test_models.py              # Tests for data models
│   ├── test_routes.py              # Tests for application routes
│   └── test_services.py            # Tests for business logic and service handling
│
├── requirements.txt                # Lists required Python packages for the project
├── README.md                       # Project overview and file structure description
└── .gitignore                      # Specifies files and directories to ignore in Git