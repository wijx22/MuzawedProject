from django.shortcuts import render
from accounts.models import ProfileBeneficiary, SupplierProfile
from django.contrib.auth import get_user_model
from main.models import Contact
User = get_user_model()

def dashboard(request):
    new_suppliers_count = SupplierProfile.objects.count()
    beneficiaries_count = ProfileBeneficiary.objects.count()
    total_users = User.objects.count()


    context = {

        'new_suppliers_count': new_suppliers_count,
        'beneficiaries_count': beneficiaries_count,
        'total_users': total_users,

    }

    return render(request, 'administration/dashboard.html', context)


def suppliers_list_view(request):
    suppliers = SupplierProfile.objects.select_related('user').all()
    return render(request, 'administration/suppliers_list.html', {
        'suppliers': suppliers
    })


def beneficiary_list_view(request):
    beneficiaries = ProfileBeneficiary.objects.select_related('user').all()
    return render(request, 'administration/beneficiary_list.html', {
        'beneficiaries': beneficiaries
    })



def contact_messages_list_view(request):
    messages = Contact.objects.all().order_by('-created_at')
    return render(request, 'administration/contact_list.html', {
        'messages': messages
    })
