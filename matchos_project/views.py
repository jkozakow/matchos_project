from django.http import HttpResponseRedirect


def url_redirect(request):
    return HttpResponseRedirect("/matchos/")