import tkinter as tk
from tkinter import filedialog as fd
import requests

##Useless
client_id = "anonym"
url = "https://api.imgur.com/3/image"


class ImgurToObsidian:
    def __init__(self):
        self.root = tk.Tk()
        self.choose_button = tk.Button()
        self.upload_button = tk.Button()
        self.entry_field = tk.Entry()
        self.open_window()

    def select_file(self):
        filetypes = (
            ('Imgur supported image files',
             ('*.jpg', '*.jpeg', '*.png', '*.gif')),
            ('JPEG-Bilder', '*.jpg'),
            ('PNG-Bilder (auch animiert APNG)', ('*.png', '*.apng')),
            ('GIF-Bilder', '*.gif'))

        image_path = fd.askopenfilename(
            title='Open a image',
            initialdir='/',
            filetypes=filetypes)
        if image_path:
            self.upload_image(image_path)

    def open_window(self):
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.title("Imgur-Uploader")

        message = tk.Label(self.root, text="Please choose an image to upload to Imgur.", font=("", 14, "bold"))
        message.pack()

        self.choose_button = tk.Button(self.root, text="Choose an image & Upload", command=self.select_file, width=30,height=2)
        self.choose_button.pack(side="top", anchor="n", pady=30)

        self.root.mainloop()

    def upload_image(self, image_path):
        try:
            headers = {
                "Authorization": f"Client-ID {client_id}"
            }
            with open(image_path, "rb") as image_file:
                payload = {
                    "image": image_file
                }
                response = requests.post(url, headers=headers, files=payload)

            if response.status_code == 200:
                entry_field = tk.Entry(self.root, bd=2, width=70)
                entry_field.insert(0, f"![{"Name"}]({response.json()['data']['link']})")
                entry_field.pack(pady=10)

            else:
                response = tk.Label(self.root, text=f"Fehler beim Upload: {response.status_code}: {response.text}")
                response.pack(expand=True)
        except requests.exceptions.RequestException as error:
            response = tk.Label(self.root, text=f"Fehler beim Upload: {error}")
            response.pack(expand=True)


if __name__ == '__main__':
    imgur = ImgurToObsidian()
    imgur.open_window()
