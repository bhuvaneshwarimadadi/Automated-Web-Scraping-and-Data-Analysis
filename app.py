from flask import Flask, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

try:
    # Specify the auth_plugin to use 'mysql_native_password'
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Bhumi@2003',
        database='web_scraping_project',
        auth_plugin='mysql_native_password'  # This line specifies the plugin
    )
    if connection.is_connected():
        print("Connected to MySQL database")

except Error as e:
    print("Error while connecting to MySQL:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/books', methods=['GET'])
def get_books():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, TimeStamp, Author, Price, Type FROM output")
    results = cursor.fetchall()
    cursor.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
