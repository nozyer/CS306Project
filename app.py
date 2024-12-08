from flask import Flask, request, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your database username
        password="",  # Replace with your database password
        database="YourDatabaseName"  # Replace with your database name
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_pilot_flights', methods=['POST'])
def get_pilot_flights():
    pilot_id = request.form['pilotID']
    
    # Database query
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc('GetPilotFlights', [pilot_id])
    
    flights = []
    for result in cursor.stored_results():
        flights = result.fetchall()
    
    conn.close()
    
    if flights:
        return render_template('result.html', pilot_id=pilot_id, flights=flights)
    else:
        return render_template('result.html', pilot_id=pilot_id, flights=[])

if __name__ == '__main__':
    app.run(debug=True)