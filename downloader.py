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

class YtDlp:
    params = {
        "windowsfilenames": True,
    }

    def __init__(self, url: str) -> None:
        self.dl: YoutubeDL = YoutubeDL(params=YtDlp.params)
        self.url = url
        self.formats: list[FileFormat] = []
        self.format_code = ""
        self.output_path = "%(title)s"
        self.progress_hooks = []

    def get_info(self) -> dict:
        try:
            data = self.dl.extract_info(self.url, download=False)
            self.formats = [FileFormat(format) for format in data["formats"]]
            return {
                "success": True,
                "title": data["title"],
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
                return True
        return False

    def set_output_path(self, path: str) -> bool:
        filepath, filename = os.path.split(path)
        if os.path.exists(filepath):
            filename = os.path.splitext(filename)[0]
            if filename.replace(" ", "") == "": filename = "%(title)s"
            self.output_path = os.path.join(filepath, filename)
            return True
        else: return False

    def add_progress_hooks(self, hook) -> None:
        # self.progress_hooks = hooks
        self.dl.add_progress_hook = hook

    def download(self) -> bool:
        try:
            self.dl.params["format"] = self.format_code
            self.dl.outtmpl_dict = {
                "default": self.output_path + ".%(ext)s",
                "chapter": self.output_path + "- %(section_number)03d %(section_title)s.%(ext)s"
            }
            self.dl.download([self.url])
            return True
        except Exception as e:
            print ("ytdlp download error:", e)
            return False