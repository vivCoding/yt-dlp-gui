from tkinter import PhotoImage, StringVar, Tk
from tkinter.constants import CENTER, END, HORIZONTAL, LEFT, N, NS, VERTICAL, W, YES
from tkinter.ttk import Button, Entry, Frame, Label, Progressbar, Scrollbar, Treeview
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox  import showerror, showinfo
from downloader import Downloader

def start_gui():
    root = Tk()
    # root config
    root.title("Simple YouTube Video Downloader")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 900
    window_height = 450
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height + window_height / 4)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    # TODO remove dependency of asset path
    # icon = PhotoImage(file="./assets/youtube_logo.png")
    # root.iconphoto(True, icon)

    downloader = Downloader()

    # url and video info UI
    frame = Frame(root, width=700, padding=5)
    frame.pack()
    url = StringVar()
    url_label = Label(frame, text="Video URL", font="Helvetica 16 bold")
    url_label.grid(column=0, row=0, sticky=W)
    url_text = Entry(frame, textvariable=url, width=50, font="Helvetica 12")
    url_text.grid(column=1, row=0)

    # TODO add progress bar for retrieving formats

    # video info UI
    title = StringVar(value="None")
    output_path = StringVar(value=downloader.get_output_path())
    title_label = Label(frame, text="Title: ", font="Helvetica 16 bold")
    title_label.grid(column=0, row=1)
    title_text = Label(frame, textvariable=title, font="Helvetica 12", wraplength=600, justify=LEFT)
    title_text.grid(column=1, row=1, sticky=N)

    # video info table
    info_table_frame = Frame(root, padding=5)
    info_table_frame.pack()
    headings = ("Id", "Ext", "Resolution", "FPS", "Filesize", "vcodec", "acodec")
    tree = Treeview(info_table_frame, columns=headings, show="headings", selectmode="browse")
    for heading in headings:
        tree.column(heading, stretch=YES, width=100, anchor=CENTER)
        tree.heading(heading, text=heading)
    tree.grid(column=0, row=0, sticky=W)

    tree_vscrollbar = Scrollbar(info_table_frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=tree_vscrollbar.set)
    tree_vscrollbar.grid(column=1, row=0, sticky=NS)

    def get_info():
        downloader.set_url(url.get())
        downloader.get_info()
        title.set(downloader.title)
        output_path.set(downloader.get_output_path())
        # clear table and insert new stuff
        for child in tree.winfo_children():
            child.destroy()
        for format in downloader.formats:
            tree.insert("", END, values=format.as_tuple())

    def item_selected(event):
        code = tree.item(tree.selection()[0])["values"][0]
        downloader.set_format(str(code))
    tree.bind('<<TreeviewSelect>>', item_selected)

    get_info_button = Button(frame, text="Get Video Info", command=get_info)
    get_info_button.grid(column=2, row=0)

    # download video UI
    download_frame = Frame(root, padding=5)
    download_frame.pack()

    status_frame = Frame(root, padding=5)
    status = StringVar(value="Status")
    status_text = Label(status_frame, textvariable=status)
    status_text.pack()
    progress = StringVar(value="")
    progress_text = Label(status_frame, textvariable=progress)
    progress_text.pack()
    progress_bar = Progressbar(status_frame, orient=HORIZONTAL, mode="determinate")
    progress_bar.pack()

    def start_download():
        # ask for path
        if not downloader.is_downloading:
            path = asksaveasfilename(title="Select Output Path", initialdir=downloader.get_output_dir(), initialfile=downloader.get_output_filename())
            if not downloader.set_output_path(path):
                showerror(title="Bad file path", message="Bad file path. Please select a different path!")
                return
            status_frame.pack()
            downloader.download()

    def update_progress(p):
        status.set(p["status"].capitalize())
        if p["status"] == "downloading":
            pv = p["_percent_str"].replace("\u001b[0;94m", "").replace("%\u001b[0m", "")
            progress_bar["value"] = float(pv)
            progress.set(pv + "%")
        elif p["status"] == "finished":
            showinfo("Finished", message="Video download succeeded!")
            status_frame.pack_forget()
        elif p["status"] == "error":
            showerror(title="Error", message="Error downloading video. Please try again later!")
            status_frame.pack_forget()
        root.update_idletasks()

    downloader.add_progress_hook(update_progress)
    download_button = Button(download_frame, text="Download", command=start_download)
    download_button.grid(column=0, row=0)

    # TODO cancel
    # def on_close():
    #     # User probably wants to cancel if closing progress window
    #     confirm_exit = askyesno(title='Cancel', message="Are you sure you want to cancel?")
    #     if confirm_exit:
    #         root.destroy()
    #         downloader.clean()
    # root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

if __name__ == "__main__":
    start_gui()