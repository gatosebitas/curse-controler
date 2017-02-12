from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Person, SessionAccount
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from main.utils import sort_by_last_session


def home(req):
    session = SessionAccount.objects.last()
    users = Person.objects.filter(is_active=True)

    if session and session.is_available:
        person_using = Person.update_who_is_using(users, session)
        if req.user.is_authenticated() and person_using:
            req.user.using_account = person_using.email == req.user.email
    else:
        session = None

    if req.user.is_authenticated():
        Person.set_picture(req.user)

    users = sorted(users, key=sort_by_last_session, reverse=True)

    return render(req, 'main/home.html', locals())


@csrf_exempt
@require_POST
def login_handler(request):
    data = {
        'email': request.POST.get('email'),
        'username': request.POST.get('name'),
        'first_name': request.POST.get('first_name'),
        'last_name': request.POST.get('last_name'),
        'picture': request.POST.get('picture'),
        'fb_id': request.POST.get('id')
    }
    data['email'] = data['email'] or '{}@anon.com'.format(data['first_name'].lower())  # NOQA

    try:
        user = Person.objects.get(email=data['email'])
    except Person.DoesNotExist:
        user = Person(**data)
        user.save()
    else:
        if not user.is_active:
            return HttpResponse('Usuario no habilitado', status=403)

    login(request, user)
    return HttpResponse()


@csrf_exempt
@require_POST
def logout_handler(request):
    logout(request)
    return HttpResponse()


@csrf_exempt
def sessions(req, pk=-1):
    if 'PUT' == req.method:
        session = get_object_or_404(SessionAccount, pk=pk)
        session.is_active = False
        session.save()
        return HttpResponse()

    if 'POST' == req.method:
        session = SessionAccount.objects.last()
        if session and session.is_available:
            return HttpResponse('La cuenta esta siendo usada en estos momentos', status=400)

        session_data = {
            'session_time': req.POST.get('session_time'),
            'person': Person.get_by_email(req.POST.get('personEmail'), True),
        }
        session = SessionAccount(**session_data)
        session.save()
        return HttpResponse()
    return HttpResponse('Not Allowed', status=405)
