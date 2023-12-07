import pymysql
import cv2
import dlib
import datetime as dt
import csv
import os
import numpy as np
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from sendgrid import SendGridAPIClient
import base64
import customtkinter as ct
from PIL import Image, ImageTk
from tkinter import PhotoImage
import CTkMessagebox as ctm
import face_login as fl
import authenticate_user as au

def attendance_System(main,frame2):
    global cap
    mssg = ctm.CTkMessagebox(master=frame2,message="Select Your Smart WebCam Preference for Face Login",
                                icon="info", option_1="IP WebCam", option_2="External WebCam",
                                option_3="Internal Built-in WebCam", 
                                title="Choose Your WebCam")
    
    if mssg.get() == "Internal Built-in WebCam":
        cap = cv2.VideoCapture(0)
        attendance_System_main()


    elif mssg.get() == "External WebCam":
        cap = cv2.VideoCapture(1)
        attendance_System_main()

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
            cap = cv2.VideoCapture(index_entry.get())
            attendance_System_main()

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

def attendance_System_main():
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
            cursor.execute("SELECT Rollno, face_descriptor FROM students")
            results = cursor.fetchall()

            face_descriptors = {}

            for result in results:
                user_name = result[0]
                face_descriptor_blob = result[1]

                if face_descriptor_blob is not None:
                    face_descriptor = np.frombuffer(face_descriptor_blob, dtype=np.float64)
                    face_descriptors[user_name] = face_descriptor
                else:
                    print(f"Warning: No face descriptor found")

            return face_descriptors

        except pymysql.Error as error:
            print(f"Error retrieving face descriptors: {error}")

        finally:
            cursor.close()

        return None

    global logged_students
    logged_students = set()

    def log_attendance_to_csv(student_id):
        try:
            global logged_students
            csv_path = 'attendance.csv'

            if student_id in logged_students:
                print(f"Attendance already logged for student {student_id}")
                return

            timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(csv_path, mode='a', newline='') as csvfile:
                fieldnames = ['Roll no.','Name' ,'Class', 'Attendance', 'Attendance Time']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()

                student_name, student_class = get_student_info_from_id(student_id)
                
                if student_name is not None and student_class is not None:
                    writer.writerow({'Roll no.': student_id, 'Name': student_name, 'Class': student_class, 'Attendance': "Present", 'Attendance Time': timestamp})
                    logged_students.add(student_id)
                    print(f"Attendance logged for student {student_name}, Rollno. {student_id}, Class: {student_class}")
                else:
                    print(f"Warning: No face descriptor found for student {student_id}")

        except Exception as error:
            print(f"Error logging attendance to CSV for student {student_id}: {error}")

    def get_student_info_from_id(student_id):
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT Name, Class FROM students WHERE Rollno = %s", (student_id,))
            result = cursor.fetchone()

            if result:
                student_name, student_class = result
                return student_name, student_class
            else:
                print(f"Error: No student found with Rollno. {student_id}")
                return None, None

        except pymysql.Error as error:
            print(f"Error retrieving student info: {error}")

        finally:
            cursor.close()

        return None, None


    global file_path
    file_path = 'attendance.csv'

    def send_email_with_attachment(file_path):
        try:

            api_key = "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"

            sender_email = 'thesmartwebcam@gmail.com'
            email = fl.get_admin_email()
            recipient_email = email

            subject = 'Attendance Report'
            body = 'Please find the attached attendance report.'

            message = Mail(
                from_email=sender_email,
                to_emails=recipient_email,
                subject=subject,
                html_content=body
            )

            with open(file_path, 'rb') as file:
                file_data = file.read()
                file_name = os.path.basename(file_path)
                file_data_base64 = base64.b64encode(file_data).decode('utf-8')

                attachment = Attachment(
                    FileContent(file_data_base64),
                    FileName(file_name),
                    FileType('text/csv'),
                    Disposition('attachment')
                )
                message.attachment = attachment

            sg = SendGridAPIClient(api_key)
            response = sg.send(message)

            print(f"Email sent! via face login")

        except Exception as error:
            try:
                api_key = "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"

                sender_email = 'thesmartwebcam@gmail.com'
                email = au.get_admins_email()
                recipient_email = email

                subject = 'Attendance Report'
                body = 'Please find the attached attendance report.'

                message = Mail(
                    from_email=sender_email,
                    to_emails=recipient_email,
                    subject=subject,
                    html_content=body
                )

                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    file_name = os.path.basename(file_path)
                    file_data_base64 = base64.b64encode(file_data).decode('utf-8')

                    attachment = Attachment(
                        FileContent(file_data_base64),
                        FileName(file_name),
                        FileType('text/csv'),
                        Disposition('attachment')
                    )
                    message.attachment = attachment

                sg = SendGridAPIClient(api_key)
                response = sg.send(message)

                print(f"Email sent! via typing authentication!")
            except Exception as error:
                print('Error sending email:',error)
            

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

        for i, face in enumerate(faces):
            landmarks = dlib.shape_predictor('Face_Read_Models/shape_predictor_68_face_landmarks.dat')(frame, face)
            face_chip = dlib.get_face_chip(frame, landmarks)
            face_descriptor = face_recognizer.compute_face_descriptor(face_chip)

            match_found = False

            for user_name, reference_face_descriptor in all_face_descriptors.items():
                distance = np.linalg.norm(np.array(face_descriptor) - np.array(reference_face_descriptor))
                if distance < threshold:
                    match_found = True
                    x, y, w, h = face.left(), face.top(), face.width(), face.height()
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    roll_number = user_name

                    cv2.putText(frame, f"Roll No: {roll_number}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    print(f"Face recognized for user: {user_name}")
                    log_attendance_to_csv(user_name)
                    break

            if not match_found:
                save_image = "unauthorized_persons/unauthorized_student.jpg"
                cv2.imwrite(save_image, frame)
                print("No matching face found in the database.")

        cv2.imshow("Face Login Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            
            break

    cap.release()
    cv2.destroyAllWindows()
    db_connection.close()