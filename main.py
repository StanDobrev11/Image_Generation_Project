import customtkinter as tk
from customtkinter import CTkImage
from dotenv import load_dotenv
from io import BytesIO
import openai
import os
import urllib.request
from PIL import Image, ImageTk


class MyRadiobuttonFrame(tk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = tk.StringVar(value="")

        self.title = tk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = tk.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)


class ToplevelWindow(tk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("200x200")

        self.label = tk.CTkLabel(self, text="ErrorMSG")
        self.label.pack(padx=20, pady=20)

        # self.button = tk.CTkButton(self, )


class Root(tk.CTk):
    def __init__(self):
        super().__init__()

        self.title('ImageX')
        self.geometry('800x600')
        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

        self.textbox = tk.CTkTextbox(self, width=400, corner_radius=0)
        self.textbox.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.textbox.insert("0.0", "Enter description of photo and choose size:")
        self.textbox.update()
        # self.input = tk.CTkEntry(self)
        # self.input.grid(row=0, column=0, padx=20, pady=20, sticky='ew', columnspan=2)

        # radio buttons
        self.radiobutton_frame = MyRadiobuttonFrame(self, "Size", values=["256x256", "512x512", "1024x1024"])
        self.radiobutton_frame.grid(row=0, column=2, padx=(0, 10), pady=(10, 0), sticky="nsew")

        # regular buttons
        self.button_submit = tk.CTkButton(self, text="Submit", command=self.get_image_url)
        self.button_submit.grid(row=2, column=0, pady=20, padx=(20, 20), sticky='w')
        self.button_clear = tk.CTkButton(self, text="Clear", command=self.clear)
        self.button_clear.grid(row=2, column=1, padx=(0, 20))

        self.image_label = tk.CTkLabel(self, text='YOUR IMAGE HERE')
        self.image_label.grid(row=3, column=0, padx=10, pady=10)

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def click(self, event):
        self.textbox.configure(state='normal')
        self.textbox.delete('0.0', 'end')
        self.textbox.unbind('<Button-1>', clicked)

    def get_image_url(self):
        try:
            image_url = self.submit()
        except openai.error.InvalidRequestError:
            self.textbox.insert('0.0', 'Prompt cannot be empty')
            self.textbox.configure(fg_color='red', text_color='yellow')
            # error_label = tk.CTkLabel(self, text='Prompt cannot be empty', fg_color='red')
            # error_label.grid(row=2, column=2)
            # self.open_toplevel()
        else:
            self.display_image(image_url)

    def display_image(self, image_url):
        """
        This functions saves the created image to the RAM. The photo is received in bytes, loading top-to-bottom first.
        Tfore, we need to download it first and then open it completely. Need to use 'urllib'. 'with' is used in order
        to open and the close the file. 'read' method is used to read the data. Next we need to save the read data to
        RAM. 'image_stream' is the float as bytes of the photo. 'from io import BytesIO' -> 'BytesIO' saves the image to
        RAM. In order to render the image, 'Pillow' lib must be installed. The image is a 2D matrix. First we render the
        as normal image using 'Image.open(image_stream)', then as Tk object. Then we create 'label' object in the Root
        class and attach the image using 'configure' method as below. To save the file we must write 'self.image_label
        = image'
        """
        with urllib.request.urlopen(image_url) as url:
            image_data = url.read()
        image_stream = BytesIO(image_data)
        image = Image.open(image_stream)
        image = ImageTk.PhotoImage(image)
        self.image_label.configure(text='', image=image)
        self.image_label = image

    def submit(self):
        load_dotenv(dotenv_path=r'C:\Users\Master\PycharmProjects\api.env')
        openai.api_key = os.getenv('DALLE_API')

        response = openai.Image.create(
            prompt=self.textbox.get('0.0', 'end'),
            n=1,
            size=self.radiobutton_frame.get()  # 256x 512x 1024x
        )
        return response['data'][0]['url']

    def clear(self):
        self.textbox.delete('0.0', 'end')
        self.textbox.configure(fg_color='white', text_color='black')


app = Root()

clicked = app.textbox.bind('<Button-1>', app.click)

app.mainloop()
