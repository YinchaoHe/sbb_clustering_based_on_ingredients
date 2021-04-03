import argparse
import unicodedata
import urllib
import urllib.request as req
import bs4
import json
import os
from socket import error as SocketError



def get_table():

    try:
        url = "https://www.kingarthurbaking.com/learn/ingredient-weight-chart#:~:text=A%20cup%20of%20all%2Dpurpose,grams%20equivalencies%20for%20common%20ingredients"
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        })
        with req.urlopen(url) as response:
            data = response.read().decode("utf-8")

    except urllib.error.URLError as e:
        print("URL ERROR")
        print(e.reason)
    except SocketError as e:
        print("SOCKET ERROR")

    try:
        ingr_chart = []
        root = bs4.BeautifulSoup(data, "html.parser")
        table_with_shell = root.find("div", class_="brick brick--type--text brick--id--2091 semi-indented remove-space-above weight-chart-table brick--text")
        table = table_with_shell.find("div", class_="brick--text__inner").find("table")
        for tr in table.find_all('tr')[1:]:
            ingr_conv = {}
            anchor = tr.find('th').find('a')
            if anchor:
                ingr_conv['name'] = anchor.string
            else:
                ingr_conv['name'] = tr.find('th').string
            print(ingr_conv['name'])
            tds = tr.find_all('td')
            ingr_conv['Volume'] = tds[0].string
            ingr_conv['Ounces'] = tds[1].string
            ingr_conv['Gras'] = tds[2].string
            ingr_chart.append(ingr_conv)
    except:
        print("Error")

    with open('ingr_conv_chart.json', 'w') as f:
        json.dump(ingr_chart, f)




def main():
    get_table()



if __name__ == '__main__':
    main()