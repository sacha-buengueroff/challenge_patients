import smtplib
from email.message import EmailMessage
from decouple import config


class NotificationSender:
    mailtrap_username = config("MAILTRAP_USERNAME")
    mailtrap_password = config("MAILTRAP_PASSWORD")
    mailtrap_smtp_host = config("MAILTRAP_SMTP_HOST")
    mailtrap_smtp_port = config("MAILTRAP_SMTP_PORT")
    sender = "sender@example.com"

    @classmethod
    async def send_email(cls, to: str):
        """
        Asynchronously send email notification

        Args:
            to (str): patient email.
        """
        msg = EmailMessage()
        msg["From"] = cls.sender
        msg["To"] = to
        msg["Subject"] = "Congratulation! Your user was created."
        msg.set_content("Your registration is confirmed, congratulations!")

        with smtplib.SMTP(cls.mailtrap_smtp_host, cls.mailtrap_smtp_port) as server:
            server.login(cls.mailtrap_username, cls.mailtrap_password)
            server.send_message(msg)

    @classmethod
    async def send_sms(cls, phone_number: int):
        """
        Asynchronously send SMS notification
        This is a placeholder and you should replace it with actual code for sending SMS

        Args:
            phone_number (int): patient phone number
        """        
        pass
