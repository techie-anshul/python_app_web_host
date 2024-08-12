from flask import Flask, request, render_template_string, redirect, url_for, jsonify
import pymysql

app = Flask(__name__)

# Configuration
DB_HOST = '10.128.0.4'  # Replace with the IP address of VM2
DB_USER = 'vm1_web'
DB_PASSWORD = 'password'
DB_NAME = 'student'

# Database connection
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route('/test')
def test():
    return "WSGI is working!"

# Initialize the database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Select the database
        cursor.execute('USE {};'.format(DB_NAME))

        # Create a table for students
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                roll_number VARCHAR(50) NOT NULL,
                dob DATE NOT NULL
            );
        ''')

        # Commit changes
        conn.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print("An error occurred: {}".format(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/init_db')
def init_db_route():
    try:
        init_db()
        return "Database initialized successfully."
    except Exception as e:
        return "An error occurred: {}".format(e)

# Route for adding a single student record via JSON
@app.route('/add_student_json', methods=['POST'])
def add_student_json():
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        roll_number = data.get('roll_number')
        dob = data.get('dob')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('USE {};'.format(DB_NAME))
            cursor.execute('INSERT INTO students (name, roll_number, dob) VALUES (%s, %s, %s)', (name, roll_number, dob))
            conn.commit()
            return jsonify({"message": "Student added successfully!"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred: {}".format(e)}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Request must be JSON"}), 400

# Route for adding a single student record via HTML form
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('USE {};'.format(DB_NAME))
            name = request.form['name']
            roll_number = request.form['roll_number']
            dob = request.form['dob']
            cursor.execute('INSERT INTO students (name, roll_number, dob) VALUES (%s, %s, %s)', (name, roll_number, dob))
            conn.commit()
            return redirect(url_for('menu'))
        except Exception as e:
            return "An error occurred: {}".format(e)
        finally:
            cursor.close()
            conn.close()
    
    return render_template_string('''
        <html>
        <head>
            <title>Add Student Details</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                form {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    max-width: 400px;
                    margin: 0 auto;
                }
                form input[type="text"], form input[type="date"] {
                    width: 100%;
                    padding: 8px;
                    margin: 8px 0;
                    box-sizing: border-box;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                form input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                }
                form input[type="submit"]:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <h1>Add Student Details</h1>
            <form action="/add_student" method="post">
                Name: <input type="text" name="name" required><br>
                Roll Number: <input type="text" name="roll_number" required><br>
                Date of Birth: <input type="date" name="dob" required><br>
                <input type="submit" value="Add Student">
            </form>
        </body>
        </html>
    ''')

# Route for displaying student data
@app.route('/view_students')
def view_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('USE {};'.format(DB_NAME))
        cursor.execute('SELECT name, roll_number, dob FROM students')
        students = cursor.fetchall()
    except Exception as e:
        return "An error occurred: {}".format(e)
    finally:
        cursor.close()
        conn.close()
    return render_template_string('''
        <html>
        <head>
            <title>View Students</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                table, th, td {
                    border: 1px solid #ddd;
                }
                th, td {
                    padding: 10px;
                    text-align: center;
                }
                th {
                    background-color: #f2f2f2;
                }
                a {
                    display: block;
                    width: 200px;
                    margin: 20px auto;
                    padding: 10px;
                    text-align: center;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                }
                a:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <h1>List of Students</h1>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Roll Number</th>
                        <th>Date of Birth</th>
                    </tr>
                </thead>
                <tbody>
                {% for student in students %}
                    <tr>
                        <td>{{ student[0] }}</td>
                        <td>{{ student[1] }}</td>
                        <td>{{ student[2] }}</td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
            <a href="{{ url_for('menu') }}">Back to Menu</a>
        </body>
        </html>
    ''', students=students)

# Menu route
@app.route('/')
def menu():
    return render_template_string('''
        <html>
        <head>
            <title>Student Management Menu</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                    margin-bottom: 50px;
                }
                .menu {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                .menu a {
                    display: block;
                    width: 200px;
                    margin: 10px 0;
                    padding: 10px;
                    text-align: center;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                }
                .menu a:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <h1>Student Management System</h1>
            <div class="menu">
                <a href="{{ url_for('add_student') }}">Add Student Details</a>
                <a href="{{ url_for('view_students') }}">View Students</a>
            </div>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
