import urllib.request
import re
from urllib.parse import urlparse
import os
import socket

def check_connectivity(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((str(host), int(port)))
        s.close()
    except socket.timeout:
        print("Failed to connect to %s:%s" %(host,port))
        return False
    except:
        print("Failed to connect to %s:%s" % (host, port))
        return False
    return True


output = open(os.getcwd()+"\output.csv","w")
output.write("URL Tested,Parameter,Response Code,Result")
output.write("\n")
inputfile = str(input("Enter the file path for the input File: "))

urllist = open(inputfile,"r")
for url in urllist:
    print(url)
    if not url.strip():
        print("empty line in input file")
    else:
        url = url.strip()
        port = 80
        if urlparse(url)[0] == "https":
            port = 443
        elif urlparse(url)[0] == "http":
            port = 80
        if check_connectivity(urlparse(url)[1],port):
            try:
                params = urlparse(url)[4].strip().split("&")
                for x in params:
                    if x in url:
                        url = url.replace(x,x+"\'")
                        with urllib.request.urlopen(url) as response:
                            the_page = response.read()
                        filename = "response_files\\"+urlparse(url)[1].replace(".","_")+".txt"
                        if re.search("sql", str(the_page).lower()):
                            output.write(str(url)+","+str(x)+","+str(response.getcode())+","+str("Possibly SQL Injection Vulnerable"))
                            output.write("\n")
                        else:
                            output.write(str(url)+","+str(x)+","+str(response.getcode())+","+str("SQL Injection Not Vulnerable"))
                            output.write("\n")
                        url = url.replace(x+"\'",x)
            except:
                output.write(str(url)+","+str(urlparse(url)[4])+","+str("000")+","+str("Error in Requesting the URL"))
                output.write("\n")
        else:
            output.write(str(url)+","+str(urlparse(url)[4])+","+str("404")+","+str("Could not connect to the host"))
            output.write("\n")

urllist.close()
output.close()

    
