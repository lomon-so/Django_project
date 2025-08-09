from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from contacts.models import Contact

# Create your views here.

def register(request):
    if request.method == 'POST':
        # Form Values 
        first_name  = request.POST['first_name'].strip()
        last_name   = request.POST['last_name'].strip()
        username    = request.POST['username'].strip()
        email       = request.POST['email'].strip()
        password    = request.POST['password'].strip()
        password2   = request.POST['password2'].strip()
        
        # Validate if fields are filled 
        if not all([first_name, last_name, username, email, password, password2]):
            messages.error(request, 'All fields are required.')
            return redirect('register')

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email.')
            return redirect('register')
        
        # Password match 
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        # Minimum password length
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('register')
        
        # Username check 
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')
        
        # Email uniqueness check
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('register')
        
        # All Good → Create User 
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')
    
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method =='POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        
        # If field are filled 
        if not username or not password:
            messages.error(request, 'Username and passoword are required.')
            return redirect('login')
         
        # Authenticate user
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Welcome back, {user.username }!")
            return redirect('dashboard')
        else: 
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
        
    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, 'You are now logged out.')
    return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
  
    return render(request, 'accounts/dashboard.html', {
        'contacts': user_contacts
    })