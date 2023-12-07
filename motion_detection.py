import cv2, os
import time as t
import authenticate_user as au
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from sendgrid import SendGridAPIClient
import base64
import customtkinter as ct
from PIL import Image, ImageTk
from tkinter import PhotoImage
import CTkMessagebox as ctm


def motion_detection(main,frame2):
    mssg = ctm.CTkMessagebox(master=frame2,message="Select Your Smart WebCam Preference for Face Login",
                                icon="info", option_1="IP WebCam", option_2="External WebCam",
                                option_3="Internal Built-in WebCam", 
                                title="Choose Your WebCam")
    
    if mssg.get() == "Internal Built-in WebCam":
        global cap
        cap = cv2.VideoCapture(0)
        main_motion_detection()

    elif mssg.get() == "External WebCam":
        cap = cv2.VideoCapture(1)
        main_motion_detection()

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
            main_motion_detection()

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

def main_motion_detection():

    previous_frame = None
    motion_detected = False
    frame_counter = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if previous_frame is not None:
            frame_diff = cv2.absdiff(previous_frame, gray)

            _, thresholded = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) > 1000:
                    if not motion_detected:
                        send_email_with_image(frame)
                        motion_detected = True

                    frame_counter += 1
                    timerecord = int(t.time())
                    cv2.imwrite(f"MotionDetectedImages/ObjectDetected_{timerecord}_{frame_counter}.jpg", frame)
                    print(f"Motion detected - Image {frame_counter} captured")

        previous_frame = gray

        cv2.imshow("Motion Detection", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()



def send_email_with_image(frame):
    message = Mail(
        from_email='thesmartwebcam@gmail.com',
        to_emails=au.admin_email,
        subject='Alert!!!',
        html_content="<strong>Alert: Object in motion Has been Detected</strong>"
    )

    cv2.imwrite("MotionDetectedImages/MotionDetection.jpg", frame)

    with open("MotionDetectedImages/MotionDetection.jpg", "rb") as img_file:
        image_data = base64.b64encode(img_file.read()).decode()
        attached_image = Attachment(
            FileContent(image_data),
            FileName("MotionDetectedImages/MotionDetection.jpg"),
            FileType("image/jpeg"),
            Disposition("attachment")
        )
        message.attachment = attached_image

    sg = SendGridAPIClient("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")
    sg.send(message)
    print("Success: Email sent with the Motion Image.")

if __name__ == "__main__":
    motion_detection()