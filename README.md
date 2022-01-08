# yt-dlp gui

Simple GUI for [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Features
- Download video from url
- Choose format to download
- Save/rename to specific output file

## Running and Building
Get required packages
```
pip install -r requirements.txt
```
You can use program simply by running `main.py`
```
python3 main.py
```
If you want to build executable for your platform, you can use `pyinstaller`
```
pyinstaller --onefile main.py
```
