import csv
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

players = {}
game_started = False
game_ended = False
questions_and_dares = []

def load_questions_and_dares():
    with open('data.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            questions_and_dares.append(row)

@app.route('/', methods=['GET', 'POST'])
def index():
    global game_started
    if not game_started and len(players) >= 2:
        game_started = True
        load_questions_and_dares()
    if game_started:
        return redirect(url_for('game'))
    if request.method == 'POST':
        name = request.form.get('name')
        if name and name not in players:
            players[name] = {'score': 0}
            session['player'] = name
    return render_template('index.html', players=players)

@app.route('/logoff', methods=['GET'])
def logoff():
    if 'player' in session:
        players.pop(session['player'], None)
        session.pop('player', None)
    return redirect(url_for('index'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    global game_ended

    if not game_started:
        return redirect(url_for('index'))
    
    if game_ended:
        return redirect(url_for('end_game'))
    
    player = players[session['player']]
    
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == 'truth' or choice == 'dare':
                player['score'] += 1
        if player['score'] > 9:
            game_ended = True
            return redirect(url_for('end_game'))
    
    question_dare = random.choice(questions_and_dares)
    return render_template('game.html', question=question_dare[0], dare=question_dare[1])

@app.route('/end_game', methods=['GET'])
def end_game():
    return render_template('end_game.html', players=players)

@app.route('/restart')
def restart():
    players = {}
    game_ended = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
