from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Create your views here.

def contact(request):
    if request.method == 'POST':
        listing_id    = request.POST['listing_id']
        listing       = request.POST['listing']
        name          = request.POST['name']
        email         = request.POST['email']
        phone         = request.POST['phone']
        message       = request.POST['message']
        user_id       = request.POST['user_id']
        realtor_email = request.POST.get('realtor_email', '')
        
        
        # Prevents duplicate inquiries
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.filter(
                listing_id=listing_id,
                user_id=user_id
            ).exists()
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing.')
                return redirect('/listings/' + listing_id) 

        
        contact = Contact(
            listing_id=listing_id,
            listing=listing,
            name=name, 
            email=email,
            phone=phone, 
            message=message,
            user_id=user_id
        )
        contact.save()
        
        if realtor_email:
            subject = 'Property Listing Inquiry'
            text_content = f'There has been an inquiry for "{listing}". Please sign into the admin panel for more details.'
            
            html_content = f"""
            <h2>Property Listing Inquiry</h2>
            <p>There has been an inquiry for <strong>{listing}</strong>.</p>
            <ul>
            <li><strong>Name:</strong> {name}</li>
            <li><strong>Email:</strong> {email}</li>
            <li><strong>Phone:</strong> {phone}</li>
            <li><strong>Message:</strong> {message}</li>
            </ul>
            <p>Please sign into the admin panel for more details.</p>
            """
            
            msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [realtor_email, 'lomonsofx@gmail.com']
       )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
        messages.success(request, 'Your request has been submitted, a realtor will respond to you soon.')
        return redirect('/listings/' + listing_id)

    