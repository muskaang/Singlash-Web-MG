from flask import Flask
from flask import render_template

app = Flask(__name__)

# Landing Page
@app.route("/")
def land():
  return render_template('landing.html')

# Loading page whilst waiting for responses
@app.route("/load")
def load():
  return render_template('loading.html')

# When 3 confirms are in
@app.route("/ready")
def ready():
  return render_template('ready.html')

# Overview: Graph 
@app.route("/end")
def end():
  return render_template('overview.html')

# Question Time
@app.route("/questions")
def questions():
  return render_template('questions.html')

# Scores for each question
@app.route("/score")
def score():
  return render_template('score.html')

# Admin Page for Admins to change topic
@app.route("/admin")
def admin():
  return render_template('admin.html')

if __name__ == "__main__":
  app.run()