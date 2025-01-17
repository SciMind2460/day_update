import datetime
import os
from dotenv import load_dotenv
from .day_update import check_for_weekend, handle_assignments, handle_appendices, handle_main_text, send_message

timetable: list[dict[str, str | None]] = [
    {"Humanities": None, "Marathi": None, "Library": None, "Biology": None, "Mathematics": None},
    {"French": None, "Chemistry": None, "PE": None, "English": None},
    {"Homeroom": None, "ICT": None, "Humanities": None, "Physics": None, "Mathematics": None},
    {"EM": None, "Math": None, "ICT": None, "iPropel": None, "English": None},
    {"Art": None, "French": None, "Humanities": None, "SEL": None, "English": None}
]

def main():
    load_dotenv()
    webhook_url: str = os.getenv("WEBHOOK_URL_1")
    weekday: int = datetime.date.today().weekday()
    weekday = check_for_weekend(weekday)
    message = handle_maintext(timetable=timetable, weekday=weekday)
    send_message(webhook_url, message)
    add_assignments = int(input("How many assignments do you want to add?"))
    message_assignment_str = handle_assignments(add_assignments)
    send_message(webhook_url=webhook_url, message=message_assignment_str)
    appendices = int(input("How many appendices do you want to add?"))
    appendices_message = handle_appendices(appendices)
    send_message(webhook_url=webhook_url, message=appendices_message)
    exit()

if __name__ == "__main__":
    main()
