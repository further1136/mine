from flask import Flask, render_template, request, jsonify
import sqlite3
import random

app = Flask(__name__, template_folder='htm/index.htm')


# Function to fetch country information from the database
def fetch_country_info(country_name):
    conn = sqlite3.connect('countries.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM countries WHERE name=?", (country_name,))
    country_info = cursor.fetchone()
    conn.close()
    return country_info

# Function to generate a random question
def generate_question(country_info):
    questions = [
        f"What is the capital of {country_info[0]}?",
        f"What is the population of {country_info[0]}?",
        # Add more questions here...
    ]
    return random.choice(questions), country_info[1]

@app.route('/')
def index():
    country_name = random.choice(['United States', 'China', 'India', 'Brazil', 'Russia', 'Japan', 'Mexico', 'Germany', 'Egypt', 'Australia'])
    country_info = fetch_country_info(country_name)
    question, current_answer = generate_question(country_info)
    return render_template('index.html', question=question, current_answer=current_answer)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_answer = request.form['answer'].strip().lower()
    correct_answer = request.form['correct_answer'].lower()
    if user_answer == correct_answer:
        return jsonify({'result': 'correct'})
    else:
        return jsonify({'result': 'incorrect', 'correct_answer': correct_answer})

if __name__ == '__main__':
    app.run(debug=True)