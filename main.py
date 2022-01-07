from tkinter import Grid, IntVar, PhotoImage, StringVar, Tk, Toplevel
from tkinter.constants import HORIZONTAL, W
from tkinter.ttk import Button, Entry, Frame, Label, Progressbar
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox  import showerror
from downloader import Downloader, FileFormat
from threading import Thread

def start_gui():
    root = Tk()
    # root config
    root.title("Simple YouTube Video Downloader")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 600
    window_height = 400
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height + window_height / 4)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    downloader = Downloader()

    # url UI
    url_frame = Frame(root)
    url_frame.grid(column=0, row=0, sticky=W)
    url = StringVar()
    url_label = Label(url_frame, text="Video URL")
    url_label.grid(column=0, row=0, sticky=W)
    url_text = Entry(url_frame, textvariable=url)
    url_text.grid(column=1, row=0,sticky=W)

    # video info UI
    info_frame = Frame(root)
    info_frame.grid(column=0, row=1, sticky=W)
    title = StringVar(value="None")
    output_path = StringVar(value=downloader.get_output_path())
    title_label = Label(info_frame, text="Title")
    title_label.grid(column=0, row=1)
    title_text = Label(info_frame, textvariable=title)
    title_text.grid(column=1, row=1)
    def get_info():
        downloader.set_url(url.get())
        downloader.get_info()
        title.set(downloader.title)
        output_path.set(downloader.get_output_path())
        # TODO: update table and jazz
    
    get_info_button = Button(url_frame, text="Get Video Info", command=get_info)
    get_info_button.grid(column=2, row=0)

    # output path UI
    output_frame = Frame(root)
    output_frame.grid(column=0, row=2, sticky=W)
    output_path_label = Label(root, text="Download file to:")
    output_path_label.grid(column=0, row=2, sticky=W)
    output_path_text = Label(root, textvariable=output_path)
    output_path_text.grid(column=1, row=2, sticky=W)
    def change_output_path():
        path = asksaveasfilename(title="Select Output Path", initialdir=downloader.get_output_dir(), initialfile=downloader.get_output_filename())
        while not downloader.set_output_path(path):
            showerror(title="Bad file path", message="Bad file path. Please select a different path!")
            path = asksaveasfilename(title="Select Output Path", initialdir=downloader.get_output_dir(), initialfile=downloader.get_output_filename())
        output_path.set(path)
    change_output_path_button = Button(root, text="Change", command=change_output_path)
    change_output_path_button.grid(column=2, row=2, sticky=W)

    # download video UI
    download_frame = Frame(root)
    download_frame.grid(column=0, row=3)

    # download progress window
    def start_download():
        window = Toplevel(root)
        window.geometry(f"300x200+{center_x}+{center_y}")
        window.title("Progress")

        status = StringVar(value="Status")
        status_text = Label(window, textvariable=status)
        status_text.pack()
        progress = StringVar("")
        progress_text = Label(window, textvariable=progress)
        progress_text.pack()
        progress_bar = Progressbar(window, orient=HORIZONTAL, mode="determinate")
        progress_bar.pack()

        def update_progress(p):
            status.set(p["status"].capitalize())
            if p["status"] == "downloading":
                pv = p["_percent_str"].replace("\u001b[0;94m", "").replace("%\u001b[0m", "")
                progress_bar["value"] = float(pv)
                progress.set(pv + "%")
            window.update_idletasks()
        
        downloader.add_progress_hook(update_progress)
        downloader.download()
        window.destroy()
    
    download_button = Button(download_frame, text="Download", command=start_download)
    download_button.grid(column=0, row=3)

    root.mainloop()


if __name__ == "__main__":
    start_gui()