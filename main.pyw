import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ファイルマネージャー")
        
        self.path_label = tk.Label(root, text="現在のパス:")
        self.path_label.pack()
        
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack()
        self.path_entry.insert(0, os.getcwd())
        
        self.list_button = tk.Button(root, text="ディレクトリ一覧", command=self.list_directory)
        self.list_button.pack()
        
        self.file_list = tk.Listbox(root, width=80, height=20)
        self.file_list.pack()
        
        self.read_button = tk.Button(root, text="ファイルを読む", command=self.read_file)
        self.read_button.pack()
        
        self.create_button = tk.Button(root, text="ファイルを作成", command=self.create_file)
        self.create_button.pack()
        
        self.delete_button = tk.Button(root, text="ファイルを削除", command=self.delete_file)
        self.delete_button.pack()
        
        self.copy_button = tk.Button(root, text="ファイルをコピー", command=self.copy_file)
        self.copy_button.pack()
        
        self.move_button = tk.Button(root, text="ファイルを移動", command=self.move_file)
        self.move_button.pack()

    def list_directory(self):
        path = self.path_entry.get()
        try:
            self.file_list.delete(0, tk.END)
            with os.scandir(path) as entries:
                for entry in entries:
                    self.file_list.insert(tk.END, entry.name)
        except FileNotFoundError as e:
            messagebox.showerror("エラー", str(e))

    def read_file(self):
        selected_file = self.file_list.get(tk.ACTIVE)
        path = os.path.join(self.path_entry.get(), selected_file)
        try:
            with open(path, 'r') as file:
                content = file.read()
            messagebox.showinfo("ファイルの内容", content)
        except FileNotFoundError as e:
            messagebox.showerror("エラー", str(e))
    
    def create_file(self):
        file_name = simpledialog.askstring("入力", "ファイル名を入力してください:")
        path = os.path.join(self.path_entry.get(), file_name)
        try:
            with open(path, 'w') as file:
                file.write("")
            self.list_directory()
        except Exception as e:
            messagebox.showerror("エラー", str(e))

    def delete_file(self):
        selected_file = self.file_list.get(tk.ACTIVE)
        path = os.path.join(self.path_entry.get(), selected_file)
        try:
            os.remove(path)
            self.list_directory()
        except FileNotFoundError as e:
            messagebox.showerror("エラー", str(e))
    
    def copy_file(self):
        src = os.path.join(self.path_entry.get(), self.file_list.get(tk.ACTIVE))
        dest = filedialog.askdirectory(title="コピー先のディレクトリを選択してください")
        if dest:
            try:
                shutil.copy(src, dest)
                self.list_directory()
            except FileNotFoundError as e:
                messagebox.showerror("エラー", str(e))
    
    def move_file(self):
        src = os.path.join(self.path_entry.get(), self.file_list.get(tk.ACTIVE))
        dest = filedialog.askdirectory(title="移動先のディレクトリを選択してください")
        if dest:
            try:
                shutil.move(src, dest)
                self.list_directory()
            except FileNotFoundError as e:
                messagebox.showerror("エラー", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()