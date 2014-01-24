import urllib
import urllib2
import re
import base64
# from bs4 import BeautifulSoup


def main():
    match = 2180000
    while True:
        aResp = urllib2.urlopen("http://robotgame.net/match/" + str(match))
        web_pg = aResp.read().replace('\n','')

        if re.search('match not found', web_pg):
            print 'match DNE yet'
            time.sleep(2.0)
            continue
        
        m = re.search('src=\"data:text/javascript;base64,[0-9a-zA-Z="]+>', web_pg)
        trimmed_m = m.group(0)[len('src=\"data:text/javascript;base64,'):len(m.group(0))-2]
        f = open('match'+str(match), 'w')
        f.write(trimmed_m)
        match = match + 1
        
    
#         decoded = base64.b64decode(trimmed_m)
#         print decoded
    
    # Should work but doesn't-- BS cuts off the src string, a lot of it
#     soup = BeautifulSoup(web_pg)
#     tag = soup.find('script', src=re.compile("data:text/javascript;base64"))
#     base64.b64decode(tag['src'][28:])
    

        

if __name__ == "__main__":
    main()
