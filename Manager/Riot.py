import json
import smtplib
import requests

# For Program
with open('Manager/riotdatabase.json') as data_file:
    data = json.load(data_file)


# For Program
with open('Manager/top_25.json') as data_file:
    data_top = json.load(data_file)


def is_riot_user(name, email):
    for player in data['players']:
        if player['name'] == name and player['email'] == email:
            return True
    return False

def is_top_team(name):
    for team in data_top['top']:
        if team['name'] == name:
            return "Top team inscribed"

def send_confimation_email(addres, data):
    fromadd = 'manager.lol.models@gmail.com'
    toadd = addres
    if data['type'] == "confirmation":
        players_list = "Team players:\n"
        for player in data['players']:
            players_list = players_list+"   - "+player.name+" ( "+player.role+" )\n"
        subj = "Welcome to Lol competition"
        text = "Hi team "+data['team']+"!\n"+players_list+"Your are ready to participate in the League of Legends competition"
    if data['type'] == "xml":
        subj = "Ronda "+str(data['id'])
        text = data['text']
    msg = "\r\n".join([
        "From: manager.lol.models@gmail.com",
        "To: "+toadd,
        "Subject:"+subj,
        "",
        "\n"+text
    ])
    username = 'manager.lol.models@gmail.com'
    password = 'managerLoL.models'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromadd, toadd, msg)
    server.quit()

def get_region_stats(region):
    data=requests.get(url="http://status.leagueoflegends.com/shards/"+region)
    return data.json()

def get_regions_names():
    data=requests.get(url="http://status.leagueoflegends.com/shards")
    return data.json()

def get_servers_stats():
    regions_info = get_regions_names()
    regions = {}
    for region in regions_info:
        regions[region['slug']]=region['name']
    servers = {}
    for slug in regions.keys():
        stats = get_region_stats(slug)
        servers[regions[slug]]=stats['services'][0]['status']
    return servers

def get_ip():
    return requests.get(url="http://localhost:3333").json()['generated-ip']