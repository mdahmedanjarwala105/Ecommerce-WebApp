from django.shortcuts import render
from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
    try:
        email = BaseEmailMessage(
            template_name="emails/hello.html", context={"name": "King"}
        )
        email.send(["hi@maabuy.com"])
    except BadHeaderError:
        pass
    return render(request, "hello.html", {"name": "King"})
