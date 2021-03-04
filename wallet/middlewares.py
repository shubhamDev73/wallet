from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

globals = settings.GLOBALS

class TransactionMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):

        if getattr(view_func, 'transaction', False):
            user_id = view_kwargs['user_id']
            while user_id in globals['transactions']:
                pass
            globals['transactions'].add(user_id)
            data = view_func(request, *view_args, **view_kwargs)
            globals['transactions'].remove(user_id)
            return data
        else:
            return view_func(request, *view_args, **view_kwargs)
