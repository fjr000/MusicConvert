from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from app.config import SUPPORTED_OUTPUT_FORMATS
from app.converter import convert_many
from app.file_ops import collect_file_items, collect_folder_items
from app.models import ConvertResult, SourceItem


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("音乐格式转换器")
        self.root.geometry("760x560")

        self.file_items: list[SourceItem] = []
        self.folder_items: list[SourceItem] = []
        self.output_dir = tk.StringVar()
        self.target_format = tk.StringVar(value=SUPPORTED_OUTPUT_FORMATS[0])

        self.summary_var = tk.StringVar(value="尚未选择输入")
        self._build_widgets()

    def _build_widgets(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        button_row = ttk.Frame(frame)
        button_row.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(button_row, text="选择文件", command=self.pick_files).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_row, text="选择文件夹", command=self.pick_folder).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_row, text="清空输入", command=self.clear_inputs).pack(side=tk.LEFT)

        format_row = ttk.Frame(frame)
        format_row.pack(fill=tk.X, pady=(0, 8))
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

        ttk.Label(frame, textvariable=self.summary_var).pack(anchor=tk.W, pady=(0, 8))

        ttk.Label(frame, text="待转换项目").pack(anchor=tk.W)
        self.input_text = tk.Text(frame, height=14)
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(4, 8))

        ttk.Button(frame, text="开始转换", command=self.start_convert).pack(fill=tk.X, pady=(0, 8))

        ttk.Label(frame, text="转换结果").pack(anchor=tk.W)
        self.result_text = tk.Text(frame, height=12)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

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
        items = self.get_all_items()
        self.input_text.delete("1.0", tk.END)
        for item in items:
            self.input_text.insert(tk.END, f"{item.source_path}\n")
        self.summary_var.set(f"已选择 {len(items)} 个项目")

    def get_all_items(self) -> list[SourceItem]:
        merged: dict[str, SourceItem] = {}
        for item in self.file_items + self.folder_items:
            merged[str(item.source_path)] = item
        return list(merged.values())

    def start_convert(self) -> None:
        items = self.get_all_items()
        if not items:
            messagebox.showwarning("提示", "请先选择要转换的文件或文件夹")
            return
        if not self.output_dir.get().strip():
            messagebox.showwarning("提示", "请选择输出目录")
            return

        output_dir = Path(self.output_dir.get().strip())
        output_dir.mkdir(parents=True, exist_ok=True)
        results = convert_many(items, output_dir, self.target_format.get())

        success_count = 0
        failed: list[ConvertResult] = []
        self.result_text.delete("1.0", tk.END)
        for result in results:
            if result.success:
                success_count += 1
                self.result_text.insert(
                    tk.END,
                    f"成功: {result.source_path} -> {result.output_path}\n",
                )
                continue

            failed.append(result)
            self.result_text.insert(
                tk.END,
                f"失败: {result.source_path} | {result.message}\n",
            )

        summary = f"完成：成功 {success_count} 个，失败 {len(failed)} 个"
        self.result_text.insert(tk.END, f"\n{summary}\n")
        if failed:
            messagebox.showwarning("转换完成", summary)
        else:
            messagebox.showinfo("转换完成", summary)


def run_app() -> None:
    app = App()
    app.root.mainloop()
