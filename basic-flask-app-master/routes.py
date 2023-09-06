import os
import psycopg2
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, render_template, \
     request, url_for

CREATE_NAMES_TABLE = (
    "CREATE TABLE IF NOT EXISTS names (id SERIAL PRIMARY KEY , first_name VARCHAR(50) NOT NULL, last_name VARCHAR(50) NOT NULL);"
)

INSERT_NAMES_RETURN_ID = "INSERT INTO names (first_name, last_name) VALUES (%s, %s) RETURNING id;"

SELECT_NAMES_ALL= "SELECT * FROM names"


load_dotenv()

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.route('/')
def root():
    return render_template('index.html')

@app.post("/api/inputname")
def create_names():
    data = request.get_json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_NAMES_TABLE)
            cursor.execute(INSERT_NAMES_RETURN_ID, (first_name,last_name,))
            name_id = cursor.fetchone()[0]
    return {"id": name_id, "message": f"name {first_name, last_name} created."}, 201


@app.get("/api/getdata")
def get_names():
    with connection:
        with connection.cursor() as cursor:
             cursor.execute(SELECT_NAMES_ALL)
             result = cursor.fetchall()
    return result

@app.route('/post_json', methods=['GET', 'POST'])
def process_json():
    if request.method == 'POST':
        result = request.form
        json_result = dict(result)
        first_name = json_result["first_name"]
        last_name = json_result["last_name"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_NAMES_TABLE)
                cursor.execute(INSERT_NAMES_RETURN_ID, (first_name,last_name,))
                name_id = cursor.fetchone()[0]
        message = f"Thanks You! {first_name} have registered for the demo!', 'success'"
        flash(message)
        return redirect("/")
                  

@app.route('/result')
def result():
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(SELECT_NAMES_ALL)
                result = cursor.fetchall()
                my_dict_result = {i: result[i] for i in range(len(result))}
        return render_template("result.html", results=my_dict_result)
        
    except Exception:
        message = f"Please check your data base connection || Database table and try again', 'unexpected error'"
        flash(message)
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug = True)