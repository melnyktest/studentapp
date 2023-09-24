from bottle import run, request, response, route, app, hook
from db_setup import *
from bottle_cors_plugin import cors_plugin
from db_config import DB_URL
import json
import dataset
from db_course_mapping import SubjectTransformer

########################################### DB_SETTING #######################################################################

db = dataset.connect(DB_URL)

# Get Tables from database
student_table = db['students']
grades_table = db['grades']
quarters_table = db['quarters']

course_mapping = SubjectTransformer()
print(course_mapping.subject_to_number('mathmatics'))
############################################# ROUTES #########################################################################

#ADD STUDENT AND GRADE
@route('/student', 'POST')
def add_student_grade():
    
    # Receive Data
    data = request.json
    name = data.get('name')
    class_name = data.get('class_name')
    birth_date = data.get('birth_date')
    
    year = int(data.get('year'))
    quarter = data.get('quarter')
    mathmatics_grade = int(data.get('mathmatics'))
    computer_grade = int(data.get('computer'))
    literature_grade = int(data.get('literature'))

    # Grade Validations
    grades = [mathmatics_grade, computer_grade, literature_grade]
    for grade in grades:
        is_valid, error_response = validate_grade(grade)
        if not is_valid:
            response.status = 400 
            return json.dumps(error_response)

    # Quarter Validation
    quarter = data.get('quarter')
    is_valid, error_response = validate_quarter(quarter)
    if not is_valid:
        response.status = 400 
        return json.dumps(error_response)
    
    # Add student & get student_id
    student_id = add_student(name, birth_date, class_name)

    # Add quarter & get quarter_id
    quarter_id = add_quarter(year, quarter)
    
    print(quarter_id)
    # Add grade
    add_grade(student_id, quarter_id, course_mapping.subject_to_number("mathmatics"), mathmatics_grade)
    add_grade(student_id, quarter_id, course_mapping.subject_to_number("computer"), computer_grade)
    add_grade(student_id, quarter_id, course_mapping.subject_to_number("literature"), literature_grade)

    response.status = 200
    return json.dumps({"status": "success", "message": "Data has been added successfully!"})

def validate_quarter(quarter):
    print(quarter)
    valid_quarters = ["Q1", "Q2", "Q3", "Q4"]
    if quarter not in valid_quarters:
        return False, {"status": "error", "message": "Quarter must be among [Q1, Q2, Q3, Q4]"}
    return True, {}

def validate_grade(grade):
    if not (0 <= grade <= 10):
        return False, {"status": "error", "message": "Grade must be between 0 and 10"}
    return True, {}

def add_student(name, birth_date, class_name):
    
    # Check existing student
    existing_student = student_table.find_one(name=name, birth_date=birth_date)
    
    if existing_student:
        return existing_student['id']
    else: 
        return student_table.insert(dict(name=name, birth_date=birth_date, class_name=class_name))

def add_quarter(year, quarter):
    
    # Check existing quarters
    existing_quarter = quarters_table.find_one(year=year, quarter=quarter)

    if existing_quarter:
        return existing_quarter['id']
    else:
        return quarters_table.insert(dict(year=year, quarter=quarter))

def add_grade(student_id, quarter_id, course_id, grade):

    # Check existing grades
    existing_grade = grades_table.find_one(student_id=student_id, quarter_id=quarter_id, course_id=course_id)
    
    if existing_grade:
        grades_table.update(dict(id=existing_grade['id'], grade=grade), ['id'])
    else:
        grades_table.insert(dict(student_id=student_id, quarter_id=quarter_id, course_id=course_id, grade=grade))

# RETRIEVE ALL STUDENT
@route('/student', method='GET')
def get_all_students():
    students_list = []
    try:
        # Fetch all records from the 'students' table
        for student in student_table.all():
            student_dict = {
                "id": student['id'],
                "name": student['name'],
                "birth_date": str(student['birth_date']),
                "class_name": student['class_name']
            }
            students_list.append(student_dict)

        response.status = 200  
        return json.dumps({"status": "success", "data": students_list})

    except Exception as e:
        response.status = 500 
        return json.dumps({"status": "error", "message": "An error occurred while fetching students"})

        
# DELETE A STUDENT
@route('/student/delete/<student_id>', method='GET')
def remove_student_and_grade(student_id):
    try:
        # Fetch the student to delete
        student = student_table.find_one(id=student_id)
        
        if not student:
            response.status = 404
            return json.dumps({"status": "error", "message": "Student not found"})
        
        # Delete the associated grades of the student from grades_table
        grades_table.delete(student_id=student_id)
        
        # Delete the student from student_table
        student_table.delete(id=student_id)
        
        response.status = 200 
        return json.dumps({"status": "success", "message": "Student and associated grades have been successfully deleted"})
        
    except Exception as e:
        print(f"Error occurred: {e}")
        response.status = 500 
        return json.dumps({"status": "error", "message": "An error occurred while deleting the student and associated grades"})

# RETRIEVE ALL STUDENTS FROM START_ID TO LAST_ID
@route('/student/<start_id>/<end_id>', method='GET')
def get_all_students_from_startid_to_endid(start_id, end_id):
    students_list = []
    try:
        # Convert start_id and end_id to integers
        start_id = int(start_id)
        end_id = int(end_id)

        # Find the maximum id in the student_table
        max_id = max([s['id'] for s in student_table] + [0])  # + [0] is to avoid max() failing on empty lists

        # Validate the fetch range
        if end_id < start_id or start_id < 1:
            response.status = 400
            return json.dumps({"status": "error", "message": "Invalid ID range, start_id should be 1 or greater and less than or equal to end_id"})
        
        if start_id > max_id:
            response.status = 200
            return json.dumps({"status": "success", "data": students_list})  # Return an empty list

        if max_id < end_id:
            end_id = max_id
        # Fetch all records from the 'students' table within the ID range
        for student in [s for s in student_table if start_id <= s['id'] <= end_id]:
            student_dict = {
                "id": student['id'],
                "name": student['name'],
                "birth_date": str(student['birth_date']),
                "class_name": student['class_name']
            }
            students_list.append(student_dict)
        
        if not students_list:
            response.status = 404
            return json.dumps({"status": "error", "message": "No students found with provided IDs"})
        
        response.status = 200
        return json.dumps({"status": "success", "data": students_list})
        
    except ValueError:
        response.status = 400
        return json.dumps({"status": "error", "message": "Invalid ID range, please provide valid integers"})
    except Exception as e:
        response.status = 500
        return json.dumps({"status": "error", "message": "An error occurred while fetching students"})

# STUDENT GENERAL AVERAGE PER QUARTER
@route('/statistics/studentperquarter/<student_id>', method='GET')
def get_student_avggrades_per_quarter(student_id):
    try:
    
        # Check if student exists
        student = student_table.find_one(id=student_id)
        if not student:
            response.status = 404  # Not Found
            return json.dumps({"status": "error", "message": "Student not found"})
        
        # Fetch all records with given student id
        grades = list(grades_table.find(student_id=student_id))
        if not grades:
            response.status = 404
            return json.dumps({"status": "error", "message": "Grades not found for the given student_id"})
        
        averages = []
        # Fetch all quarter_ids from the quarters_table.
        quarter_ids = set(quarter['id'] for quarter in quarters_table.all())
    
        # Getting all pairs of (year-quarter, avg mark)
        for quarter_id in quarter_ids:
        
            quarter_grades = [grade['grade'] for grade in grades if grade['quarter_id'] == quarter_id]

            if not quarter_grades:  
                continue

            avg_grade = sum(quarter_grades) / len(quarter_grades)
        
            quarter_info = quarters_table.find_one(id=quarter_id)
        
            quarter_str = f"{quarter_info['year']}-{quarter_info['quarter']}"

            averages.append({
                "category": quarter_str,
                "value1": avg_grade
            })
        averages = sorted(averages, key=lambda x: (
            int(x['category'].split('-')[0]),  
            int(x['category'].split('-')[1][1:])    
        ))
        response.status = 200 
        return json.dumps({"status": "success", "data": averages})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        response.status = 500  
        return json.dumps({"status": "error", "message": "An error occurred while fetching the average grade"})

# SUBJECT GRADES PER QUARTER (FILTER PER SUBJECT)
@route('/statistics/courseperquarter/<course_name>', method='GET')
def get_course_avg_grade_per_quarter(course_name):

    try:
        # Check if course exists
        course_grades = list(grades_table.find(course_id=course_mapping.subject_to_number(course_name)))
        if not course_grades:
            response.status = 404 
            return json.dumps({"status": "error", "message": f"No grades found for the course: {course_name}"})

        averages = []
        # Fetch all unique quarter_ids from the course_grades.
        quarter_ids = set(grade['quarter_id'] for grade in course_grades)

        for quarter_id in quarter_ids:
            quarter_grades = [grade['grade'] for grade in course_grades if grade['quarter_id'] == quarter_id]

            if not quarter_grades:
                continue

            avg_grade = sum(quarter_grades) / len(quarter_grades)

            quarter_info = quarters_table.find_one(id=quarter_id)
            quarter_str = f"{quarter_info['year']}-{quarter_info['quarter']}"
            
            averages.append({
                "category": quarter_str,
                "value1": avg_grade
            })
        
        averages = sorted(averages, key=lambda x: (
            int(x['category'].split('-')[0]),  
            int(x['category'].split('-')[1][1:])    
        ))
        
        response.status = 200 
        return json.dumps({"status": "success", "data": averages})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        response.status = 500
        return json.dumps({"status": "error", "message": "An error occurred while fetching the average grade"})


# RETRIEVE ALL QUARTERS (AVAILABLE)
@route('/quarter', method='GET')
def get_all_quarters():
    try:
        # Fetch all quarters
        quarters_list = list(quarters_table.all())
        
        if not quarters_list:
            response.status = 404 
            return json.dumps({"status": "error", "message": "No quarters found"})
        
        # Sort the quarters based on year and quarter
        sorted_quarters_list = sorted(quarters_list, key=lambda x: (x['year'], int(x['quarter'][1:])))
        
        # Prepare the response
        response_list = [{"id": quarter['id'], "year": quarter['year'], "quarter": quarter['quarter']} for quarter in sorted_quarters_list]
        
        response.status = 200 
        return json.dumps({"status": "success", "data": response_list})
    
    except Exception as e:
        response.status = 500
        return json.dumps({"status": "error", "message": "An error occurred while fetching the quarters"})
    

# RETRIEVE ALL COURSES GRADE ACCORDING TO QUARTER_ID
@route('/statistics/quartergradeforcourses/<quarter_id>', method='GET')
def get_quarter_grade_for_courses(quarter_id):
    try:
    
        quarter_id = quarter_id
        
        course_names = {"mathmatics", "computer", "literature"}
        
        grade_records = list(grades_table.find(quarter_id=quarter_id))

        
        if not grade_records:
            response.status = 404 
            return json.dumps({"status": "error", "message": f"No grades found for the quarter_id: {quarter_id}"})
        
        averages = []
        
        for course_name in course_names:
            # Filtering the grade records for the current course_name
            subject_grades = [grade['grade'] for grade in grade_records if grade['course_id'] == course_mapping.subject_to_number(course_name)]
            
            if not subject_grades:
                continue 
            
            avg_grade = sum(subject_grades) / len(subject_grades)
            averages.append({
                "category": course_name,
                "value1": avg_grade
            })
        
        if not averages:
            response.status = 404  
            return json.dumps({"status": "error", "message": f"No averages found for the quarter_id: {quarter_id}"})
        
        response.status = 200
        return json.dumps({"status": "success", "data": averages})
    
    except Exception as e:
        response.status = 500  
        return json.dumps({"status": "error", "message": "An error occurred while fetching the average grades per subject"})

#########################################################  MAIN  #####################################################################

app = app()
app.install(cors_plugin(origins=['*']))

if __name__ == '__main__':
    run(app, host='localhost', port=8080)