from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from payment.models import Payment
from order.models import Order
from django.shortcuts import render, get_object_or_404


def payment_page(request, order_id):
    order = Order.objects.get(id=order_id)
    amount = int(order.total * 100)  

    return render(request, 'payment/payment.html', {
        'amount': amount,
        'order_id': order.id
    })

@csrf_exempt
def save_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("بيانات الدفع:", data)

            order_id = data.get('order_id')
            ref_id = data.get('id')
            status = data.get('status')
            amount = data.get('amount') / 100

            order = Order.objects.get(id=order_id)

            Payment.objects.create(
                order=order,
                status='completed' if status == 'paid' else 'cancelled',
                total_amount=amount,
                payment_method='credit',
                ref_id=ref_id
            )

            # نحدث حالة الطلب
            order.status = 'processing'
            order.in_cart = False
            order.save()

            return JsonResponse({'message': 'تم حفظ الدفع بنجاح'}, status=201)

        except Order.DoesNotExist:
            return JsonResponse({'error': 'الطلب غير موجود'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'طلب غير صالح'}, status=400)