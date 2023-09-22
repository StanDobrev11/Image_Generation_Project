import customtkinter as tk
from dotenv import load_dotenv
import openai
import os


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


class MyTextBoxFrame(tk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.title = title


class Root(tk.CTk):
    def __init__(self):
        super().__init__()

        self.title('ImageX')
        self.geometry('400x300')
        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

        # TEXTBOX AND INPUT BOX
        self.textbox = tk.CTkTextbox(self, width=400, corner_radius=0)
        self.textbox.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.textbox.insert("0.0", "Enter description of photo:")
        self.textbox.update()
        # self.input = tk.CTkEntry(self)
        # self.input.grid(row=0, column=0, padx=20, pady=20, sticky='ew', columnspan=2)

        # RADIO BUTTONS
        self.radiobutton_frame = MyRadiobuttonFrame(self, "Size", values=["256 x 256", "512 x 512", "1024 x 1024"])
        self.radiobutton_frame.grid(row=0, column=2, padx=(0, 10), pady=(10, 0), sticky="nsew")

        # regular buttons
        self.button_submit = tk.CTkButton(self, text="Submit", command=self.get_image_url)
        self.button_submit.grid(row=2, column=0, pady=20, padx=(20, 20), sticky='w')
        self.button_clear = tk.CTkButton(self, text="Clear", command=self.clear)
        self.button_clear.grid(row=2, column=1, padx=(0, 20))

    def click(self, event):
        self.textbox.configure(state='normal')
        self.textbox.delete('0.0', 'end')
        self.textbox.unbind('<Button-1>', clicked)

    def get_image_url(self):
        image_url = self.submit()
        print(image_url)

    def submit(self):
        load_dotenv(dotenv_path=r'C:\Users\Master\PycharmProjects\api.env')
        openai.api_key = os.getenv('DALLE_API')

        if self.textbox.get('0.0', 'end'):
            response = openai.Image.create(
                prompt=self.textbox.get('0.0', 'end'),
                n=1,
                size="256x256"  # 256x 512x 1024x
            )
            return response['data'][0]['url']
        return 'Enter text'

    def clear(self):
        self.textbox.delete('0.0', 'end')


app = Root()

clicked = app.textbox.bind('<Button-1>', app.click)

app.mainloop()
