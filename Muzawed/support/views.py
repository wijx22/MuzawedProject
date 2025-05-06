from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, reverse
from notification.models import Notification

from .forms import ReportForm
from .models import Report, ReportReply


@login_required
def create_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()

            Notification.objects.create(
                recipient=request.user,
                notification_type="alert",
                message=f'تم استلام بلاغك بعنوان "{report.subject}". سنتواصل معك قريبًا.',
            )

            messages.success(request, "تم إرسال الشكوى بنجاح.", "alert-success")

        return redirect("support:create_report")

    return render(request, "reports/create_report.html")


def view_report_replies(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if not request.user.is_staff and report.user != request.user:
        messages.error(request, "ليس لديك صلاحية لعرض هذه الشكوى.", "alert-danger")
        return redirect("administration:report_list")

    if request.user.is_staff:
        replies = ReportReply.objects.filter(report=report).order_by("-created_at")
    else:
        replies = ReportReply.objects.filter(
            report=report, is_admin_reply=True
        ).order_by("-created_at")

    return render(
        request, "reports/report_replies.html", {"report": report, "replies": replies}
    )





def view_reports(request):
    # عرض جميع الشكاوى
    reports = Report.objects.filter(user=request.user)
    
    return render(request, "reports/report_list.html", {
        "reports": reports
    })


# def reply_to_report_view(request, report_id):
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
# def report_list_view(request):
#    # عرض جميع الشكاوى
#    reports = Report.objects.all()
#
#    return render(request, 'reports/report_list.html', {
#        'reports': reports,
#    })
#
# def reply_to_report_view(request, report_id):
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
