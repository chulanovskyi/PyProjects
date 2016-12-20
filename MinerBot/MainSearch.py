import requests
import time
from configparser import ConfigParser


def read_cfg():
    config = ConfigParser()
    config.read_file(open('config.cfg'))
    return dict(config.items('YourData'))


def write_cfg(data):
    config = ConfigParser()
    config['YourData'] = data
    config.write(open('config.cfg', 'w'))


def scan_free_games(pageType):
    set_headers = {
        "Host": "gameminer.net",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": user_agent,
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,cs;q=0.2,it;q=0.2,uk;q=0.2",
    }
    set_cookies = {
        "_xsrf": _xsrf,
        "token": token
    }
    session.headers.update(set_headers)
    session.cookies.update(set_cookies)
    
    print("Scanning {0} pages".format(pageType))
    free_games_dict = {}  # dict format is "Game number on page + page number":"GAME_CODE"

    site = session.get('http://gameminer.net/api/giveaways/{0}?page=1&count=20'.format(pageType)).json()
    last_page = site.get('last_page')

    for x in range(1, last_page+1):
        time.sleep(0.1)  # Without this pause we get - JSONDecodeError 0_o
        page = session.get('http://gameminer.net/api/giveaways/{0}?page={1}&count=20'.format(pageType, x)).json()
        games_on_page = len(page["giveaways"])
        counter = 1
        for i in range(games_on_page):
            take_game = page["giveaways"][i]
            name = take_game.get('game').get('name')
            price = take_game.get('price')
            entered = take_game.get('entered')
            code = take_game.get('code')
            if code not in exclude_codes and not entered and price == 0:
                free_games_dict["game "+str(counter)+" on page "+str(x)] = [code, name]
                counter += 1
            if code in exclude_codes:
                exclude.append(code)
    print("{0} free giveaways: ".format(pageType)+str(len(free_games_dict)))
    return free_games_dict


def enter_giveaway(urlA):
    set_headers = {
        "Host": "gameminer.net",
        "User-Agent": user_agent,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,cs;q=0.2,it;q=0.2,uk;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referrer": "http://gameminer.net/",
        "Content-Length": "48",
        "Connection": "keep-alive",
        "Origin": 'http://gameminer.net'
    }    
    set_cookies = {
        "_xsrf": _xsrf,
        "token": token
    }
    set_data = {
        "_xsrf": _xsrf,
        "json": "true"
    }
    response_check = session.post(urlA, data=set_data, headers=set_headers, cookies=set_cookies)
    time.sleep(0.1)
    return response_check


def scan_coal():
    coal_games = scan_free_games("coal")
    coal_codes = list(coal_games.values()) #[0] = game_code, [1] = game_name
    return coal_codes


def scan_sandbox():
    sandbox_games = scan_free_games("sandbox")
    sandbox_codes = list(sandbox_games.values()) 
    return sandbox_codes


def scan_gold():
    gold_games = scan_free_games("golden")
    gold_codes = list(gold_games.values())
    return gold_codes


def scan_all():
    all_codes = []
    all_codes.extend(scan_coal())
    all_codes.extend(scan_sandbox())
    all_codes.extend(scan_gold())
    return all_codes 


def enter_all(all_game_codes):
    entered = 0
    enter_link = "http://gameminer.net/giveaway/enter/"
    print("***Entering***")
    for game in all_game_codes:
        enter = enter_giveaway(enter_link+game[0])
        if 'enter-steam' in str(enter.text):
            print('Re-login on gameminer.net (bad cfg file)')
            return 'Re-login on gameminer.net (bad cfg file)'
        elif 'error' in str(enter.text):
            exclude.append(game[0])
            print("Conditions\DLC: {code} {name}".format(code=game[0], name=game[1]))
        elif '"status": "ok"' in str(enter.text):
            print('Entered: {code} {name}'.format(code=game[0], name=game[1]))
            entered += 1
    print("New entries: {0}".format(entered))
    my_data['excludecodes'] = exclude
    write_cfg(my_data)
    print('___Finish___')
    return entered


session = requests.Session()

my_data = read_cfg()

user_agent = my_data['useragent']
_xsrf = my_data['_xsrf'] 
token = my_data['token']
exclude_codes = my_data['excludecodes']
exclude = []

if __name__=='__main__':
    #enter_all(scan_coal())
    pass
    #DEBUG#print(str(enter_giveaway("http://gameminer.net/giveaway/enter/91c22a60671d8958d1a58114e8546025").text))
