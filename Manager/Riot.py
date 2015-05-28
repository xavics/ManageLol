import json
import smtplib
import requests
import datetime

# For Program
with open('Manager/riotdatabase.json') as data_file:
    data = json.load(data_file)

# For debugging
# with open('riotdatabase.json') as data_file:
#     data = json.load(data_file)

# For Program
# with open('Manager/top_25.json') as data_file:
#     data_top = json.load(data_file)


def make_db_inserts():
    f = open('db_in','w+')
    for x in range(24):
        if x != 0:
            st_x = str(x)
            data = str(datetime.datetime.now())
            team_name = "t"+st_x
            values = "'"+st_x+"','xxx','"+data+"','"+team_name+"',0,'mailo','','False'"
            f.write("insert into Manager_team values("+values+");\n")
            x_p = (x-1)*5
            for y in range(6):
                if y != 0:
                    p_id = str(x_p+y)
                    player_n = "p"+p_id
                    mail_p = player_n+"@mail.com"
                    values_p = "'"+p_id+"','"+player_n+"','"+mail_p+"','False','SU','"+st_x+"'"
                    f.write("insert into Manager_player values("+values_p+");\n")


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
    players_list = "Team players:\n"
    for player in data['players']:
        players_list = players_list+"   - "+player.name+" ( "+player.role+" )\n"
    msg = "\r\n".join([
        "From: manager.lol.models@gmail.com",
        "To: "+toadd,
        "Subject: Welcome to Lol competition",
        "",
        "Hi team "+data['team']+"!\n"+players_list+"Your are ready to participate in the League of Legends competition"+
        "\nWe wish you will have a cool time"
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

if __name__ == '__main__':
    make_db_inserts()