import logging
import re

LOGGER = logging.getLogger(__name__)

REGEX = re.compile(r"<td nowrap align=center><font color=red size=\+1>([a-z]+)</font><font color=green size=\+1>([a-z]+)</font><font color=blue size=\+1>([1-9])</font></td>")

def process_html(html):
    # print(html)
    match = REGEX.search(html)
    if match is None:
        LOGGER.error("Failed to find the pingyem")
        raise ValueError("Match not found.")
    headers = ["sound_part_1", "sound_part_2", "tune"]
    return dict(zip(headers, match.group(1, 2, 3)))


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        raise ValueError("Expect one argument")

    path = sys.argv[1]
    with open(path, "r") as f:
        data = process_html(f.read().replace("\n", ""))
        print(data)