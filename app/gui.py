from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

from app.config import SUPPORTED_OUTPUT_FORMATS
from app.converter import convert_many
from app.file_ops import collect_file_items, collect_folder_items
from app.models import ConvertResult, SourceItem


class App:
    """Main application window for the music format converter."""

    def __init__(self) -> None:
        self.root = TkinterDnD.Tk()
        self.root.title("音乐格式转换器")
        self.root.geometry("800x620")

        self.file_items: list[SourceItem] = []
        self.folder_items: list[SourceItem] = []
        self.output_dir = tk.StringVar()
        self.target_format = tk.StringVar(value=SUPPORTED_OUTPUT_FORMATS[0])

        self.summary_var = tk.StringVar(value="尚未选择输入")
        self._build_widgets()
        self._setup_drag_drop()

    def _build_widgets(self) -> None:
        """Build the main UI components."""
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill=tk.BOTH, expand=True)

        # Button row
        button_row = ttk.Frame(frame)
        button_row.pack(fill=tk.X, pady=(0, 12))
        ttk.Button(button_row, text="选择文件", command=self.pick_files).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_row, text="选择文件夹", command=self.pick_folder).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_row, text="清空输入", command=self.clear_inputs).pack(side=tk.LEFT)

        # Format and output directory row
        format_row = ttk.Frame(frame)
        format_row.pack(fill=tk.X, pady=(0, 12))
        ttk.Label(format_row, text="输出格式").pack(side=tk.LEFT)
        ttk.Combobox(
            format_row,
            textvariable=self.target_format,
            values=SUPPORTED_OUTPUT_FORMATS,
            state="readonly",
            width=12,
        ).pack(side=tk.LEFT, padx=(8, 16))
        ttk.Label(format_row, text="输出目录").pack(side=tk.LEFT)
        ttk.Entry(format_row, textvariable=self.output_dir).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        ttk.Button(format_row, text="选择目录", command=self.pick_output_dir).pack(side=tk.LEFT)

        # Summary label
        ttk.Label(frame, textvariable=self.summary_var).pack(anchor=tk.W, pady=(0, 8))

        # Input list area
        input_frame = ttk.LabelFrame(frame, text="待转换项目（支持拖放文件/文件夹）", padding=8)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        self.input_text = tk.Text(input_frame, height=12, wrap=tk.NONE)
        input_scrollbar_y = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.input_text.yview)
        input_scrollbar_x = ttk.Scrollbar(input_frame, orient=tk.HORIZONTAL, command=self.input_text.xview)
        self.input_text.config(yscrollcommand=input_scrollbar_y.set, xscrollcommand=input_scrollbar_x.set)
        input_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        input_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.input_text.pack(fill=tk.BOTH, expand=True)

        # Convert button
        ttk.Button(frame, text="开始转换", command=self.start_convert).pack(fill=tk.X, pady=(0, 12))

        # Result area
        result_frame = ttk.LabelFrame(frame, text="转换结果", padding=8)
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.result_text = tk.Text(result_frame, height=10, wrap=tk.NONE)
        result_scrollbar_y = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        result_scrollbar_x = ttk.Scrollbar(result_frame, orient=tk.HORIZONTAL, command=self.result_text.xview)
        self.result_text.config(yscrollcommand=result_scrollbar_y.set, xscrollcommand=result_scrollbar_x.set)
        result_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        result_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def pick_files(self) -> None:
        paths = filedialog.askopenfilenames(title="选择音频文件")
        if not paths:
            return
        items = collect_file_items(list(paths))
        if not items:
            messagebox.showwarning("提示", "所选文件中没有支持的音频格式")
            return
        self.file_items.extend(items)
        self.refresh_inputs()

    def pick_folder(self) -> None:
        folder = filedialog.askdirectory(title="选择音频文件夹")
        if not folder:
            return
        items = collect_folder_items(folder)
        if not items:
            messagebox.showwarning("提示", "所选文件夹中没有找到支持的音频文件")
            return
        self.folder_items.extend(items)
        self.refresh_inputs()

    def pick_output_dir(self) -> None:
        folder = filedialog.askdirectory(title="选择输出目录")
        if folder:
            self.output_dir.set(folder)

    def clear_inputs(self) -> None:
        self.file_items = []
        self.folder_items = []
        self.refresh_inputs()
        self.result_text.delete("1.0", tk.END)

    def refresh_inputs(self) -> None:
        """Update the input text display with current items."""
        items = self.get_all_items()
        self.input_text.delete("1.0", tk.END)
        for item in items:
            self.input_text.insert(tk.END, f"{item.source_path}\n")
        if items:
            self.summary_var.set(f"已选择 {len(items)} 个项目")
        else:
            self.summary_var.set("尚未选择输入")

    def get_all_items(self) -> list[SourceItem]:
        merged: dict[str, SourceItem] = {}
        for item in self.file_items + self.folder_items:
            merged[str(item.source_path)] = item
        return list(merged.values())

    def _setup_drag_drop(self) -> None:
        """Enable drag-and-drop for files and folders."""
        self.input_text.drop_target_register(DND_FILES)
        self.input_text.dnd_bind("<<Drop>>", self._on_drop)

    def _on_drop(self, event) -> str:
        """Handle dropped files and folders."""
        files = self.root.tk.splitlist(event.data)
        for file_path in files:
            path = Path(file_path)
            if path.is_file():
                items = collect_file_items([str(path)])
                if items:
                    self.file_items.extend(items)
            elif path.is_dir():
                items = collect_folder_items(str(path))
                if items:
                    self.folder_items.extend(items)
        self.refresh_inputs()
        return "break"
        """Start the batch conversion process."""
        items = self.get_all_items()
        if not items:
            messagebox.showwarning("提示", "请先选择要转换的文件或文件夹")
            return
        if not self.output_dir.get().strip():
            messagebox.showwarning("提示", "请选择输出目录")
            return

        output_dir = Path(self.output_dir.get().strip())
        output_dir.mkdir(parents=True, exist_ok=True)

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "正在转换，请稍候...\n")
        self.root.update()

        results = convert_many(items, output_dir, self.target_format.get())

        success_count = 0
        failed: list[ConvertResult] = []
        self.result_text.delete("1.0", tk.END)
        for result in results:
            if result.success:
                success_count += 1
                self.result_text.insert(
                    tk.END,
                    f"✓ 成功: {result.source_path.name} -> {result.output_path.name if result.output_path else '?'}\n",
                )
                continue

            failed.append(result)
            self.result_text.insert(
                tk.END,
                f"✗ 失败: {result.source_path.name} | {result.message}\n",
            )

        summary = f"完成：成功 {success_count} 个，失败 {len(failed)} 个"
        self.result_text.insert(tk.END, f"\n{summary}\n")
        if failed:
            messagebox.showwarning("转换完成", summary)
        else:
            messagebox.showinfo("转换完成", summary)


def run_app() -> None:
    """Launch the GUI application."""
    app = App()
    app.root.mainloop()
