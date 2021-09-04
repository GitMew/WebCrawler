#Mew's image crawler
#Libs
import urllib.parse
import urllib.request
import urllib.robotparser
import time
import os
import re
import random
import http.client
from io import BytesIO
from bs4 import BeautifulSoup #Needs separate download
from PIL import Image         #Needs separate download
def lookup(filename,str):
    bytes = str.replace("\r","").replace("\t","").replace("\n","").replace("\v","").encode()
    with open(filename, "rb") as handle:
        for line in handle:
            if bytes == line.replace(b"\r",b"").replace(b"\t",b"").replace(b"\n",b"").replace(b"\v",b""):
                return True
    return False
def txtAtLinenum(filename,linenumber):
    with open(filename) as handle:                   #This could cause slowing down each time it opens
        for n, line in enumerate(handle, 1):
            if n == linenumber:
                return line.strip("\n")
def numAtLine(filename,linestring):
    with open(filename) as handle:
        for n, line in enumerate(handle, 1):
            if line.strip("\n") == linestring:
                return n
def txtChangeLine(filename,linenumber,newLinevalue): #Works only for small txts
    with open(filename) as handle:
        lines = handle.readlines()
    lines[linenumber-1] = str(newLinevalue) + "\n"
    with open(filename, "w+") as handle:
        for line in lines:
            handle.write(line)
def listPartInString(list,string):
    for stringpart in list:
        if stringpart in string:
            return True
    return False
def removeListDuplicates(list):
    newlist = []
    for item in list:
        if not(item in newlist):
            newlist.append(item)
    return newlist
def robotsAllowed(crawlername,link):
    base = link[:link.find("/",8)]
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(base + "/robots.txt")
    try:
        rp.read()
        return rp.can_fetch("*",link)
    except:
        return True
        
#Vars
with open("tempSIC.txt","w+") as crawl:
    crawl.write(input("URL to start crawling from: ") + "\n")
iterations = int(input("Accesses to do: "))
obey = ""
while obey != "Y" and obey != "N":
    obey = input("Obey restrictions for web crawlers (Y/N)? ")                                                       #Maximum amount of pages to crawl this session
imgcount = 0
infringebases = [""]
infringeparts = ["/out/"]
##crawl = open(savepath + savefile + ".txt","a+") ### Only uncomment when using an always-open crawl file

#Main
for i in range(iterations):
    time.sleep(1)
    
    #Initialize
    urlstart = txtAtLinenum("tempSIC.txt",1+i)
    if not(urlstart):
        break
    try:
        print("\n-- Access #%s --" % (i+1))
        print("URL: " + urlstart)
        url = urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(urlstart).geturl()        
        if urlstart != url:
            print("Redirects to: " + url)
        baseurl = url[:url.find("/",8)]
        html = urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(url).read()   #Open actual url
        print("URL access successful.")
    except:
        print("URL access failed.")
        continue
    
    #Permissions
    if robotsAllowed("*",url):
        print("URL allows robots!")
    elif (obey == "N") or (baseurl in infringebases) or listPartInString(infringeparts,url):
        print("Beware: URL is being infringed upon!")
    else:
        print("URL doesn't allow robots!")
        continue
    
    #Find and index links
    soup = BeautifulSoup(html,"html.parser")        #Nice HTML-ification
    atags = soup("a")                               #List of all <a>...</a>s
    
    print("Reached <a> tag check.")#
    
    for num, tag in enumerate(atags):
        print("Checking if link %s is viable ..." % (int(num)+1))
        link = urllib.parse.urljoin(url,"".join(str(tag.get("href",baseurl)).split()))  #Get the properly formatted link out of the href
        if not(re.search('''\.je?pg''',link.lower())) and not(lookup("tempSIC.txt",link)):
            
            print("Entered check ...")#
            
            try:
                print("Writing link ...")#
                with open("tempSIC.txt","a+") as crawl: ### This might be slower than using an always-open crawl file
                    crawl.write(link + "\n")
                ##crawl.write(link + "\n") ### Only uncomment when using an always-open crawl file
                print("Link written.")#
            except:
                print("Wow, found a link with strange symbols! Exotic times, we live in.")
        
        print("Passed check.")#
        
    #Find and download images
    regex = '''(?<=["'])[^"']*\.jpe?g(?=[^"']*["'])'''                                  #Regex to find image links (find ".jp(eg)", make sure it's preceded and followed by any amount of non-"' chars, include everything after the preceding "'-char
    try:
        imglist = re.findall(regex,str(soup))                                           #Make list of image links in souped HTML
    except:
        print("Ew, horrible HTML!")
        continue
    for n,imglink in enumerate(imglist):
        imglist[n] = urllib.parse.urljoin(url,"".join(imglink.split()))
    imglist = removeListDuplicates(imglist)
    print("Images found: %s" % len(imglist))
    for n,img in enumerate(imglist):
        time.sleep(0.01)        
        print("Fetching image %s ..." % (n+1))#
        
        print(img)
        
        try:
            print("Size check ...")
            imgsize = Image.open(BytesIO(urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(img).read())).size          #Open the image-URL as HTML, turn that into a byte-like file, read that file's dimensions
            print("Size check complete.")
        except:
            print("Size check failed. Probably bad HTML.")
            continue
        if imgsize[0] > 500 and imgsize[1] > 500:                                       #Exclude thumbnail sizes or other low-res images
            time.sleep(0.01)
            print("Incoming resolution: " + str(imgsize[0]) + "x" + str(imgsize[1]))
            while True: #Pushes through Error 10060
                try:
                    with urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(img) as response, open(time.strftime("%Y-%m-%d") + "-" + time.strftime("%H%M%S") + "_" + str(imgcount) + ".jpg", "wb") as output:
                        data = b""
                        while True:
                            try:
                                datapart = response.read()
                            except http.client.IncompleteRead as ICread:
                                data = data + ICread.partial
                            else:
                                data = data + datapart
                                break
                        #data = response.read() -> This one failed because of an IncompleteRead-error. If it doesn't ever happen again, and all data is intact having gone through the loop, then the loop was the solution.
                        output.write(data)
                except:
                    continue
                else:
                    imgcount += 1
                    print("Succesfully got image from " + img + ".")
                    break

print("Accesses complete: %s images were successfully fetched." % imgcount)
print("Crawler shutting off.")
##crawl.close() ### Only uncomment when using an always-open crawl file
os.remove("tempSIC.txt")