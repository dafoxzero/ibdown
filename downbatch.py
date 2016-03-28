# imports
from bs4 import BeautifulSoup
import requests
import pickle
import urlparse
import os
import re
import sys
import time


def Bytes2MBytes(bytes):
    return (float(bytes) / 1024) / 1024


def Bytes2KBytes(bytes):
    return float(bytes) / 1024


def _get_links(text, filetypes):
    soup = BeautifulSoup(text)
    links = []
    for ftype in filetypes:
        re_rule = "\.%s$" % ftype
        for link in soup.find_all(href=re.compile(re_rule)):
            links.append(link.get('href'))
    return links


def download_files(url, filetypes, dirname=None):

    response = requests.get(url)
    if response.ok:
        links = _get_links(response.text, filetypes)
        if links:
            # for index, link in enumerate(links):
            #         links[index]
            for link in links:
                url = urlparse.urlparse(link)
                if not url[0]:
                    # http default, maybe this can be passed by arguments
                    url = urlparse.urlparse(url.geturl(), "http")

                default = "Default"
                if dirname is None:
                    filename = os.path.join(
                        default,
                        os.path.basename(
                            url.path))

                else:
                    filename = os.path.join(
                        dirname,
                        os.path.basename(
                            url.path))

                # check each file, because the directory can be delete
                # while run the script
                if not os.path.exists(
                        os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                    print "Directory %s created" + os.path.dirname(filename)

                if not os.path.isfile(filename):
                    with open(filename, "wb+") as f:
                        start = time.time()
                        r = requests.get(url.geturl(), stream=True)
                        total_length = r.headers.get('content-length')
                        dl = 0
                        print "Downloading %s from %s" % (filename, url.geturl())

                        # no content length header
                        if total_length is None:
                            f.write(r.content)
                        else:
                            # total = Bytes2KBytes(
                            #     dl) / (time.time() - start)

                            for chunk in r.iter_content(1024):
                                # time.sleep(1)
                                dl += len(chunk)
                                f.write(chunk)
                                done = 50 * dl / int(total_length)

                                timerate = Bytes2KBytes(
                                    dl) / (time.time() - start)

                                KB_s = Bytes2KBytes(dl) / (time.time() - start)
                                sys.stdout.write("\r[ %s%s ] (%.2f/%.2fMb) %.2fKB/s " %
                                                 ('=' * (done - 2) + ">", ' ' * (50 - done), Bytes2MBytes(dl),
                                                  Bytes2MBytes(total_length), timerate))

                            # when exit the program and one file is downloading this save corrupted
                            # os.remove in Exception for delete files with
                            # atexit() handlers
                            # temporal directory at move when file is complete

                        # return (time.clock() - start)

                    sys.stdout.write(
                        "\r[ %s ] Complete 0_o. \n" %
                        (":" * 50))
                else:
                    print "File: %s already exists, skip" % filename
        else:
            print "Files with the extension given not found"
            return None
    else:
        print "Bad Response : %s" % response.status_code
        return None


def help():
    print "Usage: python <script> <url> <extension> <directory>"
    print "       python <script>  inconfig"
    print ""


if len(sys.argv) is 4:
    ext = sys.argv[2].split(",")
    download_files(str(sys.argv[1]), ext, dirname=sys.argv[3])
elif len(sys.argv) is 3:
    ext = sys.argv[2].split(",")
    download_files(str(sys.argv[1]), ext)
elif len(sys.argv) is 2:
    if(sys.argv[1]) == "inconfig" and os.path.isfile("config.py"):
        from config import urls, extensions
        if urls and extensions:
            for url in urls:
                download_files(url, extensions)
        else:
            "urls or extensions aren't configured correctly."
            help()
    else:
        help()

else:
    help()
