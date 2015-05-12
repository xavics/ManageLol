import json
import smtplib

with open('Manager/riotdatabase.json') as data_file:
    data = json.load(data_file)

def is_riot_user(name, email):
    for player in data['players']:
        if player['name'] == name and player['email'] == email:
            return True
    return False

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


if __name__ == '__main__':
    send_confimation_email()
