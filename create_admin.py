import customtkinter as ct
from PIL import Image,ImageTk
from tkinter import PhotoImage
import pymysql
import cv2
import dlib
import CTkMessagebox as ctm
import numpy as np
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from random import randrange

verify_email_otp = randrange(4389,9394)

def create_admin_account(main):
    
    acc = ct.CTkToplevel(main)
    acc.title("Smart Web Cam")
    acc.wm_attributes('-fullscreen', True)

    image = Image.open("images/pattern.png")
    resize = image.resize((1500,1000),Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resize)

    canvas = ct.CTkCanvas(acc, width=image.width, height=image.height)
    canvas.pack()

    canvas.create_image(0, 0, anchor=ct.NW, image=background_image)

    connection = pymysql.connect(
                    host="b5ssdpfo1apmaws80bj2-mysql.services.clever-cloud.com",
                    user="us8lp5vzmmgtsk21",
                    password="aXbXSnv9cOrGinhehHLe",
                    database="b5ssdpfo1apmaws80bj2"
                )
    def sqlcom():
            cursor = connection.cursor()

            name = entry1.get()
            user_name = entry2.get()
            password = entry3.get()
            email = entry5.get()

            sql = "INSERT INTO admins (name, user_name, password, email) VALUES(%s,%s,%s,%s)"

            cursor.execute(sql, (name, user_name, password, email))

            connection.commit()

            msg = ctm.CTkMessagebox(message="You are going to set face_descriptor for face login",
                                icon="question", option_1="Cancel",option_2="No",option_3="Yes", 
                                title="Store Face Descriptor")
            
            if msg.get() == "Yes":
                setup_face()

            if msg.get() == "Cancel":
                acc.destroy()

    def setup_face():

            def store_face_descriptor_for_new_admin(connection, user_name, face_descriptor):
                try:
                    cursor = connection.cursor()

                    face_descriptor_bytes = np.array(face_descriptor, dtype=np.float64).tobytes()

                    cursor.execute("INSERT INTO admins (user_name, face_descriptor) VALUES (%s, %s) ON DUPLICATE KEY UPDATE face_descriptor = %s", (user_name, face_descriptor_bytes, face_descriptor_bytes))
                    connection.commit()
                except pymysql.Error as error:
                    print(f"Error storing face descriptor for rollno {user_name}: {error}")
                finally:
                    cursor.close()

            cap = cv2.VideoCapture(0)
            face_recognizer = dlib.face_recognition_model_v1('Face_Read_Models/dlib_face_recognition_resnet_model_v1.dat')

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read a frame from the camera stream.")
                    break

                face_detector = dlib.get_frontal_face_detector()
                faces = face_detector(frame)

                if len(faces) == 1:
                    landmarks = dlib.shape_predictor('Face_Read_Models/shape_predictor_68_face_landmarks.dat')(frame, faces[0])
                    face_chip = dlib.get_face_chip(frame, landmarks)
                    face_descriptor = face_recognizer.compute_face_descriptor(face_chip)

                    user_name = entry2.get()

                    store_face_descriptor_for_new_admin(connection, user_name, face_descriptor)
                    print(f"Face descriptor saved for rollno: {user_name}")

                    break

            cap.release()
            cv2.destroyAllWindows()
            connection.close()
            msg = ctm.CTkMessagebox(message="Admin Account has been Created Successfully!",
                                icon="check", option_1='Thanks', 
                                title="Account Created Successfully")
            if msg.get() == "Thanks":
                acc.destroy()
       
    frame = ct.CTkFrame(acc,width=400,height=400,corner_radius=20) 

    def verify_code():
        if otp_entry.get() == str(verify_email_otp):
            sqlcom()
        else:
            msg = ctm.CTkMessagebox(message="Invalid Verification Code",
                                icon="cancel", option_1='Ok', 
                                title="Error")
            if msg.get() == 'Ok':
                otp_entry.delete(0,ct.END)

    def verify_email():
        message = Mail (from_email='thesmartwebcam@gmail.com',
        to_emails=entry5.get(),
        subject='Email Verification For Admin Account',
        html_content="<strong>Your Email Verification Code is: </strong>"+ str(verify_email_otp))
        sg = SendGridAPIClient("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")
        sg.send(message)
    
    def verify_email_password():
        password = entry3.get()
        confirm_password = entry4.get()
        email = entry5.get()
        confirm_email = entry6.get()

        if password == confirm_password and email == confirm_email:
            msg = ctm.CTkMessagebox(message=f"Verification Code has been sent to your Email!",
                                icon="check", option_1="Ok", 
                                title="Email Verification")
            verify_email()
            if msg.get() == "Ok":
                
                entry1.place_forget()
                entry2.place_forget()
                entry3.place_forget()
                entry4.destroy()
                entry5.place_forget()
                entry6.destroy()
                bt.destroy()

                global otp_entry
                otp_entry = ct.CTkEntry(master=frame, width=220, placeholder_text="Verification Code")
                otp_entry.place(x=90, y= 150)
                bt2 = ct.CTkButton(master=frame, width=220, text="Verify Code", corner_radius=6, command=verify_code)
                bt2.place(x=90, y=250)
        else:
            msg = ctm.CTkMessagebox(message="Password or Email does not match",
                                    icon="cancel", option_1="Retry", 
                                    title="Email Verification")
            if msg.get() == 'Retry':
                if password != confirm_password:
                    entry3.delete(0,ct.END)
                    entry4.delete(0,ct.END)

                elif email != confirm_email:
                    entry5.delete(0,ct.END)
                    entry6.delete(0,ct.END)

                else:
                    entry3.delete(0,ct.END)
                    entry4.delete(0,ct.END)
                    entry5.delete(0,ct.END)
                    entry6.delete(0,ct.END)


    bg_image = PhotoImage(file="images/pattern.png")

    canvas = ct.CTkCanvas(frame, width=400, height=400)
    canvas.create_image(0, 0, anchor=ct.NW, image=bg_image)

    frame.place(relx=0.5, rely=0.5, anchor="center")
    canvas.pack()

    entry1 = ct.CTkEntry(master=frame, width=220, placeholder_text="Full name")
    entry1.place(x=90, y=50)

    entry2 = ct.CTkEntry(master=frame, width=220, placeholder_text="Username")
    entry2.place(x=90, y=100)

    entry3 = ct.CTkEntry(master=frame, width=220, placeholder_text="Password")
    entry3.place(x=90, y=150)

    entry4 = ct.CTkEntry(master=frame, width=220, placeholder_text="Confirm Password")
    entry4.place(x=90, y=200)

    entry5 = ct.CTkEntry(master=frame, width=220, placeholder_text="Email")
    entry5.place(x=90, y=250)

    entry6 = ct.CTkEntry(master=frame, width=220, placeholder_text="Confirm Email")
    entry6.place(x=90, y=300)

    bt = ct.CTkButton(master=frame, width=220, text="Verify Email", corner_radius=6, command=verify_email_password)
    bt.place(x=90, y=350)

    def close_app():
        acc.destroy()
        main.deiconify()
    
    def minimize_app():
        acc.iconify()

    top_bar = ct.CTkFrame(acc, fg_color="yellow", height=30)
    top_bar.place(relx = 0, rely = 0, relwidth = 1)
    
    close_button = ct.CTkButton(top_bar, text="X", command=close_app, hover_color="red",width=50,corner_radius=10)
    close_button.pack(side="right")

    minimize_button = ct.CTkButton(top_bar, text="-", command=minimize_app, hover_color="yellow",width=50, corner_radius=10)
    minimize_button.pack(side="right")
    acc.mainloop()

if __name__ == "__main__":
    create_admin_account()