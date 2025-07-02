from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError, send_mass_mail


def say_hello(request):
    try:
        # send_mail("subject", "message", "info@maabuy.com", ["from@maabuy.com"])
        mail_admins("subject", "message", html_message="message")
    except BadHeaderError:
        pass
    return render(request, "hello.html", {"name": "King"})
