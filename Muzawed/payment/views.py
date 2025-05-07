from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib import messages
from order.views import complete_order
from payment.models import Payment
from order.models import Order
from django.shortcuts import render, get_object_or_404

def payment_gateway(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    order = payment.order

    return render(request, 'payment/payment.html', {
        'payment': payment,
        'amount': order.total,  
        'order_id': order.id,
    })

@csrf_exempt
def save_payment(request):
    if request.method == "POST":
        try:
            import json
            data = json.loads(request.body)
            payment_id = data.get('order_id')
            payment = get_object_or_404(Payment, order_id=payment_id)

            # Update payment status and ref_id
    
            if data.get('status') == 'initiated':
                payment.status = Payment.StatusChoices.COMPLETED
                payment.ref_id = data.get('id')  # Assuming 'id' is the Moyasar payment ID
                cart_items = payment.order.items.all()
                complete_order(payment.order, cart_items, payment)
                messages.success(request, "تم اتمام الطلب بنجاح!")
                payment.save()

            else:
                payment.status = Payment.StatusChoices.CANCELLED
                messages.success(request, "حدث خطأاثناء محاولة الدفع !")



            return JsonResponse({'status': 'success'})

        except Exception as e:
            print(f"Error saving payment: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)


  