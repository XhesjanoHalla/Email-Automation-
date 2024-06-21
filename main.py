from datetime import date
import pandas as pd
from send_email import send_email  # local python module

# Public GoogleSheets url - not secure!

SHEET_ID = "1n7U5dGJ2UPfUY3rdpkVJ8Cgul4a8asAOltiEc46dEe4"
SHEET_NAME = "invoice_data"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"


def load_df(url):
    parse_dates = ["due_date", "reminder_date"]
    df = pd.read_csv(url, parse_dates=parse_dates, dayfirst=True)
    return df


def query_data_and_send_email(df):
    present = date.today()
    email_counter = 0
    for _, row in df.iterrows():
        if(present >= row["reminder_date"].date()) and (row["has_paid"] == "no"):
            send_email(
                subject=f'[Coding Corp] Invoice: {row["invoice_no"]}',
                receiver_email=row["email"],
                name=row["name"],
                due_date=row["due_date"].strftime("%d, %b %Y"),  # expl 21, Jun 2024
                invoice_no=row["invoice_no"],
                amount=row["amount"],
            )
            email_counter += 1
    return f"Total emails sent: {email_counter}"


df = load_df(URL)
result = query_data_and_send_email(df)
print(result)
