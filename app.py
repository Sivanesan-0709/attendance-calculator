from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

FILE_NAME = "students.csv"

# Create CSV file if it does not exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Attendance", "Risk"])


@app.route("/", methods=["GET", "POST"])
def dashboard():
    name = ""
    attendance = None
    risk = ""
    students = []

    if request.method == "POST":
        if "attended" in request.form:
            name = request.form["name"]
            attended = int(request.form["attended"])
            total = int(request.form["total"])

            # Validation: attended cannot exceed total classes
            if attended > total or total == 0:
                attendance = None
                risk = "Invalid Input"
            else:
                attendance = round((attended / total) * 100, 2)

                if attendance < 65:
                    risk = "High"
                elif attendance < 75:
                    risk = "Medium"
                else:
                    risk = "Low"

                # Save valid record to CSV
                with open(FILE_NAME, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([name, attendance, risk])

    # Read all students
    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        next(reader)
        students = list(reader)

    return render_template(
        "index.html",
        name=name,
        attendance=attendance,
        risk=risk,
        students=students
    )


@app.route("/delete/<student_name>")
def delete_student(student_name):
    rows = []

    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] != student_name:
                rows.append(row)

    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


