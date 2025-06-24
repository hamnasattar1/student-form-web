from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

DATA_PATH = 'datasets/students_data.csv'

# Route for Welcome Page
@app.route('/')
def home():
    return render_template('index.html')

# Route for Form Page
@app.route('/form.html')
def form():
    return render_template('form.html')

# Route to Handle Form Submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        age = request.form['age']
        class_level = request.form['class']
        school = request.form['school']
        father = request.form['father']
        mother = request.form['mother']
        siblings = request.form['siblings']
        friends = request.form['friends']

        student = {
            "name": name,
            "age": age,
            "class": class_level,
            "school": school,
            "father": father,
            "mother": mother,
            "siblings": siblings,
            "friends": friends
        }

        df = pd.DataFrame([student])
        os.makedirs("datasets", exist_ok=True)
        df.to_csv(DATA_PATH, mode='a', index=False, header=not os.path.exists(DATA_PATH))

        return render_template('thankyou.html', name=name)
    except Exception as e:
        return f"Error: {str(e)}"

# Render Deployment Support
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
