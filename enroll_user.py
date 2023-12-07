import customtkinter as ct
import tkinter as tk
import pymysql
import numpy as np
import cv2,dlib
import CTkMessagebox as ctm
import os
from PIL import Image,ImageTk
from tkinter import PhotoImage

def enroll_student(main,frame2):

    enroll_interface = ct.CTkToplevel(main)
    enroll_interface.wm_attributes('-fullscreen',True)
    enroll_interface.title('Admission Portal')

    image = Image.open("images/pattern.png")
    resize = image.resize((1500,1000),Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resize)

    canvas = ct.CTkCanvas(enroll_interface, width=image.width, height=image.height)
    canvas.pack()

    canvas.create_image(0, 0, anchor=ct.NW, image=background_image)    

    def close_app():
        enroll_interface.destroy()
        main.deiconify()
    
    def minimize_app():
        enroll_interface.iconify()

    frame = ct.CTkFrame(enroll_interface, width=500,height=400, corner_radius=20)

    bg_image = PhotoImage(file="images/pattern.png")

    canvas = ct.CTkCanvas(frame, width=500, height=400)
    canvas.pack()
 
    canvas.create_image(0, 0, anchor=ct.NW, image=bg_image)

    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    top_bar = ct.CTkFrame(enroll_interface, fg_color="yellow", height=30)
    top_bar.pack(fill="both")
    
    close_button = ct.CTkButton(top_bar, text="X", command=close_app, hover_color="red",width=50,corner_radius=10)
    close_button.pack(side="right")

    minimize_button = ct.CTkButton(top_bar, text="-", command=minimize_app, hover_color="yellow",width=50, corner_radius=10)
    minimize_button.pack(side="right")

    label = ct.CTkLabel(frame, text="Admission Portal", font=ct.CTkFont('century gothic',30,"bold","roman"))
    label.place(x=135,y=20)

    customfont = ct.CTkFont('century gothic',14,"bold","roman")

    sname = ct.CTkEntry(frame, placeholder_text='Full Name',width=220, font=customfont)
    sname.place(x=40,y=90)

    srollno = ct.CTkEntry(frame, placeholder_text='Roll No.',width=220, font=customfont)
    srollno.place(x=40,y=150)

    sclass = ct.CTkEntry(frame, placeholder_text='Class',width=180, font=customfont)
    sclass.place(x=280,y=90)

    sgender = ct.CTkComboBox(frame, values=["Male","Female"], font=customfont)
    sgender.set("Gender")
    sgender.place(x=280,y=150)

    sphone = ct.CTkEntry(frame, placeholder_text='Phone no.',width=220, font=customfont)
    sphone.place(x=40,y=210)

    saddress = ct.CTkEntry(frame, placeholder_text='Address',width=220, font=customfont)
    saddress.place(x=40,y=270)

    semail = ct.CTkEntry(frame, placeholder_text='Email',width=180, font=customfont)
    semail.place(x=280,y=210)
    
    def save_info():
        try:  
            conn = pymysql.connect(
                host="b5ssdpfo1apmaws80bj2-mysql.services.clever-cloud.com",
                user="us8lp5vzmmgtsk21",
                password="aXbXSnv9cOrGinhehHLe",
                database="b5ssdpfo1apmaws80bj2"
            )
            cursor = conn.cursor()
            Rollno = srollno.get()
            Name = sname.get()
            Gender = sgender.get()
            Phoneno = sphone.get()
            Address = saddress.get()
            Email = semail.get()
            Class = sclass.get()
            
            sql = "INSERT INTO students (Rollno, Name, Gender, Phoneno, Address, Email, Class) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (Rollno, Name, Gender, Phoneno, Address, Email, Class))
            conn.commit()
            conn.close()
            face_webcam_option()
            db_connection = pymysql.connect(
                host="b5ssdpfo1apmaws80bj2-mysql.services.clever-cloud.com",
                user="us8lp5vzmmgtsk21",
                password="aXbXSnv9cOrGinhehHLe",
                database="b5ssdpfo1apmaws80bj2"
            )

            def store_face_descriptor_for_rollno(db_connection, rollno, face_descriptor):
                try:
                    cursor = db_connection.cursor()

                    face_descriptor_bytes = np.array(face_descriptor, dtype=np.float64).tobytes()

                    cursor.execute("INSERT INTO students (Rollno, face_descriptor) VALUES (%s, %s) ON DUPLICATE KEY UPDATE face_descriptor = %s", (rollno, face_descriptor_bytes, face_descriptor_bytes))
                    db_connection.commit()
                except pymysql.Error as error:
                    print(f"Error storing face descriptor for rollno {rollno}: {error}")
                finally:
                    cursor.close()

            def face_webcam_option():
                global cap
                mssg = ctm.CTkMessagebox(master=frame2,message="Select Your Smart WebCam Preference for Face Storing",
                                            icon="info", option_1="IP WebCam", option_2="External WebCam",
                                            option_3="Internal Built-in WebCam", 
                                            title="Choose Your WebCam")
                
                if mssg.get() == "Internal Built-in WebCam":
                    cap = cv2.VideoCapture(0)
                    face_storing()


                elif mssg.get() == "External WebCam":
                    cap = cv2.VideoCapture(1)
                    face_storing()

                elif mssg.get() == "IP WebCam":
                    new_window = ct.CTkToplevel(main)
                    new_window.title("IP Smart WebCam")
                    new_window.wm_attributes('-fullscreen',True)

                    image = Image.open("images/pattern.png")
                    resize = image.resize((1500,1000),Image.LANCZOS)
                    background_image = ImageTk.PhotoImage(resize)

                    canvas = ct.CTkCanvas(new_window, width=image.width, height=image.height)
                    canvas.pack()

                    canvas.create_image(0, 0, anchor=ct.NW, image=background_image)

                    new_window_frame = ct.CTkFrame(new_window, width=250, height=250)

                    bg_image = PhotoImage(file="images/pattern.png")

                    canvas = ct.CTkCanvas(new_window_frame, width=250, height=250)
                    canvas.pack()
            
                    canvas.create_image(0, 0, anchor=ct.NW, image=bg_image)

                    new_window_frame.place(relx=0.5, rely=0.5, anchor=ct.CENTER)

                    index_label = ct.CTkLabel(new_window_frame, text="'Enter IP address for IP WebCam'",
                                            font=ct.CTkFont("Century Gothic", 14,'bold'))
                    index_label.place(x=20, y=50)

                    index_entry = ct.CTkEntry(new_window_frame, width=220, corner_radius=10, placeholder_text="IP address")
                    index_entry.place(x=20,y=100)

                    def set_ipcam():
                        global cap
                        cap = cv2.VideoCapture(index_entry.get())
                        face_storing()

                    index_btn = ct.CTkButton(new_window_frame,width=150, corner_radius=10, text="Connect to IP WebCam",
                                            command=set_ipcam, hover=True, hover_color='green', fg_color='transparent')
                    index_btn.place(x=50, y=200)

                    def close_app():
                        os._exit(0)
                
                    def minimize_app():
                        new_window.iconify()

                    top_bar = ct.CTkFrame(new_window, fg_color="black", height=30)
                    top_bar.place(relx=0, rely=0, relwidth=1)

                    close_button = ct.CTkButton(top_bar, text="X", command=close_app, hover_color="red",width=50,corner_radius=10)
                    close_button.pack(side="right")

                    minimize_button = ct.CTkButton(top_bar, text="-", command=minimize_app, hover_color="yellow",width=50, corner_radius=10)
                    minimize_button.pack(side="right")

                    new_window.mainloop()

            def face_storing():
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

                        rollno = srollno.get()

                        store_face_descriptor_for_rollno(db_connection, rollno, face_descriptor)
                        print(f"Face descriptor saved for rollno: {rollno}")   
                        break

                cap.release()    
                cv2.destroyAllWindows()
                db_connection.close()
                
        except pymysql.Error as e:
            print("Database Error:", e)

    def ask_question():
         msg = ctm.CTkMessagebox(title="Proceed?", message="Do you want to Proceed to Store Face Descriptor?",
                            icon="question", option_1="Cancel", option_2="No", option_3="Yes")
         response = msg.get()

         if response == "Yes":
            save_info()
         elif response == "Cancel":
             os._exit(0)
         else:
            print("Click 'Yes' to Proceed!")


    proceed = ct.CTkButton(frame, text='Procceed', hover_color="dark green", corner_radius=20, width=220,
                           command=ask_question)
    proceed.place(x=150,y=330)

    enroll_interface.mainloop()

if __name__ == "__main__":
    enroll_student()