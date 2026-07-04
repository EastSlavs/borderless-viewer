import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk


class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry("400x200+100+100")
        self.root.config(bg='gray10')

        self.scale = 1.0
        self.orig_img = None
        self.photo = None

        self.view = tk.Label(self.root, text="图片拖拽至此", fg="white", bg="gray10")
        self.view.pack(expand=True, fill='both')

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

        self.bind_events()

    def bind_events(self):
        self.view.bind("<Button-1>", self.start_move)
        self.view.bind("<B1-Motion>", self.move)
        self.view.bind("<Button-3>", lambda e: self.root.destroy())
        self.root.bind("<Control-MouseWheel>", self.zoom)
        self.root.bind("<Alt-F4>", lambda e: self.root.destroy())

    def on_drop(self, e):
        clean_path = e.data.strip('{}')
        if not clean_path: return
        try:
            self.orig_img = Image.open(clean_path)
            self.scale = 1.0  # 重置缩放比例
            self.update_image()
        except Exception:
            pass

    def update_image(self):
        if not self.orig_img: return

        w, h = self.orig_img.size
        # 计算新尺寸，限制最小为 10x10，防止缩小到崩溃
        new_w = max(10, int(w * self.scale))
        new_h = max(10, int(h * self.scale))

        # 更新图片
        resized_img = self.orig_img.resize((new_w, new_h))
        self.photo = ImageTk.PhotoImage(resized_img)
        self.view.config(image=self.photo, text="")

        # 更新窗口尺寸，保持左上角坐标不变
        x, y = self.root.winfo_x(), self.root.winfo_y()
        self.root.geometry(f"{new_w}x{new_h}+{x}+{y}")

    def zoom(self, e):
        if not self.orig_img: return

        # e.delta > 0 向上滚动放大，反之缩小 (每次缩放 15%)
        if e.delta > 0:
            self.scale *= 1.15
        else:
            self.scale *= 0.85

        self.update_image()

    def start_move(self, e):
        self.root._sx = e.x
        self.root._sy = e.y

    def move(self, e):
        x = self.root.winfo_x() - self.root._sx + e.x
        y = self.root.winfo_y() - self.root._sy + e.y
        self.root.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageViewer(root)
    root.mainloop()
