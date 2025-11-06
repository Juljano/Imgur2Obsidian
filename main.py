import tkinter as tk
from tkinter import filedialog as fd
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup



class ImgurToObsidian:
    def __init__(self):
        self.root = tk.Tk()
        webdriver_options = Options()
        webdriver_options.add_argument("--headless")
        webdriver_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=webdriver_options)

        self.entry_field = None
        self.starting_webdriver()
        self.setup_gui()

    def setup_gui(self):
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.title("Postimages-Uploader")

        message = tk.Label(self.root, text="Please choose an image to upload to Postimages.", font=("", 14, "bold"))
        message.pack()

        choose_button = tk.Button(self.root, text="Choose an image & Upload", command=self.select_file, width=30, height=2)
        choose_button.pack(pady=30)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        self.driver.quit()
        self.root.destroy()

    def select_file(self):
        filetypes = (
            ('Imgur supported image files', ('*.jpg', '*.jpeg', '*.png', '*.gif')),
            ('JPEG-Bilder', '*.jpg'),
            ('PNG-Bilder (auch animiert APNG)', ('*.png', '*.apng')),
            ('GIF-Bilder', '*.gif')
        )

        image_path = fd.askopenfilename(
            title='Open an image',
            initialdir='/',
            filetypes=filetypes
        )
        if image_path:
            self.upload_image(image_path)

    def starting_webdriver(self):
        try:
            self.driver.get("https://postimages.org/login")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div/div/h3"))
            )
            self.login()
        except Exception as error:
            print(f"Webdriver error: {error}")

    def login(self):
        try:

            username_field = self.driver.find_element(By.XPATH, "//*[@id='email']")
            username_field.send_keys("moellerjoy@outlook.com")

            password_field = self.driver.find_element(By.XPATH, "//*[@id='password']")
            password_field.send_keys("fG9tFyC6S2g6")

            login_button = self.driver.find_element(By.XPATH, "/html/body/main/div/div/div/form[1]/button")
            login_button.click()

        except Exception as error:
            print(f"Webdriver error: {error}")



    def upload_image(self, image_path):
        try:
            cookies = self.driver.get_cookies()
            session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}

            payload = {
                "gallery": "2j5R5rk",  # Obsidian Album-id
                "optsize": "0",
                "expire": "0",
                "numfiles": "1",
                "upload_session": "1762247250951.019885489023204306"
            }
            headers = {
                "User-Agent": "Mozilla/5.0",
                "X-Requested-With": "XMLHttpRequest"
            }

            with open(image_path, "rb") as image_file:
                files = {
                    "file": ("Images.jpg", image_file, "image/jpeg")
                }
                response = requests.post("https://postimages.org/json/rr", data=payload, files=files, headers=headers, cookies=session_cookies)

            if response.status_code == 200:
                image_link = response.json()['url']
                print(f"![Title]({image_link})")
                self.get_images_format(image_link)
            else:
                error_label = tk.Label(self.root, text=f"Fehler beim Upload: {response.status_code}: {response.text}")
                error_label.pack(expand=True)
        except requests.exceptions.RequestException as error:
            error_label = tk.Label(self.root, text=f"Fehler beim Upload: {error}")
            error_label.pack(expand=True)

    def get_images_format(self, image_link):
        try:
            response = requests.get(image_link)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            image_tag = soup.find(id="direct")['value']
            if image_tag:
                self.entry_field = tk.Entry(self.root, bd=2, width=70)
                self.entry_field.insert(0, f"![Title]({image_tag})")
                self.entry_field.pack(pady=10)
            else:
                print("Kein Bild mit ID 'main-image' gefunden.")
        except IOError as error:
            print(error)


if __name__ == '__main__':
    ImgurToObsidian()
