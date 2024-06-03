import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import pathlib
from tkinterdnd2 import DND_FILES, TkinterDnD
import datetime
from tkinter import messagebox

WIDTH = 600
HEIGHT = 500

class MyApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.flag = False

        self.title("Watermark Viewer")
        self.geometry(f"{WIDTH}x{HEIGHT}")

        buttonFrame = tk.Frame(self)
        load_button = tk.Button(buttonFrame, text="画像を読み込む", command=self.load_image, width=15)
        load_button.grid(column=0, row=0)
        clear_button = tk.Button(buttonFrame, text="クリア", command=self.clear_image, width= 15)
        clear_button.grid(column=1, row=0)
        watermark_button = tk.Button(buttonFrame, text="ウォーターマーク追加",command=self.add_watermark, width=15)
        watermark_button.grid(column=0, row=1)
        save_button = tk.Button(buttonFrame, text="保存",command=self.save_image,width=15)
        save_button.grid(column=1, row=1)
        buttonFrame.pack(pady=20)

        self.labelFrame = tk.LabelFrame(self, width=400, height=400, text="画像をドラッグ＆ドロップ", labelanchor="n")
        self.labelFrame.drop_target_register(DND_FILES)
        self.labelFrame.dnd_bind("<<Drop>>", self.funcDragAndDrop)
        self.labelFrame.pack()

    def load_image(self):
        if self.flag:
            self.clear_image()
        self.path = filedialog.askopenfilename()
        path = self.path

        self.image = Image.open(open(path, "rb"))
        self.image.thumbnail((400, 400))
        photoImage = ImageTk.PhotoImage(self.image)

        #画像を表示
        self.image_label = tk.Label(self.labelFrame, image=photoImage)
        self.image_label.image = photoImage
        self.image_label.pack()

        self.flag = True

    def delete_image(self):
        p = pathlib.Path(self.path)
        p.unlink()

    def clear_image(self):
        try:
            #画像非表示
            self.image_label.image = None
            #新しいLabelが生成されることを防ぐため削除
            self.image_label.destroy()
        except:
            print("Not found image_label...")

        self.flag = False

    def funcDragAndDrop(self, event):
        self.path = event.data
        #画像を表示
        self.load_image_drag_and_drop()

    #画像表示
    def load_image_drag_and_drop(self):
        if self.flag:
            self.clear_image()
        file_path = self.path
        self.image = Image.open(open(file_path, "rb"))
        self.image.thumbnail((400, 400))
        photoImage = ImageTk.PhotoImage(self.image)
        #画像を表示

        self.image_label = tk.Label(self.labelFrame, image=photoImage)
        self.image_label.image = photoImage
        self.image_label.pack()

        self.flag = True

    def add_watermark(self):
        if self.flag:
            self.clear_image()
        self.image.thumbnail((400, 400))
        drawer = ImageDraw.Draw(self.image)
        w, h = self.image.size
        x, y = int(w / 2), int(h / 2)
        drawer.text(xy=(x, y), text="©Erika Inoue", font_size=20, fill="white", anchor="ms")
        photoImage = ImageTk.PhotoImage(self.image)

        self.image_label = tk.Label(self.labelFrame, image=photoImage)
        self.image_label.image = photoImage
        self.image_label.pack()

        self.flag = True

    def save_image(self):
        try:
            dt = datetime.datetime.now()
            time = dt.strftime("%Y%m%d-%H%M%S")
            self.image.save(f"{time}-watermarked.jpg")
            messagebox.showinfo(message="画像が保存されました！")

        except:
            messagebox.showinfo(message="画像の保存に失敗しました。")


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()