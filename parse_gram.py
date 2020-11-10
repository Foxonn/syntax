import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import json


def get_local_gram_table() -> dict:
    if os.path.isfile('gram_table.json'):
        with open('gram_table.json', encoding='utf-8') as fp:
            return json.load(fp)

    pass


def get_gram_table():
    ua = UserAgent()
    url = 'http://opencorpora.org/dict.php?act=gram'

    headers = {
        'User-Agent': ua['google chrome']
    }

    resp = requests.get(url, headers=headers)

    if resp.ok and resp.text:
        soup = BeautifulSoup(resp.content, 'html.parser')

        table = soup.table

        rows = table.find_all('tr')[1:]

        gram = dict()

        for row in rows:
            inner_id, outer_id, desc, parent, *_ = row.find_all('td')[1:]

            gram.setdefault(
                inner_id.text, {
                    'inner_id': inner_id.text,
                    'outer_id': outer_id.text,
                    'desc': desc.text,
                    'parent': parent.text
                }
            )

        with open('gram_table.json', 'w', encoding='utf-8') as fp:
            json.dump(gram, fp)


if __name__ == '__main__':
    get_gram_table()
