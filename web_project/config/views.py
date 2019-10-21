import os
from django.http import HttpResponseRedirect
# Create your views here.

def set_web_style(request, web_style='False'):
    os.environ['WEB_STYLE_FIX'] = web_style
    return HttpResponseRedirect("/")

def set_web_mode(request, web_mode='localhost:8000'):
    os.environ['WEB_MODE_FIX'] = web_mode
    return HttpResponseRedirect("/")

def set_web_sys(request, web_sys='dev'):
    os.environ['WEB_SYS_FIX'] = web_sys
    return HttpResponseRedirect("/")
