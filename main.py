import re, sys, requests


# board name, return (isHit, isFinished)
def shot(bn, pos):
    content = requests.post('https://student.people.co/api/challenge/battleship/{0}/boards/{1}/{2}'.format(token, bn, pos), allow_redirects=True).content
    isFinished = re.search('"is_finished": true', content) is not None
    isHit = re.search('"is_hit": true', content) is not None
    return isHit, isFinished

def reset(bn):
    return requests.delete('https://student.people.co/api/challenge/battleship/{0}/boards/{1}/'.format(token, bn), allow_redirects=True).content

def boardInfo(bn):
    return requests.get('https://student.people.co/api/challenge/battleship/{0}/boards/{1}/'.format(token, bn), allow_redirects=True).content

def isFinished(bn):
    content = requests.get('https://student.people.co/api/challenge/battleship/{0}/boards/{1}/'.format(token, bn), allow_redirects=True).content
    return re.search('"is_finished": true', content) is not None

def run(bn):
    print reset(bn)
    isending = False
    for l in letters:
        for n in numbers:
            result = shot(bn, '{0}{1}'.format(l, n)) 
            print l, n, result
            if result[1]:
                isending = True
                break
        if (isending):
            break

token = 'ea2985aa5625'
letters = [chr(x) for x in range(ord('A'), ord('J') + 1)]
numbers = range(1, 10 + 1)

# bns = ['test_board_1' , 'test_board_2' , 'test_board_3' , 'test_board_4' , 'test_board_5']
bns = ['test_board_2']
for bn in bns:
    run(bn)
    print boardInfo(bn)
