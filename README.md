# Hashes.orgTools
Download all wordlist on hashes.org and generate one unique file
> Need Python3 and pip3
## Install

Install lib with pip3 `pip3 install -r requirements.txt`

````
Usage: Hashes.orgTools.py [OPTIONS]

  Download all wordlist on hashes.org and generate one unique file

  By @MsterHuj

Options:
  -dl, --download            Download all leaks wordlist
  -m, --merge                Merge all downloaded file in password database for export
  -ms, --merge-size INTEGER  Auto save db after X password (default 8192)
  -e, --export TEXT          Export db to a text file
  --help                     Show this message and exit.
````

## Next update
 * Download only file updated or added
 * Random agent for download
 * Regex check before add to database

## Change log
 * 1.4
   * Set max password commit by loop
   * remove all in one func to multi function
 * 1.3
   * commit import password at end of file
 * 1.2
   * replace merger to sqlite database
   * update output to exporter function
 * 1.1
   * fix download error from hashes.org
 * 1.0
   * Download all leaks wordlist
   * Merge all downloaded file in one file
   * Remove duplicated line