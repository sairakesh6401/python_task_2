from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import PatientProfile, DoctorProfile, User
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def home(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'patient':
                    return redirect('patient_dashboard')
                elif user.user_type == 'doctor':
                    return redirect('doctor_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password1')
            user.set_password(raw_password)  # Ensure the password is hashed
            print(raw_password,'raw_password')
            print(user.set_password(raw_password),'user.set_password(raw_password)')
            user.save()

            # Debug statement: Checking if the user is created and password is set
            print(f"User created: {user.username}, Password: {user.password}")

            if user.user_type == 'patient':
                PatientProfile.objects.create(
                    user=user,
                    address_line1=form.cleaned_data.get('address_line1'),
                    city=form.cleaned_data.get('city'),
                    state=form.cleaned_data.get('state'),
                    pincode=form.cleaned_data.get('pincode'),
                    profile_picture=form.cleaned_data.get('profile_picture'),
                )
            elif user.user_type == 'doctor':
                DoctorProfile.objects.create(
                    user=user,
                    address_line1=form.cleaned_data.get('address_line1'),
                    city=form.cleaned_data.get('city'),
                    state=form.cleaned_data.get('state'),
                    pincode=form.cleaned_data.get('pincode'),
                    profile_picture=form.cleaned_data.get('profile_picture'),
                )
            
            authenticated_user = authenticate(username=user.username, password=raw_password)
            
            # Debug statement: Checking if the authentication was successful
            print(f"Authenticated User: {authenticated_user}")

            if authenticated_user is not None:
                login(request, authenticated_user)
                if authenticated_user.user_type == 'patient':
                    return redirect('patient_dashboard')
                elif authenticated_user.user_type == 'doctor':
                    return redirect('doctor_dashboard')
            else:
                messages.error(request, "Authentication failed. Please try again.")
            return redirect('thank_you')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def thank_you(request):
    return render(request, 'accounts/thank_you.html')

def patient_dashboard(request):
    return render(request, 'accounts/patient_dashboard.html', {'user': request.user})

def doctor_dashboard(request):
    return render(request, 'accounts/doctor_dashboard.html', {'user': request.user})
