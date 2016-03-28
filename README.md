# ImageBoard Downloader


Script for download images, webm, gif files for imagesboards (4chan and similars)
Thats should be works on normal websites but not tested.

## Install Dependencies

pip install -r requirements.txt

## How To Use


### Normal Download 

python downbatch.py <url> <extension> <path>

#### example

python downbatch.py http://boards.4chan.org/b/thread/XXXXXX jpg,png,gif,webm mycollection7

python downbatch.py http://boards.4chan.org/gif/thread/ZZZZZZ gif gifs/threadZZZZZXX55Z

If the path not exists, will be created.
The use the same url and path to download the lastest files added, the files that already exists will be skipped.

### Multiple threads

If you want to download files of several pages, add the urls to config.py file and run:

python downbatch.py inconfig


