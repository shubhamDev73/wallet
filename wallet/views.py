import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import Wallet

def get_user(user_id):
    return User.objects.get(id=user_id)

def get_json(request):
    return json.loads(request.body.decode('utf-8'))

@require_POST
@csrf_exempt
def create(request, user_id):
    Wallet.create(get_user(user_id))
    return JsonResponse({'success': True})

@require_GET
def balance(request, user_id):
    wallet = Wallet.get(get_user(user_id))
    return JsonResponse({'success': True, 'balance': wallet.get_balance()})

@require_POST
@csrf_exempt
def credit(request, user_id):
    wallet = Wallet.get(get_user(user_id))
    json = get_json(request)
    wallet.credit(json['amount'])
    return JsonResponse({'success': True})

@require_POST
@csrf_exempt
def debit(request, user_id):
    wallet = Wallet.get(get_user(user_id))
    json = get_json(request)
    wallet.debit(json['amount'])
    return JsonResponse({'success': True})
