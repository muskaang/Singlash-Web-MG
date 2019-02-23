from flask import Flask, redirect, url_for
from flask import render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from jinja2 import Template

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

top_answer = ''
winner = ''
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Singlash").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()

def checkstart():
    while len(client.open("Singlash").sheet1.get_all_records()) != 3:
        sheet = client.open("Singlash").sheet1
        list_of_hashes = sheet.get_all_records()
    return True

round1 = ''
round1responses = []
round2 = ''
round2responses = []
round3 = ''
round3responses = []

for player in list_of_hashes:
        for key,value in player.items():
            if key == 'GIF1':
                round1 = value
            if key == 'GIF2':
                round2 = value
            if key == 'GIF3':
                round3 = value
            if key == 'Text1':
                round1responses.append(value)
            if key == 'Text2':
                round2responses.append(value)
            if key == 'Text3':
                round3responses.append(value)

def getinputs():
    inputs = {round1: round1responses, round2: round2responses, round3:round3responses}
    inputs = str(inputs)
    return inputs 

def parseData():
    with open("outputs.txt", "w") as text_file:
        text_file.write(getinputs())

def updateScores():
    for response in round1responses:
        if userinput == response:
            list_of_hashes[round1responses.index(userinput)]['GIF1score'] += 1
            list_of_hashes[round1responses.index(userinput)]['Total'] += 1
            sheet.update_cell((round1responses.index(userinput)+2), 11, list_of_hashes[round1responses.index(userinput)]['GIF1score'])
            sheet.update_cell((round1responses.index(userinput)+2), 14, list_of_hashes[round1responses.index(userinput)]['Total'])
        
    for response in round2responses:
        if userinput == response:
            list_of_hashes[round2responses.index(userinput)]['GIF2score'] += 1
            list_of_hashes[round2responses.index(userinput)]['Total'] += 1
            sheet.update_cell((round2responses.index(userinput)+2), 12, list_of_hashes[round2responses.index(userinput)]['GIF2score'])
            sheet.update_cell((round2responses.index(userinput)+2), 14, list_of_hashes[round2responses.index(userinput)]['Total'])
        
        
    for response in round3responses:
        if userinput == response:
            list_of_hashes[round3responses.index(userinput)]['GIF3score'] += 1
            list_of_hashes[round3responses.index(userinput)]['Total'] += 1
            sheet.update_cell((round3responses.index(userinput)+2), 13, list_of_hashes[round3responses.index(userinput)]['GIF3score'])
            sheet.update_cell((round3responses.index(userinput)+2), 14, list_of_hashes[round3responses.index(userinput)]['Total'])

def checkwinner():
    scores = []
    top1 = []
    top2 = []
    top3 = []
    for player in list_of_hashes:
        scores.append(player['GIF1score'])
        scores.append(player['GIF2score'])
        scores.append(player['GIF3score'])
    scores = list(set(sorted(scores)))
    
    for player in list_of_hashes:
        if player['GIF1score'] == scores[-1]:
            top1.append(player['Text1'])
        if player['GIF1score'] == scores[-2]:
            top2.append(player['Text1'])
        if player['GIF1score'] == scores[-3]:
            top3.append(player['Text1'])
        if player['GIF2score'] == scores[-1]:
            top1.append(player['Text2'])
        if player['GIF2score'] == scores[-2]:
            top2.append(player['Text2'])
        if player['GIF2score'] == scores[-3]:
            top3.append(player['Text2'])
        if player['GIF3score'] == scores[-1]:
            top1.append(player['Text3'])
        if player['GIF3score'] == scores[-2]:
            top2.append(player['Text3'])
        if player['GIF3score'] == scores[-3]:
            top3.append(player['Text3'])
    print('top1:',top1,'\n','top2:',top2,'\n','top3:',top3)
            
checkwinner()

app = Flask(__name__)

# Landing Page
@app.route("/")
def land():
  return redirect(url_for('load'))

# Loading page whilst waiting for responses
@app.route("/load")
def load():
    return render_template('loading.html')

# When 3 confirms are in
@app.route("/ready")
def ready():
    parseData()
    if checkstart():
        return render_template('loading.html')
    else:
        return render_template('ready.html')

# Overview: Graph 
@app.route("/end")
def end():
    return render_template('overview.html')

# Question Time
@app.route("/questions")
def questions():
    return render_template('questions.html', Q1 = round1, A11 = round1responses[0], A12 = round1responses[1], A13 = round1responses[2], Q2 = round2, A21 = round2responses[0], A22 = round2responses[1], A23 = round2responses[2], Q3 = round2, A31 = round2responses[0], A32 = round2responses[1], A33 = round2responses[2])

# Scores for each question
@app.route("/score")
def score():
    return render_template('score.html' )

# Admin Page for Admins to change topic
@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route("/test")
def test():
    return render_template('test.html')

if __name__ == "__main__":
  app.run()