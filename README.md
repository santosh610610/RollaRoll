# RollaRoll - Colorful Music Class Attendance Tracker

A vibrant and simple, web-based attendance tracking system designed for tutors to manage students and classes.

![RollaRoll](https://img.shields.io/badge/RollaRoll-Attendance%20Tracker-FF6B6B)

## Features

- 🎨 Colorful, modern interface with the Borel Google Font
- 👥 Manage students (add, view)
- 🎵 Manage classes (add, view)
- ✅ Take attendance with multiple status options (present, absent, late, excused)
- 📊 View attendance records by date and class
- 🔄 Track attendance history
- 🔗 Assign specific students to specific classes

## Installation

1. Make sure you have Python 3.7+ installed
2. Clone this repository or download the files
3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Running the Application

1. Navigate to the project directory
2. Run the Flask application:

```
python app.py
```

3. Open your web browser and go to `http://127.0.0.1:5000/`

## Usage

1. First, add students through the "Students" section
2. Create classes through the "Classes" section
3. For each class, assign specific students using the "Manage Students" button
4. Take attendance by selecting a class from the "Attendance" section
5. View past attendance records from the "Attendance" section

## Workflow

The application follows this workflow:
1. Create students (name only)
2. Create classes (e.g., Piano Beginner, Guitar Advanced)
3. Assign students to specific classes
4. Take attendance for each class session
5. View attendance history by class and date

## Design Features

- Vibrant color scheme with primary colors:
  - Primary: #FF6B6B (coral)
  - Secondary: #4ECDC4 (teal)
  - Accent: #FFE66D (yellow)
  - Dark: #1A535C (dark teal)
  - Light: #F7FFF7 (off-white)
- Google Font "Borel" for headings
- Card-based design for main navigation
- Responsive layout that works on mobile and desktop
- Animated elements for better user experience

## Data Storage

All data is stored in JSON files in the `data` directory:
- `students.json`: Student information
- `classes.json`: Class information (including student assignments)
- `attendance.json`: Attendance records

## License

This project is open source and available for personal and educational use.
