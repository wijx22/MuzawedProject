from django.shortcuts import render, redirect
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



