from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import os
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path), 'favicon.ico')

# Data storage paths
DATA_DIR = 'data'
STUDENTS_FILE = os.path.join(DATA_DIR, 'students.json')
CLASSES_FILE = os.path.join(DATA_DIR, 'classes.json')
ATTENDANCE_FILE = os.path.join(DATA_DIR, 'attendance.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize data files if they don't exist
def initialize_data_files():
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(CLASSES_FILE):
        with open(CLASSES_FILE, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'w') as f:
            json.dump([], f)

# Load data from JSON files
def load_students():
    try:
        with open(STUDENTS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def load_classes():
    try:
        with open(CLASSES_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def load_attendance():
    try:
        with open(ATTENDANCE_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

# Save data to JSON files
def save_students(students):
    with open(STUDENTS_FILE, 'w') as f:
        json.dump(students, f, indent=2)

def save_classes(classes):
    with open(CLASSES_FILE, 'w') as f:
        json.dump(classes, f, indent=2)

def save_attendance(attendance):
    with open(ATTENDANCE_FILE, 'w') as f:
        json.dump(attendance, f, indent=2)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    all_students = load_students()
    return render_template('students.html', students=all_students)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            students = load_students()
            new_student = {
                'id': str(uuid.uuid4()),
                'name': name,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            students.append(new_student)
            save_students(students)
            flash('Student added successfully!', 'success')
            return redirect(url_for('students'))
        flash('Student name is required!', 'error')
    return render_template('add_student.html')

@app.route('/classes')
def classes():
    all_classes = load_classes()
    return render_template('classes.html', classes=all_classes)

@app.route('/classes/add', methods=['GET', 'POST'])
def add_class():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            classes = load_classes()
            new_class = {
                'id': str(uuid.uuid4()),
                'name': name,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'student_ids': []  # Initialize with empty list of students
            }
            classes.append(new_class)
            save_classes(classes)
            flash('Class added successfully!', 'success')
            return redirect(url_for('classes'))
        flash('Class name is required!', 'error')
    return render_template('add_class.html')

@app.route('/classes/<class_id>/manage_students', methods=['GET', 'POST'])
def manage_class_students(class_id):
    classes = load_classes()
    current_class = next((c for c in classes if c['id'] == class_id), None)
    
    if not current_class:
        flash('Class not found!', 'error')
        return redirect(url_for('classes'))
    
    all_students = load_students()
    
    # Ensure student_ids exists in the class object
    if 'student_ids' not in current_class:
        current_class['student_ids'] = []
    
    if request.method == 'POST':
        # Get selected student IDs from form
        selected_student_ids = request.form.getlist('student_ids')
        
        # Update class with selected students
        current_class['student_ids'] = selected_student_ids
        
        # Save updated classes
        save_classes(classes)
        flash('Students updated successfully!', 'success')
        return redirect(url_for('classes'))
    
    return render_template('manage_class_students.html', 
                          class_info=current_class, 
                          students=all_students)

@app.route('/attendance')
def attendance():
    all_attendance = load_attendance()
    all_classes = load_classes()
    return render_template('attendance.html', attendance=all_attendance, classes=all_classes)

@app.route('/attendance/take/<class_id>', methods=['GET', 'POST'])
def take_attendance(class_id):
    all_students = load_students()
    classes = load_classes()
    current_class = next((c for c in classes if c['id'] == class_id), None)
    
    if not current_class:
        flash('Class not found!', 'error')
        return redirect(url_for('attendance'))
    
    # Ensure student_ids exists in the class object
    if 'student_ids' not in current_class:
        current_class['student_ids'] = []
        
    # Get only students assigned to this class
    class_students = [s for s in all_students if s['id'] in current_class.get('student_ids', [])]
    
    if not class_students:
        flash('No students assigned to this class. Please add students to the class first.', 'error')
        return redirect(url_for('manage_class_students', class_id=class_id))
    
    if request.method == 'POST':
        date = request.form.get('date')
        attendance_records = load_attendance()
        
        # Create a new attendance session
        attendance_session = {
            'id': str(uuid.uuid4()),
            'class_id': class_id,
            'date': date,
            'records': []
        }
        
        # Process each student's attendance
        for student in class_students:
            status = request.form.get(f'status_{student["id"]}')
            if status:
                attendance_session['records'].append({
                    'student_id': student['id'],
                    'status': status
                })
        
        attendance_records.append(attendance_session)
        save_attendance(attendance_records)
        flash('Attendance recorded successfully!', 'success')
        return redirect(url_for('attendance'))
    
    return render_template('take_attendance.html', students=class_students, class_info=current_class, today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/attendance/view/<session_id>')
def view_attendance(session_id):
    attendance_records = load_attendance()
    students = load_students()
    classes = load_classes()
    
    session_data = next((s for s in attendance_records if s['id'] == session_id), None)
    
    if not session_data:
        flash('Attendance session not found!', 'error')
        return redirect(url_for('attendance'))
    
    class_info = next((c for c in classes if c['id'] == session_data['class_id']), None)
    
    # Map student IDs to names for display
    student_map = {s['id']: s['name'] for s in students}
    
    records = []
    for record in session_data['records']:
        student_name = student_map.get(record['student_id'], 'Unknown')
        records.append({
            'student_name': student_name,
            'status': record['status']
        })
    
    return render_template('view_attendance.html', 
                          records=records, 
                          date=session_data['date'], 
                          class_name=class_info['name'] if class_info else 'Unknown')

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    initialize_data_files()
    app.run(debug=True)