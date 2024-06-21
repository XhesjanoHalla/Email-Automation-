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
def send_email(subject, receiver_email, name, due_date, invoice_no, amount):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((" TeamSystem ", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        Hello {name},
        I hope you are well.
        I just wanted to kindly remind you that {amount}$ in respect of our
        invoice {invoice_no} is due for payment on {due_date}.
        I would be really grateful if you confirm that everything is on track for payment.
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
                <p> Hi {name} </p>
                <p> I hope you are well. </p>
                <p>  I just wanted to kindly remind you that <strong>{amount}$</strong> in respect of our</p>
                <p> invoice {invoice_no} is due for payment on {due_date}. </p>
                <p> I would be really grateful if you confirm that everything is on track for payment. </p>
                <p> Best regards </p>
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


