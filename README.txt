APPROCH - 

First i created a model for both Subscriber and Campaigns

Since to add new Records we are using Django Admin
I directly started with the endpoint to unsubscribe

In Unsubscribe-endpoint -
I need email in reqbody 
then if i get the email i try to retrieve the object with the email address provided
then i update the isActive Field with the FALSE value since its boolean
also handled the exception - DoesNotExist
follow - Campaigns/views.py to see the code

After this i wrote a django management command to send daily campaigns using smtp

In send_daily_campaigns - 
i fetch todays date and then according to it retrieve the campaigns object so that i can get todays campaigns to send today
after that retrieved all the active subscribers to send them todays campaigns
then i defined SMTP server setting
and wrote the send_email which require subscriber-object and campaign-object as parameter
    In Send-email - 
    i established the connection with the SMTP details i defined above
    then created the email-message and email-content,
    in email-content then html part is rendered using the base_email_template
    after that we attach the email-content in email-message and send it, which then quit the smtp connection
now to send all the todays campaign to all the active subscriber -
multiple threads are used, each responsible for sending emails to different subscribers for different campaigns

now to run code on your system please export the env-
1 - EMAIL_USER - with your email address
2 - EMAIL_Pass - with the password - if you are using 2FA in your email follow the link to create your secret password-
    link - https://accounts.google.com/v3/signin/challenge/pwd?TL=AJeL0C4H8K6mzRbJECpuh5peyNUN8XEEEd4mobqYEo7ptpVzobZolRA3bdVYgAo3&cid=2&continue=https://myaccount.google.com/apppasswords&flowName=GlifWebSignIn&ifkv=AYZoVhfHigPWvuSCr2vwKDAaAUsouU9kGxOHl0t7PDbO9aObx9G_Abhv6REbtuaj0POUGCnFAVKb5A&rart=ANgoxcffDSNlIkhgz9EgvMh5wBQ393TJCrj11XOk4M5wMEwabLqZN9urxv4Fc9-bEGbEEZHbsNpz63oZhS6qtxMpG911LqqgcA&rpbg=1&sarp=1&scc=1&service=accountsettings&hl=en_US

Admin end-point - http://localhost:8000/admin/
Unsubscribe end-point - http://localhost:8000/campaigns/unsubscribe/
To hit send email-campaigns - python manage.py send_daily_campaigns
To run server - python manage.py runserver
