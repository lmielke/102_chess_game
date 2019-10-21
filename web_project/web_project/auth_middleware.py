import os, re, requests
from datetime import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from web_project.helper import MyHelper
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group, Permission


class LoginRequiredMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
            Auth Checks on incoming request
            sets web_mode depending on request.META['HTTP_HOST']
            if path.endswith auth relevant action, then check action authorization
        """
        # sets the landing page, if path is blank
        if request.META['PATH_INFO'] == "/":
            return redirect("/blog/articles/Theme=0/Article=0/Frame=0/view/")
        # setting web_mode - not auth check
        #request.META['HTTP_HOST'] = 'wutmensch.de'# if settings.PRODUCTION == True else "black-pelican.rocks"
        print("auth_middleware web_mode: {}".format(request.META['HTTP_HOST']))
        session = MyHelper()
        session.set_web_mode(hostname=request.META['HTTP_HOST'])
        session.set_web_sys(hostname=request.META['HTTP_HOST'])
        # for key, values in request.META.items():
        #     print(key, values)
        # auth check starts here
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        login_not_required = path in settings.LOGIN_NOT_REQUIRED
        login_forbidden = path in settings.LOGIN_FORBIDDEN
        print(f'\n\nauth_middleware with path: {path}')
        if False: #settings.PRODUCTION == False:  # !!! REPLACE WHEN SHIP TO CUSTOMER !!!
            print('!!! Development authorizations apply !!!')
            return None
        elif path.startswith('admin/') or path.startswith('media/') or path in settings.LOGIN_NOT_REQUIRED:
            return None
        elif request.user.is_authenticated and login_forbidden:
            return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.is_authenticated and not login_forbidden:
            return self.action_authorization(request, path, session)
        elif not request.user.is_authenticated and login_not_required:
            return None
        else:
            return None

    def action_authorization(self, request, path, session):
        """
            if path.endswith auth relevant action, then check action authorization
            if parmissions are missing then return auth error and redirect to origin
            else return None
        """
        path_list = path.strip('/').split('/')
        auth_action = str(path_list[-1])
        if auth_action in session.get_auth_actions():
            auth_app = str(path_list[0])
            db_models = session.parse_tgt_url(path)
            auth_model = [str(db_model).lower() for db_model in db_models.keys() if db_model != 'Frame' and not type(db_model)==int][-1]
            auth_value = auth_app + '.' + auth_action + '_' + auth_model
            if not request.user.has_perm(auth_value):
                auth_failed_redirect = '/' + path.replace(auth_action, 'view')
                messages.warning(request, 'Sie verfügen nicht über die erforderlichen Berechtigungen!')
                return redirect(auth_failed_redirect)
        return None
