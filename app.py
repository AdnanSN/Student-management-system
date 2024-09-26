from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from time import time

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    grade TEXT NOT NULL);''')
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view_students')
def view_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('view_students.html', students=students)

@app.route('/add_student', methods=['GET'])
def add_student_page():
    return render_template('add_student.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
    conn.commit()
    conn.close()

    return redirect(url_for('view_students'))

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('view_students'))

if __name__ == '__main__':
    init_db()  
    app.run(debug=True)
