from django.conf import settings

def tougcomsys(request):
    #the following line adds the name of the active theme to be returned with the key name 'active'
    settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]['active']=settings.TOUGCOMSYS['active']
    return {
        "tougcomsys": settings.TOUGCOMSYS[settings.TOUGCOMSYS['active']]
    }

