"""FFmpeg 缺失时的自动下载器（仅用于精简版）"""
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from urllib.request import Request, urlopen
import zipfile
import shutil
import threading


FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-lgpl-shared.zip"
REQUIRED_FILES = ["ffmpeg.exe", "ffprobe.exe", "avcodec-62.dll", "avformat-62.dll", "avutil-60.dll"]


def check_ffmpeg(tools_dir: Path) -> bool:
    """检查 FFmpeg 工具和 DLL 是否齐全"""
    ffmpeg_dir = tools_dir / "ffmpeg"
    return all((ffmpeg_dir / f).exists() for f in REQUIRED_FILES)


def download_ffmpeg(tools_dir: Path, on_complete, on_error):
    """后台线程下载并解压 FFmpeg"""
    ffmpeg_dir = tools_dir / "ffmpeg"
    temp_dir = tools_dir.parent / ".tmp-ffmpeg"
    temp_zip = temp_dir / "ffmpeg.zip"

    try:
        temp_dir.mkdir(parents=True, exist_ok=True)
        ffmpeg_dir.mkdir(parents=True, exist_ok=True)

        req = Request(FFMPEG_URL, headers={"User-Agent": "MusicConvert"})
        with urlopen(req, timeout=30) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            with open(temp_zip, "wb") as f:
                while chunk := resp.read(8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        on_complete(("progress", downloaded, total))

        on_complete(("extract",))
        with zipfile.ZipFile(temp_zip) as z:
            z.extractall(temp_dir)

        # 递归查找并复制所需文件
        for item in REQUIRED_FILES:
            src = next(temp_dir.rglob(item), None)
            if not src:
                raise FileNotFoundError(f"解压后未找到 {item}")
            shutil.copy2(src, ffmpeg_dir / item)

        shutil.rmtree(temp_dir, ignore_errors=True)
        on_complete(("done",))
    except Exception as e:
        on_error(str(e))


class DownloadDialog:
    def __init__(self, tools_dir: Path):
        self.tools_dir = tools_dir
        self.root = tk.Tk()
        self.root.title("首次运行 - 下载 FFmpeg")
        self.root.geometry("450x200")
        self.root.resizable(False, False)

        self.cancelled = False

        ttk.Label(self.root, text="检测到精简版，需下载 FFmpeg 音频引擎（约 50 MB）",
                  font=("", 10)).pack(pady=20)

        self.status = tk.StringVar(value="准备下载...")
        ttk.Label(self.root, textvariable=self.status).pack()

        self.progress = ttk.Progressbar(self.root, length=400, mode="determinate")
        self.progress.pack(pady=15)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack()
        ttk.Button(btn_frame, text="开始下载", command=self.start).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="退出", command=self.cancel).pack(side=tk.LEFT, padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self.cancel)

    def start(self):
        self.status.set("正在下载...")
        threading.Thread(target=download_ffmpeg,
                         args=(self.tools_dir, self.on_event, self.on_error),
                         daemon=True).start()

    def on_event(self, event):
        if self.cancelled:
            return

        if event[0] == "progress":
            downloaded, total = event[1], event[2]
            self.progress["maximum"] = total
            self.progress["value"] = downloaded
            self.status.set(f"已下载 {downloaded//1048576}/{total//1048576} MB")
        elif event[0] == "extract":
            self.progress["mode"] = "indeterminate"
            self.progress.start()
            self.status.set("正在解压...")
        elif event[0] == "done":
            self.progress.stop()
            self.status.set("下载完成！")
            messagebox.showinfo("成功", "FFmpeg 安装完成，程序即将启动")
            self.root.quit()

    def on_error(self, msg):
        if self.cancelled:
            return
        self.progress.stop()
        messagebox.showerror("下载失败", f"FFmpeg 下载失败：{msg}\n\n请检查网络或手动下载放置到 tools/ffmpeg/")
        sys.exit(1)

    def cancel(self):
        self.cancelled = True
        sys.exit(0)

    def run(self):
        self.root.mainloop()
        self.root.destroy()


def ensure_ffmpeg(tools_dir: Path) -> bool:
    """确保 FFmpeg 可用，缺失则触发下载。返回 True 表示可继续"""
    if check_ffmpeg(tools_dir):
        return True

    # 精简版首次启动，弹窗下载
    dialog = DownloadDialog(tools_dir)
    dialog.run()
    return check_ffmpeg(tools_dir)
