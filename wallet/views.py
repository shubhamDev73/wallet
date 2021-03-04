import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import Wallet

def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

def get_json(request):
    try:
        return json.loads(request.body.decode('utf-8'))
    except:
        return {}

def response(success=True, **kwargs):
    return JsonResponse({'success': success, **kwargs})

@require_POST
@csrf_exempt
def create(request, user_id):
    if user := get_user(user_id):
        if wallet := Wallet.get(user):
            return response(success=False, error='wallet already exists')
        else:
            Wallet.create(user)
            return response()
    else:
        return response(success=False, error='user does not exist')

@require_GET
def balance(request, user_id):
    if user := get_user(user_id):
        if wallet := Wallet.get(user):
            return response(balance=wallet.get_balance())
        else:
            return response(success=False, error='wallet does not exist')
    else:
        return response(success=False, error='user does not exist')

@require_POST
@csrf_exempt
def credit(request, user_id):
    amount = get_json(request).get('amount', 0)
    if user := get_user(user_id):
        if wallet := Wallet.get(user):
            wallet.credit(amount)
            return response(message=f'credited {amount}')
        else:
            return response(success=False, error='wallet does not exist')
    else:
        return response(success=False, error='user does not exist')

@require_POST
@csrf_exempt
def debit(request, user_id):
    amount = get_json(request).get('amount', 0)
    if user := get_user(user_id):
        if wallet := Wallet.get(user):
            wallet.debit(amount)
            return response(message=f'debited {amount}')
        else:
            return response(success=False, error='wallet does not exist')
    else:
        return response(success=False, error='user does not exist')
