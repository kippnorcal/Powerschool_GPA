import smtplib
import os


GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PWD = os.getenv("GMAIL_PWD")
SLACK_EMAIL = os.getenv("SLACK_EMAIL")


def notify(error=False, error_message=None, success_message=None):
    """Send email message with success or error notification"""
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(GMAIL_USER, GMAIL_PWD)
    if error:
        subject = "PS GPA - Error"
        text = f"The PowerSchool GPA Selenium script encountered an error:\n{error_message}"
        message = f"Subject: {subject}\n\n{text}"
    else:
        subject = "PS GPA - Success"
        text = (
            f"The PowerSchool GPA Selenium script ran successfully.\n{success_message}"
        )
        message = f"Subject: {subject}\n\n{text}"
    server.sendmail(GMAIL_USER, SLACK_EMAIL, message)
    server.quit()
