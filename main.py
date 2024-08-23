import re
import datetime
import math
import mysql.connector
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivy.clock import Clock

Window.size = (310, 580)

mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Waj#ivm<>yp%",
            database="railway_management_system"
)
c = mydb.cursor()

class ScreenManager(ScreenManager):
    screen_manager = ObjectProperty()
class Example(MDApp):
    dialog = None
    view = ModalView()
    view.dismiss(force=True)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.regex = r'\b[A-Za-z0-9.%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.screen = Builder.load_file("back.kv")
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light"
        return self.screen
    def login_fun(self, email, password):
        self.email=email
        self.password=password

        try:

            query = "SELECT * FROM user WHERE email = %s AND user_password = %s"
            c.execute(query, (email, password))
            user = c.fetchone()

            if user:
                print("Login successful")

                Clock.schedule_once(self.change_to_main_screen,45)
                self.root.screen_manager.current="main"

            else:
                print("Invalid credentials")
                self.root.ids.showmsg.text="Inavild credentials"

        except mysql.connector.Error as er:
            print(f"Error: {er}")
        finally:
            if 'connection' in locals():
                con.close()

    def change_to_main_screen(self,dt):
        self.root.screen_manager.current = 'main'

    def change_screen_to_main(self):
        self.root.screen_manager.current = "main"


    def send_data(self):
        email = self.root.ids.lemail.text
        password = self.root.ids.lpassword.text
        user_id = self.root.ids.user_id.text  # Assuming user_id is a TextInput widget
        self.phone_number = self.root.ids.phone_number.text
        self.root.ids.createfn.text="Succesfully created ur account now go to\n to login to continue"
        c.execute("insert into user(email,user_password,user_id,phone_no) values(%s,%s,%s,%s)",(email, password, user_id, self.phone_number))
        mydb.commit()

    def receive_data(self, email, password):
        c.execute("select * from user")
        email_list = []
        for i in c.fetchall():
            email_list.append(i[0])
        if email.text in email_list and email.text != "":
            c.execute(f"select user_password from user where email='{email.text}'")
            for j in c:
                if password.text == j[0]:
                    print("You have successfully LoggedIn! ")
                else:
                    print("Incorrect Password")
        else:
            print("Incorrect Email")
    def login_button_pressed(self):
        email = self.root.ids.email.text
        password = self.root.ids.password.text
        self.login_fun(email, password)
    def booking_details(self):
        self.root.ids.From_Book.text=str(self.station_code[0][0]) + '                                    '+ str(self.station_code[1][0]) + '\n' + str(self.depart_traine)+' | '+str(self.xyz) + "                       "+ str(self.arrive_traine) + ' | '+str(self.xyz)
        self.root.ids.uEmail.text=self.email
        c.execute("select phone_no from user where email=%s",(self.email,))
        self.ph=c.fetchall()
        self.root.ids.umobile_no.text=str(self.ph[0][0])
    def passenger(self):
        c.execute(" select max(pasenger_id) from passenger_details")
        Pass_id = c.fetchall()
        Pass_id_insert = Pass_id[0][0]
        Pass_id_insert = Pass_id_insert + 1
        print(type(Pass_id_insert))
        c.execute(" select max(pnr_no) from ticket")
        pnr=c.fetchall()
        self.pnr_insert=pnr[0][0]
        self.pnr_insert=self.pnr_insert+1
        c.execute(" select max(booking_id) from booking")
        booking_id = c.fetchall()
        self.booking_id_insert=booking_id[0][0]
        self.booking_id_insert=self.booking_id_insert+1
        c.execute("select max(ticket_id) from ticket")
        ticket_id=c.fetchall()
        self.ticket_id_insert=ticket_id[0][0]
        self.ticket_id_insert=self.ticket_id_insert+1
        if self.Cls_type=='general':
            seat_nogm = self.seatn_nog / 30
            sg=math.ceil(self.seatn_nog)
            divg = math.ceil(seat_nogm)
            self.coach_nom='D'+str(divg)
            self.avl_seat=divg*30-(sg-1)
            print(self.coach_nom)
            print(self.avl_seat)
        if self.Cls_type=='sl':
            seat_noslm = self.seatn_nosl / 24
            ssl=math.ceil(self.seatn_nosl)
            divsl = math.ceil(seat_noslm)
            self.coach_nom='s'+str(divsl)
            self.avl_seat=divsl*24-(ssl-1)
        if self.Cls_type=='3a':
            seat_no3am = self.seatn_no3a / 24
            s3a=math.ceil(self.seatn_no3a)
            div3a = math.ceil(seat_no3am)
            self.coach_nom='B'+str(div3a)
            self.avl_seat=div3a*24-(s3a-1)
        if self.Cls_type=='2a':
            seat_no2am = self.seatn_no2a / 16
            s2a=math.ceil(self.seatn_no2a)
            div2a = math.ceil(seat_no2am)
            self.coach_nom='A'+str(div2a)
            self.avl_seat=div2a*16-(seat_no2am-1)
        if self.Cls_type=='1a':
            seat_no1am = self.seatn_no1a / 8
            s1a=math.ceil(self.seatn_no1a)
            div1a = math.ceil(seat_no1am)
            self.coach_nom='H'+str(div1a)
            self.avl_seat=div1a*8-(seat_no1am-1)
        psql = "insert into passenger_details(pasenger_id,passenger_name,age,gender,coach_no,seat_no) values(%s,%s,%s,%s,%s,%s)"
        values = (Pass_id_insert, self.root.ids.pname.text, int(self.root.ids.p_age.text), self.gender, self.coach_nom,self.avl_seat)
        c.execute(psql, values)
        c.execute("insert into booking (booking_id,train_no,p_source,p_destination,fare,booking_date,schedule_arrival,schedule_departure,Journey_date,passenger_no,user_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.booking_id_insert, self.tNuM, self.From, self.To, self.farec, self.todt, self.arrive_traine,self.depart_traine, self.dt, Pass_id_insert,self.email))
        t2 = "insert into ticket(ticket_id,pnr_no,train_no,train_name,booking_date,class_type,coach_no,age,gender,p_name,seat_no,journey_date, source,schedule_dept,destination,schedule_arrive,phone_no) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        t2value = (self.ticket_id_insert, self.pnr_insert, self.tNuM, self.var, self.todt, self.Cls_type, self.coach_nom,int(self.root.ids.p_age.text),self.gender,self.root.ids.pname.text,self.avl_seat,self.dt,self.From,self.depart_traine,self.To,self.arrive_traine,str(self.ph[0][0]))
        c.execute(t2, t2value)
        mydb.commit()
    def cancelling(self):
        c.execute("delete from ticket where pnr_no=%s",(self.root.ids.pnr_cancel.text,))
        c.execute("select max(cancel_id) from cancel;")
        t=c.fetchall()
        top=t[0][0]
        top=top+1
        c.execute("insert into cancel values(%s,'2024-01-31',%s,%s)",(top,self.root.ids.reason.text,int(self.root.ids.pnr_cancel.text)))
        c.execute("delete from ticket where pnr_no=%s",(self.root.ids.pnr_cancel.text,))
        mydb.commit()

    def hogayapay(self):
        c.execute('select fare from booking where booking_id=%s',(self.booking_id_insert,))
        t=c.fetchall()
        fare=t[0][0]
        c.execute("select max(transaction_id) from payment;")
        t=c.fetchall()
        top=t[0][0]
        top=top+1
        acc=int(self.root.ids.acc_num.text)
        bank=self.root.ids.bank_name.text
        name=self.root.ids.acc_hold_name.text
        c.execute("insert into payment values(%s,%s,'2024-01-31',%s,%s,%s,%s)",(top,self.booking_id_insert,fare,acc,bank,name,))
        c.execute("update ticket set transaction_id=%s where ticket_id =%s",(top,self.ticket_id_insert))
        mydb.commit()
    def loged(self):
        if self.root.ids.username.text =='admin' and self.root.ids.pass2.text=='123':
            self.root.ids.appwaala.disabled=False
        else:
            self.root.ids.appwaala.disabled=True
    def showticket(self):
        self.Pnrsearch=None
        if self.root.ids.flat.text.strip():  # strip() removes leading/trailing whitespaces
            try:
                self.Pnrsearch = int(self.root.ids.flat.text)
            except ValueError:
                # Handle the case where the input cannot be converted to an integer
                print("Invalid input: Not a valid integer")
        else:
            print("Input is empty")
        if self.Pnrsearch is not None:

            c.execute("select pnr_no from ticket where pnr_no=%s",(self.Pnrsearch,))
            ticket_id=c.fetchall()
            self.root.ids.PNR_no.text='PNR No:'+str(ticket_id[0][0])
            c.execute("select train_no,train_name from ticket where pnr_no=%s",(self.Pnrsearch,))
            tran_no_name=c.fetchall()
            self.root.ids.train_no_name.text='Train No/:  '+str(tran_no_name[0][0])+"\nTrain Name  "+str(tran_no_name[0][1])
            c.execute("select booking_date from ticket where pnr_no=%s",(self.Pnrsearch,))
            booking_date=c.fetchall()
            self.root.ids.date_book.text='Booking date'+str(booking_date[0][0])
            c.execute("select class_type from ticket where pnr_no=%s",(self.Pnrsearch,))
            class_type=c.fetchall()
            self.root.ids.classt.text='Class: '+str(class_type[0][0])
            c.execute("select transaction_id from ticket where pnr_no=%s",(self.Pnrsearch,))
            trans_id=c.fetchall()
            self.root.ids.trans_id.text='Transaction ID: '+str(trans_id[0][0])
            c.execute("select journey_date from ticket where pnr_no=%s", (self.Pnrsearch,))
            jour_date = c.fetchall()
            self.root.ids.date_journey.text = 'Date of\nJourney: ' + str(jour_date[0][0])
            self.root.ids.date_b.text = 'Date of\nBoarding: ' + str(jour_date[0][0])
            c.execute("select source from ticket where pnr_no=%s", (self.Pnrsearch,))
            board_at = c.fetchall()
            self.root.ids.boarding.text = 'Boarding at: ' + str(board_at[0][0])
            c.execute("select schedule_dept from ticket where pnr_no=%s", (self.Pnrsearch,))
            schedule_dept = c.fetchall()
            self.root.ids.schedule_depart.text = 'Schedule\ndeparture: ' + str(schedule_dept[0][0])
            c.execute("select destination from ticket where pnr_no=%s", (self.Pnrsearch,))
            res_utp = c.fetchall()
            self.root.ids.Res_upto.text = 'Reservation upto: ' + str(res_utp[0][0])
            c.execute("select schedule_arrive from ticket where pnr_no=%s", (self.Pnrsearch,))
            svh_arrive = c.fetchall()
            self.root.ids.schedule_arrive.text = 'Schedule\narrival: ' + str(svh_arrive[0][0])
            c.execute("select phone_no from ticket where pnr_no=%s", (self.Pnrsearch,))
            pno1= c.fetchall()
            self.root.ids.pn0.text = 'Phone number: ' + str(pno1[0][0])
            c.execute("select p_name from ticket where pnr_no=%s",(self.Pnrsearch,))
            pppname=c.fetchall()
            self.root.ids.pppname.text="Name: "+str(pppname[0][0])
            c.execute("select age from ticket where pnr_no=%s",(self.Pnrsearch,))
            pppage=c.fetchall()
            self.root.ids.pppage.text="Age: "+str(pppage[0][0])
            c.execute("select gender from ticket where pnr_no=%s",(self.Pnrsearch,))
            pppgender=c.fetchall()
            self.root.ids.pppgender.text="Gender: "+str(pppgender[0][0])
            c.execute("select coach_no from ticket where pnr_no=%s",(self.Pnrsearch,))
            pppcoach=c.fetchall()
            self.root.ids.pppcoach.text="Coach: "+str(pppcoach[0][0])
            c.execute("select seat_no from ticket where pnr_no=%s",(self.Pnrsearch,))
            pppseat=c.fetchall()
            self.root.ids.pppseatno.text="Seat No: "+str(pppseat[0][0])

    def male(self):
        self.gender='Male'
    def female(self):
        self.gender='Female'
    def other(self):
        self.gender='Other'

    def from_pressed(self):
        c.execute("select distinct station_name from station")
        myresult = c.fetchall()
        self.root.ids.from1.text=str(myresult[0][0])
        self.root.ids.from2.text=str(myresult[1][0])
        self.root.ids.from3.text = str(myresult[2][0])
        self.root.ids.from4.text = str(myresult[3][0])
        self.root.ids.from5.text = str(myresult[4][0])
        self.root.ids.from6.text = str(myresult[5][0])
        self.root.ids.from7.text = str(myresult[6][0])
        self.root.ids.from8.text = str(myresult[7][0])
        self.root.ids.from9.text = str(myresult[8][0])
        self.root.ids.from10.text = str(myresult[9][0])
        self.root.ids.from11.text = str(myresult[10][0])
        self.root.ids.from12.text = str(myresult[11][0])
        self.root.ids.from13.text = str(myresult[12][0])
        self.root.ids.from14.text = str(myresult[13][0])
        self.root.ids.from15.text = str(myresult[14][0])
        self.root.ids.from16.text = str(myresult[15][0])
        self.root.ids.from17.text = str(myresult[16][0])
        self.root.ids.from18.text = str(myresult[17][0])
        self.root.ids.from19.text = str(myresult[18][0])
        self.root.ids.from20.text = str(myresult[19][0])
        self.root.ids.from21.text = str(myresult[20][0])
        self.root.ids.from22.text = str(myresult[21][0])
        self.root.ids.from23.text = str(myresult[22][0])
        self.root.ids.from24.text = str(myresult[23][0])
        self.root.ids.from25.text = str(myresult[24][0])
        self.root.ids.from26.text = str(myresult[25][0])
        self.root.ids.from27.text = str(myresult[26][0])
        self.root.ids.from28.text = str(myresult[27][0])

    def to_pressed(self):
        c.execute("select distinct station_name from station")
        myresult = c.fetchall()
        self.root.ids.to1.text=str(myresult[0][0])
        self.root.ids.to2.text=str(myresult[1][0])
        self.root.ids.to3.text = str(myresult[2][0])
        self.root.ids.to4.text = str(myresult[3][0])
        self.root.ids.to5.text = str(myresult[4][0])
        self.root.ids.to6.text = str(myresult[5][0])
        self.root.ids.to7.text = str(myresult[6][0])
        self.root.ids.to8.text = str(myresult[7][0])
        self.root.ids.to9.text = str(myresult[8][0])
        self.root.ids.to10.text = str(myresult[9][0])
        self.root.ids.to11.text = str(myresult[10][0])
        self.root.ids.to12.text = str(myresult[11][0])
        self.root.ids.to13.text = str(myresult[12][0])
        self.root.ids.to14.text = str(myresult[13][0])
        self.root.ids.to15.text = str(myresult[14][0])
        self.root.ids.to16.text = str(myresult[15][0])
        self.root.ids.to17.text = str(myresult[16][0])
        self.root.ids.to18.text = str(myresult[17][0])
        self.root.ids.to19.text = str(myresult[18][0])
        self.root.ids.to20.text = str(myresult[19][0])
        self.root.ids.to21.text = str(myresult[20][0])
        self.root.ids.to22.text = str(myresult[21][0])
        self.root.ids.to23.text = str(myresult[22][0])
        self.root.ids.to24.text = str(myresult[23][0])
        self.root.ids.to25.text = str(myresult[24][0])
        self.root.ids.to26.text = str(myresult[25][0])
        self.root.ids.to27.text = str(myresult[26][0])
        self.root.ids.to28.text = str(myresult[27][0])

    def release1(self):
        self.root.ids.From.text=self.root.ids.from1.text
        self.From='BAY'
        self.xf=1
    def release2(self):
        self.root.ids.From.text = self.root.ids.from2.text
        self.From=' BDVT'
        self.xf = 2
    def release3(self):
        self.root.ids.From.text = self.root.ids.from3.text
        self.From= 'CMGR'
        self.xf = 3
    def release4(self):
        self.root.ids.From.text = self.root.ids.from4.text
        self.From='CMR'
        self.xf = 4
    def release5(self):
        self.root.ids.From.text = self.root.ids.from5.text
        self.From = 'CPT'
        self.xf = 5

    def release6(self):
        self.root.ids.From.text = self.root.ids.from6.text
        self.From = 'DBU'
        self.xf = 6

    def release7(self):
        self.root.ids.From.text = self.root.ids.from7.text
        self.From = 'DMM'
        self.xf = 7

    def release8(self):
        self.root.ids.From.text = self.root.ids.from8.text
        self.From = 'GBD'
        self.xf = 8

    def release9(self):
        self.root.ids.From.text = self.root.ids.from9.text
        self.From = 'GDG'
        self.xf = 9

    def release10(self):
        self.root.ids.From.text = self.root.ids.from10.text
        self.From = 'HAS'
        self.xf = 10

    def release11(self):
        self.root.ids.From.text = self.root.ids.from11.text
        self.From = 'HPT'
        self.xf = 11

    def release12(self):
        self.root.ids.From.text = self.root.ids.from12.text
        self.From = 'HVR'
        self.xf = 12

    def release13(self):
        self.root.ids.From.text = self.root.ids.from13.text
        self.From = 'KGI'
        self.xf = 13

    def release14(self):
        self.root.ids.From.text = self.root.ids.from14.text
        self.From = 'MAD'
        self.xf = 14

    def release15(self):
        self.root.ids.From.text = self.root.ids.from15.text
        self.From = 'MAJN'
        self.xf = 15

    def release16(self):
        self.root.ids.From.text = self.root.ids.from16.text
        self.From = 'MYA'
        self.xf = 16

    def release17(self):
        self.root.ids.From.text = self.root.ids.from17.text
        self.From = 'MYS'
        self.xf = 17

    def release18(self):
        self.root.ids.From.text = self.root.ids.from18.text
        self.From = 'NMGA'
        self.xf = 18

    def release19(self):
        self.root.ids.From.text = self.root.ids.from19.text
        self.From = 'NTW'
        self.xf = 19

    def release20(self):
        self.root.ids.From.text = self.root.ids.from20.text
        self.From = 'PANP'
        self.xf = 20
    def release21(self):
        self.root.ids.From.text = self.root.ids.from21.text
        self.From='RNR'
        self.xf = 21
    def release22(self):
        self.root.ids.From.text = self.root.ids.from22.text
        self.From='SBC'
        self.xf = 22
    def release23(self):
        self.root.ids.From.text = self.root.ids.from23.text
        self.From='SKLR'
        self.xf = 23
    def release24(self):
        self.root.ids.From.text = self.root.ids.from24.text
        self.From='SME'
        self.xf = 24
    def release25(self):
        self.root.ids.From.text = self.root.ids.from25.text
        self.From='TK'
        self.xf = 25
    def release26(self):
        self.root.ids.From.text = self.root.ids.from26.text
        self.From='UBL'
        self.xf = 26
    def release27(self):
        self.root.ids.From.text = self.root.ids.from27.text
        self.From='YNK'
        self.xf = 27
    def release28(self):
        self.root.ids.From.text = self.root.ids.from28.text
        self.From='YPR'
        self.xf = 28

    def to1(self):
        self.root.ids.To.text = self.root.ids.to1.text
        self.To = 'BAY'
        self.yt=1

    def to2(self):
        self.root.ids.To.text = self.root.ids.to2.text
        self.To = 'BDVT'
        self.yt = 2

    def to3(self):
        self.root.ids.To.text = self.root.ids.to3.text
        self.To = 'CMGR'
        self.yt = 3

    def to4(self):
        self.root.ids.To.text = self.root.ids.to4.text
        self.To = 'CMR'
        self.yt = 4

    def to5(self):
        self.root.ids.To.text = self.root.ids.to5.text
        self.To = 'CPT'
        self.yt = 5

    def to6(self):
        self.root.ids.To.text = self.root.ids.to6.text
        self.To = 'DBU'
        self.yt = 6

    def to7(self):
        self.root.ids.To.text = self.root.ids.to7.text
        self.To = 'DMM'
        self.yt = 7

    def to8(self):
        self.root.ids.To.text = self.root.ids.to8.text
        self.To = 'GBD'
        self.yt = 8

    def to9(self):
        self.root.ids.To.text = self.root.ids.to9.text
        self.To = 'GDG'
        self.yt = 9

    def to10(self):
        self.root.ids.To.text = self.root.ids.to10.text
        self.To = 'HAS'
        self.yt = 10

    def to11(self):
        self.root.ids.To.text = self.root.ids.to11.text
        self.To = 'HPT'
        self.yt = 11

    def to12(self):
        self.root.ids.To.text = self.root.ids.to12.text
        self.To = 'HVR'
        self.yt = 12

    def to13(self):
        self.root.ids.To.text = self.root.ids.to13.text
        self.To = 'KGI'
        self.yt = 13

    def to14(self):
        self.root.ids.To.text = self.root.ids.to14.text
        self.To = 'MAD'
        self.yt = 14

    def to15(self):
        self.root.ids.To.text = self.root.ids.to15.text
        self.To = 'MAJN'
        self.yt = 15

    def to16(self):
        self.root.ids.To.text = self.root.ids.to16.text
        self.To = 'MYA'
        self.yt = 16

    def to17(self):
        self.root.ids.To.text = self.root.ids.to17.text
        self.To = 'MYS'
        self.yt = 17

    def to18(self):
        self.root.ids.To.text = self.root.ids.to18.text
        self.To = 'NMGA'
        self.yt = 18

    def to19(self):
        self.root.ids.To.text = self.root.ids.to19.text
        self.To = 'NTW'
        self.yt = 19

    def to20(self):
        self.root.ids.To.text = self.root.ids.to20.text
        self.To = 'PANP'
        self.yt = 20

    def to21(self):
        self.root.ids.To.text = self.root.ids.to21.text
        self.To='RNR'
        self.yt = 21
    def to22(self):
        self.root.ids.To.text = self.root.ids.to22.text
        self.To='SBC'
        self.yt = 22
    def to23(self):
        self.root.ids.To.text = self.root.ids.to23.text
        self.To='SKLR'
        self.yt = 23
    def to24(self):
        self.root.ids.To.text = self.root.ids.to24.text
        self.To='SME'
        self.yt = 24

    def to25(self):
        self.root.ids.To.text = self.root.ids.to25.text
        self.To='TK'
        self.yt = 25
    def to26(self):
        self.root.ids.To.text = self.root.ids.to26.text
        self.To='UBL'
        self.yt = 26
    def to27(self):
        self.root.ids.To.text = self.root.ids.to27.text
        self.To='YNK'
        self.yt = 27
    def to28(self):
        self.root.ids.To.text = self.root.ids.to28.text
        self.To='YPR'
        self.yt = 28


    def on_save(self, instance, value, date_range):
        self.todt=datetime.date.today()
        self.dt=value
        self.xyz=self.dt.strftime('%A')
        print(self.dt.strftime('%A'))
    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def count1(self, count_list):
        if count_list[0] == 1:
            self.root.ids.c1.disabled = False
            self.root.ids.c1.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[0][0])
            self.root.ids.c1.line_color = self.theme_cls.primary_color
        elif count_list[0] == 2:
            self.root.ids.c1.disabled = False
            self.root.ids.c1.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[0][0])
            self.root.ids.c1.line_color = "purple"
            self.root.ids.c2.disabled = False
            self.root.ids.c2.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[0][1])
            self.root.ids.c2.line_color = self.theme_cls.primary_color
        elif count_list[0] == 3:
            self.root.ids.c1.disabled = False
            self.root.ids.c1.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[0][0])
            self.root.ids.c1.line_color = self.theme_cls.primary_color
            self.root.ids.c2.disabled = False
            self.root.ids.c2.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[0][1])
            self.root.ids.c2.disabled = False
            self.root.ids.c3.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[0][2])
            self.root.ids.c3.line_color = self.theme_cls.primary_color
        elif count_list[0] == 4:
            self.root.ids.c1.disabled = False
            self.root.ids.c1.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[0][0])
            self.root.ids.c1.line_color = self.theme_cls.primary_color
            self.root.ids.c2.disabled = False
            self.root.ids.c2.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[0][1])
            self.root.ids.c2.line_color = self.theme_cls.primary_color
            self.root.ids.c3.disabled = False
            self.root.ids.c3.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[0][2])
            self.root.ids.c3.line_color = self.theme_cls.primary_color
            self.root.ids.c4.disabled = False
            self.root.ids.c4.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[0][3])
            self.root.ids.c4.line_color = self.theme_cls.primary_color
        elif count_list[0] == 5:
            self.root.ids.c1.disabled = False
            self.root.ids.c1.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[0][0])
            self.root.ids.c1.line_color = self.theme_cls.primary_color
            self.root.ids.c2.disabled = False
            self.root.ids.c2.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[0][1])
            self.root.ids.c2.line_color = self.theme_cls.primary_color
            self.root.ids.c3.disabled = False
            self.root.ids.c3.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[0][2])
            self.root.ids.c3.line_color = self.theme_cls.primary_color
            self.root.ids.c4.disabled = False
            self.root.ids.c4.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[0][3])
            self.root.ids.c4.line_color = self.theme_cls.primary_color
            self.root.ids.c5.disabled = False
            self.root.ids.c5.text = '1A . ₹' + str(self.fare1a) + '\nAVL' + str(self.res[0][4])
            self.root.ids.c5.line_color = self.theme_cls.primary_color

    def count2(self, count_list):
        self.count1(count_list)
        if count_list[1] == 1:
            self.root.ids.c12.disabled = False
            self.root.ids.c12.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[1][0])
            self.root.ids.c12.line_color = self.theme_cls.primary_color
        elif count_list[1] == 2:
            self.root.ids.c12.disabled = False
            self.root.ids.c12.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[1][0])
            self.root.ids.c12.line_color = self.theme_cls.primary_color
            self.root.ids.c22.disabled = False
            self.root.ids.c22.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[1][1])
            self.root.ids.c22.line_color = self.theme_cls.primary_color
        elif count_list[1] == 3:
            self.root.ids.c12.disabled = False
            self.root.ids.c12.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[1][0])
            self.root.ids.c12.line_color = self.theme_cls.primary_color
            self.root.ids.c22.disabled = False
            self.root.ids.c22.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[1][1])
            self.root.ids.c22.line_color = self.theme_cls.primary_color
            self.root.ids.c32.disabled = False
            self.root.ids.c32.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[1][2])
            self.root.ids.c32.line_color = self.theme_cls.primary_color
        elif count_list[1] == 4:
            self.root.ids.c12.disabled = False
            self.root.ids.c12.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[1][0])
            self.root.ids.c12.line_color = self.theme_cls.primary_color
            self.root.ids.c22.disabled = False
            self.root.ids.c22.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[1][1])
            self.root.ids.c22.line_color = self.theme_cls.primary_color
            self.root.ids.c32.disabled = False
            self.root.ids.c32.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[1][2])
            self.root.ids.c32.line_color = self.theme_cls.primary_color
            self.root.ids.c42.disabled = False
            self.root.ids.c42.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[1][2])
            self.root.ids.c42.line_color = self.theme_cls.primary_color
        elif count_list[1] == 5:
            self.root.ids.c12.disabled = False
            self.root.ids.c12.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[1][0])
            self.root.ids.c12.line_color = self.theme_cls.primary_color
            self.root.ids.c22.disabled = False
            self.root.ids.c22.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[1][1])
            self.root.ids.c22.line_color = self.theme_cls.primary_color
            self.root.ids.c32.disabled = False
            self.root.ids.c32.text = '3A .  ₹' + str(self.fare3a) + '\nAVL' + str(self.res[1][2])
            self.root.ids.c32.line_color = self.theme_cls.primary_color
            self.root.ids.c42.disabled = False
            self.root.ids.c42.text = '2A .  ₹' + str(self.fare2a) + '\nAVL' + str(self.res[1][2])
            self.root.ids.c42.line_color = self.theme_cls.primary_color
            self.root.ids.c52.disabled = False
            self.root.ids.c52.text = '1A .  ₹' + str(self.fare1a) + '\nAVL' + str(self.res[1][3])
            self.root.ids.c52.line_color = self.theme_cls.primary_color

    def count3(self, count_list):
        self.count2(count_list)
        if count_list[2] == 1:
            self.root.ids.c13.disabled = False
            self.root.ids.c13.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[2][0])
            self.root.ids.c13.line_color = self.theme_cls.primary_color
        elif count_list[2] == 2:
            self.root.ids.c13.disabled = False
            self.root.ids.c13.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[2][0])
            self.root.ids.c13.line_color = self.theme_cls.primary_color
            self.root.ids.c23.disabled = False
            self.root.ids.c23.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[2][1])
            self.root.ids.c23.line_color = self.theme_cls.primary_color
        elif count_list[2] == 3:
            self.root.ids.c13.disabled = False
            self.root.ids.c13.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[2][0])
            self.root.ids.c13.line_color = self.theme_cls.primary_color
            self.root.ids.c23.disabled = False
            self.root.ids.c23.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[2][1])
            self.root.ids.c23.line_color = self.theme_cls.primary_color
            self.root.ids.c33.disabled = False
            self.root.ids.c33.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[2][2])
            self.root.ids.c3.line_color = self.theme_cls.primary_color
        elif count_list[2] == 4:
            self.root.ids.c13.disabled = False
            self.root.ids.c13.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[2][0])
            self.root.ids.c13.line_color = self.theme_cls.primary_color
            self.root.ids.c23.disabled = False
            self.root.ids.c23.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[2][1])
            self.root.ids.c23.line_color = self.theme_cls.primary_color
            self.root.ids.c33.disabled = False
            self.root.ids.c33.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[2][2])
            self.root.ids.c33.line_color = self.theme_cls.primary_color
            self.root.ids.c43.disabled = False
            self.root.ids.c43.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[2][3])
            self.root.ids.c43.line_color = self.theme_cls.primary_color
        elif count_list[2] == 5:
            self.root.ids.c13.disabled = False
            self.root.ids.c13.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[2][0])
            self.root.ids.c13.line_color = self.theme_cls.primary_color
            self.root.ids.c23.disabled = False
            self.root.ids.c23.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[2][1])
            self.root.ids.c23.line_color = self.theme_cls.primary_color
            self.root.ids.c33.disabled = False
            self.root.ids.c33.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[2][2])
            self.root.ids.c33.line_color = self.theme_cls.primary_color
            self.root.ids.c43.disabled = False
            self.root.ids.c43.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[2][3])
            self.root.ids.c43.line_color = self.theme_cls.primary_color
            self.root.ids.c53.disabled = False
            self.root.ids.c53.text = '1A . ₹' + str(self.fare1a) + '\nAVL' + str(self.res[2][4])
            self.root.ids.c53.line_color = self.theme_cls.primary_color

    def count4(self, count_list):
        self.count3(count_list)
        if count_list[3] == 1:
            self.root.ids.c14.disabled = False
            self.root.ids.c14.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[3][0])
            self.root.ids.c14.line_color = self.theme_cls.primary_color
        elif count_list[3] == 2:
            self.root.ids.c14.disabled = False
            self.root.ids.c14.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[3][0])
            self.root.ids.c14.line_color = self.theme_cls.primary_color
            self.root.ids.c24.disabled = False
            self.root.ids.c24.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[3][1])
            self.root.ids.c24.line_color = self.theme_cls.primary_color
        elif count_list[3] == 3:
            self.root.ids.c14.disabled = False
            self.root.ids.c14.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[3][0])
            self.root.ids.c14.line_color = self.theme_cls.primary_color
            self.root.ids.c24.disabled = False
            self.root.ids.c24.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[3][1])
            self.root.ids.c24.line_color = self.theme_cls.primary_color
            self.root.ids.c34.disabled = False
            self.root.ids.c34.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[3][2])
            self.root.ids.c34.line_color = self.theme_cls.primary_color
        elif count_list[3] == 4:
            self.root.ids.c14.disabled = False
            self.root.ids.c14.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[3][0])
            self.root.ids.c14.line_color = self.theme_cls.primary_color
            self.root.ids.c24.disabled = False
            self.root.ids.c24.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[3][1])
            self.root.ids.c24.line_color = self.theme_cls.primary_color
            self.root.ids.c34.disabled = False
            self.root.ids.c34.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[3][2])
            self.root.ids.c34.line_color = self.theme_cls.primary_color
            self.root.ids.c44.disabled = False
            self.root.ids.c44.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[3][3])
            self.root.ids.c44.line_color = self.theme_cls.primary_color
        elif count_list[3] == 5:
            self.root.ids.c14.disabled = False
            self.root.ids.c14.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[3][0])
            self.root.ids.c14.line_color = self.theme_cls.primary_color
            self.root.ids.c24.disabled = False
            self.root.ids.c24.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[3][1])
            self.root.ids.c24.line_color = self.theme_cls.primary_color
            self.root.ids.c34.disabled = False
            self.root.ids.c34.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[3][2])
            self.root.ids.c34.line_color = self.theme_cls.primary_color
            self.root.ids.c44.disabled = False
            self.root.ids.c44.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[3][3])
            self.root.ids.c44.line_color = self.theme_cls.primary_color
            self.root.ids.c54.disabled = False
            self.root.ids.c54.text = '1A . ₹' + str(self.fare1a) + '\nAVL' + str(self.res[3][4])
            self.root.ids.c54.line_color = self.theme_cls.primary_color

    def count5(self, count_list):
        self.count4(count_list)
        if count_list[4] == 1:
            self.root.ids.c15.disabled = False
            self.root.ids.c15.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[4][0])
            self.root.ids.c15.line_color = self.theme_cls.primary_color
        elif count_list[4] == 2:
            self.root.ids.c15.disabled = False
            self.root.ids.c15.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[4][0])
            self.root.ids.c15.line_color = self.theme_cls.primary_color
            self.root.ids.c25.disabled = False
            self.root.ids.c25.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[4][1])
            self.root.ids.c25.line_color = self.theme_cls.primary_color
        elif count_list[4] == 3:
            self.root.ids.c15.disabled = False
            self.root.ids.c15.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[4][0])
            self.root.ids.c15.line_color = self.theme_cls.primary_color
            self.root.ids.c25.disabled = False
            self.root.ids.c25.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[4][1])
            self.root.ids.c25.line_color = self.theme_cls.primary_color
            self.root.ids.c35.disabled = False
            self.root.ids.c35.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[4][2])
            self.root.ids.c35.line_color = self.theme_cls.primary_color
        elif count_list[4] == 4:
            self.root.ids.c15.disabled = False
            self.root.ids.c15.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[4][0])
            self.root.ids.c15.line_color = self.theme_cls.primary_color
            self.root.ids.c25.disabled = False
            self.root.ids.c25.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[4][1])
            self.root.ids.c25.line_color = self.theme_cls.primary_color
            self.root.ids.c35.disabled = False
            self.root.ids.c35.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[4][2])
            self.root.ids.c35.line_color = self.theme_cls.primary_color
            self.root.ids.c45.disabled = False
            self.root.ids.c45.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[4][3])
            self.root.ids.c45.line_color = self.theme_cls.primary_color
        elif count_list[4] == 5:
            self.root.ids.c15.disabled = False
            self.root.ids.c15.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[4][0])
            self.root.ids.c15.line_color = self.theme_cls.primary_color
            self.root.ids.c25.disabled = False
            self.root.ids.c25.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[4][1])
            self.root.ids.c25.line_color = self.theme_cls.primary_color
            self.root.ids.c35.disabled = False
            self.root.ids.c35.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[4][2])
            self.root.ids.c35.line_color = self.theme_cls.primary_color
            self.root.ids.c45.disabled = False
            self.root.ids.c45.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[4][3])
            self.root.ids.c45.line_color = self.theme_cls.primary_color
            self.root.ids.c55.disabled = False
            self.root.ids.c55.text = '1A . ₹' + str(self.fare1a) + '\nAVL' + str(self.res[4][3])
            self.root.ids.c55.line_color = self.theme_cls.primary_color
    def count6(self, count_list):
        self.count5(count_list)
        if count_list[5] == 1:
            self.root.ids.c16.disabled = False
            self.root.ids.c16.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[5][0])
            self.root.ids.c16.line_color = self.theme_cls.primary_color
        elif count_list[5] == 2:
            self.root.ids.c16.disabled = False
            self.root.ids.c16.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[5][0])
            self.root.ids.c16.line_color = self.theme_cls.primary_color
            self.root.ids.c26.disabled = False
            self.root.ids.c26.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[5][1])
            self.root.ids.c26.line_color = self.theme_cls.primary_color
        elif count_list[5] == 3:
            self.root.ids.c16.disabled = False
            self.root.ids.c16.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[5][0])
            self.root.ids.c16.line_color = self.theme_cls.primary_color
            self.root.ids.c26.disabled = False
            self.root.ids.c26.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[5][1])
            self.root.ids.c26.line_color = self.theme_cls.primary_color
            self.root.ids.c36.disabled = False
            self.root.ids.c36.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[5][2])
            self.root.ids.c36.line_color = self.theme_cls.primary_color
        elif count_list[5] == 4:
            self.root.ids.c16.disabled = False
            self.root.ids.c16.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[5][0])
            self.root.ids.c16.line_color = self.theme_cls.primary_color
            self.root.ids.c26.disabled = False
            self.root.ids.c26.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[5][1])
            self.root.ids.c26.line_color = self.theme_cls.primary_color
            self.root.ids.c36.disabled = False
            self.root.ids.c36.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[5][2])
            self.root.ids.c36.line_color = self.theme_cls.primary_color
            self.root.ids.c46.disabled = False
            self.root.ids.c46.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[5][3])
            self.root.ids.c46.line_color = self.theme_cls.primary_color
        elif count_list[5] == 5:
            self.root.ids.c16.disabled = False
            self.root.ids.c16.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[5][0])
            self.root.ids.c16.line_color = self.theme_cls.primary_color
            self.root.ids.c26.disabled = False
            self.root.ids.c26.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[5][1])
            self.root.ids.c26.line_color = self.theme_cls.primary_color
            self.root.ids.c36.disabled = False
            self.root.ids.c36.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[5][2])
            self.root.ids.c36.line_color = self.theme_cls.primary_color
            self.root.ids.c46.disabled = False
            self.root.ids.c46.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[5][3])
            self.root.ids.c46.line_color = self.theme_cls.primary_color
            self.root.ids.c56.disabled = False
            self.root.ids.c56.text = '1A . ₹' + str(self.fare1a) + '\nAVL' + str(self.res[5][4])
            self.root.ids.c56.line_color = self.theme_cls.primary_color

    def count7(self, count_list):
        self.count6(count_list)
        if count_list[6] == 1:
            self.root.ids.c17.disabled = False
            self.root.ids.c17.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[6][0])
            self.root.ids.c17.line_color = self.theme_cls.primary_color
        elif count_list[6] == 2:
            self.root.ids.c17.disabled = False
            self.root.ids.c17.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[6][0])
            self.root.ids.c17.line_color = self.theme_cls.primary_color
            self.root.ids.c27.disabled = False
            self.root.ids.c27.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[6][1])
            self.root.ids.c27.line_color = self.theme_cls.primary_color
        elif count_list[6] == 3:
            self.root.ids.c17.disabled = False
            self.root.ids.c17.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[6][0])
            self.root.ids.c17.line_color = self.theme_cls.primary_color
            self.root.ids.c27.disabled = False
            self.root.ids.c27.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[6][1])
            self.root.ids.c27.line_color = self.theme_cls.primary_color
            self.root.ids.c37.disabled = False
            self.root.ids.c37.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[6][2])
            self.root.ids.c37.line_color = self.theme_cls.primary_color
        elif count_list[6] == 4:
            self.root.ids.c17.disabled = False
            self.root.ids.c17.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[6][0])
            self.root.ids.c17.line_color = self.theme_cls.primary_color
            self.root.ids.c27.disabled = False
            self.root.ids.c27.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[6][1])
            self.root.ids.c27.line_color = self.theme_cls.primary_color
            self.root.ids.c37.disabled = False
            self.root.ids.c37.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[6][2])
            self.root.ids.c37.line_color = self.theme_cls.primary_color
            self.root.ids.c47.disabled = False
            self.root.ids.c47.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[6][3])
            self.root.ids.c47.line_color = self.theme_cls.primary_color
        elif count_list[6] == 5:
            self.root.ids.c17.disabled = False
            self.root.ids.c17.text = '2S . ₹' + str(self.fareg) + '\nAVL' + str(self.res[6][0])
            self.root.ids.c17.line_color = self.theme_cls.primary_color
            self.root.ids.c27.disabled = False
            self.root.ids.c27.text = 'SL . ₹' + str(self.faresl) + '\nAVL' + str(self.res[6][1])
            self.root.ids.c27.line_color = self.theme_cls.primary_color
            self.root.ids.c37.disabled = False
            self.root.ids.c37.text = '3A . ₹' + str(self.fare3a) + '\nAVL' + str(self.res[6][2])
            self.root.ids.c37.line_color = self.theme_cls.primary_color
            self.root.ids.c47.disabled = False
            self.root.ids.c47.text = '2A . ₹' + str(self.fare2a) + '\nAVL' + str(self.res[6][3])
            self.root.ids.c47.line_color = self.theme_cls.primary_color
            self.root.ids.c57.disabled = False
            self.root.ids.c57.text = '1A . ₹' + str(self.fare1a) + '\nAVL' + str(self.res[6][4])
            self.root.ids.c57.line_color = self.theme_cls.primary_color
    def c1return(self):
        self.var=self.root.ids.tname1.text
        self.root.ids.c2.disabled = True
        self.root.ids.c3.disabled = True
        self.root.ids.c4.disabled = True
        self.root.ids.c5.disabled = True
        self.farec=self.fareg
        self.arrive_traine=self.arrive[0][0]
        self.depart_traine=self.depart[0][0]
        self.seatn_nog=self.res[0][0]
        self.root.ids.submitt1.disabled = False
        self.Cls_type = 'general'
        self.tNuM=self.root.ids.num1.text

    def c2return(self):
        self.var = self.root.ids.tname1.text
        self.root.ids.c1.disabled = True
        self.root.ids.c3.disabled = True
        self.root.ids.c4.disabled = True
        self.root.ids.c5.disabled = True
        self.farec = self.faresl
        self.arrive_traine = self.arrive[0][0]
        self.depart_traine = self.depart[0][0]
        self.seatn_nosl = self.res[0][1]
        self.root.ids.submitt1.disabled = False
        self.Cls_type = 'sl'
        self.tNuM = self.root.ids.num1.text
    def c3return(self):
        self.var = self.root.ids.tname1.text
        self.root.ids.c1.disabled = True
        self.root.ids.c2.disabled = True
        self.root.ids.c4.disabled = True
        self.root.ids.c5.disabled = True
        self.farec = self.fare3a
        self.arrive_traine = self.arrive[0][0]
        self.depart_traine = self.depart[0][0]
        self.seatn_no3a = self.res[0][2]
        self.root.ids.submitt1.disabled = False
        self.Cls_type = '3a'
        self.tNuM = self.root.ids.num1.text
    def c4return(self):
        self.var = self.root.ids.tname1.text
        self.root.ids.c1.disabled = True
        self.root.ids.c2.disabled = True
        self.root.ids.c3.disabled = True
        self.root.ids.c5.disabled = True
        self.farec = self.fare2a
        self.arrive_traine = self.arrive[0][0]
        self.depart_traine = self.depart[0][0]
        self.seatn_no2a = self.res[0][3]
        self.root.ids.submitt1.disabled = False
        self.Cls_type = '2a'
        self.tNuM = self.root.ids.num1.text
    def c5return(self):
        self.var = self.root.ids.tname1.text
        self.root.ids.c1.disabled = True
        self.root.ids.c2.disabled = True
        self.root.ids.c3.disabled = True
        self.root.ids.c4.disabled = True
        self.farec = self.fare1a
        self.arrive_traine = self.arrive[0][0]
        self.depart_traine = self.depart[0][0]
        self.seatn_no1a = self.res[0][4]
        self.root.ids.submitt1.disabled = False
        self.Cls_type = '1a'
        self.tNuM = self.root.ids.num1.text
    def c12return(self):
        self.var = self.root.ids.tname2.text
        self.root.ids.c22.disabled = True
        self.root.ids.c32.disabled = True
        self.root.ids.c42.disabled = True
        self.root.ids.c52.disabled = True
        self.root.ids.submitt2.disabled = False
        self.farec = self.fareg
        self.arrive_traine = self.arrive[1][0]
        self.depart_traine = self.depart[1][0]
        self.seatn_nog = self.res[1][0]
        self.Cls_type = 'general'
        self.tNuM = self.root.ids.num2.text
    def c22return(self):
        self.var = self.root.ids.tname2.text
        self.root.ids.c12.disabled = True
        self.root.ids.c32.disabled = True
        self.root.ids.c42.disabled = True
        self.root.ids.c52.disabled = True
        self.farec = self.faresl
        self.arrive_traine = self.arrive[1][0]
        self.depart_traine = self.depart[1][0]
        self.seatn_nosl = self.res[1][1]
        self.root.ids.submitt2.disabled = False
        self.Cls_type = 'sl'
        self.tNuM = self.root.ids.num2.text
    def c32return(self):
        self.var = self.root.ids.tname2.text
        self.root.ids.c12.disabled = True
        self.root.ids.c22.disabled = True
        self.root.ids.c42.disabled = True
        self.root.ids.c52.disabled = True
        self.farec = self.fare3a
        self.arrive_traine = self.arrive[1][0]
        self.depart_traine = self.depart[1][0]
        self.seatn_no3a = self.res[1][2]
        self.root.ids.submitt2.disabled = False
        self.Cls_type = '3a'
        self.tNuM = self.root.ids.num2.text
    def c42return(self):
        self.var = self.root.ids.tname2.text
        self.root.ids.c12.disabled = True
        self.root.ids.c22.disabled = True
        self.root.ids.c32.disabled = True
        self.root.ids.c52.disabled = True
        self.farec = self.fare2a
        self.arrive_traine = self.arrive[1][0]
        self.depart_traine = self.depart[1][0]
        self.seatn_no2a = self.res[1][3]
        self.root.ids.submitt2.disabled = False
        self.Cls_type = '2a'
        self.tNuM = self.root.ids.num2.text
    def c52return(self):
        self.var = self.root.ids.tname2.text
        self.root.ids.c12.disabled = True
        self.root.ids.c22.disabled = True
        self.root.ids.c32.disabled = True
        self.root.ids.c42.disabled = True
        self.farec = self.fare1a
        self.arrive_traine = self.arrive[1][0]
        self.depart_traine = self.depart[1][0]
        self.seatn_no1a = self.res[1][4]
        self.root.ids.submitt2.disabled = False
        self.Cls_type = '1a'
        self.tNuM = self.root.ids.num2.text
    def c13return(self):
        self.var = self.root.ids.tname3.text
        self.root.ids.c13.disabled = True
        self.root.ids.c23.disabled = True
        self.root.ids.c33.disabled = True
        self.root.ids.c43.disabled = True
        self.farec = self.fareg
        self.arrive_traine = self.arrive[2][0]
        self.depart_traine = self.depart[2][0]
        self.seatn_nog = self.res[2][0]
        self.root.ids.submitt3.disabled = False
        self.Cls_type = 'general'
        self.tNuM = self.root.ids.num3.text
    def c23return(self):
        self.var = self.root.ids.tname3.text
        self.root.ids.c13.disabled = True
        self.root.ids.c33.disabled = True
        self.root.ids.c43.disabled = True
        self.root.ids.c53.disabled = True
        self.farec = self.faresl
        self.arrive_traine = self.arrive[2][0]
        self.depart_traine = self.depart[2][0]
        self.seatn_nosl = self.res[2][1]
        self.root.ids.submitt3.disabled = False
        self.Cls_type = 'sl'
        self.tNuM = self.root.ids.num3.text
    def c33return(self):
        self.var = self.root.ids.tname3.text
        self.root.ids.c13.disabled = True
        self.root.ids.c23.disabled = True
        self.root.ids.c43.disabled = True
        self.root.ids.c53.disabled = True
        self.farec = self.fare3a
        self.arrive_traine = self.arrive[2][0]
        self.depart_traine = self.depart[2][0]
        self.seatn_no3a = self.res[2][2]
        self.root.ids.submitt3.disabled = False
        self.Cls_type = '3a'
        self.tNuM = self.root.ids.num3.text
    def c43return(self):
        self.var = self.root.ids.tname3.text
        self.root.ids.c13.disabled = True
        self.root.ids.c23.disabled = True
        self.root.ids.c33.disabled = True
        self.root.ids.c53.disabled = True
        self.farec = self.fare2a
        self.arrive_traine = self.arrive[2][0]
        self.depart_traine = self.depart[2][0]
        self.seatn_no2a = self.res[2][3]
        self.root.ids.submitt3.disabled = False
        self.Cls_type = '2a'
        self.tNuM = self.root.ids.num3.text
    def c53return(self):
        self.var = self.root.ids.tname3.text
        self.root.ids.c13.disabled = True
        self.root.ids.c23.disabled = True
        self.root.ids.c33.disabled = True
        self.root.ids.c43.disabled = True
        self.farec = self.fare1a
        self.arrive_traine = self.arrive[2][0]
        self.depart_traine = self.depart[2][0]
        self.seatn_no1a = self.res[2][4]
        self.root.ids.submitt3.disabled = False
        self.Cls_type = '1a'
        self.tNuM = self.root.ids.num3.text
    def c14return(self):
        self.var = self.root.ids.tname4.text
        self.root.ids.c24.disabled = True
        self.root.ids.c34.disabled = True
        self.root.ids.c44.disabled = True
        self.root.ids.c54.disabled = True
        self.farec = self.fareg
        self.arrive_traine = self.arrive[3][0]
        self.depart_traine = self.depart[3][0]
        self.seatn_nog = self.res[3][0]
        self.root.ids.submitt4.disabled = False
        self.Cls_type = 'general'
        self.tNuM = self.root.ids.num4.text
    def c24return(self):
        self.var = self.root.ids.tname4.text
        self.root.ids.c14.disabled = True
        self.root.ids.c34.disabled = True
        self.root.ids.c44.disabled = True
        self.root.ids.c54.disabled = True
        self.farec = self.faresl
        self.arrive_traine = self.arrive[3][0]
        self.depart_traine = self.depart[3][0]
        self.seatn_nosl = self.res[3][1]
        self.root.ids.submitt4.disabled = False
        self.Cls_type = 'sl'
        self.tNuM = self.root.ids.num4.text
    def c34return(self):
        self.var = self.root.ids.tname4.text
        self.root.ids.c14.disabled = True
        self.root.ids.c24.disabled = True
        self.root.ids.c44.disabled = True
        self.root.ids.c54.disabled = True
        self.farec = self.fare3a
        self.arrive_traine = self.arrive[3][0]
        self.depart_traine = self.depart[3][0]
        self.seatn_no3a = self.res[3][2]
        self.root.ids.submitt4.disabled = False
        self.Cls_type = '3a'
        self.tNuM = self.root.ids.num4.text
    def c44return(self):
        self.var = self.root.ids.tname4.text
        self.root.ids.c14.disabled = True
        self.root.ids.c24.disabled = True
        self.root.ids.c34.disabled = True
        self.root.ids.c54.disabled = True
        self.farec = self.fare2a
        self.arrive_traine = self.arrive[3][0]
        self.depart_traine = self.depart[3][0]
        self.seatn_no2a = self.res[3][3]
        self.root.ids.submitt4.disabled = False
        self.Cls_type = '2a'
        self.tNuM = self.root.ids.num4.text
    def c54return(self):
        self.var = self.root.ids.tname4.text
        self.root.ids.c14.disabled = True
        self.root.ids.c24.disabled = True
        self.root.ids.c34.disabled = True
        self.root.ids.c44.disabled = True
        self.farec = self.fare1a
        self.arrive_traine = self.arrive[3][0]
        self.depart_traine = self.depart[3][0]
        self.seatn_no1a = self.res[3][4]
        self.root.ids.submitt4.disabled = False
        self.Cls_type = '1a'
        self.tNuM = self.root.ids.num4.text
    def c15return(self):
        self.var = self.root.ids.tname5.text
        self.root.ids.c25.disabled = True
        self.root.ids.c35.disabled = True
        self.root.ids.c45.disabled = True
        self.root.ids.c55.disabled = True
        self.farec = self.fareg
        self.arrive_traine = self.arrive[4][0]
        self.depart_traine = self.depart[4][0]
        self.seatn_nog = self.res[4][0]
        self.root.ids.submitt5.disabled = False
        self.Cls_type = 'general'
        self.tNuM = self.root.ids.num5.text
    def c25return(self):
        self.var = self.root.ids.tname5.text
        self.root.ids.c15.disabled = True
        self.root.ids.c35.disabled = True
        self.root.ids.c45.disabled = True
        self.root.ids.c55.disabled = True
        self.farec = self.faresl
        self.arrive_traine = self.arrive[4][0]
        self.depart_traine = self.depart[4][0]
        self.seatn_nosl = self.res[4][1]
        self.root.ids.submitt5.disabled = False
        self.Cls_type = 'sl'
        self.tNuM = self.root.ids.num5.text
    def c35return(self):
        self.var = self.root.ids.tname5.text
        self.root.ids.c15.disabled = True
        self.root.ids.c25.disabled = True
        self.root.ids.c45.disabled = True
        self.root.ids.c55.disabled = True
        self.farec = self.fare3a
        self.arrive_traine = self.arrive[4][0]
        self.depart_traine = self.depart[4][0]
        self.seatn_no3a = self.res[4][2]
        self.root.ids.submitt5.disabled = False
        self.Cls_type = '3a'
        self.tNuM = self.root.ids.num5.text
    def c45return(self):
        self.var = self.root.ids.tname5.text
        self.root.ids.c15.disabled = True
        self.root.ids.c25.disabled = True
        self.root.ids.c35.disabled = True
        self.root.ids.c55.disabled = True
        self.farec = self.fare2a
        self.arrive_traine = self.arrive[4][0]
        self.depart_traine = self.depart[4][0]
        self.seatn_no2a = self.res[4][3]
        self.root.ids.submitt5.disabled = False
        self.Cls_type = '2a'
        self.tNuM = self.root.ids.num5.text
    def c55return(self):
        self.var = self.root.ids.tname5.text
        self.root.ids.c15.disabled = True
        self.root.ids.c25.disabled = True
        self.root.ids.c35.disabled = True
        self.root.ids.c45.disabled = True
        self.farec = self.fare1a
        self.arrive_traine = self.arrive[4][0]
        self.depart_traine = self.depart[4][0]
        self.seatn_no1a = self.res[4][4]
        self.root.ids.submitt5.disabled = False
        self.Cls_type = '1a'
        self.tNuM = self.root.ids.num5.text

    def c16return(self):
        self.var = self.root.ids.tname6.text
        self.root.ids.c26.disabled = True
        self.root.ids.c36.disabled = True
        self.root.ids.c46.disabled = True
        self.root.ids.c56.disabled = True
        self.farec = self.fareg
        self.arrive_traine = self.arrive[5][0]
        self.depart_traine = self.depart[5][0]
        self.seatn_nog = self.res[5][0]
        self.root.ids.submitt6.disabled = False
        self.Cls_type = 'general'
        self.tNuM = self.root.ids.num6.text

    def c26return(self):
        self.var = self.root.ids.tname6.text
        self.root.ids.c16.disabled = True
        self.root.ids.c36.disabled = True
        self.root.ids.c46.disabled = True
        self.root.ids.c56.disabled = True
        self.farec = self.faresl
        self.arrive_traine = self.arrive[5][0]
        self.depart_traine = self.depart[5][0]
        self.seatn_nosl = self.res[5][1]
        self.root.ids.submitt6.disabled = False
        self.Cls_type = 'sl'
        self.tNuM = self.root.ids.num6.text

    def c36return(self):
        self.var = self.root.ids.tname6.text
        self.root.ids.c16.disabled = True
        self.root.ids.c26.disabled = True
        self.root.ids.c46.disabled = True
        self.root.ids.c56.disabled = True
        self.farec = self.fare3a
        self.arrive_traine = self.arrive[5][0]
        self.depart_traine = self.depart[5][0]
        self.seatn_no3a = self.res[5][2]
        self.root.ids.submitt6.disabled = False
        self.Cls_type = '3a'
        self.tNuM = self.root.ids.num6.text

    def c46return(self):
        self.var = self.root.ids.tname6.text
        self.root.ids.c16.disabled = True
        self.root.ids.c26.disabled = True
        self.root.ids.c36.disabled = True
        self.root.ids.c56.disabled = True
        self.farec = self.fare2a
        self.arrive_traine = self.arrive[5][0]
        self.depart_traine = self.depart[5][0]
        self.seatn_no2a = self.res[5][3]
        self.root.ids.submitt6.disabled = False
        self.Cls_type = '2a'
        self.tNuM = self.root.ids.num6.text

    def c56return(self):
        self.var = self.root.ids.tname6.text
        self.root.ids.c16.disabled = True
        self.root.ids.c26.disabled = True
        self.root.ids.c36.disabled = True
        self.root.ids.c46.disabled = True
        self.farec = self.fare1a
        self.arrive_traine = self.arrive[5][0]
        self.depart_traine = self.depart[5][0]
        self.seatn_no1a = self.res[5][4]
        self.root.ids.submitt6.disabled = False
        self.Cls_type = '1a'
        self.tNuM = self.root.ids.num6.text

    def c17return(self):
        self.var = self.root.ids.tname7.text
        self.root.ids.c27.disabled = True
        self.root.ids.c37.disabled = True
        self.root.ids.c47.disabled = True
        self.root.ids.c57.disabled = True
        self.farec = self.fareg
        self.arrive_traine = self.arrive[6][0]
        self.depart_traine = self.depart[6][0]
        self.seatn_nog = self.res[6][0]
        self.root.ids.submitt7.disabled = False
        self.Cls_type = 'general'
        self.tNuM = self.root.ids.num7.text

    def c27return(self):
        self.var = self.root.ids.tname7.text
        self.root.ids.c17.disabled = True
        self.root.ids.c37.disabled = True
        self.root.ids.c47.disabled = True
        self.root.ids.c57.disabled = True
        self.farec = self.faresl
        self.arrive_traine = self.arrive[6][0]
        self.depart_traine = self.depart[6][0]
        self.seatn_nosl = self.res[6][1]
        self.root.ids.submitt7.disabled = False
        self.Cls_type = 'sl'
        self.tNuM = self.root.ids.num7.text

    def c37return(self):
        self.var = self.root.ids.tname7.text
        self.root.ids.c17.disabled = True
        self.root.ids.c27.disabled = True
        self.root.ids.c47.disabled = True
        self.root.ids.c57.disabled = True
        self.farec = self.fare3a
        self.arrive_traine = self.arrive[6][0]
        self.depart_traine = self.depart[6][0]
        self.seatn_no3a = self.res[6][2]
        self.root.ids.submitt7.disabled = False
        self.Cls_type = '3a'
        self.tNuM = self.root.ids.num7.text

    def c47return(self):
        self.var = self.root.ids.tname7.text
        self.root.ids.c17.disabled = True
        self.root.ids.c27.disabled = True
        self.root.ids.c37.disabled = True
        self.root.ids.c57.disabled = True
        self.farec = self.fare2a
        self.arrive_traine = self.arrive[6][0]
        self.depart_traine = self.depart[6][0]
        self.seatn_no2a = self.res[6][3]
        self.root.ids.submitt7.disabled = False
        self.Cls_type = '2a'
        self.tNuM = self.root.ids.num7.text

    def c57return(self):
        self.var = self.root.ids.tname7.text
        self.root.ids.c17.disabled = True
        self.root.ids.c27.disabled = True
        self.root.ids.c37.disabled = True
        self.root.ids.c47.disabled = True
        self.farec = self.fare1a
        self.arrive_traine = self.arrive[6][0]
        self.depart_traine = self.depart[6][0]
        self.seatn_no1a = self.res[6][4]
        self.root.ids.submitt7.disabled = False
        self.Cls_type = '1a'
        self.tNuM = self.root.ids.num7.text

    def search1(self,search,time_depart,dur,time_arrive):
        self.root.ids.num1.text = str(search[0][0])
        self.root.ids.tname1.text = search[0][1]
        self.root.ids.durlab1.text = "  " + str(self.From) + "                                                                " + str(self.To) + '\n' + str(time_depart[0][0]) + ':' + str(time_depart[0][1]) + "  o ------------" + str(dur[0][0]) + 'hr' + str(dur[0][1]) + 'mins' + "------------ o  " + str(time_arrive[0][0]) + ':' + str(time_arrive[0][1])
    def search2(self,search,time_depart,dur,time_arrive):
        self.search1(search, time_depart, dur, time_arrive)
        self.root.ids.num2.text = str(search[1][0])
        self.root.ids.tname2.text = search[1][1]
        self.root.ids.durlab2.text = "  " + str(self.From) + "                                                                " + str(self.To) + '\n' + str(time_depart[1][0]) + ':' + str(time_depart[1][1]) + "  o ------------" + str(dur[1][0]) + 'hr' + str(dur[1][1]) + 'mins' + "------------ o  " + str(time_arrive[1][0]) + ':' + str(time_arrive[1][1])
    def search3(self,search,time_depart,dur,time_arrive):
        self.search2(search, time_depart, dur, time_arrive)
        self.root.ids.num3.text = str(search[2][0])
        self.root.ids.tname3.text = search[2][1]
        self.root.ids.durlab3.text = "  " + str(self.From) + "                                                                " + str(self.To) + '\n' + str(time_depart[2][0]) + ':' + str(time_depart[2][1]) + "  o ------------" + str(dur[2][0]) + 'hr' + str(dur[2][1]) + 'mins' + "------------ o  " + str(time_arrive[2][0]) + ':' + str(time_arrive[2][1])
    def search4(self,search,time_depart,dur,time_arrive):
        self.search3(search, time_depart, dur, time_arrive)
        self.root.ids.num4.text = str(search[3][0])
        self.root.ids.tname4.text = search[3][1]
        self.root.ids.durlab4.text = "  " + str(self.From) + "                                                                " + str(self.To) + '\n' + str(time_depart[3][0]) + ':' + str(time_depart[3][1]) + "  o ------------" + str(dur[3][0]) + 'hr' + str(dur[3][1]) + 'mins' + "------------ o  " + str(time_arrive[3][0]) + ':' + str(time_arrive[3][1])
    def search5(self,search,time_depart,dur,time_arrive):
        self.search4(search, time_depart, dur, time_arrive)
        self.root.ids.num5.text = str(search[4][0])
        self.root.ids.tname5.text = search[4][1]
        self.root.ids.durlab5.text = "  " + str(self.From) + "                                                                " + str(self.To) + '\n' + str(time_depart[4][0]) + ':' + str(time_depart[4][1]) + "  o ------------" + str(dur[4][0]) + 'hr' + str(dur[4][1]) + 'mins' + "------------ o  " + str(time_arrive[4][0]) + ':' + str(time_arrive[4][1])
    def search6(self, search, time_depart, dur, time_arrive):
        self.search5(search, time_depart, dur, time_arrive)
        self.root.ids.num6.text = str(search[5][0])
        self.root.ids.tname6.text = search[5][1]
        self.root.ids.durlab6.text = "  " + str(self.From) + "                                                                " + str(self.To) + '\n' + str(time_depart[5][0]) + ':' + str(time_depart[5][1]) + "  o ------------" + str(dur[5][0]) + 'hr' + str(dur[5][1]) + 'mins' + "------------ o  " + str(time_arrive[5][0]) + ':' + str(time_arrive[5][1])

    def search7(self, search, time_depart, dur, time_arrive):
        self.search6(search, time_depart, dur, time_arrive)
        self.root.ids.num7.text = str(search[6][0])
        self.root.ids.tname7.text = search[6][1]
        self.root.ids.durlab7.text = "  " + str(self.From) + "                                                               " + str(self.To) + '\n' + str(time_depart[6][0]) + ':' + str(time_depart[6][1]) + "  o ------------" + str(dur[6][0]) + 'hr' + str(dur[6][1]) + 'mins' + "------------ o  " + str(time_arrive[6][0]) + ':' + str(time_arrive[6][1])

    def dialog_box(self):
        super().on_start()
        MDDialog(
            title="As Your Booking is completed you now proceed with transaction in main screen ",
            text="PNR NO:"+str(self.pnr_insert)
        ).open()

    def search_train(self):

        query = "select train_no, train_name from train where train_no in (select train_no from days_working where tuesday=1 and train_no in ((select train_no from station where station_code=%s) intersect (select train_no from station where station_code=%s))) ORDER BY train_no ASC"
        c.execute(query, ( self.From,self.To))
        search=c.fetchall()
        try:
            c.execute("select  distinct class_type,train_no from coach where train_no in ((select train_no from station where station_code=%s) intersect(select train_no from station where station_code=%s))",(self.From,self.To,))
            coach=c.fetchall()
            c.execute("select departure_time from station where station_code=%s and train_no in ( select train_no from days_working where tuesday=1 and train_no in((select train_no from station where station_code=%s) intersect(select train_no from station where station_code=%s)))",(self.From,self.From,self.To,))
            self.depart=c.fetchall()
            print("DEpart",self.depart)
            c.execute("select arrival_time from station where station_code=%s and train_no in ( select train_no from days_working where tuesday=1 and train_no in((select train_no from station where station_code=%s) intersect(select train_no from station where station_code=%s)))",(self.To,self.From,self.To,))
            self.arrive=c.fetchall()
            print("ARRIVE",self.arrive)
            c.execute("(select station_name from station where station_code=%s) union (select station_name from station where station_code=%s)",(self.From,self.To,))
            self.station_code=c.fetchall()
            print(self.station_code)
            c.execute("select class_type,train_no,no_coach from coach where train_no in ((select train_no from station where station_code=%s) intersect(select train_no from station where station_code=%s));",(self.From,self.To,))
            no_seatcoach=c.fetchall()
            print(no_seatcoach)

            x = no_seatcoach[0][1]
            y = no_seatcoach[0][0]
            sum_temp = 0
            temp = []
            self.res = []

            for i in no_seatcoach:
                if x == i[1]:
                    if y == i[0]:
                        sum_temp = sum_temp + i[2]
                    else:
                        temp.append(sum_temp)
                        y = i[0]
                        sum_temp = i[2]
                else:
                    temp.append(sum_temp)
                    self.res.append(tuple(temp))
                    temp = []
                    x = i[1]
                    sum_temp = i[2]
            temp.append(sum_temp)
            self.res.append(tuple(temp))

            print(self.res)
            time_depart = []
            for i in self.depart:
                timedelta_tuple = i
                for time_delta in timedelta_tuple:
                    total_seconds = time_delta.total_seconds()
                    hours, remainder = divmod(total_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    time_depart.append([int(hours), int(minutes), int(seconds)])
                    print(time_depart)

            time_arrive = []
            for i in self.arrive:
                print(i)
                timedelta_tuple = i

                for time_delta in timedelta_tuple:
                    total_seconds = time_delta.total_seconds()
                    hours, remainder = divmod(total_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    time_arrive.append([int(hours), int(minutes), int(seconds)])
                    print(time_arrive)

            mins_arrive = 0
            mins_depart = 0
            res = 0
            dur = []
            count = 0
            for i in search:
                count = count + 1

            for i in range(0, count):
                mins_arrive += (time_arrive[i][0]) * 60 + time_arrive[i][1]
                mins_depart += (time_depart[i][0]) * 60 + time_depart[i][1]
                res = mins_arrive - mins_depart
                mins = res % 60
                hr = res // 60
                x = (hr, mins)
                dur.append(x)
                mins_arrive = 0
                mins_depart = 0
            print(dur)

            x = coach[0][1]
            f = {}
            for i in coach:
                if i[1] == x:
                    if x in f:
                        f[x] += 1
                    else:
                        f[x] = 1
                else:
                    x=i[1]
                    f[x]=1
            count_list=[]
            for key in f:
                count_list.append(f[key])
            print("count",count_list)

            self.fareg=round(24*(abs(self.yt-self.xf)))
            self.faresl=round(self.fareg*0.64)
            self.fare3a=round(self.fareg*2.11)
            self.fare2a=round(self.fareg*5.92)
            self.fare1a=round(self.fareg*7.3)
            print(coach)
            print("ss",search)
            print(self.xyz,self.From,self.To)

            if count == 1:
                self.search1(search,time_depart,dur,time_arrive)
                self.count1(count_list)
            if count == 2:
                self.search2(search,time_depart,dur,time_arrive)
                self.count2(count_list)
            if count == 3:
                self.search3(search,time_depart,dur,time_arrive)
                self.count3(count_list)
            if count == 4:
                self.search4(search,time_depart,dur,time_arrive)
                self.count4(count_list)
            if count == 5:
                self.search5(search,time_depart,dur,time_arrive)
                self.count5(count_list)
            if count == 6:
                self.search6(search, time_depart, dur, time_arrive)
                self.count6(count_list)
            if count == 7:
                self.search7(search, time_depart, dur, time_arrive)
                self.count7(count_list)
        except IndexError:
            self.root.ids.notrain.text="No Trains are Available"

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="To Continue your booking... \nclick on ticket booking button on home screen",

            )
        self.dialog.open()
        self.root.ids.thankutext.text = "Thank you for reserving in this " + self.var + "train we hope to provide the best experiencee below is your ticket details:-"
        c.execute("SELECT coach_no, no_coach FROM coach WHERE train_no = %s AND class_type = %s ORDER BY coach_no",(int(self.tNuM), self.Cls_type))
        coaches = c.fetchall()
        for coach in coaches:
            if coach[1] > 0:
                c.execute("UPDATE coach SET no_coach = no_coach - 1 WHERE train_no = %s AND class_type = %s AND coach_no = %s",(int(self.tNuM),self.Cls_type, coach[0]))
                mydb.commit()
                break


Example().run()