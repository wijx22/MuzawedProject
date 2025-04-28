from django.shortcuts import render, get_object_or_404, reverse, redirect
from accounts.models import ProfileBeneficiary, SupplierProfile
from django.contrib.auth import get_user_model
from main.models import Contact
from support.models import Report, ReportReply
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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



#def suppliers_list_view(request):
#    suppliers = SupplierProfile.objects.select_related('user').all()
#
#    if request.method == 'POST':
#        supplier_id = request.POST.get('supplier_id')
#        
#        # التفعيل / التعطيل
#        if 'toggle_activation' in request.POST:
#            try:
#                supplier_profile = SupplierProfile.objects.get(id=supplier_id)
#                supplier_profile.is_active = not supplier_profile.is_active
#                supplier_profile.save()
#                messages.success(request, f"تم {'تفعيل' if supplier_profile.is_active else 'تعطيل'} حساب المورد بنجاح.")
#            except SupplierProfile.DoesNotExist:
#                messages.error(request, "المورد غير موجود.")
#
#        # الحذف
#        elif 'delete_supplier' in request.POST:
#            try:
#                supplier_profile = SupplierProfile.objects.get(id=supplier_id)
#                supplier_profile.delete()
#                messages.success(request, "تم حذف المورد بنجاح.")
#            except SupplierProfile.DoesNotExist:
#                messages.error(request, "المورد غير موجود.")
#        
#        return redirect('administration:suppliers_list_view')
#
#    return render(request, 'administration/suppliers_list.html', {
#        'suppliers': suppliers
#    })


def suppliers_list_view(request):
    suppliers = SupplierProfile.objects.select_related('user').all()

    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')
        
        if 'toggle_activation' in request.POST:
            try:
                supplier_profile = SupplierProfile.objects.get(id=supplier_id)
                supplier_profile.is_active = not supplier_profile.is_active
                supplier_profile.save()
                messages.success(request, f"تم {'تفعيل' if supplier_profile.is_active else 'تعطيل'} حساب المورد بنجاح.")
            except SupplierProfile.DoesNotExist:
                messages.error(request, "المورد غير موجود.")

        elif 'delete_supplier' in request.POST:
            try:
                supplier_profile = SupplierProfile.objects.get(id=supplier_id)
                
                supplier_profile.user.delete() 
                supplier_profile.delete()  

                messages.success(request, "تم حذف المورد بنجاح.")
            except SupplierProfile.DoesNotExist:
                messages.error(request, "المورد غير موجود.")
        
        return redirect('administration:suppliers_list_view')

    return render(request, 'administration/suppliers_list.html', {
        'suppliers': suppliers
    })

#def suppliers_list_view(request):
#    suppliers = SupplierProfile.objects.select_related('user').all()
#    return render(request, 'administration/suppliers_list.html', {
#        'suppliers': suppliers
#    })


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






#def report_list_view(request):
#    reports = Report.objects.all()
#
#    return render(request, 'administration/report_list.html', {
#        'reports': reports,
#    })

def report_list_view(request):
    if request.user.is_staff:
        reports = Report.objects.all()
    else:
        reports = Report.objects.filter(user=request.user)

    return render(request, 'administration/report_list.html', {
        'reports': reports,
    })



def reply_to_report_view(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    replies = ReportReply.objects.filter(report=report)

    if not request.user.is_staff:
        messages.error(request, "ليس لديك صلاحية للرد على الشكوى.", 'alert-danger')
        return redirect('administration:report_list')





    if request.method == 'POST':
        message = request.POST.get('message')
        responder = request.user  

        new_status = request.POST.get('status')
        if new_status in ['in_progress', 'closed']:
            report.status = new_status
            report.save()

        report_reply = ReportReply(
            report=report,
            responder=responder,
            message=message,
            is_admin_reply=True  
        )
        report_reply.save()

        messages.success(request, 'تم الرد على الشكوى بنجاح.', 'alert-success')
        return redirect('administration:reply_to_report_view', report_id=report.id)

    return render(request, 'administration/reply_to_report.html', {
        'report': report,
        'replies': replies,
    })




def view_report_replies(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    replies = ReportReply.objects.filter(report=report).order_by('-created_at')
    return render(request, 'administration/report_replies.html', {'report': report, 'replies': replies})
