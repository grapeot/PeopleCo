import urllib2
import httplib 
import requests


token = 'ea2985aa5625'

# board name
def Shot(bn, pos):
    req = requests.put('https://student.people.co/api/challenge/battleship/{0}/boards/{1}/{2}'.format(token, bn, pos), allow_redirects=True).content

def Reset(bn):
    return requests.delete('https://student.people.co/api/challenge/battleship/{0}/boards/{1}/'.format(token, bn), allow_redirects=True).content

def BoardInfo(bn):
    return requests.get('https://student.people.co/api/challenge/battleship/{0}/boards/{1}/'.format(token, bn), allow_redirects=True).content

bn = 'test_board_1'
print Shot(bn, 'A2')
print BoardInfo(bn)
print Reset(bn)
print BoardInfo(bn)
