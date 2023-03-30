from flask import Flask ,render_template, request,Response ,send_file
import sqlite3
import os
import uuid
import csv
import io

currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/form.html',methods=['GET','POST'])
def form():
    return render_template('form.html')
    

@app.route('/submit-form', methods=['POST'])
def submit_form():
    id = str(uuid.uuid4())[0:15]

    date = request.form.get('date',None)
    place = request.form.get('place',None)
    name = request.form.get('name',None)
    gender = request.form.get('gender',None)
    cheif_complaint = request.form.get('complaint',None)
    # past_medical_history = request.form.get('history')

    Diabetes = request.form.get('Diabetes',None)
    HyperTension = request.form.get('HyperTension',None)
    Thyroid = request.form.get('Thyroid',None)
    Cardiovascular = request.form.get('Cardiovascular',None)
    Respiratory = request.form.get('Respiratory',None)
    Bleeding = request.form.get('Bleeding',None)

    past_dental_visit = request.form.get('visit',None)

    # personal_habits = request.form.get('habits')
    smoking = request.form.get('Smoking',None)
    Alcohol = request.form.get('Alcohol',None)
    Nothing = request.form.get('Nothing',None)



    tooth_number = request.form.get('toothnumber',None)
    decayed = request.form.get('decayed',None)
    missing = request.form.get('missing',None)
    filled = request.form.get('filled',None)
    pain = request.form.get('pain',None)
    fractured = request.form.get('fractured',None)
    mobility = request.form.get('mobility',None)
    others = request.form.get('others',None)

    # gingiva = request.form.get('gingiva')

    Calculus = request.form.get('Calculus',None)
    Stains = request.form.get('Stains',None)
    gingivitis = request.form.get('gingivitis',None)
    periodontitis = request.form.get('periodontitis',None)




    # description = request.form.get('comment')
    dental_fluorosis = request.form.get('floro',None)
    malocclusion = request.form.get('malo',None)
    oral_muscosal_lesion = request.form.get('masc',None)
    # condition = request.form.get('condition')

    Doctors_name = request.form.get('doctors_name',None)

    treatment_done = request.form.get('treatment',None)
    expalnation = request.form.get('explanation',None)



    conn = sqlite3.connect('patient.db') # create a database if it does not exist
    c = conn.cursor()

    # c.execute("DROP TABLE Patients")

    # create a table if it does not exist
    c.execute('''CREATE TABLE IF NOT EXISTS Patients
                (Patient_id TEXT, DateOfVisit TEXT, Place TEXT, Name_Of_Patient TEXT, Gender TEXT, Cheif_Complaint TEXT, Diabetes TEXT, HyperTension TEXT, Thyroid_Disorders TEXT, Cardiovascular_Diseases TEXT, Respiratory_diseases TEXT, Bleeding_Disorders TEXT, past_dental_visit TEXT, Smoking TEXT, Alcohol TEXT, `Nothing` TEXT, tooth_number TEXT, decayed_tooth TEXT, missing_tooth TEXT, filled_tooth TEXT, pain_in_tooth TEXT, fractured_tooth TEXT, mobility_tooth TEXT, others TEXT, Calculus TEXT, Stains TEXT, Gingivitis TEXT, Periodontitis TEXT, dental_fluorosis TEXT, malocclusion TEXT, oral_muscosal_lesion TEXT, Doctors_name TEXT, treatment_done TEXT, expalnation TEXT)''')

    # insert data into the table
    c.execute("INSERT INTO Patients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(id,date,place,name,gender,cheif_complaint,Diabetes,HyperTension,Thyroid,Cardiovascular,Respiratory,Bleeding,past_dental_visit,smoking,Alcohol,Nothing,tooth_number,decayed,missing,filled,pain,fractured,mobility,others,Calculus,Stains,gingivitis,periodontitis,dental_fluorosis,malocclusion,oral_muscosal_lesion,Doctors_name,treatment_done,expalnation))


    conn.commit()
    conn.close()
    return 'Form submitted successfully!'


# Define the route to display the data
@app.route('/display-data')
def display_data():
    # Connect to the database
    conn = sqlite3.connect('patient.db')

    # Get a cursor object
    cursor = conn.cursor()

    # Execute a SELECT query to get all the data from the table
    cursor.execute('SELECT * FROM Patients')

    # Fetch all the rows from the query result
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Pass the rows to a Jinja2 template for rendering
    return render_template('show.html', rows=rows)


@app.route('/download-data')
def download_data():
    # Get data from the database
    conn = sqlite3.connect('patient.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Patients')
    rows = cur.fetchall()
    conn.close()

    # Create a CSV file from the data
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID','Date','Place','Name','Gender','cheif_complaint','Diabetes','HyperTension','Thyroid_disorders','Cardiovascular_diseases','Resiratory_diseases','Bleeding_disorders','past_dental_visit','smoking','Alcohol','Nothing','tooth_number','decayed','missing','filled','pain','fractured','mobility','others','Calculus','Stains','gingivitis','periodontitis','dental_fluorosis','malocclusion','oral_muscosal_lesion','Doctors_name','treatment_done','expalnation'])  # Add column headings
    for row in rows:
        writer.writerow(row)

    # Create a response object to return the file
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'

    return response

@app.route('/FilterByDate.html',methods=['GET','POST'])
def fill():
    return render_template('FilterByDate.html')

@app.route('/filter', methods=['POST'])
def filter():
    # Get the start and end dates from the form data
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    gender = request.form.get('gender')

    conn = sqlite3.connect('patient.db')
    cursor = conn.cursor()

    # # Perform the filter query to get the filtered data
    # cursor.execute("SELECT * FROM Patients WHERE DateOfVisit BETWEEN ? AND ?", (start_date, end_date))


    if gender:
        sql_query = "SELECT * FROM Patients WHERE DateOfVisit BETWEEN ? AND ? AND Gender=?"
        filtered_data = cursor.execute(sql_query, (start_date, end_date, gender)).fetchall()
    else:
        sql_query = "SELECT * FROM Patients WHERE DateOfVisit BETWEEN ? AND ?"
        filtered_data = cursor.execute(sql_query, (start_date, end_date)).fetchall()


    # Check if the "download_csv" button was clicked
    if 'download_csv' in request.form:
        # Generate a CSV file containing the filtered data
        with open('filtered_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([i[0] for i in cursor.description]) # Write the column headers
            writer.writerows(filtered_data)

        # Return the CSV file as a download
        return send_file('filtered_data.csv', as_attachment=False) #make it as True

    # If the "download_csv" button was not clicked, render the template with the filtered data
    return render_template('show.html', rows=filtered_data)




if __name__ == '__main__':
    app.run(debug=True)
    

