import re, sys, requests

token = 'ea2985aa5625'
letters = [chr(x) for x in range(ord('A'), ord('J') + 1)]
numbers = range(1, 10 + 1)

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
    board = [['u' for x in range(10)] for y in range(10)]
    isending = False
    isBestAvailable = False
    for y in range(10):
        for x in range(10):
            if isBestAvailable:
                l = letters[besty]
                n = numbers[bestx]
                isBestAvailable = False
            else:
                l = letters[y]
                n = numbers[x]
            result = shot(bn, '{0}{1}'.format(l, n)) 
            print l, n, result
            if result[0]:
                # hit
                board[y][x] = 'h'
# begin a series of reasoning
# generate a list of possible ship configurations, which are just tuples of underlying positions (y, x)
                tmplist = []
# horizontal ones
                tmplist.extend([(y, xx) for xx in range(x - 1, x + 1)])
                tmplist.extend([(y, xx) for xx in range(x - 2, x + 2)])
                tmplist.extend([(y, xx) for xx in range(x - 3, x + 3)])
                tmplist.extend([(y, xx) for xx in range(x - 4, x + 4)])
# vertical ones
                tmplist.extend([(yy, x) for yy in range(y - 1, y + 1)])
                tmplist.extend([(yy, x) for yy in range(y - 2, y + 2)])
                tmplist.extend([(yy, x) for yy in range(y - 3, y + 3)])
                tmplist.extend([(yy, x) for yy in range(y - 4, y + 4)])
# remove impossible ones
                for tmp in tmplist:
                    if (tmp[0] < 0 or tmp[0] >= 10 or tmp[1] < 0 or tmp[1] >= 10):
                        tmplist.remove(tmp)
# get a histogram
                print 'tmplist = ', tmplist
                hist = [0 for i in range(100)]
                for tmp in tmplist:
                    hist[tmp[0] * 10 + tmp[1]] = hist[tmp[0] * 10 + tmp[1]] + 1
                print 'hist = ', hist
                # shoot on the most likely position in the histogram
                maxi = 0
                for i in range(100):
                    if (hist[i] > hist[maxi]):
                        maxi = i
                bestx = maxi % 10
                besty = (maxi - bestx) / 10
                isBestAvailable = True;
            else:
                # not hit (empty)
                board[y][x] = 'e'

            # guard of wasting time if the game is already finished
            if result[1]:
                isending = True
                break
        if (isending):
            break


# bns = ['test_board_1' , 'test_board_2' , 'test_board_3' , 'test_board_4' , 'test_board_5']
bns = ['test_board_2']
for bn in bns:
    run(bn)
    print boardInfo(bn)
