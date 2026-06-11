import queue
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

from app.config import SUPPORTED_OUTPUT_FORMATS
from app.converter import convert_many
from app.decryptor import is_encrypted_audio_file
from app.file_ops import collect_file_items, collect_folder_items
from app.models import ConvertResult, SourceItem

POLL_INTERVAL_MS = 100


class App:
    """Main application window for the music format converter."""

    def __init__(self) -> None:
        self.root = TkinterDnD.Tk()
        self.root.title("音乐格式转换器")
        self.root.geometry("840x640")
        self.root.minsize(700, 560)

        self.items: dict[str, SourceItem] = {}
        self.output_dir = tk.StringVar()
        self.target_format = tk.StringVar(value=SUPPORTED_OUTPUT_FORMATS[0])
        self.summary_var = tk.StringVar(value="尚未选择输入")
        self.progress_var = tk.StringVar(value="")

        self._converting = False
        self._cancel_event: threading.Event | None = None
        self._queue: queue.Queue = queue.Queue()

        self._setup_style()
        self._build_widgets()
        self._setup_drag_drop()

    def _setup_style(self) -> None:
        style = ttk.Style(self.root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        default_font = ("Microsoft YaHei UI", 9)
        style.configure(".", font=default_font)
        style.configure("Accent.TButton", font=("Microsoft YaHei UI", 11, "bold"), padding=(0, 6))
        style.configure("Treeview", rowheight=24)

    def _build_widgets(self) -> None:
        """Build the main UI components."""
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill=tk.BOTH, expand=True)

        button_row = ttk.Frame(frame)
        button_row.pack(fill=tk.X, pady=(0, 12))
        self.pick_files_button = ttk.Button(button_row, text="选择文件", command=self.pick_files)
        self.pick_files_button.pack(side=tk.LEFT, padx=(0, 8))
        self.pick_folder_button = ttk.Button(button_row, text="选择文件夹", command=self.pick_folder)
        self.pick_folder_button.pack(side=tk.LEFT, padx=(0, 8))
        self.clear_button = ttk.Button(button_row, text="清空输入", command=self.clear_inputs)
        self.clear_button.pack(side=tk.LEFT)

        format_row = ttk.Frame(frame)
        format_row.pack(fill=tk.X, pady=(0, 12))
        ttk.Label(format_row, text="输出格式").pack(side=tk.LEFT)
        self.format_combo = ttk.Combobox(
            format_row,
            textvariable=self.target_format,
            values=SUPPORTED_OUTPUT_FORMATS,
            state="readonly",
            width=12,
        )
        self.format_combo.pack(side=tk.LEFT, padx=(8, 16))
        ttk.Label(format_row, text="输出目录").pack(side=tk.LEFT)
        self.output_entry = ttk.Entry(format_row, textvariable=self.output_dir)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        self.pick_output_button = ttk.Button(format_row, text="选择目录", command=self.pick_output_dir)
        self.pick_output_button.pack(side=tk.LEFT)

        ttk.Label(frame, textvariable=self.summary_var).pack(anchor=tk.W, pady=(0, 8))

        input_frame = ttk.LabelFrame(frame, text="待转换项目（支持拖放文件/文件夹，Delete 键或右键删除所选）", padding=8)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        self.input_tree = ttk.Treeview(input_frame, columns=("type", "path"), selectmode="extended", height=10)
        self.input_tree.heading("#0", text="文件名")
        self.input_tree.heading("type", text="类型")
        self.input_tree.heading("path", text="源路径")
        self.input_tree.column("#0", width=260, anchor=tk.W)
        self.input_tree.column("type", width=100, anchor=tk.W, stretch=False)
        self.input_tree.column("path", width=380, anchor=tk.W)
        input_scrollbar_y = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.input_tree.yview)
        input_scrollbar_x = ttk.Scrollbar(input_frame, orient=tk.HORIZONTAL, command=self.input_tree.xview)
        self.input_tree.config(yscrollcommand=input_scrollbar_y.set, xscrollcommand=input_scrollbar_x.set)
        input_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        input_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.input_tree.pack(fill=tk.BOTH, expand=True)
        self.input_tree.bind("<Delete>", self._on_delete_selected)
        self.input_tree.bind("<Button-3>", self._on_tree_right_click)

        self._tree_menu = tk.Menu(self.root, tearoff=0)
        self._tree_menu.add_command(label="删除所选", command=self.delete_selected)
        self._tree_menu.add_command(label="清空全部", command=self.clear_inputs)

        self.convert_button = ttk.Button(frame, text="开始转换", style="Accent.TButton", command=self.start_convert)
        self.convert_button.pack(fill=tk.X, pady=(0, 8))

        progress_row = ttk.Frame(frame)
        progress_row.pack(fill=tk.X, pady=(0, 12))
        self.progress_bar = ttk.Progressbar(progress_row, mode="determinate")
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.cancel_button = ttk.Button(progress_row, text="取消", command=self.cancel_convert, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=(8, 0))
        ttk.Label(frame, textvariable=self.progress_var).pack(anchor=tk.W, pady=(0, 8))

        result_frame = ttk.LabelFrame(frame, text="转换结果", padding=8)
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.result_text = tk.Text(result_frame, height=8, wrap=tk.NONE, state=tk.DISABLED)
        self.result_text.tag_configure("ok", foreground="#1a7f37")
        self.result_text.tag_configure("fail", foreground="#cf222e")
        self.result_text.tag_configure("info", foreground="#57606a")
        result_scrollbar_y = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        result_scrollbar_x = ttk.Scrollbar(result_frame, orient=tk.HORIZONTAL, command=self.result_text.xview)
        self.result_text.config(yscrollcommand=result_scrollbar_y.set, xscrollcommand=result_scrollbar_x.set)
        result_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        result_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def pick_files(self) -> None:
        paths = filedialog.askopenfilenames(title="选择音频文件")
        if paths:
            items = collect_file_items(list(paths))
            if items:
                self._add_items(items)
            else:
                messagebox.showwarning("提示", "所选文件中没有支持的音频格式")

    def pick_folder(self) -> None:
        folder = filedialog.askdirectory(title="选择音频文件夹")
        if folder:
            items = collect_folder_items(folder)
            if items:
                self._add_items(items)
            else:
                messagebox.showwarning("提示", "所选文件夹中没有找到支持的音频文件")

    def pick_output_dir(self) -> None:
        folder = filedialog.askdirectory(title="选择输出目录")
        if folder:
            self.output_dir.set(folder)

    def _add_items(self, items: list[SourceItem]) -> None:
        for item in items:
            iid = str(item.source_path)
            if iid in self.items:
                continue
            self.items[iid] = item
            type_text = f"加密({item.source_path.suffix})" if is_encrypted_audio_file(item.source_path) else "普通"
            self.input_tree.insert("", tk.END, iid=iid, text=item.source_path.name, values=(type_text, iid))
        self._update_summary()

    def delete_selected(self) -> None:
        if self._converting:
            return
        for iid in self.input_tree.selection():
            self.items.pop(iid, None)
            self.input_tree.delete(iid)
        self._update_summary()

    def _on_delete_selected(self, _event) -> str:
        self.delete_selected()
        return "break"

    def _on_tree_right_click(self, event) -> None:
        if self._converting:
            return
        row = self.input_tree.identify_row(event.y)
        if row and row not in self.input_tree.selection():
            self.input_tree.selection_set(row)
        if self.input_tree.selection():
            self._tree_menu.tk_popup(event.x_root, event.y_root)

    def clear_inputs(self) -> None:
        if self._converting:
            return
        self.items = {}
        self.input_tree.delete(*self.input_tree.get_children())
        self._update_summary()
        self._clear_results()

    def _update_summary(self) -> None:
        count = len(self.items)
        self.summary_var.set(f"已选择 {count} 个项目" if count else "尚未选择输入")

    def get_all_items(self) -> list[SourceItem]:
        return list(self.items.values())

    def _setup_drag_drop(self) -> None:
        self.input_tree.drop_target_register(DND_FILES)
        self.input_tree.dnd_bind("<<Drop>>", self._on_drop)

    def _on_drop(self, event) -> str:
        if self._converting:
            return "break"
        dropped: list[SourceItem] = []
        files = self.root.tk.splitlist(event.data)
        for file_path in files:
            path = Path(file_path)
            if path.is_file():
                dropped.extend(collect_file_items([str(path)]))
            elif path.is_dir():
                dropped.extend(collect_folder_items(str(path)))
        self._add_items(dropped)
        return "break"

    def _clear_results(self) -> None:
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state=tk.DISABLED)

    def _append_result_line(self, line: str, tag: str) -> None:
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, line, tag)
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)

    def start_convert(self) -> None:
        if self._converting:
            return
        items = self.get_all_items()
        if not items:
            messagebox.showwarning("提示", "请先选择要转换的文件或文件夹")
            return
        if not self.output_dir.get().strip():
            messagebox.showwarning("提示", "请选择输出目录")
            return

        output_dir = Path(self.output_dir.get().strip())
        output_dir.mkdir(parents=True, exist_ok=True)

        self._clear_results()
        self._set_converting_state(True)
        self.progress_bar.config(maximum=len(items), value=0)
        self.progress_var.set(f"准备转换 {len(items)} 个文件...")

        self._cancel_event = threading.Event()
        self._queue = queue.Queue()
        worker = threading.Thread(
            target=self._convert_worker,
            args=(items, output_dir, self.target_format.get(), self._cancel_event),
            daemon=True,
        )
        worker.start()
        self.root.after(POLL_INTERVAL_MS, self._poll_queue)

    def _convert_worker(
        self, items: list[SourceItem], output_dir: Path, target_format: str, cancel_event: threading.Event
    ) -> None:
        def on_progress(index: int, total: int, item: SourceItem) -> None:
            self._queue.put(("progress", index, total, item))

        def on_result(result: ConvertResult) -> None:
            self._queue.put(("result", result))

        results = convert_many(
            items, output_dir, target_format, progress_callback=on_progress, result_callback=on_result, cancel_event=cancel_event
        )
        self._queue.put(("done", results, cancel_event.is_set()))

    def _poll_queue(self) -> None:
        done = False
        while True:
            try:
                message = self._queue.get_nowait()
            except queue.Empty:
                break
            kind = message[0]
            if kind == "progress":
                _, index, total, item = message
                self.progress_bar.config(value=index - 1)
                self.progress_var.set(f"正在转换 ({index}/{total})：{item.source_path.name}")
            elif kind == "result":
                result: ConvertResult = message[1]
                self.progress_bar.config(value=self.progress_bar.cget("value") + 1)
                if result.success:
                    output_name = result.output_path.name if result.output_path else "?"
                    self._append_result_line(f"✓ 成功: {result.source_path.name} -> {output_name}\n", "ok")
                else:
                    self._append_result_line(f"✗ 失败: {result.source_path.name} | {result.message}\n", "fail")
            elif kind == "done":
                _, results, cancelled = message
                done = True
                self._finish_convert(results, cancelled)
        if not done and self._converting:
            self.root.after(POLL_INTERVAL_MS, self._poll_queue)

    def _finish_convert(self, results: list[ConvertResult], cancelled: bool) -> None:
        success_count = sum(1 for r in results if r.success)
        failed_count = len(results) - success_count
        summary = f"完成：成功 {success_count} 个，失败 {failed_count} 个"
        if cancelled:
            summary = f"已取消：成功 {success_count} 个，失败 {failed_count} 个，剩余未转换"
        self._append_result_line(f"\n{summary}\n", "info")
        self.progress_var.set(summary)
        self._set_converting_state(False)
        if cancelled:
            messagebox.showinfo("已取消", summary)
        elif failed_count:
            messagebox.showwarning("转换完成", summary)
        else:
            messagebox.showinfo("转换完成", summary)

    def cancel_convert(self) -> None:
        if self._cancel_event is not None and not self._cancel_event.is_set():
            self._cancel_event.set()
            self.cancel_button.config(text="正在取消…", state=tk.DISABLED)
            self.progress_var.set("正在取消，等待当前文件完成...")

    def _set_converting_state(self, converting: bool) -> None:
        self._converting = converting
        state = tk.DISABLED if converting else tk.NORMAL
        self.convert_button.config(state=state)
        self.pick_files_button.config(state=state)
        self.pick_folder_button.config(state=state)
        self.clear_button.config(state=state)
        self.pick_output_button.config(state=state)
        self.output_entry.config(state=state)
        self.format_combo.config(state=tk.DISABLED if converting else "readonly")
        if converting:
            self.cancel_button.config(text="取消", state=tk.NORMAL)
        else:
            self.cancel_button.config(text="取消", state=tk.DISABLED)
            self._cancel_event = None


def run_app() -> None:
    """Launch the GUI application."""
    app = App()
    app.root.mainloop()
