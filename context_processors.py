from django.conf import settings


def tougcomsys(request):
    # the following line adds the name of the active theme to be returned with the key name 'active'
    return {"tougcomsys": settings.TOUGCOMSYS}
