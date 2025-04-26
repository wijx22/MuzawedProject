from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import ProfileBeneficiary, SupplierProfile
from django.db import transaction



# Create your views here.
def sign_up_beneficiary(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("main:index_view")
    
    if request.method == 'POST':
        try:
            new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])            
            new_user.save()
            #create profile after user save 
            profile = ProfileBeneficiary(user=new_user,name=new_user.get_full_name(),contact_info=request.POST['contact_info'], address=request.POST['address'])
            profile.save()
            
            messages.success(request,"مرحبًا بك تم تسجيلك بنجاح", "alert-success")
            return redirect("accounts:sign_in")
        
        except Exception as e:
            messages.error(request, "تعذر تسجيل المستخدم. حاول مرة أخرى.", "alert-danger")
            print(e)


    
    return render(request, "accounts/beneficiary/signup.html")



def sign_in(request:HttpRequest):
    if request.user.is_authenticated:
        return redirect("main:index_view")
    
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request,"مرحبًا بك من جديد", "alert-success" )
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صالحة", "alert-danger")

    



    return render(request, "accounts/signin.html")





def beneficiary_profile_view(request: HttpRequest, user_name):
    
    try:
        user = User.objects.get(username=user_name)
        if request.user != user or not ProfileBeneficiary.objects.filter(user=user).exists():
            messages.error(request, "لا يحق لك مشاهدة هذا الملف الشخصي.", "alert-danger")
            return redirect('accounts:sign_in')
        
        #if SupplierProfile.objects.filter(user=user).exists():
        #    messages.warning(request, "هذا المستخدم هو المورد وليس المستفيد", "alert-warning")
        
        profile = ProfileBeneficiary.objects.filter(user=user).first()
        if not profile:
            return render(request, '404.html')

        return render(request, 'accounts/beneficiary/beneficiary_profile.html', {
            'user': user,
            'profile': profile
        })

    except Exception as e:
        print(e)
        return render(request, '404.html')






def update_beneficiary_profile(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.warning(request, 'يمكن فقط للمستخدمين المسجلين تحديث الملف الشخصي', 'alert-warning')
        return redirect('accounts:sign_in')
    
    if SupplierProfile.objects.filter(user=request.user).exists():
        messages.error(request, "لا يمكن للموردين تحديث ملف المستفيد", "alert-danger")
        return redirect('/')  

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

            messages.success(request, 'تم تحديث الملف الشخصي بنجاح', 'alert-success')

    except Exception as e:
        messages.error(request, "لم أتمكن من تحديث الملف الشخصي", "alert-danger")
        print(e)
    
    return render(request, 'accounts/beneficiary/update_beneficiary_profile.html')



def sign_up_supplier(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("main:index_view")
    
    if request.method == 'POST':
        try:
            new_user = User.objects.create_user(username=request.POST["username"],
                                                password=request.POST["password"],
                                                email=request.POST["email"],
                                                first_name=request.POST["first_name"],
                                                last_name=request.POST["last_name"])            
            new_user.save()
            profile = SupplierProfile(user=new_user,name=new_user.get_full_name(),contact_info=request.POST['contact_info'])
            profile.save()

            
            messages.success(request, "تم تسجيل المورد بنجاح", "alert-success")
            return redirect("accounts:sign_in")
        
        except Exception as e:
            messages.error(request, "تعذّر تسجيل المورّد. حاول مجددًا.", "alert-danger")
            print(e)


    
    return render(request, "accounts/supplier/supplier_signup.html")

def supplier_profile_view(request: HttpRequest, user_name):
    if not request.user.is_authenticated:
        messages.error(request, "يجب عليك تسجيل الدخول لمشاهدة الملف الشخصي.", "alert-danger")
        return redirect('accounts:sign_in')

    try:
        user = User.objects.get(username=user_name)

        if request.user != user:
            messages.error(request, "لا يحق لك مشاهدة هذا الملف الشخصي.", "alert-danger")
            return redirect('accounts:sign_in')

        profile, created = SupplierProfile.objects.get_or_create(user=user)

        return render(request, 'accounts/supplier/supplier_profile.html', {
            'user': user,
            'profile': profile
        })

    except User.DoesNotExist:
        messages.error(request, "المستخدم غير موجود.", "alert-danger")
        return redirect('main:index_view')

    except Exception as e:
        print(e)
        return render(request, '404.html')


#def supplier_profile_view(request: HttpRequest, user_name):
#  
#    try:
#        user = User.objects.get(username=user_name)
#        if request.user != user or not SupplierProfile.objects.filter(user=user).exists():
#            messages.error(request, "لا يحق لك مشاهدة هذا الملف الشخصي.", "alert-danger")
#            return redirect('accounts:sign_in')
#
#        profile = SupplierProfile.objects.filter(user=user).first()
#        if not profile:
#            profile = SupplierProfile.objects.create(user=user)
#
#        return render(request, 'accounts/supplier/supplier_profile.html', {
#            'user': user,
#            'profile': profile
#        })
#
#    except Exception as e:
#        print(e)
#        return render(request, '404.html')
#


def update_supplier_profile(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.warning(request, 'يمكن للمورد المسجل فقط تحديث الملف الشخصي', 'alert-warning')
        return redirect('accounts:sign_in')
    
    try:
        with transaction.atomic():
            user: User = request.user

            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.save()

            profile, created = SupplierProfile.objects.get_or_create(user=user)
            
            profile.contact_info = request.POST.get('contact_info', profile.contact_info)
            profile.save()

            messages.success(request, 'تم تحديث الملف الشخصي بنجاح', 'alert-success')

    except Exception as e:
        messages.error(request, "لم أتمكن من تحديث الملف الشخصي", "alert-danger")
        print(e)
    
    return render(request, 'accounts/supplier/update_profile.html')


def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, "تم تسجيل الخروج بنجاح", "alert-warning")
    return redirect(request.GET.get("next", "/"))






#def update_beneficiary_profile(request: HttpRequest):
#    if not request.user.is_authenticated :
#        messages.warning(request, 'Only registered users can update profile', 'alert-warning')
#        return redirect('accounts:sign_in')
#    
#    try:
#        with transaction.atomic():
#            user: User = request.user
#
#            user.first_name = request.POST.get('first_name', user.first_name)
#            user.last_name = request.POST.get('last_name', user.last_name)
#            user.email = request.POST.get('email', user.email)
#            user.save()
#
#            profile, created = ProfileBeneficiary.objects.get_or_create(user=user)
#            
#            profile.contact_info = request.POST.get('contact_info', profile.contact_info)
#            profile.address = request.POST.get('address', profile.address)
#            profile.save()
#
#            messages.success(request, 'Profile updated successfully', 'alert-success')
#
#    except Exception as e:
#        messages.error(request, "Couldn't update profile", "alert-danger")
#        print(e)
#    
#    return render(request, 'accounts/beneficiary/update_beneficiary_profile.html')



#def beneficiary_profile_view(request: HttpRequest, user_name):
#    try:
#        user = User.objects.get(username=user_name)
#        profile = ProfileBeneficiary.objects.filter(user=user).first()
#        if not profile:
#            profile = ProfileBeneficiary.objects.create(user=user)
#
#        return render(request, 'accounts/beneficiary/beneficiary_profile.html', {
#            'user': user,
#            'profile': profile
#        })
#
#    except Exception as e:
#        print(e)
#        return render(request, '404.html')
