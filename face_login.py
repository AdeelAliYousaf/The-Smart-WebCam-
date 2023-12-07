import customtkinter as ct
import pymysql
import cv2, dlib, os
import numpy as np
from tkinter import PhotoImage
from PIL import Image, ImageTk
import datetime as dt
import playsoundsimple as ps
import base64
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from sendgrid import SendGridAPIClient
import CTkMessagebox as ctm
import main_menu as mm

def get_all_admins_email():
    connect = pymysql.connect(
        host="b5ssdpfo1apmaws80bj2-mysql.services.clever-cloud.com",
        user="us8lp5vzmmgtsk21",
        password="aXbXSnv9cOrGinhehHLe",
        database="b5ssdpfo1apmaws80bj2"
    )
    try:
        cursor = connect.cursor()
        cursor.execute("SELECT email FROM admins")
        result = cursor.fetchall()
        if result:
            emails = [email[0] for email in result]
            return emails
        else:
            return None

    except pymysql.Error as e:
        print(f"Error has been occurred i.e.,: {e}")
    
    finally:
        cursor.close()
        connect.close()

def send_unauthorized_alert(emails,frame):
        message = Mail(
        from_email='thesmartwebcam@gmail.com',
        to_emails=emails,
        subject='Alert!!!',
        html_content="<strong>Alert: UnAuthorized Login Attempt</strong>"
    )

        cv2.imwrite("unauthorized_persons/unauthorized_person_login.jpg", frame)

        with open("unauthorized_persons/unauthorized_person_login.jpg", "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode()
            attached_image = Attachment(
                FileContent(image_data),
                FileName("unauthorized_persons/unauthorized_person_login.jpg"),
                FileType("image/jpeg"),
                Disposition("attachment")
            )
            message.attachment = attached_image

        sg = SendGridAPIClient("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")
        sg.send(message)
        print("Success: Email sent with the Image.")

def face_login_logic(app,login_page_frame):

    mssg = ctm.CTkMessagebox(master=login_page_frame,message="Select Your Smart WebCam Preference for Face Login",
                                icon="info", option_1="IP WebCam", option_2="External WebCam",
                                option_3="Internal Built-in WebCam", 
                                title="Choose Your WebCam")
    
    if mssg.get() == "Internal Built-in WebCam":
        global cap
        cap = cv2.VideoCapture(0)
        face_recognition(app,login_page_frame)

    elif mssg.get() == "External WebCam":
        cap = cv2.VideoCapture(1)
        face_recognition(app,login_page_frame)

    elif mssg.get() == "IP WebCam":
        new_window = ct.CTkToplevel(app)
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
            face_recognition(app,login_page_frame)

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

def get_admin_email():
    try:
        connection = pymysql.connect(
            host="b5ssdpfo1apmaws80bj2-mysql.services.clever-cloud.com",
            user="us8lp5vzmmgtsk21",
            password="aXbXSnv9cOrGinhehHLe",
            database="b5ssdpfo1apmaws80bj2"
        )
        cursor = connection.cursor()

        sql = "SELECT email FROM admins WHERE user_name = %s"
        cursor.execute(sql, (user_name,))
        result = cursor.fetchone()
        if result:
            admin_email = result[0]
            return admin_email
        else:
            return None

    except pymysql.Error as e:
        print("Database Error:", e)

    finally:
        cursor.close()
        connection.close()
        
def face_recognition(app, login_page_frame):

    db_connection = pymysql.connect(
        host="b5ssdpfo1apmaws80bj2-mysql.services.clever-cloud.com",
        user="us8lp5vzmmgtsk21",
        password="aXbXSnv9cOrGinhehHLe",
        database="b5ssdpfo1apmaws80bj2"
    )
    
    face_recognizer = dlib.face_recognition_model_v1('Face_Read_Models/dlib_face_recognition_resnet_model_v1.dat')
    threshold = 0.6

    def get_all_face_descriptors(db_connection):
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT user_name, face_descriptor FROM admins")
            results = cursor.fetchall()

            face_descriptors = {}

            for result in results:
                global user_name
                user_name = result[0]
                face_descriptor_blob = result[1]

                if face_descriptor_blob is not None:
                    face_descriptor = np.frombuffer(face_descriptor_blob, dtype=np.float64)
                    face_descriptors[user_name] = face_descriptor
                else:
                    print(f"Warning: No face descriptor found for user {user_name}")

            return face_descriptors

        except pymysql.Error as error:
            print(f"Error retrieving face descriptors: {error}")

        finally:
            cursor.close()

        return None

    def set_login_time(user_name):
        try:
            cursor = db_connection.cursor()
            login_time = dt.datetime.now()
            insert_login_time = "UPDATE admins SET Login_Time = %s WHERE user_name = %s"
            cursor.execute(insert_login_time, (login_time, user_name))
            db_connection.commit()

        except pymysql.Error as error:
            print(f"Error updating login time for user {user_name}: {error}")

        finally:
            cursor.close()

    all_face_descriptors = get_all_face_descriptors(db_connection)

    if all_face_descriptors is None or len(all_face_descriptors) == 0:
        print("Error: No face descriptors found in the database.")
        return

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

            match_found = False

            for user_name, reference_face_descriptor in all_face_descriptors.items():
                distance = np.linalg.norm(np.array(face_descriptor) - np.array(reference_face_descriptor))
                if distance < threshold:
                    match_found = True
                    s = ps.Sound("sound/Face_Login_Success.wav")
                    s.play(1)
                    s.wait()
                    cap.release()
                    cv2.destroyAllWindows()
                    set_login_time(user_name)
                    global admin_email
                    admin_email = get_admin_email()
                    print(admin_email)
                    print(f"Face recognized for user: {user_name}")
                    msg = ctm.CTkMessagebox(master=login_page_frame, title="Authorization Successful", icon="info", option_1="ok",
                                message="Welcome Back sir! You have logged in Successfully!")
                    if msg.get() == "ok":
                        app.iconify()
                        mm.main_menu(app)
                    break

            if not match_found:
                s = ps.Sound("sound/Face_Login_Unsuccess.wav")
                s.play(1)
                s.wait()
                save_image ="unauthorized_persons/unauthorized_person_login.jpg"
                cv2.imwrite(save_image, frame)
                emails = get_all_admins_email()
                send_unauthorized_alert(emails,frame)
                msg = ctm.CTkMessagebox(master=login_page_frame,title="Warning Message!!!!", message="Unknown Face Detected",
                                icon="warning", option_1="Cancel")
                if msg.get == 'Cancel':
                    exit()
                break

        cv2.imshow("Face Login Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    db_connection.close()