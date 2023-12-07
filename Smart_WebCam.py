import customtkinter as ct
from tkinter import PhotoImage
from PIL import ImageTk, Image
import forget_password as fp
import face_login as fl
import authenticate_user as au
import os

def login_page():
      
        ct.set_appearance_mode("system")
        ct.set_default_color_theme("green")

        app = ct.CTk()
        app.title("Smart Web Cam")
        app.wm_attributes('-fullscreen', True)

        image = Image.open("images/pattern.png")
        resize = image.resize((1500,1000),Image.LANCZOS)
        background_image = ImageTk.PhotoImage(resize)

        canvas = ct.CTkCanvas(app, width=image.width, height=image.height)
        canvas.pack()

        canvas.create_image(0, 0, anchor=ct.NW, image=background_image)

        custom_font = ct.CTkFont("Century Gothic", 20,'bold')

        login_page_frame = ct.CTkFrame(master=app, width=320, height=400, corner_radius=100, bg_color='transparent')
        bg_image = PhotoImage(file="images/pattern.png")

        canvas = ct.CTkCanvas(login_page_frame, width=320, height=400)
        canvas.pack()
 
        canvas.create_image(0, 0, anchor=ct.NW, image=bg_image)

        login_page_frame.place(relx=0.5, rely=0.5, anchor=ct.CENTER)

        label = ct.CTkLabel(master=login_page_frame, text="Log into your Smart WebCam", font=custom_font)
        label.place(x=18, y=45)

        user_label = ct.CTkLabel(login_page_frame, text="Username: ", font=ct.CTkFont('century gothic', 14,'bold'))
        user_label.place(x=30, y=165)

        e1 = ct.CTkEntry(master=login_page_frame, width=150, placeholder_text="")
        e1.place(x=120, y=165)

        pass_label = ct.CTkLabel(login_page_frame, text="Password: ", font=ct.CTkFont('century gothic', 14,'bold'))
        pass_label.place(x=30, y=210)

        e2 = ct.CTkEntry(master=login_page_frame, width=150, placeholder_text="")
        e2.place(x=120, y=210)

        global counter
        counter = 1
        def toggle_password():
                global counter
                counter += 1
                if counter %2 == 0:
                        passlabel.configure(text = "Show")
                else:
                        passlabel.configure(text = "Hide")

                current_state = e2.cget("show")
                e2.configure(show="" if current_state else "*")
                

        passlabel = ct.CTkLabel(login_page_frame, text="Hide", font=ct.CTkFont('gothic', 12))
        passlabel.place(x=280, y=210)

        def on_pass_label_enter():
                passlabel.configure(font=ct.CTkFont("Gothic",14,'bold'))
                
        def on_pass_label_leave():
                passlabel.configure(font=ct.CTkFont("Gothic",12))

        passlabel.bind("<Button-1>",lambda event:toggle_password())
        passlabel.bind("<Enter>", lambda event: on_pass_label_enter())
        passlabel.bind("<Leave>", lambda event: on_pass_label_leave())

        global forgetbtn

        forgetbtn= ct.CTkLabel(master=login_page_frame, text="Forgot Password?", font=ct.CTkFont("Century Gothic",12,"bold"))
        forgetbtn.place(x=160, y=240)

        def on_forget_label_enter():
                forgetbtn.configure(font=ct.CTkFont("Century Gothic",14,'bold'))
                
        def on_forget_label_leave():
                forgetbtn.configure(font=ct.CTkFont("Century Gothic",12,'bold'))

        forgetbtn.bind("<Button-1>",lambda event:fp.forget_button(app))
        forgetbtn.bind("<Enter>", lambda event: on_forget_label_enter())
        forgetbtn.bind("<Leave>", lambda event: on_forget_label_leave())
                

        bt = ct.CTkButton(master=login_page_frame, width=220, text="Login", corner_radius=6, command=lambda: au.authenticate_user(e1,e2,login_page_frame,app), hover_color="dark green")
        bt.place(x=50, y=310)

        bt2 = ct.CTkButton(master=login_page_frame, width=220, text="Exit", corner_radius=6, command=lambda:os._exit(0), hover_color="dark red")
        bt2.place(x=50, y=350)
                
        faceloginbtn = ct.CTkLabel(master=login_page_frame, text="Face Login")
        faceloginbtn.place(x=135,y=110)

        def on_label_enter():
                faceloginbtn.configure(font=ct.CTkFont("century gothic", 14, 'bold'))

        def on_label_leave():
                faceloginbtn.configure(font=ct.CTkFont("century gothic",12,'bold'))

        faceloginbtn.bind("<Button-1>", lambda event: fl.face_login_logic(app,login_page_frame))
        faceloginbtn.bind("<Enter>", lambda event: on_label_enter())
        faceloginbtn.bind("<Leave>", lambda event: on_label_leave())

        app.bind("<Return>", lambda event=None: bt.invoke())
        app.mainloop()

if __name__ == "__main__":
      login_page()