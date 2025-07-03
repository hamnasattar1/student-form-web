from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

DATA_PATH = 'datasets/students_data.csv'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form.html')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        class_level = request.form['class']
        school = request.form['school']
        father = request.form['father']
        mother = request.form['mother']
        grandfather = request.form.get('grandfather', '')
        grandmother = request.form.get('grandmother', '')
        neighbours = request.form.get('neighbours', '')
        description = request.form.get('description', '')

        # Handle siblings
        siblings = []
        siblings_count = int(request.form.get('siblingsCount', 0))
        for i in range(1, siblings_count + 1):
            sibling_name = request.form.get(f'sibling_name_{i}', '')
            sibling_gender = request.form.get(f'sibling_gender_{i}', '')
            siblings.append(f"{sibling_name} ({sibling_gender})")

        # Handle friends
        friends = []
        friends_count = int(request.form.get('friendsCount', 0))
        for i in range(1, friends_count + 1):
            friend_name = request.form.get(f'friend_name_{i}', '')
            friend_gender = request.form.get(f'friend_gender_{i}', '')
            friends.append(f"{friend_name} ({friend_gender})")

        student = {
            "name": name,
            "gender": gender,
            "age": age,
            "class": class_level,
            "school": school,
            "father": father,
            "mother": mother,
            "grandfather": grandfather,
            "grandmother": grandmother,
            "siblings": ", ".join(siblings),
            "friends": ", ".join(friends),
            "neighbours": neighbours,
            "description": description
        }

        df = pd.DataFrame([student])
        os.makedirs("datasets", exist_ok=True)
        df.to_csv(DATA_PATH, mode='a', index=False, header=not os.path.exists(DATA_PATH))

        return render_template('thankyou.html', name=name)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
