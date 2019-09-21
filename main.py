import asyncio
import aiohttp
import json
import logging

logging.basicConfig(level=logging.DEBUG)

# from sqlalchemy import create_engine
# from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
# from sqlalchemy.sql import select
from sqlalchemy.dialects.postgresql import insert

from db import conn, metadata


'''名字吉凶：吉'''

async def post_name_query(session, sem, first_name, last_name):
    url = 'https://s.8s8s.com/m/xingmingceshi_2.php'
    data = {
        'nametype': '0817',
        'pf_xing': last_name,
        'pf_ming': first_name,
        'submit': '名字測試打分',
    }
    async with sem:
        async with session.post(url, data=data) as response:
            return await response.text()

def process_html(html):
    html = html.replace('\n', '')
    # logging.debug(html)
    import re
    match = re.search(r'<font color="red">(\d{1,3})分</font>', html)
    if match is None:
        raise ValueError('No score found.')
    score = int(match.group(1))

    match = re.search(r'<p><strong>名字吉凶</strong>：<font color="#\d{6}"><strong>(.*)</strong></font></p>', html)
    luck = match.group(1)
    return [score, luck]


async def query_name(session, sem, first_name, last_name):
    name = last_name + first_name[0] + first_name[1]
    html = await post_name_query(session, sem, first_name, last_name)
    result = process_html(html)
    logging.debug(f'{name}: newly fetched result = {result}')
    return (name, result)

def get_first_names(middle_chars, last_chars, batch_size=100):
    from itertools import product
    names = []
    for first_name in product(middle_chars, last_chars):
        names.append(first_name)
        if len(names) == batch_size:
            yield names
            names = []
    yield names


def batch_get_names_from_db(names):
  sql = select([names_table.c.name])\
      .where(names_table.c.name.in_(names))
  ret = [row[0] for row in conn.execute(sql).fetchall()]
  logging.debug(ret)
  return ret


def batch_insert_names_and_scores(names_and_scores):
  stmt = insert(names_table).values(names_and_scores)
  on_update_stmt = stmt.on_conflict_do_update(
      index_elements=['name'],
      set_=dict(luck=stmt.excluded.luck, score=stmt.excluded.score)
      )
  ret = conn.execute(on_update_stmt)
  logging.debug(f'insert = {ret}')



async def main():
    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession() as session:
        with open('data_files/char_9_strokes.json', 'r') as f:
            middle_chars = json.load(f)
        with open('data_files/char_by_freq.json', 'r') as f:
            last_chars = json.load(f)


        last_name = '馮'
        futures = []

        # batch call
        for batch_no, first_names in enumerate(get_first_names(middle_chars, last_chars)):
            full_names = [last_name + first_name[0] + first_name[1] for first_name in first_names]
            names_in_db = batch_get_names_from_db(full_names)
            missing_full_names = set(full_names) - set(names_in_db)
            logging.debug(f'To fecth {missing_full_names}')
            if len(missing_full_names) == 0:
              continue
            for full_name in missing_full_names:
                futures.append(query_name(session, sem, full_name[1:], full_name[0]))
            ret = await asyncio.gather(*futures)
            logging.debug(f'ret = {ret}')
            futures = []
            to_insert = [{'name': full_name, 'score': score, 'luck': luck} for full_name, (score, luck) in ret]
            logging.debug(f'to_insert = {to_insert}')
            batch_insert_names_and_scores(to_insert)
            if batch_no >= 100:
              break

        conn.close()


asyncio.run(main())
