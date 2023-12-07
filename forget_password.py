import customtkinter as ct
import tkinter as tk
import pymysql
import CTkMessagebox as ctm
from PIL import Image, ImageTk
from tkinter import PhotoImage
from random import randrange
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import os

otp = randrange(10204, 98493)

def forget_button(app):
    app.iconify()
    new = ct.CTkToplevel(app)
    new.title("Send OTP Verification")
    new.wm_attributes('-fullscreen', True)
    
    image = Image.open("images/pattern.png")
    resize = image.resize((1500,1000),Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resize)

    canvas = ct.CTkCanvas(new, width=image.width, height=image.height)
    canvas.pack()

    canvas.create_image(0, 0, anchor=ct.NW, image=background_image)

    frame1 = ct.CTkFrame(master=new, width=360, height=360, corner_radius=15, bg_color='transparent')
    
    bg_image = PhotoImage(file="images/pattern.png")
    canvas = ct.CTkCanvas(frame1, width=360, height=360)
    canvas.pack()

    canvas.create_image(0, 0, anchor=ct.NW, image=bg_image)
    frame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    custom_font1 = ct.CTkFont("Century Gothic", 20)

    def sendmail():
        enable()
        enable1()

        message = Mail (from_email='thesmartwebcam@gmail.com',
        to_emails=entry1.get(),
        subject='Final Year Project Smart WebCam',
        html_content="<strong>Your OTP verification Code is: </strong>"+ str(otp))
        sg = SendGridAPIClient("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")
        sg.send(message)

    label1 = ct.CTkLabel(master=frame1, text="Forget Password", font=custom_font1)
    label1.place(x=110, y=30)

    label2 = ct.CTkLabel(master= frame1, text="Registered Email:", font=ct.CTkFont('century gothic', 12))
    label2.place(x=30, y=90)

    entry1 = ct.CTkEntry(master=frame1, width=190)
    entry1.place(x=140, y=90)

    label3 = ct.CTkLabel(master= frame1, text="OTP:", font=ct.CTkFont('century gothic', 12))
    label3.place(x=100, y=130)

    entry2 = ct.CTkEntry(master=frame1, width=190, placeholder_text="OTP code", state="disabled")
    entry2.place(x=140, y=130)

    label4 = ct.CTkLabel(master= frame1, text="New Password:", font=ct.CTkFont('century gothic', 12))
    label4.place(x=40, y=170)

    entry3 = ct.CTkEntry(master=frame1, width=190, placeholder_text="New Password", state="disabled")
    entry3.place(x=140, y=170)

    def enable1():
         entry2.configure(state = "normal")

    def enable():
         entry3.configure(state = "normal")

    def update_password():
        entered_otp = entry2.get()
        if entered_otp == str(otp):
            try:
                connection = pymysql.connect(
                    host="b5ssdpfo1apmaws80bj2-mysql.services.clever-cloud.com",
                    user="us8lp5vzmmgtsk21",
                    password="aXbXSnv9cOrGinhehHLe",
                    database="b5ssdpfo1apmaws80bj2"
                )
                cursor = connection.cursor()

                email = entry1.get()
                new_password = entry3.get()

                sql = "UPDATE admins SET password = %s WHERE email = %s"

                cursor.execute(sql, (new_password, email))
                connection.commit()

                if cursor.rowcount > 0:
                    msg = ctm.CTkMessagebox(message="Password Updated Successfully",
                                    icon="check", option_1="Thanks", title="Password Update")
                else:
                    msg = ctm.CTkMessagebox(message="Wrong Email or No Changes Made",
                                    icon="warning", option_1="Cancel", title="Password Update")

            except pymysql.Error as e:
                print("Database Error", e)
                cursor.close()
                connection.close()

        else:
            msg = ctm.CTkMessagebox(message="Wrong OTP Code",
                                icon="warning", option_1="Cancel", title="Password Update")

        if msg.get() == "Cancel":
            new.destroy()

    def destroy(window):
        window.destroy()
        app.deiconify()

    bt = ct.CTkButton(master=frame1, width=220, text="Send OTP to Email", corner_radius=6, command=sendmail, hover_color="green")
    bt.place(x=85, y=230)

    bt2 = ct.CTkButton(master=frame1, width=220, text="Verify OTP & Reset Password", corner_radius=6, command=update_password, hover_color="green")
    bt2.place(x=85, y=270)

    bt3 = ct.CTkButton(master=frame1, width=220, text="Return to Login Page", corner_radius=6, command=lambda: destroy(new), hover_color="dark red")
    bt3.place(x=85, y=310)
    
    def close_app():
        os._exit(0)
    
    def minimize_app():
        new.iconify()

    top_bar = ct.CTkFrame(new, fg_color="dark red", height=30)
    top_bar.place(relx=0, rely=0, relwidth=1)
    
    close_button = ct.CTkButton(top_bar, text="X", command=close_app, hover_color="red",width=50,corner_radius=10)
    close_button.pack(side="right")

    minimize_button = ct.CTkButton(top_bar, text="-", command=minimize_app, hover_color="yellow",width=50, corner_radius=10)
    minimize_button.pack(side="right")

    new.mainloop()

if __name__ == "__main__":
    forget_button()