import logging
logging.basicConfig(level=logging.DEBUG)
import re
from xml.etree import ElementTree as ET
import sys
import os

sound = re.compile(r'''<font color=red size=\+1>([a-z]*)</font><font color=green size=\+1>([a-z]+)</font><font color=blue size=\+1>([1-9])</font>''')

from db import insert_char_sound_parts_and_tone, drop_all_sounds, conn

def parse_file(filename):
    ret = []
    with open(filename, "r") as f:
        html = f.read()
        logging.debug(html)
        for tr_html in re.findall(r"<tr><td>(.*?)</td><td align=center>(.*?)</td><td>(.*?)</td></tr>", html):
            logging.debug(tr_html[0])
            sound_parts = sound.search(tr_html[0]).group(1,2,3)
            logging.debug(sound_parts)
            logging.debug('='* 80)
            # logging.debug(tr_html[1])
            # logging.debug('='* 80)
            logging.debug(tr_html[2])
            characters = re.findall(r"""<a .*?">(.)</a>""", tr_html[2])
            logging.debug(characters)
            logging.debug('='* 80)
            for ch in characters:
                ret.append({
                    'char': ch,
                    'sound_part_1': sound_parts[0],
                    'sound_part_2': sound_parts[1],
                    'tone': int(sound_parts[2], 10),
                })

    logging.debug(ret)
    return insert_char_sound_parts_and_tone(ret)


if __name__ == '__main__':
    basepath = sys.argv[1]
    files = os.listdir(basepath)
    if len(files) == 0:
        raise ValueError("No file found")

    drop_all_sounds()

    for filename in files:
        parse_file(os.path.join(basepath, filename))

    conn.close()