
from __future__ import print_function
import subprocess
import re

#host="yahoo.com"
avg=[]
hostData = [['us-east-1','23.23.255.255',0],['us-east-2','13.58.0.253',0],['us-west-1','13.56.63.251',0],['us-west-2','34.208.63.251',0],['us-gov-west-1', '52.61.0.254',0],['ca-central-1', '35.182.0.251',0],['eu-west-1', '34.240.0.253',0],['eu-central-1', '18.194.0.252',0],['eu-west-2','35.176.0.252',0],['ap-northeast-1', '13.112.63.251',0],['ap-northeast-2', '13.124.63.251',0],['ap-southeast-1','13.228.0.251',0], ['ap-southeast-2','13.54.63.252',0],['ap-south-1', '13.126.0.252',0],['sa-east-1', '52.67.255.254',0]]

for element in hostData:
    for host in element:
        ping = subprocess.Popen(
        ["ping", "-n", "3", element[1]],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
        out, error = ping.communicate()
        command_text=out.decode(encoding='windows-1252')
        command_text=command_text.split("Average =",1)[1].strip()
        element[2]=int(command_text.split("ms",1)[0])
from operator import itemgetter
hostData.sort(key=itemgetter(2))
print(hostData)        

for x in hostData:
    print(x[0]+" "+"["+x[1]+"]"+" - "+str(x[2])+" ms")

