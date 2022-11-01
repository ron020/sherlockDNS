#!/usr/bin/python3
import requests
import argparse
import socket
import time
import sys
from bs4 import BeautifulSoup


#Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d","--domain", help="Domains to find subdomains for")
parser.add_argument("-vh","--vhost", help="Find VHOST", dest="vhost")
parser.add_argument("-dL","--list", help="file containing list of domains for subdomain discovery")
parser.add_argument("-w", "--wordlist", help="file containing list of subdomains")
parser.add_argument("-s", "--silent", action="store_true", help="Silent mode", dest="silent")
parser.add_argument("-o", "--output", help="Output file to write results", dest="output")
parser.add_argument("-sc", "--status", help="Filter results VHOST Status Code", type=int, default=0, dest="status")
parser.add_argument("-vf", "--verbose", help="VHOST STATUS_CODE: Verbose mode", action="store_true", dest="verbose")
parser.add_argument("-sf", "--size", help="VHOST SIZE Filter", type=int, default=0, dest="size")
parser.add_argument("-lf", "--linefilter", help="VHOST LINES Filter", type=int, default=0, dest="linefilter")
parser.add_argument("-wf", "--words", help="VHOST WORDS Filter", type=int, default=0, dest="words")

args = parser.parse_args()
domain_str = args.domain
wordlist_L = args.list
wordlist_W = args.wordlist
output_F = args.output
st_cd = args.status
vhost_V = args.vhost
verbose = args.verbose
size = args.size
lineS = args.linefilter
words = args.words

#Banner
def banner():
        printx ("   _____ __              __           __   ____  _   _______ ")
        printx ("  / ___// /_  ___  _____/ /___  _____/ /__/ __ \/ | / / ___/ ")
        printx ("  \__ \/ __ \/ _ \/ ___/ / __ \/ ___/ //_/ / / /  |/ /\__ \  ")
        printx (" ___/ / / / /  __/ /  / / /_/ / /__/ ,< / /_/ / /|  /___/ /  ")
        printx ("/____/_/ /_/\___/_/  /_/\____/\___/_/|_/_____/_/ |_//____/   ")
        printx ("                                             version 1.0     ")
        printx ("Developed by ron020")
        printx ("Github: https://github.com/ron020")
        printx ("usage: sherlockDNS.py [-h HELP] [-d DOMAIN] [-dL LIST] [-vh VHOST]")
        printx ("                     [-w WORDLIST] [-s SILENT] [-o OUTPUT]")
        printx (" ")

#Gethostbyname
def test_sub(host):
        ok = False
        try:
                ok = socket.gethostbyname(host)
        except Exception as ex:
                ok = False

        if ok:
                return True

        return ok


#"-d, --domain; Domains to find subdomains for"
def run_sub():
        letsgo = []
        with open(wordlist_W, "r") as file:
                for line in file.readlines():
                        try:
                                line = line.strip() + "." + domain_str
                                if test_sub(line):
                                        print (line)
                                        letsgo.append(line)
                        except Exception as ex:
                                pass
        return letsgo





#"-dL, --list string; file containing list of domains for subdomain discovery"
def run_list_subs():
        dfile_list = []
        letsgo = []
        with open(wordlist_L, "r") as dfile:
                for dline in dfile.readlines():
                        dline = dline.strip()
                        with open(wordlist_W, "r") as file:
                                for line in file.readlines():
                                        try:
                                                line = line.strip() + "." + dline
                                                if test_sub(line):
                                                        print (line)
                                                        letsgo.append(line)
                                        except Exception as ex:
                                                pass
        return letsgo


#Save output
def save(results):
        if domain_str:
                with open(output_F, "a") as saved1:
                        for res in results:
                                saved1.write(res + "\n")
        elif wordlist_L:
                with open(output_F, "a") as saved2:
                        for res in results:
                                saved2.write(res + "\n")
                                                            

#Silent Banner(Optional)
def printx(text):
        if not args.silent:
                print(text, file=sys.stderr)


#=================================================
# Scanner Vhost
#=================================================

#"-vh, --vhost; Find Vhost"
def run_vhost():
        letsgo = []
        with open(wordlist_W, "r") as file:
                for line in file.readlines():
                        try:
                                line = line.strip() + "." + vhost_V
                                letsgo.append(line)
                        except:
                                pass
        return letsgo


#Vhost requests
def vhost_H():
        run = run_vhost()
        for i in run:
                Headers = {"Host":"{}".format(i)}
                try:
                        r = requests.get("https://" + vhost_V, headers=Headers)
                        filter(r, i)
                except:
                        break
#Vhost Filter
def filter(res, host):
        vmode = ""
        status_R = res.status_code
        length = res.content
        beaut = BeautifulSoup(res.content, 'lxml')
        #HTML Parser
        soup = BeautifulSoup(res.text, 'html.parser')
        lines_Parser = soup.prettify()
        lines_P = soup.find_all()
        seconds = str(res.elapsed.total_seconds())

        if verbose:
                vmode = "       [Status: "+ str(status_R) + "," +"  Size: " + str(len(length)) + "," + "  Words: " + str(len(beaut)) + "," + "  Lines: " + str(len(lines_P)) + "," + "  Duration: " + seconds +" ms]"

        if st_cd > 0:
                if st_cd != status_R:
                        print (host + vmode)

        elif size  > 0:
                if size != len(length):
                        print (host + vmode)

        elif words > 0:
                if words != len(beaut):
                        print (host + vmode)


        elif lineS > 0:
                if lineS != len(lines_P):
                        print (host + vmode)

        else:
                print (host + vmode)


#Main
def main():
        results = []
        banner()
        if domain_str:
                printx ("[+] Find Subdomains [+] ")
                results = run_sub()
        elif wordlist_L:
                printx ("[+] Find Subdomains [+] ")
                results = run_list_subs()

        if vhost_V:
                printx ("[+] Find Vhosts [+] ")
#               results = vhost_H()
                vhost_H()
        if results != []:
                if args.output:
                        save(results)

        else:
#               print ("[!] No Results! [!]")
                pass

if __name__ == "__main__":
        try:
                main()
        except:
                print ("\n[WARN] Caught keyboard interrupt (Ctrl-C)")
