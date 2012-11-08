# IPython log file

import subprocess
import urllib
from shlex import split
from collections import namedtuple
api_url = "https://maps.googleapis.com/maps/api/browserlocation/json?browser=firefox&sensor=true"


p = subprocess.Popen(NMCLI_CMD, stdout=subprocess.PIPE)
stdout,stderr = p.communicate()
AP = namedtuple('AP', ('signal','ssid','bssid'))
aps = [split(l) for l in stdout.replace("""'s""",'===s').split('\n')[1:-1]]
aps = [AP(ap[0],ap[1].replace('===s',"'s"),ap[2]) for ap in aps]
for ap in aps:
    print '&wifi=mac:%s%7Cssid:%s%7Css:%s' % (ap.bssid, urllib.quote_plus(ap.ssid), ap.signal)
for ap in aps:
    print '&wifi=mac:%s%%7Cssid:%s%%7Css:%s' % (ap.bssid, urllib.quote_plus(ap.ssid), ap.signal)
api_url
#[Out]# 'https://maps.googleapis.com/maps/api/browserlocation/json?browser=firefox&sensor=true'
urllib.unquote('%7C')
#[Out]# '|'
for ap in aps:
    print ''|.join(ap.bssid, urllib.quote_plus(ap.ssid), ap.signal)
for ap in aps:
    print '|'.join(ap.bssid, urllib.quote_plus(ap.ssid), ap.signal)
for ap in aps:
    print '|'.join((ap.bssid, urllib.quote_plus(ap.ssid), ap.signal))
for ap in aps:
    print urllib.quote_plus('|'.join((ap.bssid, urllib.quote_plus(ap.ssid), ap.signal)))
for ap in aps:
    print urllib.quote_plus('|'.join((ap.bssid, urllib.quote_plus(ap.ssid), ap.signal)))
for ap in aps:
    print '|'.join((ap.bssid, urllib.quote_plus(ap.ssid), ap.signal))
wifilist = ['|'.join((ap.bssid, urllib.quote_plus(ap.ssid), ap.signal)) for ap in aps]
wifilist
#[Out]# ['00:21:29:B1:7C:48|_wireless_|63', '58:35:D9:64:02:20|CUWireless|69', '98:FC:11:5A:4C:9E|68102|72', '00:21:E9:B8:28:66|Matt|69', '20:AA:4B:9C:5A:4E|Forerunner+5|47', 'BA:C7:5D:03:E7:90|Lorenzo+Limones%27s+Guest+Network|30', 'B8:C7:5D:03:E7:97|Lorenzo%27s++Network|32', '2C:B0:5D:FD:1E:E8|Velociraptor|44', '00:26:BB:77:8C:F3|Dwight%27s+Wi-Fi+Network|15', '00:26:99:22:4F:D0|CUWireless|19', '00:24:36:A6:1A:4D|FGI+Wireless|17', '06:24:36:A6:1A:4D|FGI+Guest+Network|24', '10:BD:18:CF:24:10|AFP|5', '2C:B0:5D:FB:62:39|FB6239|7', '00:14:A5:91:FD:F4|Motorola|19', '58:35:D9:3B:23:D0|CUWireless|34', '10:BD:18:CF:25:00|AFP|19', '00:24:93:5D:BF:E0|Sisters|24', '00:18:3F:30:A3:C1|Kelly+Firm|5', 'C0:3F:0E:6E:F4:AE|JDSteffen-PC-Wireless|30', '4C:60:DE:45:00:52|NETGEAR70|12', '2C:B0:5D:FC:46:D7|G-Net|24', '7C:D1:C3:D2:7A:24|Scott+Beals%27s+Network|5', '00:14:51:6E:71:05|Ekapon+Tanthana%27s+Network|12', '00:18:39:41:51:7D|Black+Mesa|0', '68:7F:74:E8:78:8E|LiveCover|22', 'C0:C1:C0:9C:7A:BA|Cupcakes%21|17', '00:1C:F0:61:D2:99|ICC-Wireless|17', '00:1E:52:F4:FA:F5|Apple+Network+5fea21|12', '00:1A:70:63:EC:28|Molly%21|5', '40:F4:EC:DB:13:80|BBFWTN|4', '00:23:69:ED:77:20|Forerunner+3|32', '08:86:3B:B2:CB:CA|Development|12', 'E0:91:F5:0D:28:86|Padraig|0']
get_ipython().magic(u'pinfo urllib.urlencode')
urllib.urlencode(( ('wifi',ap') for ap in wifilist))
urllib.urlencode(( ('wifi',ap') for ap in wifilist)
urllib.urlencode( ('wifi',ap') for ap in wifilist)
urllib.urlencode( ('wifi',ap) for ap in wifilist)
[('wifi',ap) for ap in wifilist]
#[Out]# [('wifi', '00:21:29:B1:7C:48|_wireless_|63'), ('wifi', '58:35:D9:64:02:20|CUWireless|69'), ('wifi', '98:FC:11:5A:4C:9E|68102|72'), ('wifi', '00:21:E9:B8:28:66|Matt|69'), ('wifi', '20:AA:4B:9C:5A:4E|Forerunner+5|47'), ('wifi', 'BA:C7:5D:03:E7:90|Lorenzo+Limones%27s+Guest+Network|30'), ('wifi', 'B8:C7:5D:03:E7:97|Lorenzo%27s++Network|32'), ('wifi', '2C:B0:5D:FD:1E:E8|Velociraptor|44'), ('wifi', '00:26:BB:77:8C:F3|Dwight%27s+Wi-Fi+Network|15'), ('wifi', '00:26:99:22:4F:D0|CUWireless|19'), ('wifi', '00:24:36:A6:1A:4D|FGI+Wireless|17'), ('wifi', '06:24:36:A6:1A:4D|FGI+Guest+Network|24'), ('wifi', '10:BD:18:CF:24:10|AFP|5'), ('wifi', '2C:B0:5D:FB:62:39|FB6239|7'), ('wifi', '00:14:A5:91:FD:F4|Motorola|19'), ('wifi', '58:35:D9:3B:23:D0|CUWireless|34'), ('wifi', '10:BD:18:CF:25:00|AFP|19'), ('wifi', '00:24:93:5D:BF:E0|Sisters|24'), ('wifi', '00:18:3F:30:A3:C1|Kelly+Firm|5'), ('wifi', 'C0:3F:0E:6E:F4:AE|JDSteffen-PC-Wireless|30'), ('wifi', '4C:60:DE:45:00:52|NETGEAR70|12'), ('wifi', '2C:B0:5D:FC:46:D7|G-Net|24'), ('wifi', '7C:D1:C3:D2:7A:24|Scott+Beals%27s+Network|5'), ('wifi', '00:14:51:6E:71:05|Ekapon+Tanthana%27s+Network|12'), ('wifi', '00:18:39:41:51:7D|Black+Mesa|0'), ('wifi', '68:7F:74:E8:78:8E|LiveCover|22'), ('wifi', 'C0:C1:C0:9C:7A:BA|Cupcakes%21|17'), ('wifi', '00:1C:F0:61:D2:99|ICC-Wireless|17'), ('wifi', '00:1E:52:F4:FA:F5|Apple+Network+5fea21|12'), ('wifi', '00:1A:70:63:EC:28|Molly%21|5'), ('wifi', '40:F4:EC:DB:13:80|BBFWTN|4'), ('wifi', '00:23:69:ED:77:20|Forerunner+3|32'), ('wifi', '08:86:3B:B2:CB:CA|Development|12'), ('wifi', 'E0:91:F5:0D:28:86|Padraig|0')]
wifilist = ['|'.join((ap.bssid, urllib.quote(ap.ssid), ap.signal)) for ap in aps]
wifilist
#[Out]# ['00:21:29:B1:7C:48|_wireless_|63', '58:35:D9:64:02:20|CUWireless|69', '98:FC:11:5A:4C:9E|68102|72', '00:21:E9:B8:28:66|Matt|69', '20:AA:4B:9C:5A:4E|Forerunner%205|47', 'BA:C7:5D:03:E7:90|Lorenzo%20Limones%27s%20Guest%20Network|30', 'B8:C7:5D:03:E7:97|Lorenzo%27s%20%20Network|32', '2C:B0:5D:FD:1E:E8|Velociraptor|44', '00:26:BB:77:8C:F3|Dwight%27s%20Wi-Fi%20Network|15', '00:26:99:22:4F:D0|CUWireless|19', '00:24:36:A6:1A:4D|FGI%20Wireless|17', '06:24:36:A6:1A:4D|FGI%20Guest%20Network|24', '10:BD:18:CF:24:10|AFP|5', '2C:B0:5D:FB:62:39|FB6239|7', '00:14:A5:91:FD:F4|Motorola|19', '58:35:D9:3B:23:D0|CUWireless|34', '10:BD:18:CF:25:00|AFP|19', '00:24:93:5D:BF:E0|Sisters|24', '00:18:3F:30:A3:C1|Kelly%20Firm|5', 'C0:3F:0E:6E:F4:AE|JDSteffen-PC-Wireless|30', '4C:60:DE:45:00:52|NETGEAR70|12', '2C:B0:5D:FC:46:D7|G-Net|24', '7C:D1:C3:D2:7A:24|Scott%20Beals%27s%20Network|5', '00:14:51:6E:71:05|Ekapon%20Tanthana%27s%20Network|12', '00:18:39:41:51:7D|Black%20Mesa|0', '68:7F:74:E8:78:8E|LiveCover|22', 'C0:C1:C0:9C:7A:BA|Cupcakes%21|17', '00:1C:F0:61:D2:99|ICC-Wireless|17', '00:1E:52:F4:FA:F5|Apple%20Network%205fea21|12', '00:1A:70:63:EC:28|Molly%21|5', '40:F4:EC:DB:13:80|BBFWTN|4', '00:23:69:ED:77:20|Forerunner%203|32', '08:86:3B:B2:CB:CA|Development|12', 'E0:91:F5:0D:28:86|Padraig|0']
