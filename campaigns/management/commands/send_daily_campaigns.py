import os
import datetime
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from campaigns.models import Campaign, Subscriber
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

class Command(BaseCommand):
    help = 'Send daily campaigns using SMTP'

    def handle(self, *args, **kwargs):
        # Getting today's date
        today = datetime.date.today()

        # Query campaigns scheduled for today
        campaigns = Campaign.objects.filter(published_date__date=today)

        # Query active subscribers
        active_subscribers = Subscriber.objects.filter(isActive=True)

        # SMTP server settings
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # SMTP server port number
        smtp_username = os.environ.get('EMAIL_USER') #getting SMTP username from env
        smtp_password = os.environ.get('EMAIL_PASS') #getting SMTP password from env

        # Define a function to send emails
        def send_email(subscriber, campaign):
            email_subject = campaign.subject
            email_preview_text = campaign.preview_text
            article_url = campaign.article_url
            html_content = campaign.html_content
            plain_text_content = campaign.plain_text_content

            # Create an SMTP connection
            smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
            smtp_conn.starttls()
            smtp_conn.login(smtp_username, smtp_password)

            # Create the email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = email_subject
            msg['From'] =  smtp_username#smtp_username
            msg['To'] = subscriber.email

            # Create HTML and plain text parts
            text_part = MIMEText(plain_text_content, 'plain')
            html_content = render_to_string('campaigns/base_email_template.html', {
                'subject': email_subject,
                'preview_text': email_preview_text,
                'article_url': article_url,
                'html_content': html_content,
            })
            html_part = MIMEText(html_content, 'html')

            msg.attach(text_part)
            msg.attach(html_part)

            # Send the email
            smtp_conn.sendmail(msg['From'], msg['To'], msg.as_string())

            # Close the SMTP connection
            smtp_conn.quit()

            self.stdout.write(self.style.SUCCESS(f'Sent campaign to {subscriber.email}: {email_subject}'))

        # Use threads to send emails in parallel
        threads = []
        for campaign in campaigns:
            for subscriber in active_subscribers:
                thread = threading.Thread(target=send_email, args=(subscriber, campaign))
                threads.append(thread)
                thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()