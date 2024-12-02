import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class Mail:
    def __init__(
        self, smtp_server=None, smtp_port=None, smtp_username=None, smtp_password=None
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def connection(self):
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_username, self.smtp_password)
        return server

    def send(
        self, subject=str, html=str, email=str, cc=None, caminho=None, filename=None
    ):
        message = MIMEMultipart()
        if caminho is not None:
            file = open(caminho, "rb")
            attachment = MIMEApplication(file.read(), _subtype="xlsx")
            attachment.add_header(
                "Content-Disposition", "attachment", filename=filename
            )
        message["Subject"] = subject
        message["From"] = self.smtp_username
        message["To"] = email
        if cc is not None:
            message["Cc"] = cc
        message.attach(MIMEText(html, "html"))
        if caminho is not None:
            message.attach(attachment)
        server = self.connection()
        server.send_message(message)
        return print("Email enviado com sucesso!")
