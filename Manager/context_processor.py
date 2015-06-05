from Manager.models import Competition

def competition_state(request):
    return {'competition_state': Competition.objects.get(id=1).state,}

def competition_active(request):
            return {'competition_active': Competition.objects.get(id=1).is_active,}

def competition_generated(request):
            return {'competition_generated' :Competition.objects.get(id=1).generated,}


