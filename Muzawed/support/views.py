from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Report, ReportReply
from django.contrib import messages
from notification.models import Notification                                        

# Create your views here.
def create_report_view(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        attachment = request.FILES.get('attachment') 

        report = Report.objects.create(
            user=request.user,
            category=category,
            subject=subject,
            description=description,
            attachment=attachment 
        )
        Notification.objects.create(
                            recipient=request.user,
                            notification_type='alert',
                            message=f'تم استلام بلاغك بعنوان "{report.subject}". سنتواصل معك قريبًا.'
                        )

        messages.success(request, 'تم إرسال الشكوى بنجاح.', 'alert-success')
        #return redirect('report_detail', pk=report.pk)

    return render(request, 'reports/create_report.html')



#def reply_to_report_view(request, report_id):
#    report = Report.objects.get(id=report_id)
#    if request.method == 'POST':
#        reply_text = request.POST.get('reply_text')
#        ReportReply.objects.create(
#            report=report,
#            admin=request.user,
#            reply_text=reply_text
#        )
#        messages.success(request, 'تم إرسال الرد بنجاح.', 'alert-success')
#        return redirect('report_detail', pk=report.pk)  
#
#    return render(request, 'reports/reply_to_report.html', {'report': report})
# test2 is working
#def report_list_view(request):
#    # عرض جميع الشكاوى
#    reports = Report.objects.all()
#
#    return render(request, 'reports/report_list.html', {
#        'reports': reports,
#    })
#
#def reply_to_report_view(request, report_id):
#    # جلب التقرير بناءً على ID
#    report = get_object_or_404(Report, id=report_id)
#
#    # عرض الردود السابقة
#    replies = ReportReply.objects.filter(report=report)
#
#    # الرد على الشكوى
#    if request.method == 'POST':
#        message = request.POST.get('message')
#        responder = request.user  # الرد من المستخدم أو الأدمن
#
#        # التحقق إذا كان الرد من الأدمن أو المستخدم
#        is_admin_reply = request.user.is_staff  # تحديد إذا كان المستخدم هو الأدمن أم لا
#
#        # التحقق من حالة التقرير وتحديثها بناءً على الاختيار
#        new_status = request.POST.get('status')
#        if new_status in ['in_progress', 'closed']:
#            report.status = new_status
#            report.save()
#
#        # إضافة الرد إلى قاعدة البيانات
#        report_reply = ReportReply(
#            report=report,
#            responder=responder,
#            message=message,
#            is_admin_reply=is_admin_reply  # تحديد إذا كان الرد من الأدمن
#        )
#        report_reply.save()
#
#        # إرسال رسالة تفيد بأن الرد تم بنجاح
#        messages.success(request, 'تم الرد على الشكوى بنجاح.', 'alert-success')
#        return redirect('support:reply_to_report_view', report_id=report.id)
#
#    return render(request, 'reports/reply_to_report.html', {
#        'report': report,
#        'replies': replies,
#    })
#