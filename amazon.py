from selectorlib import Extractor
import json 
import requests 
import sys


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('amazon.yml')

try: #catching arguements from the console
    argTrue = False
    
    printM = str(sys.argv[1])
    urlL = str(sys.argv[2])
    if (printM != "-p" and printM != "-w"): #raise exception if outside of param
        raise Exception
    
    argTrue = True
    
except:
    print("Looks like your arguements were bad. ")
    end = int(input("1.Yes\n2.No\nWould you like to continue without commandline arguements? "))
    if (end == 2):
        print("Try again")
        sys.exit()

def scraper(url):  

    headers = { #adding headers so websites allow me in
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)

if (not argTrue): #if not using command line args
    with open("urls.txt",'r') as urllist, open('output.jsonl','w') as outfile: #reads url from url file and seting up write file
        for url in urllist.read().splitlines():
            data = scraper(url) 
            if data:
                json.dump(data,outfile)
                outfile.write("\n\n")
else: 
    data = scraper(urlL)
    with open('output.jsonl','w') as outfile: #setting up write file
        if data:
            json.dump(data,outfile)
            if (printM == "-p"):
                print(data)
            elif (printM == "-w"):
                outfile.write("\n\n")
            
