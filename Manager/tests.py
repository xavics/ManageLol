from django.test import TestCase
from Manager.Riot import is_riot_user, send_confimation_email


# Create your tests here.

class Player:
    name="Hola"
    role="Nidea"

    def __init__(self, name, role):
        self.name = name
        self.role = role


class RiotTest(TestCase):
    def test_check_riot_user(self):
        print ("Passing Test Check Riot User")
        name = "Tonita"
        email = "Tonita@hotmail.com"
        self.assertTrue(is_riot_user(name, email))

    def test_send_confirmaton_email(self):
        print ("Testing send confirmation email")
        a = Player("Hola", "Support")
        b = Player("Adeu", "Jungle")
        c = Player("SemiAdeu", "Attack Damage Carry")
        d = Player("SemiHola", "Middle")
        e = Player("HolaAdeu", "Solo")

        data = {'players': [a, b, c, d, e], 'team': u'Dignitas'}
        send_confimation_email("PUT YOUR EMAIL HERE", data)

