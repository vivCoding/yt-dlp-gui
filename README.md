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
Additionally, if you are on Windows, you can get the zipped already-compiled executable [here](https://github.com/vivCoding/yt-dlp-gui/releases/tag/v0.1.0)

## TODO
- Create pipeline to automate updating/building/publishing
- Make a better UI (actually learn tkinter lol)

## Contributions
Feel free to make a PR or open an issue. I think the code is small and readable enough to understand.

(I have no idea what I wrote 3 years ago)