from django.shortcuts import render, get_object_or_404, reverse, redirect
from accounts.models import ProfileBeneficiary, SupplierProfile
from django.contrib.auth import get_user_model
from main.models import Contact
from support.models import Report, ReportReply
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from supplier.models import CommercialInfo, SupplyDetails
from products.models import Product
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


#def supplier_requests_list(request):
#    if request.user.is_staff:  
#        suppliers = SupplierProfile.objects.filter(status=SupplierProfile.RequestStatusChoises.PENDING)
#        return render(request, 'administration/supplier_requests.html', {'suppliers': suppliers})
#    else:
#        messages.error(request, "غير مصرح لك.")
#        return redirect("main:index_view")



#test3 with try and excepts

def supplier_requests_list(request):
    if not request.user.is_staff:
        messages.error(request, "غير مصرح لك.")
        return redirect("main:index_view")
    
    try:
        pending_suppliers = SupplierProfile.objects.all()
        return render(request, 'administration/supplier_requests.html', {'suppliers': pending_suppliers})
    except Exception as e:
        messages.error(request, f"حدث خطأ أثناء جلب بيانات الموردين: {e}")
        return redirect("main:index_view")


def supplier_request_detail(request, supplier_id):
    if not request.user.is_staff:
        messages.error(request, "غير مصرح لك.")
        return redirect("main:index_view")

    try:
        supplier = get_object_or_404(SupplierProfile, id=supplier_id)
        commercial_info = CommercialInfo.objects.filter(supplier=supplier).first()
        supply_details = SupplyDetails.objects.filter(supplier=supplier).first()

        context = {
            'supplier': supplier,
            'commercial_info': commercial_info,
            'supply_details': supply_details,
        }

        return render(request, 'administration/supplier_request_detail.html', context)
    except Exception as e:
        messages.error(request, f"حدث خطأ أثناء تحميل تفاصيل المورد: {e}")
        return redirect("administration:supplier_requests_list")


def approve_supplier_view(request, supplier_id):
    if not request.user.is_staff:
        messages.warning(request, "غير مصرح لك بالوصول")
        return redirect("main:index_view")

    try:
        supplier = get_object_or_404(SupplierProfile, id=supplier_id)
        supplier.status = SupplierProfile.RequestStatusChoises.ACCEPTED
        supplier.is_active = True
        supplier.save()

        messages.success(request, "تم قبول المورد وتفعيل الحساب بنجاح.")
        return redirect("administration:supplier_request_detail", supplier_id=supplier.id)
    except Exception as e:
        messages.error(request, f"حدث خطأ أثناء قبول المورد: {e}")
        return redirect("administration:supplier_requests_list")


def reject_supplier_view(request, supplier_id):
    if not request.user.is_staff:
        messages.warning(request, "غير مصرح لك بالوصول")
        return redirect("main:index_view")

    try:
        supplier = get_object_or_404(SupplierProfile, id=supplier_id)
        rejection_reason = request.POST.get('reason', 'تم الرفض من قبل الإدارة.')

        supplier.status = SupplierProfile.RequestStatusChoises.REJECTED
        supplier.rejection_reason = rejection_reason
        supplier.is_active = False
        supplier.save()

        messages.success(request, "تم رفض المورد.")
        return redirect("administration:supplier_request_detail", supplier_id=supplier.id)
    except Exception as e:
        messages.error(request, f"حدث خطأ أثناء رفض المورد: {e}")
        return redirect("administration:supplier_requests_list")




def supplier_products_view(request, supplier_id):
    try:
        supplier = get_object_or_404(User, id=supplier_id)
        products = Product.objects.filter(supplier=supplier)
        return render(request, 'administration/supplier_products.html', {
            'supplier': supplier,
            'products': products
        })
    except Exception as e:
        messages.error(request, f"حدث خطأ أثناء جلب المنتجات: {e}")
        return redirect("main:index_view")
  



#def supplier_requests_list(request):
#    if request.user.is_staff:  
#     #pending_suppliers = SupplierProfile.objects.filter(status=SupplierProfile.RequestStatusChoises.PENDING)
#     pending_suppliers = SupplierProfile.objects.all()
#
#     return render(request, 'administration/supplier_requests.html', {'suppliers': pending_suppliers})
#
#    else:
#        messages.error(request, "غير مصرح لك.")
#        return redirect("main:index_view")
#
#
#
#def supplier_request_detail(request, supplier_id):
#    supplier = get_object_or_404(SupplierProfile, id=supplier_id)
#    commercial_info = CommercialInfo.objects.filter(supplier=supplier).first()
#    supply_details = SupplyDetails.objects.filter(supplier=supplier).first()
#
#    context = {
#        'supplier': supplier,
#        'commercial_info': commercial_info,
#        'supply_details': supply_details,
#    }
#
#    return render(request, 'administration/supplier_request_detail.html', context)
#
#
#
#
#
#def approve_supplier_view(request, supplier_id):
#    if not request.user.is_staff:
#        messages.warning(request, "غير مصرح لك بالوصول")
#        return redirect("main:index_view")
#
#    supplier = get_object_or_404(SupplierProfile, id=supplier_id)
#
#    supplier.status = SupplierProfile.RequestStatusChoises.ACCEPTED
#    supplier.is_active = True
#    supplier.save()
#
#    messages.success(request, "تم قبول المورد وتفعيل الحساب بنجاح.")
#    return redirect("administration:supplier_request_detail", supplier_id=supplier.id)
#
#
#def reject_supplier_view(request, supplier_id):
#    if not request.user.is_staff:
#        messages.warning(request, "غير مصرح لك بالوصول")
#        return redirect("main:index_view")
#    supplier = get_object_or_404(SupplierProfile, id=supplier_id)
#
#    rejection_reason = request.POST.get('reason', 'تم الرفض من قبل الإدارة.')
#
#    supplier.status = SupplierProfile.RequestStatusChoises.REJECTED
#    supplier.rejection_reason = rejection_reason
#    supplier.is_active = False
#    supplier.save()
#
#    messages.success(request, "تم رفض المورد.")
#    return redirect("administration:supplier_request_detail", supplier_id=supplier.id)
#



#def supplier_request_action(request, supplier_id):
#    if not request.user.is_staff:
#        messages.warning(request, "غير مصرح لك بالوصول")
#        return redirect("main:index_view")
#
#    supplier = get_object_or_404(SupplierProfile, id=supplier_id)
#
#    if request.method == "POST":
#        action = request.POST.get("action")
#
#        if action == "approve":
#            supplier.status = SupplierProfile.RequestStatusChoises.ACCEPTED
#            supplier.is_active = True
#            messages.success(request, "تم قبول المورد.")
#        elif action == "reject":
#            reason = request.POST.get("reason", "تم الرفض من قبل الإدارة.")
#            supplier.status = SupplierProfile.RequestStatusChoises.REJECTED
#            supplier.rejection_reason = reason
#            supplier.is_active = False
#            messages.success(request, "تم رفض المورد.")
#
#        supplier.save()
#
#    return redirect("administration:supplier_request_detail", supplier_id=supplier.id)


