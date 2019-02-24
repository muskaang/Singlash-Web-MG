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
parseData()
def updateScoresA11():
    list_of_hashes[0]['GIF1score'] += 1
    list_of_hashes[0]['Total'] += 1
    sheet.update_cell((2), 11, list_of_hashes[0]['GIF1score'])
    sheet.update_cell((2), 14, list_of_hashes[0]['Total'])

def updateScoresA12():
    list_of_hashes[1]['GIF1score'] += 1
    list_of_hashes[1]['Total'] += 1
    sheet.update_cell((3), 11, list_of_hashes[1]['GIF1score'])
    sheet.update_cell((3), 14, list_of_hashes[1]['Total'])
    
def updateScoresA13():
    list_of_hashes[2]['GIF1score'] += 1
    list_of_hashes[2]['Total'] += 1
    sheet.update_cell((4), 11, list_of_hashes[1]['GIF1score'])
    sheet.update_cell((4), 14, list_of_hashes[1]['Total'])

def updateScoresA21():
    list_of_hashes[0]['GIF2score'] += 1
    list_of_hashes[0]['Total'] += 1
    sheet.update_cell((2), 12, list_of_hashes[0]['GIF2score'])
    sheet.update_cell((2), 14, list_of_hashes[0]['Total'])

def updateScoresA22():
    list_of_hashes[1]['GIF2score'] += 1
    list_of_hashes[1]['Total'] += 1
    sheet.update_cell((3), 12, list_of_hashes[1]['GIF2score'])
    sheet.update_cell((3), 14, list_of_hashes[1]['Total'])
    
def updateScoresA23():
    list_of_hashes[2]['GIF2score'] += 1
    list_of_hashes[2]['Total'] += 1
    sheet.update_cell((4), 12, list_of_hashes[2]['GIF2score'])
    sheet.update_cell((4), 14, list_of_hashes[2]['Total'])

def updateScoresA31():
    list_of_hashes[0]['GIF3score'] += 1
    list_of_hashes[0]['Total'] += 1
    sheet.update_cell((2), 13, list_of_hashes[0]['GIF3score'])
    sheet.update_cell((2), 14, list_of_hashes[0]['Total'])

def updateScoresA32():
    list_of_hashes[1]['GIF3score'] += 1
    list_of_hashes[1]['Total'] += 1
    sheet.update_cell((3), 13, list_of_hashes[1]['GIF3score'])
    sheet.update_cell((3), 14, list_of_hashes[1]['Total'])
    
def updateScoresA33():
    list_of_hashes[2]['GIF3score'] += 1
    list_of_hashes[2]['Total'] += 1
    sheet.update_cell((4), 13, list_of_hashes[2]['GIF3score'])
    sheet.update_cell((4), 14, list_of_hashes[2]['Total'])

def getScoreA11():
    return list_of_hashes[0]['GIF1score']

def getScoreA12():
    return list_of_hashes[1]['GIF1score']

def getScoreA13():
    return list_of_hashes[2]['GIF1score']


def getScoreA21():
    return list_of_hashes[0]['GIF2score']

def getScoreA22():
    return list_of_hashes[1]['GIF2score']

def getScoreA23():
    return list_of_hashes[2]['GIF2score']

def getScoreA31():
    return list_of_hashes[0]['GIF3score']

def getScoreA32():
    return list_of_hashes[1]['GIF3score']

def getScoreA33():
    return list_of_hashes[2]['GIF3score']
scores = []
top1 = []
top2 = []
top3 = []
for player in list_of_hashes:
    try:
        scores.append(int(player['GIF1score']))
        scores.append(int(player['GIF2score']))
        scores.append(int(player['GIF3score']))
    except:
        pass
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



def getScoreP1():
    return round(list_of_hashes[0]['Total']/(list_of_hashes[0]['Total']+ list_of_hashes[1]['Total']+ list_of_hashes[2]['Total']) * 100,2)

def getScoreP2():
    return round(list_of_hashes[1]['Total']/(list_of_hashes[0]['Total']+ list_of_hashes[1]['Total']+ list_of_hashes[2]['Total']) * 100,2)

def getScoreP3():
    return round(list_of_hashes[2]['Total']/(list_of_hashes[0]['Total']+ list_of_hashes[1]['Total']+ list_of_hashes[2]['Total']) * 100,2)

def P1user():
    return list_of_hashes[0]['Username']

def P2user():
    return list_of_hashes[1]['Username']

def P3user():
    return list_of_hashes[2]['Username']

app = Flask(__name__)

# Landing Page
@app.route("/land")
def land():
    return render_template('landing.html')

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
    return render_template('questions.html', Q1 = round1, A11 = round1responses[0], A12 = round1responses[1], A13 = round1responses[2])

@app.route("/question2")
def question2():
    return render_template('question2.html', Q2 = round2, A21 = round2responses[0], A22 = round2responses[1], A23 = round2responses[2])

@app.route("/analytics1")
def analytics1():
    return render_template('analytics1.html', Q1 = round1, A11 = round1responses[0], A12 = round1responses[1], A13 = round1responses[2], A11P = updateScoresA11(), scoreA11 = getScoreA11(), scoreA12 = getScoreA12(), scoreA13 = getScoreA13())

@app.route("/analytics12")
def analytics12():
    return render_template('analytics1.html', Q1 = round1, A11 = round1responses[0], A12 = round1responses[1], A13 = round1responses[2], A12P = updateScoresA12(), scoreA11 = getScoreA11(), scoreA12 = getScoreA12(), scoreA13 = getScoreA13())

@app.route("/analytics13")
def analytics13():
    return render_template('analytics1.html', Q1 = round1, A11 = round1responses[0], A12 = round1responses[1], A13 = round1responses[2], A13P = updateScoresA13(), scoreA11 = getScoreA11(), scoreA12 = getScoreA12(), scoreA13 = getScoreA13())


@app.route("/analytics2")
def analytics2():
    return render_template('analytics2.html', Q2 = round2, A21 = round2responses[0], A22 = round2responses[1], A23 = round2responses[2], A21P = updateScoresA21(), scoreA21 = getScoreA21(), scoreA22 = getScoreA12(), scoreA23 = getScoreA13())

@app.route("/analytics22")
def analytics22():
    return render_template('analytics2.html', Q2 = round2, A21 = round2responses[0], A22 = round2responses[1], A23 = round2responses[2], A22P = updateScoresA22(), scoreA21 = getScoreA21(), scoreA22 = getScoreA12(), scoreA23 = getScoreA13())

@app.route("/analytics23")
def analytics23():
    return render_template('analytics2.html', Q2 = round2, A21 = round2responses[0], A22 = round2responses[1], A23 = round2responses[2], A23P = updateScoresA23(), scoreA21 = getScoreA21(), scoreA22 = getScoreA12(), scoreA23 = getScoreA13())

@app.route("/analytics3")
def analytics3():
    return render_template('analytics3.html', Q3 = round3, A31 = round3responses[0], A32 = round3responses[1], A33 = round3responses[2], A31P = updateScoresA31(), scoreA31 = getScoreA31(), scoreA32 = getScoreA32(), scoreA33 = getScoreA33())

@app.route("/analytics32")
def analytics32():
    return render_template('analytics3.html', Q3 = round3, A31 = round3responses[0], A32 = round3responses[1], A33 = round3responses[2], A32P = updateScoresA32(), scoreA31 = getScoreA31(), scoreA32 = getScoreA32(), scoreA33 = getScoreA33())

@app.route("/analytics33")
def analytics33():
    return render_template('analytics3.html', Q3 = round3, A31 = round3responses[0], A32 = round3responses[1], A33 = round3responses[2], A33P = updateScoresA33(), scoreA31 = getScoreA31(), scoreA32 = getScoreA32(), scoreA33 = getScoreA33())

@app.route("/question3")
def question3():
    return render_template('question3.html', Q3 = round3, A31 = round3responses[0], A32 = round3responses[1], A33 = round3responses[2])

@app.route("/winner")
def winner():
    return render_template('winner.html', P1 = getScoreP1() , P2 = getScoreP2() , P3 = getScoreP3(), P1user = P1user(), P2user = P2user(), P3user = P3user() )


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