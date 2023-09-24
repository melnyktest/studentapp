# Student Application

## Overview

This is a simple online tool made to help schools look after and understand student grade records easily. It lets teachers put in and save information and marks of students and create different charts to see and learn from the data.

## Installation

### Database Configuration

This application uses a MySQL database named `student`, running on port `3306`. There is no password set for accessing this database.

### Server Setup

1. Install the required Python packages:

   ```bash
   cd backend
   pip install -r requirements.txt

2. Start the server:

   ```bash
   python main.py
   ```

### Client Setup

1. Navigate to the `frontend` directory.

   ```bash
   cd frontend
   ```
2. Install Ember.js and its dependencies:

   ```bash
   npm install
   ```

3. Start the Ember development server:

   ```bash
   npm run start
   ```

4. Access the web application by opening a web browser and visiting `http://localhost:4200`.


## API Endpoints

Students
- Add Student and Grade: 'POST /student'
- Retrieve All Students: 'GET /student'
- Retrieve Students from start_id to end_id: 'GET /student/<start_id>/<end_id>'
- Delete Student: 'GET /student/delete/<student_id>'

Statistics
- Student General Average per Quarter: 'GET /statistics/studentperquarter/<student_id>'
- Subject Grades per Quarter: 'GET /statistics/courseperquarter/<course_name>'
- Retrieve All Courses Grade according to Quarter ID: 'GET /statistics/quartergradeforcourses/<quarter_id>'

Quarters
- Retrieve All Quarters: 'GET /quarter'

## Contributing

For contributing to this project, please send an email to the project administrator or create a Pull Request.

## Contact Information
Name: Michael Melnyk
Email: Melnyk001@hotmail.com
