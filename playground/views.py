from django.shortcuts import render
from django.core.mail import EmailMessage, BadHeaderError


def say_hello(request):
    try:
        email = EmailMessage(
            "subject", "message", "from@maabuy.com", ["hello@maabuy.com"]
        )
        email.attach_file("playground/static/images/test_image.jpg")
        email.send()
    except BadHeaderError:
        pass
    return render(request, "hello.html", {"name": "King"})
