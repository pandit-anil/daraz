from .models import *


def SystemSetting(request):
    sys = SystemSystem.objects.filter(status = True).first()
    return {'sys':sys}