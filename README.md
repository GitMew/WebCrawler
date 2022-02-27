# Project WebCrawler (2018)
Repo backing up my first ever big Python project, started in 2018.

## Backstory
Back in 2017, in 11th grade, I spent winter break (the last week of February) taking Dr. Charles R. Severance's *Python4Everybody* course on Coursera. In it, he teaches some basics of web scraping, and IIRC, he provides a stateless, bare-bones example of a program that collects and crawls links.

If the creation dates of the scripts and all the crawled files are to be trusted, I started this project around mid-February 2018. It crawls webpages, scrapes links from HTML, and downloads any JP(E)G images it comes across. It remembers both its entire crawling history, as well as where it stopped if terminated during the crawl. It can also manage more than one crawl session's data.

Some intriguing historical notes:
* I used `Notepad++` and `Windows cmd` to program the entire thing. Since starting uni, I've ditched `Notepad++` in favour of PyCharm and VS Code.
* I had no idea about good coding practices. My only background at that point had been programming in TI-BASIC on my TI-84+ for three years.
* *Python4Everybody* still taught Python 2 back then. It has since been updated to Python 3, but since I'm quite stubborn, I followed the Python-2 course using a Python-3 installation, modifying example scripts along the way.
* A lot of the file stuff was done using the `os` library. Since my favourite Python library is `pathlib`, I can't fathom how I got any file manipulation working (probably StackOverflow `:/`).
* Web stuff was done using `urllib`'s API. I definitely treated that as a magical black box, and wrote my code by example from other sources.
* I only discovered Git and GitHub at the end of 2019, hence I never tracked this project.

## Usage
The main program is only one script: `ImageCrawler.py`. It has several prompts and printouts that guide the user along. The diagnostic tools are several scripts that should be self-explanatory.
