import click
import requests
import json
import os
from glob import glob


@click.command()
@click.option('--download', '-dl', type=bool, is_flag=True, help="Download all leaks wordlist")
@click.option('--merge', '-m', type=bool, is_flag=True, help="Merge all downloaded file in one file")
@click.option('--clean', '-c', type=bool, is_flag=True, help="Remove duplicated line")
@click.option('--output', '-o', help="output file exit")
def main(download: bool, merge: bool, clean: bool, output: str):
    """
        Download all wordlist on hashes.org and generate one unique file
        By @MsterHuj
    """

    if merge or clean:
        if output is None:
            print("Error you need to specify an output file (--output <filename>)")
            exit(1)

    if download:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
                   "Referer": "https://temp.hashes.org/", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        session = requests.Session()
        session.headers.update(headers)

        leaks = json.loads(
            session.get("https://temp.hashes.org/api/data.php?select=leaks").content.strip().decode('utf-8'))

        if not os.path.exists("wordlist/"):
            os.makedirs("wordlist")

        # download all leaks
        for leak in leaks:
            name: str = leak["name"].split("<br>")[0]
            print("Downloading leak of " + name + ", " + leak["found"] + " passwords")
            filestream = session.get(
                "https://temp.hashes.org/download.php?hashlistId={0}&type=found".format(leak["id"]), stream=True)
            with open("wordlist/" + name + "-" + leak["id"] + ".txt", "wb") as file:
                for data in filestream.iter_content(chunk_size=1024):
                    if data:
                        file.write(data)

    if merge:
        print("Merging files")
        with open(output, "wb") as outfile:
            for url in glob("wordlist/*.txt"):
                print("Merging " + str(url) + " in " + output)
                with open(url, "rb") as infile:
                    outfile.write(infile.read())

    if clean:  # make this function less ram-eating ^^'
        print("Cleaning file")
        lines_seen = set()
        with open("temp_" + output, "w") as output_file:
            for each_line in open(output, "r"):
                if each_line not in lines_seen:
                    output_file.write(each_line)
                    lines_seen.add(each_line)
                    print("Removing duplicated line : " + each_line.replace('\n', ''))
        os.remove(output)
        os.rename("temp_" + output, output)

    if download is None and merge is None and clean is None and output is None:
        os.system("python3 Hashes.orgTools.py --help")
    else:
        if output is not None:
            print(str(sum(1 for line in open(output))) + " : passwords in file")
        print("End of app thanks to using me !")
        print("Written by @MsterHuj")


if __name__ == '__main__':
    main()
