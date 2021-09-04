"""
Mew's JP(E)G crawler.

Date started: 2018-02-11
Date ~finished: 2019-03-12
"""

# Libs
import urllib.parse
import urllib.request
import urllib.robotparser
import time
import os
import re
import http.client
from io import BytesIO
from bs4 import BeautifulSoup  # Needs separate download
from PIL import Image          # Needs separate download


def lookup(filepath, string):
    """
    Looks up the the given string, with any whitespace characters that are not spaces removed, as bytes in the given file.
    """
    string_as_bytes = string.replace("\r","").replace("\t","").replace("\n","").replace("\v","").encode()
    with open(filepath, "rb") as handle:
        for line in handle:
            if string_as_bytes == line.replace(b"\r",b"").replace(b"\t",b"").replace(b"\n",b"").replace(b"\v",b""):
                return True
    return False


def txtAtLinenum(filename, linenumber):
    """
    Returns the text at the given line number in the given text file, else None.
    Note: line number is 1-based.
    """
    with open(filename) as handle:  # This could cause slowing down in the main program, since open() is called over and over.
        for n, line in enumerate(handle, 1):
            if n == linenumber:
                return line.strip("\n")


def numAtLine(filename, linestring):
    """
    Returns the line number of the first occurrence of the given string as a line in the given text file, else None.
    Note: line number is 1-based.
    """
    with open(filename) as handle:
        for n, line in enumerate(handle, 1):
            if line.strip("\n") == linestring:
                return n


def txtChangeLine(filename, linenumber, new_line_value):  # Works only for small txts
    """
    Replaces the line at the given line number in the given text file by the given new string.
    Note: line number is 1-based.
    """
    with open(filename) as handle:
        lines = handle.readlines()

    lines[linenumber-1] = str(new_line_value) + "\n"

    with open(filename, "w+") as handle:
        for line in lines:
            handle.write(line)


def listPartInString(lst, string):
    """
    Checks whether any of the elements in the given list are a substring of the given string.
    """
    for stringpart in lst:
        if stringpart in string:
            return True
    return False


def removeListDuplicates(lst):
    """
    Returns the given list, but only with all occurrence of an element past its first removed. Identity-based.
    """
    newlist = []
    for item in lst:
        if item not in newlist:
            newlist.append(item)
    return newlist


def robotsAllowed(crawlername, link):
    """
    Checks whether the given link's domain allows web crawlers by means of the robots.txt convention.
    """
    base = link[:link.find("/", 8)]  # Find the part of the URL that terminates at the first slash past https://
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(base + "/robots.txt")  # Configure parser
    try:
        rp.read()  # Update parser
        return rp.can_fetch("*", link)
    except:
        return True


MANAGEMENT_STEM = "data"  # Data managing crawlers is stored in data.txt
management_filename = MANAGEMENT_STEM + ".txt"

MAX_ERROR_10060_TRIES = 10
URL_SLEEP_S = 1
IMG_SLEEP_S = 0.01

MIN_WIDTH_PX = 400
MIN_HEIGHT_PX = 400

# File management
with open(management_filename, mode="a+", encoding="utf-8") as handle:
    handle.write("")

crawler_name = MANAGEMENT_STEM
while crawler_name == MANAGEMENT_STEM:
    crawler_name = input("Crawler name: ").lower()

savepath = ""
mode = ""

savelinenum = numAtLine(management_filename, crawler_name)
if savelinenum is not None:
    savepath = txtAtLinenum(management_filename, savelinenum + 1)
    if not(os.path.exists(savepath)):
        print(f"A crawler with the same name existed at {savepath}, but that folder is gone.")
    elif not(os.path.exists(savepath + crawler_name + ".txt")):
        print(f"A crawler with the same name existed at {savepath}, but its log is gone.")
    else:
        print(f"A crawler with the same name already exists at {savepath}.\n")
        while mode != "O" and mode != "R":
            mode = input("Resume or overwrite (R/O)? ")
            if mode == "O":
                txtChangeLine(management_filename, savelinenum + 2, "1")
else:
    with open(management_filename, "a+") as data:
        data.write(crawler_name + "\n")
        data.write("\n")
        data.write("1\n")
    savelinenum = numAtLine(management_filename, crawler_name)

startline = int(txtAtLinenum(management_filename, savelinenum + 2))

if mode == "" or mode == "O":
    savepath = os.getcwd() + "\\" + crawler_name + "\\"
    satisfied = input(f"Crawler data and output will be stored at {savepath}. Is that okay? (Y/N) ").upper() == "Y"
    while not satisfied:
        savepath = input("Enter folder path to store crawler data and output at: ")
        if not savepath.endswith("\\"):
            savepath += "\\"
        satisfied = input(f"Crawler data and output will be stored at {savepath}. Is that okay? (Y/N) ").upper() == "Y"

    txtChangeLine(management_filename, savelinenum + 1, savepath)
    os.makedirs(savepath, exist_ok=True)

    with open(savepath + crawler_name + ".txt", "w+") as crawl:
        print("A fresh file, " + crawler_name + ".txt, was created there successfully.\n")
        crawl.write(input("URL to start crawling from (use http(s) & ending slash): ") + "\n")
elif mode == "R":
    print("Resuming at line %s." % startline)

iterations = int(input("Accesses to do: "))  # Maximum amount of pages to crawl this session
imgcount = 0

# Robots
obey = ""
while obey != "Y" and obey != "N":
    obey = input("Obey restrictions for web crawlers (Y/N)? ").upper()
INFRINGE_ON_DOMAINS = [""]          # Infringe upon this possible restriction if any of these domains is accessed.
INFRINGE_ON_PATH_PARTS = ["/out/"]  # Infringe upon this possible restriction if any of these path parts is in the URL.
##crawl = open(savepath + savefile + ".txt","a+") ### Only uncomment when using an always-open crawl file

# Main
for i in range(iterations):
    time.sleep(URL_SLEEP_S)
    
    # Initialize
    urlstart = txtAtLinenum(savepath + crawler_name + ".txt", startline + i)
    if not(urlstart):
        break
    try:
        print(f"\n-- Access #{i+1} (#{startline + i} total) --")
        print("URL: " + urlstart)
        url = urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(urlstart).geturl()        
        if urlstart != url:
            print("Redirects to: " + url)
        baseurl = url[:url.find("/", 8)]
        html = urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(url).read()   # Open actual url
        print("URL access successful.")
    except:
        print("URL access failed.")
        txtChangeLine(management_filename, savelinenum+2, startline+i+1)
        continue
    
    # Permissions
    if robotsAllowed("*", url):
        print("URL allows robots!")
    elif (obey == "N") or (baseurl in INFRINGE_ON_DOMAINS) or listPartInString(INFRINGE_ON_PATH_PARTS, url):
        print("Beware: URL is being infringed upon!")
    else:
        print("URL doesn't allow robots!")
        txtChangeLine(management_filename, savelinenum+2, startline+i+1)
        continue
    
    # Find and index links
    soup = BeautifulSoup(html, "html.parser")        # Nice HTML-ification
    atags = soup("a")                               # List of all <a>...</a>s
    print(f"Collected {len(atags)} <a> tags. Checking for relevant webpages among them ...")
    
    for num, tag in enumerate(atags):
        link = urllib.parse.urljoin(url, "".join(str(tag.get("href",baseurl)).split()))  # Get the properly formatted link out of the href
        if re.search('''\.je?pg''', link.lower()):
            print("Link %s is an image." % (int(num) + 1))
        elif lookup(savepath + crawler_name + ".txt", link):
            print("Link %s was or is already in the queue." % (int(num) + 1))
        else:
            print("Link %s will be added to the queue." % (int(num) + 1))
            try:
                with open(savepath + crawler_name + ".txt", "a+") as crawl:  ### This might be slower than using an always-open crawl file
                    crawl.write(link + "\n")
                ##crawl.write(link + "\n") ### Only uncomment when using an always-open crawl file
            except:
                print("\tWow, it had strange symbols! Exotic times, we live in. Throwing it out.")

    # Find and download images
    regex = '''(?<=["'])[^"']*\.jpe?g(?=[^"']*["'])'''  # Regex to find image links (find ".jp(eg)", make sure it's preceded and followed by any amount of non-"' chars, include everything after the preceding "'-char
    try:
        imglist = re.findall(regex, str(soup))  # Make list of image links in souped HTML
    except:
        print("\nEw, horrible HTML!")
        txtChangeLine(management_filename, savelinenum+2, startline+i+1)
        continue

    for n, imglink in enumerate(imglist):
        imglist[n] = urllib.parse.urljoin(url, "".join(imglink.split()))
    imglist = removeListDuplicates(imglist)
    print("\nUnique images found: %s" % len(imglist))

    for n,img in enumerate(imglist):
        time.sleep(IMG_SLEEP_S)
        print("Fetching image %s." % (n+1))#
        try:
            print("\tSize check ...")
            imgsize = Image.open(BytesIO(urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(img).read())).size  # Open the image-URL as HTML, turn that into a byte-like file, read that file's dimensions
        except:
            print("\tSize check failed. Probably bad HTML.")
            continue

        if imgsize[0] > MIN_WIDTH_PX and imgsize[1] > MIN_HEIGHT_PX:  # Exclude thumbnail sizes or other low-res images
            time.sleep(IMG_SLEEP_S)
            print("\tIncoming resolution: " + str(imgsize[0]) + "x" + str(imgsize[1]))
            n_tries = 0
            while True:  # Pushes through Error 10060
                n_tries += 1
                try:
                    with urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open(img) as response, open(savepath + time.strftime("%Y-%m-%d") + "-" + time.strftime("%H%M%S") + "_" + str(imgcount) + ".jpg", "wb") as output:
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
                    if n_tries < MAX_ERROR_10060_TRIES:
                        continue
                    else:
                        print("\tGave up on image. Probably some kind of timeout.")
                        break
                else:
                    imgcount += 1
                    print("\tSuccesfully got image from " + img + ".")
                    break
        else:
            print(f"\tDid not download image. Too small for our liking ({imgsize[0]} x {imgsize[1]}).")
    txtChangeLine(management_filename, savelinenum+2, startline+i+1)

print("Accesses complete: %s images were fetched successfully." % imgcount)
print("Crawler shutting off.")
##crawl.close()  ### Only uncomment when using an always-open crawl file