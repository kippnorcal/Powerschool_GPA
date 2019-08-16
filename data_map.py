from os import getenv

method = getenv("METHOD")
columns = {
    "student_number": "student_number",
    "lastfirst": "lastfirst",
    "grade_level": "grade_level",
    "[39]name": "School",
    f'^(*gpa method="{method}" format=##0.00)': "Cumulative_GPA",
    '^(*gpa method="Weighted" format=##0.00 grade="9,10,11,12")': "Cumulative_Weighted_GPA",
}

column_names = {
    key.replace("^(", "").replace(")", "").replace(" ", "_"): value
    for key, value in columns.items()
}

keys = list(columns.keys())
