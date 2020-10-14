import click
import requests
import json
import os
import sys


@click.command()
@click.option('--output', '-o', help="File output")
def main(output: str):

    if output is None:
        print("Need output file")
        exit(1)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
               "Referer": "https://temp.hashes.org/", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    session = requests.Session()
    session.headers.update(headers)

    leaks = json.loads(session.get("https://temp.hashes.org/api/data.php?select=leaks").content.strip().decode('utf-8'))

    if not os.path.exists("wordlist/"):
        os.makedirs("wordlist")

    # download all leaks
    for leak in leaks:
        name: str = leak["name"].split("<br>")[0]
        print("Downloading " + name)
        responce = session.get("https://temp.hashes.org/download.php?hashlistId={0}&type=found".format(leak["id"]),
                               stream=True)
        with open("wordlist/" + name + "-" + leak["id"] + ".txt", "wb") as file:
            for data in responce.iter_content(chunk_size=1024):
                if data:
                    file.write(data)


if __name__ == '__main__':
    main()
