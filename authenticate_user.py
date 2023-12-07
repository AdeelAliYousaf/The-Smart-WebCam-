import pymysql
import CTkMessagebox as ctm
import datetime as dt
import playsoundsimple as ps
import main_menu as mm
import customtkinter as ct

def get_admins_email():
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


def authenticate_user(e1,e2,login_page_frame,app):
    global admin_email
    
    try:
        connection =  pymysql.connect(
            host="b5ssdpfo1apmaws80bj2-mysql.services.clever-cloud.com",
            user="us8lp5vzmmgtsk21",
            password="aXbXSnv9cOrGinhehHLe",
            database="b5ssdpfo1apmaws80bj2"
        )
        cursor = connection.cursor()

        global user_name
        user_name = e1.get()
        password = e2.get()
        Login_Time = dt.datetime.now()

        sql = "SELECT * FROM admins WHERE user_name = %s AND password = %s"
        insert_logintime = "UPDATE admins SET Login_Time = %s WHERE user_name = %s"
        cursor.execute(sql, (user_name, password))
        results = cursor.fetchall()

        if results:
            cursor.execute(insert_logintime,(Login_Time,user_name))
            connection.commit()
            admin_email = get_admins_email()
            s = ps.Sound("sound/Login_success.wav")
            s.play(1)
            s.wait()

            msg = ctm.CTkMessagebox(master=login_page_frame, title="Authorization Successful", icon="info", option_1="ok",
                                message="Welcome Back sir! You have logged in Successfully!")
            if msg.get() == "ok":
                e1.delete(0, ct.END)
                e2.delete(0, ct.END)
                mm.main_menu(app)

        else:
            msg = ctm.CTkMessagebox(title="Warning Message!", message="Incorrect Credentials",
                                icon="warning", option_1="Cancel", option_2="Retry")

            s = ps.Sound("sound/Login_unsuccessful.wav")
            s.play(1)
            s.wait()

            if msg.get() == "Cancel":
                cursor.close()
            connection.close()

    except pymysql.Error as e:
        ctm.CTkMessagebox(master=app,title='Database Error', message=f"Database Error has been occured i.e.{e}",
                          icon='Warning',option1='Ok')

if __name__ == "__main__":
    authenticate_user()