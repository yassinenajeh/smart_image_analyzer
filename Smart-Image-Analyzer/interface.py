import customtkinter as ctk
from PIL import Image
from tkinter import filedialog
import detector
import cv2
from translations import TEXTS

class Interface:

    def __init__(self):

        self.window = ctk.CTk()

        self.window.title("Smart Image Analyzer")

        self.window.geometry("1200x750")

        self.language = "EN"

        self.title = ctk.CTkLabel(
        
            self.window,
        
            text=TEXTS[self.language]["title"],
        
            font=("Arial", 28, "bold")
        
        )

        self.subtitle = ctk.CTkLabel(

            self.window,

            text=TEXTS[self.language]["sub"],

            font=("Arial", 20),

            text_color="grey"

        )

        self.image_path = None

        self.image_label = ctk.CTkLabel(

            self.window,

            text=TEXTS[self.language]["no_image"]

        )

        self.annotated_label = ctk.CTkLabel(
        
            self.window,
        
            text=""
        
        )

        self.upload_button = ctk.CTkButton(
                
            self.window,
        
            command=self.choose_image,
                
            text=TEXTS[self.language]["upload"]
                
        )

        self.analyze_button = ctk.CTkButton(
        
            self.window,

            command=self.analyze_image,
        
            text=TEXTS[self.language]["analyze"]
        
        )

        self.result_label = ctk.CTkLabel(
                
            self.window,
                
            text=TEXTS[self.language]["results"]
                
        )

        self.lang_button = ctk.CTkButton(

            self.window,

            command=self.lang,

            text=TEXTS[self.language]["lang"]

        )

        self.title.grid(row=0, column=0, columnspan=2, padx=20)

        self.subtitle.grid(row=1, column=0, columnspan=2, padx=20)
                
        self.image_label.grid(row=2, column=0, padx=20, pady=20)

        self.annotated_label.grid(row=2, column=1, padx=20, pady=20)
                
        self.upload_button.grid(row=3, column=0, padx=20, pady=20)
                
        self.analyze_button.grid(row=3, column=1, padx=20, pady=20)
                
        self.result_label.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

        self.lang_button.grid(row=5, column=0, columnspan=2, padx=20, pady=20)


    def run(self):

        self.window.mainloop()


    def choose_image(self):

        self.image_path = filedialog.askopenfilename(

        title=TEXTS[self.language]["choose"],

        filetypes=[

            ("Images", "*.jpg *.jpeg *.png")
        
        ]
    
        )

        if not self.image_path:
        
            return

        self.result_label.configure(
        
            text=TEXTS[self.language]["results"]
        
        )

        self.annotated_label.image = None

        image = Image.open(self.image_path)

        ctk_image = ctk.CTkImage(

            light_image=image,

            dark_image=image,

            size=(350,350)

        )

        self.image_label.configure(

            image=ctk_image,

            text=""
        
        )

        self.image_label.image = ctk_image


    def analyze_image(self):

        if self.image_path is None:

            self.result_label.configure(

            text=TEXTS[self.language]["no_image"]

            )

            return

        self.result_label.configure(

            text=TEXTS[self.language]["analyzing"]

        )

        self.window.update()

        try:

            final_text, annotated_image = detector.detect(self.image_path)

        except Exception as error:

            self.result_label.configure(
            
                text=f'{TEXTS[self.language]["error"]} : {error}'
            
            )

            return

        self.result_label.configure(

            text=final_text

        )

        annotated_rgb = cv2.cvtColor(

            annotated_image,

            cv2.COLOR_BGR2RGB

        )

        pil_image = Image.fromarray(annotated_rgb)

        final_image = ctk.CTkImage(

            light_image=pil_image,

            dark_image=pil_image,

            size=(350, 350)

        )

        self.annotated_label.configure(

            image=final_image,

            text=""

        )

        self.annotated_label.image = final_image


    def lang(self):

        if self.language == "EN":
            
            self.language = "FR"

        else:

            self.language = "EN"

        self.title.configure(

            text=TEXTS[self.language]["title"]

        )

        self.subtitle.configure(

            text=TEXTS[self.language]["sub"]

        )

        self.result_label.configure(
        
            text=TEXTS[self.language]["results"]
        
        )

        self.upload_button.configure(

            text=TEXTS[self.language]["upload"]

        )

        self.analyze_button.configure(

            text=TEXTS[self.language]["analyze"]

        )

        self.lang_button.configure(

            text=TEXTS[self.language]["lang"]

        )

        if self.image_path is None:

            self.image_label.configure(

                text=TEXTS[self.language]["no_image"]

            )