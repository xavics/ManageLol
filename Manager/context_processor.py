from Manager.models import Competition

def competition_state(request):
    return {'state_inscriptions': Competition.objects.get(id=1).state,
            'competition_active': Competition.objects.get(id=1).state}


