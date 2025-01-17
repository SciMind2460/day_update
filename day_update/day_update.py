import datetime
import os
import sys
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


def should_be_removed(line: str) -> bool:
    _, _, due_date_string = line.split(',', maxsplit=2)
    due_date = datetime.strptime(due_date_string, "%d/%m/%y").date()
    if due_date < datetime.date.today():
        return True
    return False


def check_for_weekend(weekday_number: int) -> int:
    if weekday_number > 4:
        is_makeup_day: bool = input("Is today a make-up day for a holiday? (y/n)").lower() == 'y'
        if not is_makeup_day:
            print("Sorry, but today is not a day for the request to be sent.")
            exit()
        which_day_to_make_up_for: str = input(
            "Which day is today supposed to make up for? Reply with the full name of the day.").upper()
        if not any(weekdaylist == which_day_to_make_up_for for weekdaylist in weekdays):
            print("You have made an illegal input! Restart the process!")
            os.execv(sys.argv[0], sys.argv)
        for weekdaylist in weekdays:
            if weekdaylist.name == which_day_to_make_up_for:
                weekday_number = weekdaylist.value
                return weekday_number
    else:
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