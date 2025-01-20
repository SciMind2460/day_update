import json
import sqlite3
from enum import Enum

import requests


class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


weekdays = list(Weekday)
weekdays_working = [Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY]
weekdaynames = [weekday.name for weekday in weekdays]


def handle_timetable(timetable_file: str = "timetable.json") -> list[dict[str, str | None]]:
    with open(timetable_file) as timetable:
        json_decoded = json.load(timetable)
    change_timetable = input("Do you want to change the timetable?").lower() == 'y'
    if change_timetable:
        json_decoded = []
        timetable_values = [input(f"Enter the new subjects for {weekday}").split() for weekday in weekdays_working]
        for i, timetable_value in enumerate(timetable_values):
            for subject in timetable_value:
                json_decoded[i][subject] = None
    with open(timetable_file, 'w') as timetable:
        json.dump(json_decoded, timetable)
    return json_decoded


def initalize_db():
    conn = sqlite3.connect("assignments.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS assignments (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, description TEXT, due_date TEXT")
    conn.commit()
    conn.close()


def remove_old_assignments():
    conn = sqlite3.connect("assignments.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assignments WHERE due_date < DATE('now')")
    conn.commit()
    conn.close()


def check_for_weekend(make_up_for_day='') -> int:
    make_up_for_day = make_up_for_day.upper()
    if make_up_for_day not in weekdaynames:
        raise ValueError("Invalid weekday name provided.")
    for weekdayitem in weekdays:
        if weekdayitem.name == make_up_for_day:
            weekday_number = weekdayitem.value
            return weekday_number


def handle_main_text(timetable: list[dict[str, str | None]], weekday: int) -> str:
    today_timetable = timetable[weekday]
    for subject, description in today_timetable.items():
        description = input(f'Enter a description for the subject {subject}.')
        today_timetable[subject] = description
    message_list = [f'{subject}: {description}\n' for subject, description in today_timetable.items()]
    message = ''.join(message_list)
    return message


def handle_assignments(assignment_number: int) -> str:
    initalize_db()
    remove_old_assignments()
    if assignment_number == 0:
        print("Ok! Proceeding to next stage.")
    else:
        conn = sqlite3.connect("assignments.db")
        cursor = conn.cursor()
        for i in range(assignment_number):
            subject = input("What subject is this assignment for?")
            description = input("Enter a short description for the assignment.")
            due_date = input("Which date is this assignment due on? Enter in DD/MM/YY format.")
            cursor.execute("INSERT INTO assignments (subject, description, due_date) VALUES (?, ?, ?)",
                           (subject, description, due_date))
        conn.commit()
        conn.close()
    conn = sqlite3.connect("assignments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT (subject, description, due_date) FROM assignments")
    assignments = cursor.fetchall()
    conn.close()
    assignment_strs = [f'{subject} assignment: {description}. Due on {due_date}\n' for subject, description, due_date in
                       assignments]
    message_assignment_str = "Assignments:\n" + '\n'.join(assignment_strs)
    return message_assignment_str


def handle_appendices(appendices):
    appendix_strings = []
    if appendices == 0:
        print("Ok! Exiting program.")
        exit()
    for appendix in range(appendices):
        appendix_strings.append("Appendix {appendix + 1}: " + input(f'Enter appendix {appendix + 1}.') + '\n')
    appendix_message = ''.join(appendix_strings)
    return appendix_message


def send_message(webhook_url: str | bytes, message: str):
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }
    data = {
        "text": message
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Update sent successfully!")
    else:
        print(f'Failed to send update. Status code: {response.status_code}, message: {response.message}')