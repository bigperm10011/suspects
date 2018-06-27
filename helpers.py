from suspect_scrape_app.settings import get_con_string
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.automap import automap_base
import sendgrid
import os
from sendgrid.helpers.mail import *

#loads db tables from postgres
def load_tables():
    """"""
    cs = get_con_string()
    # automap base
    Base = automap_base()

    # pre-declare User for the 'user' table
    class Leaver(Base):
        __tablename__ = 'leaver'

    # reflect
    engine = create_engine(cs)
    Base.prepare(engine, reflect=True)

    Suspect = Base.classes.suspect
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, Suspect, Leaver

# to remove html tags from text selected in spider
def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

def gen_html(added):
    html = """\
        <!DOCTYPE html><html lang="en"><head>SAR Suspects Added Today</head><body><table border='1'>
        <thead><tr><th>Name</th><th>Firm</th><th>Role</th><th>Location</th><th>Link</th></tr></thead>"""

    for l in added:
        html = html + "<tr>"
        html = html + "<td>" + l.name + "</td>"
        try:
            html = html + "<td>" + l.firm + "</td>"
        except:
            html = html + "<td>None</td>"
        try:
            html = html + "<td>" + l.role + "</td>"
        except:
            html = html + "<td>None</td>"
        try:
            html = html + "<td>" + l.location + "</td>"
        except:
            html = html + "<td>None</td>"
        try:
            html = html + '<td><a target="_blank" href="'+ l.link + ' ">LinkedIn</a></td></tr>'
        except:
            html = html + '<td><a target="_blank" href=None">None</a></td></tr>'
    html = html + "</table></body></html>"
    return html

def send_mail(body):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("jdbuhrman@gmail.com")
    subject = "SAR Suspects Added Today"
    to_email = Email("jbuhrman2@bloomberg.net")
    content = Content("text/html", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response.status_code
