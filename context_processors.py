from django.conf import settings

def tougcomsys(request):
    return {
        "tougcomsys": settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]
    }

