from flask import Blueprint, request, redirect, url_for, render_template, current_app
from app import db

main_bp = Blueprint("main", __name__)

TABLE_CONFIG = {
    "students": {
        "Headers": ["ID", "Name"],
        "form_type": ["Name"]
    },

    "courses": {
        "Headers": ["Code", "Course"],
        "form_type": []
    },

    "grades": {
        "Headers": ["Name", "Course", "score", "Grade", "Rec_at"],
        "form_type": ["Student_id", "Course_code", "Score"]
    }
}

@main_bp.route("/", methods=["GET"])
def main():
    table = request.args.get("table", "students")

    try:
        if table == "students":
            info = db.get_students()
        elif table == "courses":
            info = db.get_courses()
        elif table == "grades":
            info = db.get_grades()
        else:
            table = "students"
            info = db.get_students()

        config = TABLE_CONFIG.get(table, TABLE_CONFIG["students"])

        return render_template(
            "index.html",
            form_type = config["form_type"],
            headers = config["Headers"],
            info = info,
            current_table = table
            )
    
    except Exception:
        current_app.logger.exception("Error loading main page")
        return "Internal server error", 500
    

@main_bp.route("/", methods=["POST"])
def post():
    table = request.args.get("table", "students")

    try:
        if table == "students":
            name = request.form.get("Name")
            if not name:
                return "Name is required", 400
            db.add_students(name)
        elif table == "grades":
            student_id = request.form.get("Student_id")
            course = request.form.get("Course_code")
            score = request.form.get("Score")
            
            if not all([student_id, course, score]):
                return "All fields required", 400
            
            db.add_grades(student_id, course, score)
        
        return redirect(url_for("main.main", table=table))
    
    except Exception:
        current_app.logger.exception("Error processing POST request")
        return "Internal server Error", 500



            

