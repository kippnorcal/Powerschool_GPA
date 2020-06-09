import email, smtplib, ssl
from os import getenv
import glob

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:
    def __init__(self, jobname):
        self.user = getenv("GMAIL_USER")
        self.password = getenv("GMAIL_PWD")
        self.slack_email = getenv("SLACK_EMAIL")
        context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        self.from_address = "KIPP Bay Area Job Notification"
        self.to_address = "databot"
        self.jobname = jobname

    def _subject_line(self):
        subject_type = "Error" if self.error else "Success"
        return f"{self.jobname} - {subject_type}"

    def _body_text(self):
        if self.error:
            return f"{self.jobname} encountered an error:\n{self.message}"
        else:
            return f"{self.jobname} completed successfully.\n{self.message}"

    def _attachments(self, msg):
        filenames = glob.glob("*.png")
        for filename in filenames:
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {filename}")
            msg.attach(part)

    def _message(self, attachments=False):
        msg = MIMEMultipart()
        msg["Subject"] = self._subject_line()
        msg["From"] = self.from_address
        msg["To"] = self.to_address
        msg.attach(MIMEText(self._body_text(), "plain"))
        if attachments:
            self._attachments(msg)
        return msg.as_string()

    def notify(self, error=False, message=None):
        self.error = error
        self.message = message
        with self.server as s:
            s.login(self.user, self.password)
            msg = self._message(attachments=error)
            s.sendmail(self.user, self.slack_email, msg)
