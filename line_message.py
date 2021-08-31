#line_message.py
#line message ver 1.0 Update: 30/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/LINE_Messaging_API
#This code send LINE message. 
#LINE Messaging API is presented by LINE Corporation Japan.
#For detail, reffer to LINE Developers Docs
##https://developers.line.biz/en/docs/


import LINE_Messaging_API_setting
import datetime
import sys
import sqlite3

class line_message_db:
    def __init__(self):
        self.lvNormal = 0
        self.lvError = 1
        self.enablev = 1
        self.desablev = 0
        self.update_flg_linemsg_on = 2  #unsend
        self.update_flg_linemsg_off = 9 #sent
        self.update_flg_linemsg_ignore = 99 #ignore
        self.line_message_db_path = r".\linemessage.db" # initial value. you can change this parameter in executing.
        self.application = "" #this parameter is setting in executing.
    
    def read_line_message_maxnumber(self):
        conn = sqlite3.connect(self.line_message_db_path)
        cur = conn.cursor()

        try:
            cur.execute("SELECT MAX(number) FROM line_message")
            self.line_message_maxnumber = cur.fetchone()[0]
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError
        conn.close()
        return ret

    def read_line_message_get_unsend_list(self, update_flg):
        conn = sqlite3.connect(self.line_message_db_path)
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM line_message WHERE update_flg = '" + str(update_flg) + "' AND application = '" + self.application + "'")
            self.linemsg_send_list = cur.fetchall()
            print(self.linemsg_send_list)
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError
        conn.close()
        return ret

    def write_line_message_request(self, update_flg, request_datetime, send_datetime, msg, number):
        conn = sqlite3.connect(self.line_message_db_path)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO line_message VALUES('" + str(update_flg) + "', '" + msg + "', '" + request_datetime + "', '" + send_datetime + "', " + str(number) + ", '" + self.application + "')")
            conn.commit()
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def update_line_message_flg(self, update_flg, send_datetime, number):
        conn = sqlite3.connect(self.line_message_db_path)
        cur = conn.cursor()
        try:
            cur.execute("UPDATE line_message SET update_flg = '" + str(update_flg) + "', send_datetime = '" + send_datetime + "' WHERE number = " + str(number))
            conn.commit()
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def read_line_secret(self):
        conn = sqlite3.connect(self.line_message_db_path)
        cur = conn.cursor()

        try:
            cur.execute("SELECT CHANNEL_ACCESS_TOKEN, USER_ID, enable FROM line_secret WHERE application = '" + self.application + "'")
            record = cur.fetchone()
            self.CHANNEL_ACCESS_TOKEN = record[0]
            self.USER_ID = record[1]
            self.enable = record[2]
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError
        conn.close()
        return ret


class line_message_useAPI:
    def __init__(self):
        self.lvNormal = 0
        self.lvError = 1
        self.update_flg_linemsg_on = 2  #unsend
        self.update_flg_linemsg_off = 9 #sent
        self.update_flg_linemsg_ignore = 99 #ignore
        self.line_message_db_path = r".\linemessage.db" # initial value. you can change this parameter in executing.
        self.CHANNEL_ACCESS_TOKEN = "" #this parameter is setting in executing.
        self.USER_ID = "" #this parameter is setting in executing.
        self.application = "" #this parameter is setting in executing.
        self.msg = "" #this parameter is setting in executing.

    def post_message(self):
        #read secret information from database
        cls_db = line_message_db()
        cls_db.line_message_db_path = self.line_message_db_path
        cls_db.application = self.application
        ret = cls_db.read_line_secret()

        if ret == cls_db.lvNormal:
            #LINE secret parameter set to LINE Messaging API
            cls_Line_Messaging_API_setting = LINE_Messaging_API_setting.LINE_Messaging_API()
            cls_Line_Messaging_API_setting.CHANNEL_ACCESS_TOKEN = "Bearer {" + cls_db.CHANNEL_ACCESS_TOKEN + "}"
            cls_Line_Messaging_API_setting.USER_ID = cls_db.USER_ID
            print(cls_Line_Messaging_API_setting.CHANNEL_ACCESS_TOKEN)
            print(cls_Line_Messaging_API_setting.USER_ID)

            if cls_db.enable == cls_db.desablev:
                print("This secret parameter desabled. check table: 'line_secret'")
                sys.exit(0)

            #Get unsend list
            ret = cls_db.read_line_message_get_unsend_list(cls_db.update_flg_linemsg_on)
            if ret == cls_db.lvNormal:
                ret = self.lvNormal
                unsend_list = cls_db.linemsg_send_list
                dt_now = datetime.datetime.now()
                for unsend in unsend_list:
                    print(unsend)
                    ret = cls_Line_Messaging_API_setting.post_messages(unsend[1]  + '\r\n' + " request date : " + unsend[2]+ '\r\n' + " application : " + unsend[5])
                    if ret == cls_Line_Messaging_API_setting.lvNormal:
                        print("post success number = " + str(unsend[4]))
                        ret = cls_db.update_line_message_flg(self.update_flg_linemsg_off, dt_now.strftime('%Y/%m/%d %H:%M:%S'), unsend[4])
                        if ret == cls_db.lvError:
                            print("table: line_message flg update error --- number = " + unsend[4])
                            self.ret = self.lvError
                    elif ret == cls_Line_Messaging_API_setting.lvError:
                        print("post_messages error")
                        print(cls_Line_Messaging_API_setting.err_code)
            elif ret == cls_db.lvError:
                ret = self.lvError
        elif ret == cls_db.lvError:
            ret = self.lvError

        return ret

    def line_message_request(self):
        #database
        cls_db = line_message_db()
        dt_now = datetime.datetime.now()
        cls_db.line_message_db_path = self.line_message_db_path
        cls_db.application = self.application
        ret = cls_db.read_line_message_maxnumber()
        if ret == cls_db.lvNormal:
            ret = cls_db.write_line_message_request(self.update_flg_linemsg_on, dt_now.strftime('%Y/%m/%d %H:%M:%S'), dt_now.strftime('%Y/%m/%d %H:%M:%S'), self.msg, cls_db.line_message_maxnumber + 1)
            if ret == cls_db.lvNormal:
                ret = self.lvNormal
            elif ret == cls_db.lvError:
                ret = self.lvError
        elif ret == cls_db.lvError:
            ret = self.lvError
        return ret


#this module test
def Test():
    #read line_secret
    cls_db = line_message_db()
    cls_db.line_message_db_path = r"\\DESKTOP-2322PPH\Users\Public\line_message\linemessage.db"
    cls_db.application = "test"
    ret = cls_db.read_line_secret()
    print(cls_db.CHANNEL_ACCESS_TOKEN)
    print(cls_db.USER_ID)

    cls_UseAPI = line_message_useAPI()
    print(cls_UseAPI.line_message_db_path)
    cls_UseAPI.line_message_db_path = r"\\DESKTOP-2322PPH\Users\Public\line_message\linemessage.db"
    print(cls_UseAPI.line_message_db_path)
   #send message request
    print("send message request")
    cls_UseAPI.line_message_request("test", "testApp")
    #post message
    print("post message for above request")
    cls_UseAPI.CHANNEL_ACCESS_TOKEN = "Bearer {your token}"
    cls_UseAPI.USER_ID = "your user id"
    cls_UseAPI.post_message()

#main
def main():
    if len(sys.argv) < 2:
        #parameter guide
        print("Request to database sending message to LINE --- line_message.py [r] [database] [msg] [application]")
        print("Post message to LINE --- line_message.py [p] [database] [application]")
    else:
        cls_useAPI = line_message_useAPI()
        if sys.argv[1] == "r":
            cls_useAPI.line_message_db_path = sys.argv[2]
            cls_useAPI.msg = sys.argv[3]
            cls_useAPI.application = sys.argv[4]
            ret = cls_useAPI.line_message_request()
            if ret == cls_useAPI.lvNormal:
                print("request success")
                print(sys.argv[3] + " " + sys.argv[4])
                print(ret)
            elif ret == cls_useAPI.lvError:
                print("request error")
                print(ret)
        elif sys.argv[1] == "p":
            cls_useAPI.line_message_db_path = sys.argv[2]
            cls_useAPI.application = sys.argv[3]
            ret = cls_useAPI.post_message()
            if ret == cls_useAPI.lvNormal:
                print("post success")
                print(ret)
            elif ret == cls_useAPI.lvError:
                print("post error")
                print(ret)
        else:
            print("argument value error")
            print("Request to database sending message to LINE --- line_message.py [r] [database] [msg] [application]")
            print("Post message to LINE --- line_message.py [p] [database] [application]")


if __name__ == '__main__':
    main()