from django.shortcuts import render, get_object_or_404, reverse, redirect
from accounts.models import ProfileBeneficiary, SupplierProfile
from django.contrib.auth import get_user_model
from main.models import Contact
from support.models import Report, ReportReply
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from supplier.models import CommercialInfo, SupplyDetails
from products.models import Product
from notification.models import Notification
from django.db.models import Count
from order.models import Order
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator

User = get_user_model()

#def dashboard(request):
#    new_suppliers = SupplierProfile.objects.filter(status='Pending')
#
#    new_suppliers_count = SupplierProfile.objects.count()
#    beneficiaries_count = ProfileBeneficiary.objects.count()
#    total_users = User.objects.count()
#
#
#    status_counts = SupplierProfile.objects.values('status').annotate(count=Count('id'))
#    status_data = {
#        'مقبول': 0,
#        'مرفوض': 0,
#        'قيد المعالجة': 0,
#        'لا طلب': 0
#    }
#
#    for status in status_counts:
#        if status['status'] == 'Accepted':
#            status_data['مقبول'] = status['count']
#        elif status['status'] == 'Rejected':
#            status_data['مرفوض'] = status['count']
#        elif status['status'] == 'Pending':
#            status_data['قيد المعالجة'] = status['count']
#        elif status['status'] == 'No-request':
#            status_data['لا طلب'] = status['count']
#
#    print(status_data)
#    
#    #suppliers = SupplierProfile.objects.all()
#    open_count = Report.objects.filter(status='open').count()
#    closed_count = Report.objects.filter(status='closed').count()
#    in_progress_count = Report.objects.filter(status='in_progress').count()
#
#
#    context = {
#
#        'new_suppliers_count': new_suppliers_count,
#        'beneficiaries_count': beneficiaries_count,
#        'total_users': total_users,
#        'status_counts': status_data, 
#        'suppliers': new_suppliers,
#        'open_count': open_count,
#        'closed_count': closed_count,
#        'in_progress_count': in_progress_count
#
#
#
#    }
#
#    return render(request, 'administration/dashboard.html', context)
#


def dashboard(request):
    try:
        new_suppliers = SupplierProfile.objects.filter(status='Pending')
        new_suppliers_count = SupplierProfile.objects.count()
        beneficiaries_count = ProfileBeneficiary.objects.count()
        total_users = User.objects.count()

        status_counts = SupplierProfile.objects.values('status').annotate(count=Count('id'))
        status_data = {
            'مقبول': 0,
            'مرفوض': 0,
            'قيد المعالجة': 0,
            'لا طلب': 0
        }

        for status in status_counts:
            if status['status'] == 'Accepted':
                status_data['مقبول'] = status['count']
            elif status['status'] == 'Rejected':
                status_data['مرفوض'] = status['count']
            elif status['status'] == 'Pending':
                status_data['قيد_المعالجة'] = status['count']
            elif status['status'] == 'No-request':
                status_data['لا_طلب'] = status['count']

        open_count = Report.objects.filter(status='open').count()
        closed_count = Report.objects.filter(status='closed').count()
        in_progress_count = Report.objects.filter(status='in_progress').count()
        print(f'in_progress is: {in_progress_count}')
        
    except Exception as e:
        print(f"Error in dashboard view: {e}")
        messages.error(request, "حدث خطأ أثناء تحميل لوحة التحكم.")
        new_suppliers = []
        new_suppliers_count = 0
        beneficiaries_count = 0
        total_users = 0
        status_data = {
            'مقبول': 0,
            'مرفوض': 0,
            'قيد_المعالجة': 0,
            'لا_طلب': 0
        }
        open_count = closed_count = in_progress_count = 0

    context = {
        'new_suppliers_count': new_suppliers_count,
        'beneficiaries_count': beneficiaries_count,
        'total_users': total_users,
        'status_counts': status_data, 
        'suppliers': new_suppliers,
        'open_count': open_count,
        'closed_count': closed_count,
        'in_progress_count': in_progress_count
    }

    return render(request, 'administration/dashboard.html', context)



def suppliers_list_view(request):
    suppliers = SupplierProfile.objects.select_related('user').all()

    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')

        try:
            if 'delete_supplier' in request.POST:
                supplier_profile = SupplierProfile.objects.get(id=supplier_id)

                supplier_profile.user.delete()
                supplier_profile.delete()



                messages.success(request, "تم حذف المورد بنجاح.")
        except SupplierProfile.DoesNotExist:
            messages.error(request, "المورد غير موجود.")
        except Exception as e:
            messages.error(request, f"حدث خطأ: {str(e)}")

        return redirect('administration:suppliers_list_view')

    return render(request, 'administration/supplier/suppliers_list.html', {
        'suppliers': suppliers,

        'hide_header': True

    })


#def suppliers_list_view(request):
#    suppliers = SupplierProfile.objects.select_related('user').all()
#
#    if request.method == 'POST':
#        supplier_id = request.POST.get('supplier_id')
#
#        try:
#            if 'delete_supplier' in request.POST:
#                supplier_profile = SupplierProfile.objects.get(id=supplier_id)
#                supplier_profile.user.delete()
#                supplier_profile.delete()
#                messages.success(request, "تم حذف المورد بنجاح.")
#
#            elif 'activate_supplier' in request.POST:
#                supplier_profile = SupplierProfile.objects.get(id=supplier_id)
#                supplier_profile.user.is_active = True
#                supplier_profile.user.save()
#                messages.success(request, "تم تفعيل المورد.")
#
#            elif 'deactivate_supplier' in request.POST:
#                supplier_profile = SupplierProfile.objects.get(id=supplier_id)
#                supplier_profile.user.is_active = False
#                supplier_profile.user.save()
#                messages.success(request, "تم تعطيل المورد.")
#
#        except SupplierProfile.DoesNotExist:
#            messages.error(request, "المورد غير موجود.")
#        except Exception as e:
#            messages.error(request, f"حدث خطأ: {str(e)}")
#
#        return redirect('administration:suppliers_list_view')
#
#    return render(request, 'administration/supplier/suppliers_list.html', {
#        'suppliers': suppliers,
#        'hide_header': True
#    })
#

def supplier_requests_list(request):
    if not request.user.is_staff:
        messages.error(request, "غير مصرح لك.")
        return redirect("main:index_view")
    
    try:
        pending_suppliers = SupplierProfile.objects.filter(commercial_info__isnull=False, supply_details__isnull=False)
        return render(request, 'administration/supplier/supplier_requests.html', {'suppliers': pending_suppliers,  'hide_header': True})

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

        print(55555)
        context = {
            'supplier': supplier,
            'commercial_info': commercial_info,
            'supply_details': supply_details,
            'hide_header': True
        }
        

        return render(request, 'administration/supplier/supplier_request_detail.html', context)

    except Exception as e:
        messages.error(request, f"حدث خطأ أثناء تحميل تفاصيل المورد: {e}")
        
        return redirect("administration:supplier_requests_view")


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
        return render(request, 'administration/supplier/supplier_products.html', {
            'supplier': supplier,
            'products': products
        })
    except Exception as e:
        messages.error(request, f"حدث خطأ أثناء جلب المنتجات: {e}")
        return redirect("main:index_view")




def beneficiary_list_view(request):
    beneficiaries = ProfileBeneficiary.objects.select_related('user').all()
    return render(request, 'administration/beneficiary/beneficiary_list.html', {
        'beneficiaries': beneficiaries,
        'hide_header': True

    })



def contact_messages_list_view(request):
    messages = Contact.objects.all().order_by('-created_at')
    return render(request, 'administration/contact/contact_list.html', {
        'messages': messages,
        'hide_header': True

    })







#def report_list_view(request):
#    if request.user.is_staff:
#        reports = Report.objects.all()
#    else:
#        reports = Report.objects.filter(user=request.user)
#
#
#
#
#
#    return render(request, 'administration/reports/report_list.html', {
#        'reports': reports,
#        'hide_header': True
#
#
#    })

def report_list_view(request):
    if request.user.is_staff:
        reports = Report.objects.all()
    else:
        reports = Report.objects.filter(user=request.user)

    return render(request, 'administration/reports/report_list.html', {
        'reports': reports,
        'hide_header': True
    })


def reply_to_report_view(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    replies = ReportReply.objects.filter(report=report)

    if not request.user.is_staff:
        messages.error(request, "ليس لديك صلاحية للرد على الشكوى.", 'alert-danger')
        return redirect('administration:report_list')





    if request.method == 'POST':
        try:
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
            Notification.objects.create(
                recipient=report.user,
                notification_type="reply",
                message=f'تم الرد على بلاغك رقم {report.id}.'
            )
    
            report_reply.save()
    
            messages.success(request, 'تم الرد على الشكوى بنجاح.', 'alert-success')
            return redirect('administration:reply_to_report_view', report_id=report.id)
        

        except Exception as e:
            print(f"Error while replying to report {report.id}: {e}")
            messages.error(request, 'حدث خطأ أثناء إرسال الرد، حاول مرة أخرى.', 'alert-danger')


    return render(request, 'administration/reports/reply_to_report.html', {
        'report': report,
        'replies': replies,
        'hide_header': True

    })




#def view_report_replies(request, report_id):
#    report = get_object_or_404(Report, id=report_id)
#    replies = ReportReply.objects.filter(report=report).order_by('-created_at')
#    return render(request, 'administration/reports/report_replies.html', {'report': report, 'replies': replies})






  







def order_requests_list(request):
    if not request.user.is_staff:
        messages.error(request, "غير مسموح لك بالوصول إلى هذه الصفحة.")
        return redirect("main:index_view")
    
    try:
        # استعلام الطلبات المفتوحة
        open_orders = Order.objects.filter(status="open")
        
        # استعلام الطلبات المغلقة
        closed_orders = Order.objects.filter(status="closed")

        return render(request, 'administration/order_requests.html', {
            'open_orders': open_orders,
            'closed_orders': closed_orders,
            'hide_header': True
        })

    except Exception as e:
        messages.error(request, f"حدث خطأ أثناء جلب بيانات الطلبات: {e}")
        return redirect("main:index_view")
    

    messages.success(request, "تم تحديث حالة المورد وإرسال الإشعار.")
    return redirect("administration:supplier_requests_list")


















#def supplier_requests_list(request):
#    if request.user.is_staff:  
#        suppliers = SupplierProfile.objects.filter(status=SupplierProfile.RequestStatusChoises.PENDING)
#        return render(request, 'administration/supplier_requests.html', {'suppliers': suppliers})
#    else:
#        messages.error(request, "غير مصرح لك.")
#        return redirect("main:index_view")

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

#هذا مع تفعيل و تعطيل حساب المورد بحيث الادمن بنفسة يفعل ويعطل
#def suppliers_list_view(request):
#    suppliers = SupplierProfile.objects.select_related('user').all()
#
#    if request.method == 'POST':
#        supplier_id = request.POST.get('supplier_id')
#        
#        if 'toggle_activation' in request.POST:
#            try:
#                supplier_profile = SupplierProfile.objects.get(id=supplier_id)
#                supplier_profile.is_active = not supplier_profile.is_active
#                supplier_profile.save()
#                messages.success(request, f"تم {'تفعيل' if supplier_profile.is_active else 'تعطيل'} حساب المورد بنجاح.")
#            except SupplierProfile.DoesNotExist:
#                messages.error(request, "المورد غير موجود.")
#
#        elif 'delete_supplier' in request.POST:
#            try:
#                supplier_profile = SupplierProfile.objects.get(id=supplier_id)
#                
#                supplier_profile.user.delete() 
#                supplier_profile.delete()  
#
#                messages.success(request, "تم حذف المورد بنجاح.")
#            except SupplierProfile.DoesNotExist:
#                messages.error(request, "المورد غير موجود.")
#        
#        return redirect('administration:suppliers_list_view')
#
#    return render(request, 'administration/supplier/suppliers_list.html', {
#        'suppliers': suppliers
#    })

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



#def update_supplier_status(request, supplier_id):
#    if not request.user.is_staff:
#        messages.error(request, "غير مصرح لك.")
#        return redirect("main:index_view")
#
#    supplier = get_object_or_404(SupplierProfile, id=supplier_id)
#    action = request.POST.get("action")
#    reason = request.POST.get("rejection_reason", "").strip()
#
#    if action == "accept":
#        supplier.status = "Accepted"
#        supplier.rejection_reason = ""
#    elif action == "reject":
#        supplier.status = "Rejected"
#        supplier.rejection_reason = reason or "لم يتم توضيح السبب."
#    else:
#        messages.error(request, "عملية غير صالحة.")
#        return redirect("administration:supplier_request_detail", supplier_id=supplier_id)
#
#    supplier.save()
#
#    
#    message = f"تم {'قبول' if supplier.status == 'Accepted' else 'رفض'} طلبك."
#    if supplier.status == "Rejected":
#        message += f" السبب: {supplier.rejection_reason}"
#    # حفظ التغييرات في قاعدة البيانات
#    supplier.save()
#
#    # إنشاء الإشعار للمورد
#    if action == "accept":
#        notif_msg = "تم قبول طلب التوريد الخاص بك. يمكنك الآن الدخول إلى لوحة المورد."
#    else:
#        notif_msg = f"تم رفض طلب التوريد الخاص بك. السبب: {supplier.rejection_reason}"
#
#    Notification.objects.create(
#        recipient=supplier.user,
#        notification_type="alert",
#        message=message
#    )
#
#    messages.success(request, "تم تحديث حالة المورد وإرسال الإشعار.")
#    return redirect("administration:supplier_requests_list")

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
