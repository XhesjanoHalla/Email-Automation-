import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv

PORT = 587
EMAIL_SERVER = "smtp-mail.outlook.com"

# Loading the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")


# The function that will send the email
def send_email(subject, receiver_email, name):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Coding Corp.", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        Hi {name},
        This is a test email.
        I just want to test the script!
        Best regards
        Xhesjano Halla
        """
    )

    # Adding the HTML version. This converts the message into a multipart/alternative
    # container, with the original text message as the first part and the new html
    # message as the second part.
    msg.add_alternative(
        f"""\
        <html>
            <body>
                <p>Hi {name}</p>
                <p>This is a test email.</p>
                <p>I just want to test the script!</p>
                <p>Best regards</p>
                <strong>Xhesjano Halla</strong>
            </body>
        </html>
        """,
        subtype="html",
    )

    try:
        with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password_email)  # Login to the email server
            server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    send_email(
        subject="Subject Testing",
        name="Testing Test",
        receiver_email="orgestbitri@gmail.com",
    )
