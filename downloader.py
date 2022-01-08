import shutil
from yt_dlp import YoutubeDL
from yt_dlp.utils import format_bytes, format_field, join_nonempty
import os

class FileFormat:
    def __init__(self, params) -> None:
        self.format_id = params.get("format_id", "")
        self.ext = params.get("ext", "")
        self.resolution = params.get("resolution", "")
        self.fps = params.get("fps", "")
        self.filesize = format_bytes(params.get("filesize", ""))
        self.tbr = format_field(params, 'tbr', '%dk')
        self.proto = params.get("proto", "")
        self.vcodec = params.get("vcodec", "").replace('none', 'images' if params.get('acodec') == 'none' else 'audio only')
        self.acodec = params.get("acodec", "").replace('none', '' if params.get('vcodec') == 'none' else 'video only')
        self.abr = format_field(params, 'abr', '%dk')
        self.asr = format_field(params, 'asr', '%dHz')
        self.more_info = join_nonempty(
            'UNSUPPORTED' if params.get('ext') in ('f4f', 'f4m') else None,
            format_field(params, 'language', '[%s]'),
            join_nonempty(
                format_field(params, 'format_note'),
                format_field(params, 'container', ignore=(None, params.get('ext'))),
                delim=', '),
            delim=' ')
    
    def as_tuple(self) -> tuple:
        return (
            self.format_id, self.ext, self.resolution, self.fps,
            self.filesize, self.vcodec, self.acodec
        )

class Downloader:

    def __init__(self) -> None:
        self.url = ""
        self.formats: list[FileFormat] = []
        self.format_code = ""
        self.title = ""
        self.ext = ""
        self.output_dir = os.getcwd()
        self.output_filename = ""
        self.progress_hooks = []
        self.is_downloading = False

    def set_url(self, url: str) -> None:
        self.url = url

    def get_url(self) -> str:
        return self.url

    def get_title(self) -> str:
        return self.title

    def get_info(self) -> dict:
        try:
            data = YoutubeDL().extract_info(self.url, download=False)
            self.formats = [FileFormat(format) for format in data["formats"]]
            self.title = data["title"]
            self.output_filename = self.title
            return {
                "success": True,
                "title": self.title,
                "id": data["id"],
                "formats": self.formats
            }
        except Exception as e:
            self.formats = []
            print("ytdlp getinfo error:", e)
            return { "success": False }

    def set_format(self, code: str) -> bool:
        for format in self.formats:
            if format.format_id == code:
                self.format_code = code
                self.ext = format.ext
                return True
        return False

    def get_output_path(self) -> str:
        return os.path.join(self.output_dir, self.output_filename) + "." + self.ext

    def get_output_dir(self) -> str:
        return self.output_dir

    def get_output_filename(self) -> str:
        return self.output_filename + "." + self.ext

    def set_output_path(self, path: str) -> bool:
        filepath, filename = os.path.split(path)
        if os.path.exists(filepath):
            filename = os.path.splitext(filename)[0]
            if filename.replace(" ", "") == "": return False
            self.output_dir, self.output_filename = filepath, filename
            return True
        else: return False

    def add_progress_hook(self, hook) -> None:
        self.progress_hooks.append(hook)

    def download(self) -> bool:
        try:
            self.is_downloading = True
            temp_dir = os.path.join(self.output_dir, "temp")
            params = {
                "windowsfilenames": True,
                "overwrites": True,
                "format": self.format_code,
                "outtmpl": {
                    "default": os.path.join(temp_dir, self.output_filename) + ".%(ext)s",
                    "chapter": os.path.join(temp_dir, self.output_filename) + "- %(section_number)03d %(section_title)s.%(ext)s"
                },
                "progress_hooks": self.progress_hooks
            }
            with YoutubeDL(params) as dl:
                dl.download([self.url])
            shutil.move(os.path.join(temp_dir, self.output_filename) + "." + self.ext, self.get_output_path())
            self.clean()
            self.is_downloading = False
            return True
        except Exception as e:
            print ("ytdlp download error:", e)
            self.is_downloading = False
            return False

    def clean(self) -> None:
        temp_dir = os.path.join(self.output_dir, "temp")
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)