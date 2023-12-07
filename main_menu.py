import customtkinter as ct
import CTkMessagebox as ctm
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import create_admin as ca
import face_attendance as fa
import enroll_user as eu
import motion_detection as md

def main_menu(app):

    main = ct.CTkToplevel(app)
    main.title("Smart Web Cam")
    main.wm_attributes('-fullscreen', True)

    image = Image.open("images/pattern.png")
    resize = image.resize((1500,1000),Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resize)

    canvas = ct.CTkCanvas(main, width=image.width, height=image.height)
    canvas.pack()

    canvas.create_image(0, 0, anchor=ct.NW, image=background_image)
    
    bg_image = PhotoImage(file="images/pattern.png")
    
    frame2 = ct.CTkFrame(master=main, width=480, height=320, corner_radius=15)

    canvas = ct.CTkCanvas(frame2, width=480, height=320)
    canvas.create_image(0, 0, anchor=ct.NW, image=bg_image)

    frame2.place(relx=0.5, rely=0.5, anchor=ct.CENTER)
    canvas.pack()

    def ask_question():
            msg = ctm.CTkMessagebox(title="Proceed?", message="Do you want to Proceed?",
                                icon="question", option_1="Cancel", option_3="Yes")
            response = msg.get()

            if response == "Yes":
                app.iconify()
                ca.create_admin_account(main)
            else:
                print("Click 'Yes' to Proceed!")

    def ask_question_motion():
            msg = ctm.CTkMessagebox(title="Proceed?", message="Do you want to Proceed?",
                                icon="question", option_1="Cancel", option_3="Yes")
            response = msg.get()

            if response == "Yes":
                app.iconify()
                md.motion_detection(main,frame2)
            else:
                print("Click 'Yes' to Proceed!")

    def ask_question_enroll():
            msg = ctm.CTkMessagebox(title="Proceed?", message="Do you want to Proceed?",
                                icon="question", option_1="Cancel", option_3="Yes")
            response = msg.get()

            if response == "Yes":
                app.iconify()
                eu.enroll_student(main,frame2)
            else:
                print("Click 'Yes' to Proceed!")

    def ask_question_attendance():
            msg = ctm.CTkMessagebox(title="Proceed?", message="Do you want to Proceed?",
                                icon="question", option_1="Cancel", option_3="Yes")
            response = msg.get()

            if response == "Yes":
                app.iconify()
                fa.attendance_System(main,frame2)
            else:
                print("Click 'Yes' to Proceed!")

    attendance = ct.CTkButton(master=frame2, width=15, height=30, corner_radius=12, hover_color="black",
                              text="1. Attendance System",
                              font=ct.CTkFont("Century Gothic", 14, "bold", "roman"),
                              command=ask_question_attendance)
    attendance.place(x=20, y=100)

    security = ct.CTkButton(master=frame2, width=15, height=30, corner_radius=12, hover_color="black",
                            text="3. Motion Detection",
                            font=ct.CTkFont("Century Gothic", 14, "bold", "roman"),
                            command=ask_question_motion)
    security.place(x=20, y=200)

    enroll = ct.CTkButton(master=frame2, width=15, height=30, corner_radius=12, hover_color="blue",
                        text="4. Enroll User",
                        font=ct.CTkFont("Century Gothic", 14, "bold", "roman"),
                        command=ask_question_enroll)
    enroll.place(x=275, y=100)

    create = ct.CTkButton(master=frame2, width=15, height=30, corner_radius=12, hover_color="blue",
                       text="6. Create New Admin",
                       font=ct.CTkFont("Century Gothic", 14, "bold", "roman"),
                       command=ask_question)
    create.place(x=275, y=200)

    main_label = ct.CTkLabel(frame2, text="Main Menu", font=ct.CTkFont("Century Gothic", 20, "bold", "roman"))
    main_label.place(x=180, y=35)

    def destroy(window):
         window.destroy()
         app.deiconify()
         
    exitbtn = ct.CTkButton(master=frame2, corner_radius=13, hover=True, hover_color="dark red", text="EXIT",
                           font=ct.CTkFont("Century Gothic", 14, "bold", "roman"), fg_color="transparent", command=lambda: destroy(main))
    exitbtn.place(x=170, y=270)

    def close_app():
        os._exit(0)
    
    def minimize_app():
        app.iconify()
        main.iconify()

    top_bar = ct.CTkFrame(main, fg_color="green", height=30)
    top_bar.place(relx=0, rely=0, relwidth=1)

    close_button = ct.CTkButton(top_bar, text="X", command=close_app, hover_color="red",width=50,corner_radius=10)
    close_button.pack(side="right")

    minimize_button = ct.CTkButton(top_bar, text="-", command=minimize_app, hover_color="yellow",width=50, corner_radius=10)
    minimize_button.pack(side="right")

    main.mainloop()