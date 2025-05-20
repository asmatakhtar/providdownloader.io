import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from yt_dlp import YoutubeDL
import threading
import os


def download_video():
    url = url_var.get()
    format_type = format_var.get()

    if not url:
        messagebox.showerror("❌ Error", "Please enter a video or playlist URL.")
        return

    # Select download folder
    download_folder = filedialog.askdirectory(title="Select Download Folder")
    if not download_folder:
        return

    btn_download.config(text="Downloading...", state=tk.DISABLED)

    def run_download():
        try:
            ydl_opts = {
                'format': 'bestaudio/best' if format_type == "mp3" else 'best',
                'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }] if format_type == "mp3" else [],
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            messagebox.showinfo("✅ Success", "Download completed successfully!")
        except Exception as e:
            messagebox.showerror("❌ Download Failed", str(e))
        finally:
            btn_download.config(text="Download", state=tk.NORMAL)

    threading.Thread(target=run_download).start()


# =========================
# 🖼️ GUI Design
# =========================
app = tk.Tk()
app.title("🎬 Pro Video Downloader - by Asmat Akhtar")
app.geometry("500x320")
app.resizable(False, False)
app.configure(bg="#1f2937")

# Fonts & Styles
style = ttk.Style(app)
style.theme_use('clam')
style.configure('TLabel', background="#1f2937", foreground="#f1f5f9", font=('Segoe UI', 10))
style.configure('TEntry', fieldbackground="#1e293b", background="#1e293b", foreground="#f1f5f9")
style.configure('TCombobox', fieldbackground="#1e293b", background="#1e293b", foreground="#f1f5f9")
style.configure('TButton', font=('Segoe UI', 10, 'bold'))

# Title
ttk.Label(app, text="🎬 Pro Video Downloader", font=('Segoe UI', 14, 'bold'), foreground="#60a5fa").pack(pady=(15, 10))

# URL Input
ttk.Label(app, text="Paste Video or Playlist URL:").pack(pady=(5, 5))
url_var = tk.StringVar()
ttk.Entry(app, textvariable=url_var, width=60).pack()

# Format Selector
ttk.Label(app, text="Choose Format:").pack(pady=(15, 5))
format_var = tk.StringVar(value="mp4")
ttk.Combobox(app, textvariable=format_var, values=["mp4", "mp3"], state="readonly", width=10).pack()

# Download Button
btn_download = ttk.Button(app, text="Download", command=download_video)
btn_download.pack(pady=20)

# Footer Information
tk.Label(app, text="Supported Platforms: YouTube, Instagram, TikTok, X, Facebook, and more...",
         bg="#1f2937", fg="#94a3b8", font=("Segoe UI", 8)).pack(side=tk.BOTTOM, pady=(5, 0))

tk.Label(app,
         text="Owner: Asmat Akhtar (Professional Developer & Designer)\n📧 mr.asmatbuneri@gmail.com | ☎️ +92-315-7272577",
         bg="#1f2937", fg="#64748b", font=("Segoe UI", 8), justify="center").pack(side=tk.BOTTOM, pady=(0, 10))

# Launch App
app.mainloop()
