from django.shortcuts import render
from .models import ContactUs
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.contrib import messages
from . models import *
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.views import View


def Contact(request):
    if request.method == "POST":
        data = request.POST
        db = ContactUs()
        db.customer = request.user
        db.name = data.get('name')
        db.message = data.get('message')
        db.email = data.get('email')
        if not (db.name and  db.message and db.email):
            error_message = "All fields are required."
            return render(request, 'about.html', {'error_message': error_message, 'data': data})

        db.save()

        subject = "new Query "
        from_email = 'info.demodjango@gmail.com'
        recipient_list = ['info.demodjango@gmail.com'] 
        
        context = {
            'name': db.name,
            'email': db.email,
            'subject':subject,
            'message': db.message,
        }
        text_content = f"Name: {db.name}\nEmail: {db.email}\nMessage: {db.message}\nSubject:{subject}"
        html_content = render_to_string('contact_email.html', context)

        # Send email
        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()

        messages.success(request, 'This data has been sent to the admin.')
       
        return redirect('contact')
    return render(request,'contactUs.html')


class AboutView(View):
    def get(self, request):
        return render(request,'about.html')