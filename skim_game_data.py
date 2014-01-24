from urllib.request import urlopen
import re
import base64
import argparse
# from bs4 import BeautifulSoup

def get_args():
    parser = argparse.ArgumentParser(description='Gather game data from robotgame.net')
    parser.add_argument('--output', '-o', default='', help='where to output the logs')
    parser.add_argument('--num_games', '-n', default=1, help='how many games to record')
    parser.add_argument('--decode', '-d', default=False, help='decode each record before saving')
    parser.add_argument('--decode_one', '-D', help='path to file to be decoded')
    parser.add_argument('--start_game', '-s', default=0, help='the match to start on')
    parser.add_argument('--user', '-u', help='not implemented')
    return parser.parse_args()


def find_recent_match(webpage):
    match = re.search('href=\"/match/[0-9]+\"', webpage)
    return int(match.group(0)[13:-1])

def main():
    
    parsed_args = get_args()
    
    url = ''
    count = 0
    match = parsed_args.start_game
    if match == 0:
        url = 'http://robotgame.net'
    else:
        url = 'http://robotgame.net/match/' + str(match)
        
    resp = urlopen(url)
    pg_bytes = resp.read()
    web_pg = pg_bytes.decode('utf8').replace('\n', '')
    latest_match = find_recent_match(web_pg)
    resp.close()
    
    # 300k is a little less than the amount of games the site stores
    if match == 0 or match > latest_match or match < latest_match - 300000:
        match = latest_match
    
    while count < parsed_args.num_games:
        url = 'http://robotgame.net/match/' + str(match)
        resp = urlopen(url)
        pg_bytes = resp.read()
        web_pg = pg_bytes.decode('utf8').replace('\n','')
        resp.close()
        
        if re.search('match not found', web_pg):
            print ('match DNE yet')
            time.sleep(2.0)
            continue
        
        # search for the section we want
        m = re.search('src=\"data:text/javascript;base64,[0-9a-zA-Z="]+>', web_pg)
        
        # fatal error
        if not m:
            print('error')
            return
            
        # trim the fat and write to file
        trimmed_m = m.group(0)[len('src=\"data:text/javascript;base64,'):len(m.group(0))-2]
        f = open('match'+str(match), 'w')
        f.write(trimmed_m)
        print ('Recorded match ' + str(match))
        match = match + 1
        count = count + 1
        
        
#     while True:
#         aResp = urllib2.urlopen("http://robotgame.net/match/" + str(match))
#         web_pg = aResp.read().replace('\n','')
# 
        
#         

        
    
#         decoded = base64.b64decode(trimmed_m)
#         print decoded
    
    # Should work but doesn't-- BS cuts off the src string, a lot of it
#     soup = BeautifulSoup(web_pg)
#     tag = soup.find('script', src=re.compile("data:text/javascript;base64"))
#     base64.b64decode(tag['src'][28:])
    

        

if __name__ == "__main__":
    main()
