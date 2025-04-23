from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import ProfileBeneficiary
from django.db import transaction
# Create your views here.
def sign_up_beneficiary(request: HttpRequest):
    
    if request.method == 'POST':
        try:
            new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])            
            new_user.save()
            #create profile after user save 
            profile = ProfileBeneficiary(user=new_user,name=new_user.get_full_name(),contact_info=request.POST['contact_info'], address=request.POST['address'])
            profile.save()
            
            messages.success(request, "Registered User Successfuly", "alert-success")
            return redirect("accounts:sign_in")
        
        except Exception as e:
            messages.error(request, "Couldn't register user. Try again", "alert-danger")
            print(e)


    
    return render(request, "accounts/signup.html")

def sign_in(request:HttpRequest):
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request,"Logged in successfuly", "alert-success" )
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Invalid username or password", "alert-danger")

    



    return render(request, "accounts/signin.html")



def beneficiary_profile_view(request: HttpRequest, user_name):
    try:
        user = User.objects.get(username=user_name)
        profile = ProfileBeneficiary.objects.filter(user=user).first()
        if not profile:
            profile = ProfileBeneficiary.objects.create(user=user)

        return render(request, 'accounts/beneficiary_profile.html', {
            'user': user,
            'profile': profile
        })

    except Exception as e:
        print(e)
        return render(request, '404.html')




def update_beneficiary_profile(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.warning(request, 'Only registered users can update profile', 'alert-warning')
        return redirect('accounts:sign_in')
    
    try:
        with transaction.atomic():
            user: User = request.user

            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.save()

            profile, created = ProfileBeneficiary.objects.get_or_create(user=user)
            
            profile.contact_info = request.POST.get('contact_info', profile.contact_info)
            profile.address = request.POST.get('address', profile.address)
            profile.save()

            messages.success(request, 'Profile updated successfully', 'alert-success')

    except Exception as e:
        messages.error(request, "Couldn't update profile", "alert-danger")
        print(e)
    
    return render(request, 'accounts/update_beneficiary_profile.html')






def sign_up_supplier(request: HttpRequest):
    
    if request.method == 'POST':
        try:
            new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])            
            new_user.save()
            
            messages.success(request, "Registered User Successfuly", "alert-success")
            return redirect("accounts:sign_in")
        
        except Exception as e:
            messages.error(request, "Couldn't register user. Try again", "alert-danger")
            print(e)


    
    return render(request, "accounts/supplier_signup.html")



def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")
    return redirect(request.GET.get("next", "/"))
