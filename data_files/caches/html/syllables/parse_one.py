import re
from xml.etree import ElementTree as ET

import sys

sound = re.compile(r'''<font color=red size=\+1>([a-z]*)</font><font color=green size=\+1>([a-z]+)</font><font color=blue size=\+1>([1-9])</font>''')

with open(sys.argv[1], "r") as f:
    html = f.read()
    print(html)
    for tr_html in re.findall(r"<tr><td>(.*?)</td><td align=center>(.*?)</td><td>(.*?)</td></tr>", html):
        print(tr_html[0])
        sound_parts = sound.search(tr_html[0]).group(1,2,3)
        print(sound_parts)
        print('='* 80)
        # print(tr_html[1])
        # print('='* 80)
        print(tr_html[2])
        print(re.findall(r"""<a .*?">(.)</a>""", tr_html[2]))
        print('='* 80)
#         root = ET.fromstring(html)
#         for tr in root.findall('./tr'):
#             print(tr)
