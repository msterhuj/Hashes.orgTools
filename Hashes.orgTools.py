import click
import requests
import json
import os
from glob import glob
import sqlite3
from progress.bar import Bar


@click.command()
@click.option('--download', '-dl', type=bool, is_flag=True, help="Download all leaks wordlist")
@click.option('--merge', '-m', type=bool, is_flag=True, help="Merge all downloaded file in password database for export")
@click.option('--export', '-e', help="export db to a text file")
def main(download: bool, merge: bool, export: str):
    """
        Download all wordlist on hashes.org and generate one unique file\n
        By @MsterHuj
    """

    if download:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
                   "Referer": "https://hashes.org/", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        session = requests.Session()
        session.headers.update(headers)

        leaks = json.loads(
            session.get("https://hashes.org/api/data.php?select=leaks").content.strip().decode('utf-8'))

        if not os.path.exists("wordlist/"):
            os.makedirs("wordlist")

        # download all leaks
        leak_current = 1
        leak_totals = len(leaks)
        for leak in leaks:
            name: str = leak["name"].split("<br>")[0]
            print("(" + str(leak_current) + "/" + str(leak_totals) + ") Downloading leak of " + name + ", " + leak["found"] + " passwords")
            filestream = session.get(
                "https://hashes.org/download.php?hashlistId={0}&type=found".format(leak["id"]), stream=True)
            with open("wordlist/" + name + "-" + leak["id"] + ".txt", "wb") as file:
                for data in filestream.iter_content(chunk_size=1024):
                    if data:
                        file.write(data)
            leak_current += 1

    if merge:
        database = sqlite3.connect("password.db")
        database_cursor = database.cursor()
        try:
            database_cursor.execute("create table password(content varchar not null);")
            database_cursor.execute("create unique index password_unique on password (content);")
            database.commit()
            print("Created password table on password.db")
        except sqlite3.OperationalError:
            print("Table already exists [Skipped]")

        print("Merging files on database and remove duplicate password")
        for url in glob("wordlist/*.txt"):
            name = url.replace("\\", "/").split("/")[1]
            alist = [line.rstrip() for line in open(url)]
            bar = Bar(name, max=len(alist))
            for password in alist:
                try:
                    database_cursor.execute("insert into password (content) values (?);", (password,))
                except sqlite3.IntegrityError:
                    pass
                finally:
                    bar.next()
            database.commit()
            bar.finish()
        database.close()

    if export:
        database = sqlite3.connect("password.db")
        database_cursor = database.cursor()
        print("Exporting password database")
        passwords = database_cursor.execute("select * from password;")
        with open(export, 'w') as f:
            for item in passwords:
                f.write("%s\n" % item)
        database.close()


if __name__ == '__main__':
    main()
