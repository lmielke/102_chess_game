from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from . tokens import account_activation_token
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import get_connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from web_project.helper import MyHelper
from django.http import HttpResponse
import os

def get_email_connection():
    use_tls = True
    use_ssl = False
    fail_silently=False
    connection = get_connection(host=settings.EMAIL_HOST,
                        port=settings.EMAIL_PORT,
                        username=settings.EMAIL_HOST_USER,
                        password=settings.EMAIL_HOST_PASSWORD,
                        use_tls=use_tls,
                        use_ssl=use_ssl,
            fail_silently=fail_silently)
    return connection

def register(request):
    """
            handels user registration
            if the form validates it saves the user to the database
            after saving the user is redirected to
    """
    helper_text = MyHelper.get_web_modes('helper', os.environ.get('WEB_MODE', '0'))
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            username = form.cleaned_data.get('username')
            # before user is saved do some checking
            email = form.cleaned_data.get('email')
            if email.endswith(".ru"):
                return redirect('https://de.securelist.com/redirects-im-spam/59778')
            user.save()
            # assignes the auth Group to the newly created user
            my_group = Group.objects.get(name='commenter_group')
            my_group.user_set.add(User.objects.get(username=username))
            # sent verification mail
            current_site = get_current_site(request)
            connection = get_email_connection()
            subject = 'Aktivieren Sie mit diesem Link ihren Zugang!'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': "https://" + request.META['HTTP_HOST'],
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                        })
            from_email = settings.EMAIL_HOST_USER
            print(from_email,"email here")
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                subject, message, settings.EMAIL_HOST_USER, [to_email], connection=connection)
            email.send()
            messages.success(request, helper_text.get('user_views_msg_1', 'no text'))
            return redirect('checkmail')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def activate(request, uidb64, token):
    helper_text = MyHelper.get_web_modes('helper', os.environ.get('WEB_MODE', '0'))
    try:
        uid = uidb64[2:-1]
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print(uidb64, user, token)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, helper_text.get('user_views_msg_2', 'no text'))
        return redirect('login')
    else:
        messages.warning(request, helper_text.get('user_views_msg_3', 'no text'))
        return HttpResponse(helper_text.get('user_views_msg_3', 'no text'))

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Pofil wurde gesichert!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    view_args = {'page_title': "Profil",
                'template_name': 'users/profile.html',
                'extensions': ['blog/body.html',  'blog/base_iframe.html']}
    session = MyHelper()
    tgt_url_args = session.parse_tgt_url(request.path_info)
    context.update(session.get_context_metadata(view_args=view_args, request=request))
    print(f"\ncontext dict: {context}\n")
    return render(request, 'users/profile.html', context)

def impressum(request):
    context = {}
    view_args = {'page_title': "Profil",
                'template_name': 'users/impressum.html',
                'extensions': ['blog/body.html',  False]}
    session = MyHelper()
    tgt_url_args = session.parse_tgt_url(request.path_info)
    context.update(session.get_context_metadata(view_args=view_args, request=request))
    print(f"\ncontext dict: {context}\n")
    return render(request, 'users/impressum.html', context)


def my_cv(request):
    context = {}
    view_args = {'page_title': "Profil",
                'template_name': 'users/my_cv.html',
                'extensions': ['blog/body.html',  False]}
    session = MyHelper()
    tgt_url_args = session.parse_tgt_url(request.path_info)
    context.update(session.get_context_metadata(view_args=view_args, request=request))
    print(f"\ncontext dict: {context}\n")
    return render(request, 'users/my_cv.html', context)
