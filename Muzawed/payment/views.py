from django.shortcuts import render

# Create your views here.
def payment_page(request):
    return render(request, 'payment/payment.html')


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def save_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # تقدر تحفظها في قاعدة البيانات هنا
        print("تم الدفع:", data)
        return JsonResponse({'message': 'Payment received!'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)
