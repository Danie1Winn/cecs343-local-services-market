from flask import Blueprint, render_template, redirect, url_for

home_bp = Blueprint('home', __name__)


@home_bp.route('/home')
def home():
    return render_template('index.html')

@home_bp.route('/')
def root():
    return redirect(url_for('home.home'))