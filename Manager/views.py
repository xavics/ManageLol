from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from Manager.Forms import TeamForm
from django.contrib.auth import authenticate, login, logout

def mainpage(request):
    form = TeamForm()
    return render(request, 'Main.html', {'form': form})

def register(request):
    if request.method == 'POST':
        team_form = TeamForm(data=request.POST)
        if team_form.is_valid():
            team = team_form.save()
            team.points = 0
            team.set_password(team.password)
            team.save()
            return HttpResponseRedirect('/login/')
            # return HttpResponse("Team saved correct")
        else:
            return HttpResponse("Malament..."+team_form.errors)
    else:
        team_form = TeamForm()
        return render(request, 'register.html', {'form': team_form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        team = authenticate(username=username, password=password)
        # User exist in our database
        if team:
            # Is active
            if team.is_active:
                login(request, team)
                # return HttpResponseRedirect('/base/')
                return HttpResponse("YUHUUUUU")
            else:
                return HttpResponse("Your account is disabled")
        else:
            print "Invalid log details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid log details")
    # si la request no es un HTTP POST se mostre el loguin form.
    else:
        return render(request, 'Login.html', {})
