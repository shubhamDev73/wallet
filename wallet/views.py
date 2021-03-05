import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import Wallet
from .decorators import transaction

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
@transaction
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
@transaction
def debit(request, user_id):
    amount = get_json(request).get('amount')
    if type(amount) is not int or amount <= 0:
        return response(success=False, error='invalid amount')

    if user := get_user(user_id):
        if wallet := Wallet.get(user):
            try:
                wallet.debit(amount)
                return response(message=f'debited {amount}')
            except Exception as e:
                return response(success=False, error='transaction not allowed', message=e.message)
        else:
            return response(success=False, error='wallet does not exist')
    else:
        return response(success=False, error='user does not exist')

@require_POST
@csrf_exempt
@transaction
def credit(request, user_id):
    amount = get_json(request).get('amount')
    if type(amount) is not int or amount <= 0:
        return response(success=False, error='invalid amount')

    if user := get_user(user_id):
        if wallet := Wallet.get(user):
            try:
                wallet.credit(amount)
                return response(message=f'credited {amount}')
            except Exception as e:
                return response(success=False, error='transaction not allowed', message=e.message)
        else:
            return response(success=False, error='wallet does not exist')
    else:
        return response(success=False, error='user does not exist')
