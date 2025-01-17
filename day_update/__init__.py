import datetime
import secrets

from dotenv import load_dotenv

from .day_update import check_for_weekend, handle_assignments, handle_appendices, handle_main_text, send_message, \
    handle_timetable

def main(webhook_url: str):
    load_dotenv()
    weekday: int = datetime.date.today().weekday()
    timetable = handle_timetable()
    if weekday > 4:
        make_up_day = input("Which day do we have to make up for? Reply in the full format.").upper()
        weekday = check_for_weekend(make_up_day)
    if weekday == -1:
        exit("Today is not a school day!")
    message = handle_main_text(timetable=timetable, weekday=weekday)
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
