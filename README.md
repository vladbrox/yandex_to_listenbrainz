# From Yandex Music To ListenBrainz.com
Smoothly export your history from Y.Music.

## Download data
First of all you need to download all your data from Yandex. You can go [here](https://id.yandex.com/personal/data?dialog=service-data&slug=music) to download archive. Then you need to wait. Yandex will mail you when archive is ready.

## Get ListenBrainz User Token
Register an account if you don't have one. The go to [settings](https://listenbrainz.org/settings/) and copy User Token. You will need it later.

## Clone sources
If you have git installed use:
```
https://github.com/vladbrox/yandex_to_listenbrainz.git
```
If not then just [download sources via zip-archive](https://github.com/vladbrox/yandex_to_listenbrainz/archive/refs/heads/main.zip) and extract it.
You will need this directory in future.

## Extract data
Since you downloaded your data, you need to extract archive that you downloaded. You may use [7-zip](https://www.7-zip.org/download.html). Then copy history.json into project directory.

## Installing python and requirements
Install python and pip. You may use [official website](https://www.python.org/downloads/), then open terminal in project directory and install requirements.txt using pip:
```
pip install -r requirements.txt
```

## Run script
Nice. All done. Now you can type this command to run script with menu:
```
python main.py
```
Then select `3. Prepare and Upload history`.
It will ask you for ListenBrainz User Token.
Then script will run through all your history and prepare it for uploading, after thet it will upload all your history with dates(and ListenBrainz account create date doesn't matter). ```errors.json``` will contains all tracks ids that script couldn't find.

# How it works
It use async httpx library for web requests. ```main.py``` is just simple tui. ```prepare.py``` go through all your history.json, makes ```https://api.music.yandex.net/tracks/{id}``` requests and get Artist, Album and Title. Then converts iso time to Unix Timestamp and save it to history_for_lb.json, errors to errors.json. ```upload.py``` create payload for each 100 points and upload directly using ```post```
