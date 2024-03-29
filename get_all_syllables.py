import re
import subprocess
import os
import sys

basepath = sys.argv[1]

with open("./data_files/caches/html/syllables/syllables.htm", "r") as f:
    html = f.read()
    for s1, s2 in re.findall(r"pho-rel\.php\?s1=([a-z]*)&s2=([a-z]+)", html):
        url = "http://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/pho-rel.php?s1={s1}&s2={s2}".format(s1=s1, s2=s2)
        print(url)
        filename = os.path.join(basepath, "{s1}_{s2}.htm".format(s1=s1, s2=s2))
        retcode = subprocess.call("wget -O - \"{url}\" | iconv -f BIG5-HKSCS -t utf8 > {filename}".format(url=url, filename=filename), shell=True)

        print(retcode)
        if retcode != 0:
            raise RuntimeError("failed.")
        # break
