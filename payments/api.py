from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .paymob import get_paymob_token, create_order, get_payment_key, card_payment
from Reservation.models import Reservation
from django.shortcuts import redirect
from django.http import HttpResponseRedirect



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def update_reservation_details(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id, created_by=request.user)

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone = request.data.get('phone')

        reservation.first_name = first_name
        reservation.last_name = last_name
        reservation.email = email
        reservation.phone = phone
        reservation.save()

        return Response({'success': True, 'message': 'Reservation details updated successfully.'})

    except Reservation.DoesNotExist:
        return Response({'success': False, 'error': 'Reservation not found.'}, status=404)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def initiate_payment(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id, created_by=request.user)
        
        paymob_token = get_paymob_token()

        amount_cents = int(reservation.total_price * 100)
        order_id = create_order(paymob_token, amount_cents)

        payment_token = get_payment_key(paymob_token, order_id, amount_cents)

        reservation.paymob_order_id = order_id
        reservation.save()

        iframe_url = card_payment(payment_token)

        return Response({'success': True, 'iframe_url': iframe_url})

    except Reservation.DoesNotExist:
        return Response({'success': False, 'error': 'Reservation not found.'}, status=404)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def payment_status_webhook(request):
    print("Hellllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllo")
    # data = request.GET.dict()
     # Process the transaction data
    payment_status_str = request.GET.get('success')
    transaction_id = request.GET.get('id')
    paymob_order_id  = request.GET.get('order')
    payment_status = True if payment_status_str == 'true' else False
    
    reservation = Reservation.objects.get(paymob_order_id=paymob_order_id)

        # Update reservation based on payment status
    reservation.is_paid = payment_status
    reservation.payment_status = 'Paid' if payment_status else 'Failed'
    reservation.save()
    
    if payment_status:
      
        print(f"Transaction {transaction_id} for Order {paymob_order_id} successfully processed.")

    return Response({
            'success': True,
            'redirect_url': 'http://localhost:5173/'
        })  

@api_view(['GET'])
@permission_classes([AllowAny])
def payment_redirect(request):
    success = request.query_params.get('success')
    
    if success == 'true':
        return HttpResponseRedirect("http://localhost:5173/")
    return Response({"received_param": success})