import re
import subprocess

with open("./syllables.htm", "r") as f:
    html = f.read()
    for s1, s2 in re.findall(r"pho-rel\.php\?s1=([a-z]?)&s2=([a-z]+)", html):
        url = "http://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/pho-rel.php?s1={s1}&s2={s2}".format(s1=s1, s2=s2)
        filename = "{s1}_{s2}.htm".format(s1=s1, s2=s2)
        subprocess.call("wget -O - \"{url}\" | iconv -f big5 -t utf8 > {filename}".format(url=url, filename=filename), shell=True)
        print(url)
        # break
