import os
import re
import sys
import time
import pycurl
import hashlib
import urlparse
import StringIO
import subprocess
from math import floor
from urllib import *

class HTTP():

    @staticmethod
    def getPage(**kwargs):

        url         = kwargs.get("url")
        method      = kwargs.get("method", "GET")
        parameter   = kwargs.get("parameter", None)
        postdata    = kwargs.get("postdata", None)
        ua          = kwargs.get("ua", "Mozilla/5.0 (Windows NT 5.1; rv:10.0.2; SinaSec) Gecko/20100101 Firefox/10.0.2")
        cookie      = kwargs.get("cookie", None)
        referer     = kwargs.get("referer", None)
        timeout     = kwargs.get("timeout", 300)
        fl          = kwargs.get("followlocation", 1)
        totaltime   = kwargs.get("totaltime", 0)

        if parameter is not None:
            url = "%s?%s" % (url, parameter)

        url = url.encode("ascii")
        print url
        rContent = ""
        rHeaders = ""
        headers = []

        responseContent = StringIO.StringIO()
        responseHeaders = StringIO.StringIO()

        headers.append("User-Agent: %s" % ua)
        if referer is not None:
            headers.append("Referer: %s" % referer)
        if cookie is not None:
            headers.append("Cookie: %s" % cookie)

        try:
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, url)
            if method == "POST":
                curl.setopt(pycurl.POST, True)
                curl.setopt(pycurl.POSTFIELDS, postdata)
            curl.setopt(pycurl.HTTPHEADER, headers)
            curl.setopt(pycurl.HEADERFUNCTION, responseHeaders.write)
            curl.setopt(pycurl.WRITEFUNCTION, responseContent.write)
            curl.setopt(pycurl.TIMEOUT, timeout)
            curl.setopt(pycurl.MAXREDIRS, 5)
            curl.setopt(pycurl.NOSIGNAL, 1)
            curl.setopt(pycurl.SSL_VERIFYHOST,0)
            curl.setopt(pycurl.SSL_VERIFYPEER,0)
            curl.perform()
            rContent = responseContent.getvalue()
            rHeaders = responseHeaders.getvalue()
            rTotaltime = curl.getinfo(pycurl.TOTAL_TIME)
        except pycurl.error, e:
            if e.args[1] == "Recv failure: Connection was reset":
                if totaltime == 1:
                    return "", None, 0
                else:
                    return "", None
            if totaltime == 1:
                return e, None, 0
            else:
                return e, None
        if totaltime == 1:
            return rContent, rHeaders, rTotaltime
        else:
            return rContent, rHeaders


def getGoogle(keyword, page):
    googleMobile = "http://203.116.165.138//search?hl=zh-CN&sky=ee&q=%s&num=100&start=%s" % (keyword, page)
    googleResponse, googleHeaders = HTTP.getPage(url=googleMobile, referer="http://www.sina.com/")
    if not isinstance(page, pycurl.error):
        googleUrls = re.findall('<h3 class=\"r\"><a href=\"(.*?)\"', googleResponse)
        if len(googleUrls) != 0:
            return googleUrls
        else:
            return None
    else:
        return None

def searchGoogle(keyword, page):
    flashUrls = []
    flashHashs = []
    for i in range(int(page)):
        time.sleep(5)
        start = i * 100
        urls = getGoogle(quote(keyword), start)
        if urls != None:
            for url in urls:
                _url = unquote(url)
                __url = urlparse.urlparse(_url)
                flashUrl = "%s://%s%s" % (__url[0],__url[1],__url[2])
                flashHash = hashlib.md5(flashUrl).hexdigest()
                if flashHash not in flashHashs:
                    flashHashs.append(flashHash)
                    flashUrls.append(flashUrl.encode("ascii"))
        else:
            break
    return flashUrls


def xargs():
        print "xargs: %s [mode] [option]" % sys.argv[0]
        print " mode:"
        print "  -s    search"
        print "  -t    test"
        print "  -p    pentest"
        print " option:"
        print "  -u    url"
        print "  -c    cmd with pentest"
        print "  -k    keyword with search"
        print "  -page page with search"
        print "  -h    help"



if __name__ == "__main__":

    if len(sys.argv) <= 1:
        xargs()
        sys.exit(1)

    count = 0
    mode = ""
    url = ""
    cmd = ""
    keyword = ""
    page = ""

    outfile=open('google_out','a')

    for arg in sys.argv:
        if arg == "-h":
            xargs()
            sys.exit(1)
        elif arg == "-s":
            mode = arg
        elif arg == "-k":
            keyword = sys.argv[count+1]
        elif arg == "-page":
            page = sys.argv[count+1]
        count += 1

    if mode == "-s":
        if keyword == "" or page == "":
            xargs()
            sys.exit(1)
        else:
            flashUrls = []
            flashUrls = searchGoogle(keyword, page)
            if len(flashUrls) != 0:
                for flashUrl in flashUrls:
                    outfile.write(flashUrl+"\n")


