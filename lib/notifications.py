import lib.gpw as gpw
import lib.manipulation as manip
import imghdr
import smtplib
from email.message import EmailMessage
from datetime import date, timedelta
import pandas as pd
import matplotlib.pyplot as plt


def make_table(df):
    plt.figure(figsize=(6, 0.36 * len(df)))
    tab = plt.table(cellText=df.values,
                    colLabels=df.columns,
                    loc='center',
                    cellLoc='center',
                    colWidths=[0.3] * len(df.columns))

    tab.auto_set_font_size(False)
    tab.set_fontsize(10)

    tab.scale(1, 1.5)

    plt.axis('off')
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.02, top=0.98)
    file_png = 'Wybicia tygodnia ' + str(manip.this_friday(date.today())) + '.png'
    plt.savefig(file_png)

    df = df.drop(columns='walor')
    file_csv = file_png[:-4] + '.csv'
    df.to_csv(file_csv)
    return [file_png, file_csv]


def make_title(title):
    return title + str(manip.this_friday(date.today()))


def send_mail(title, content, files, sender, recipient, password):
    email = sender
    receiver = recipient

    subject = title
    message = content

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = receiver
    msg.set_content(message)
    for filename in files:
        with open(filename, 'rb') as file:
            file_data = file.read()
            file_name = file.name
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)

        smtp.send_message(msg)
