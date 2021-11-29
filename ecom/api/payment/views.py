from json.encoder import JSONEncoder
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

import braintree


gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id='qtq7ttdw9s6s8th6',
    public_key='2s98p4fm86qgtpjv',
    private_key='7a9222cb02cc2c6db69a7b272705173e'
  )
)

def validate_user_session(id, token):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def generate_token(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({'error':'Invalid session,login again'})
    return JsonResponse({'clientToken':gateway.client_token.generate(),'success':True})

@csrf_exempt
def process_payment(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({'error':'Invalid session,login again'})

    nonce_from_the_client=request.POST["paymentMethodNonce"]
    amount_from_the_client=request.POST["amount"]

    result = gateway.transaction.sale({
    "amount": amount_from_the_client,
    "payment_method_nonce": nonce_from_the_client,
    "options": {
      "submit_for_settlement": True
    }
    })

    if result.is_success:
        return JsonResponse({"success":result.is_success,"transaction":{'id':result.transaction.id,'amount':result.transaction.amount}})
    else:
        return JsonResponse({'error':True,'success':False})

    