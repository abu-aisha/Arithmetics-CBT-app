import tkinter as tk
import csv
from app_funcs import gen_quests
from datetime import datetime
import csv
from argon2 import PasswordHasher
import pymongo
from tkinter.messagebox import showerror, showwarning, showinfo
from tkintertable import TableCanvas, TableModel
from PIL import ImageTk, Image
import time
import os



ph = PasswordHasher()

count = 0
ops_sign_dict = {'add':'+','substr':'-','div':'÷','mul':'x'}
operators = ['add','substr','div','mul']



my_mongo_api = os.environ.get('mongo_api')





def goto_stu_lg():
    stu_login_pg.tkraise()


######### Start Login functions
def stu_login_():
    
    global firstname,lastname,level,bestscore,lg_usernm,level,password_hash
    lg_usernm = lg_usernm_entry.get()  
    lg_usr_pswd = lg_usr_pswd_entry.get()
   
    try:
        mongoc = pymongo.MongoClient(my_mongo_api)
        db = mongoc['Students_database']

        student_data = db['Students_coll'].find_one({'username':lg_usernm},{'_id':0,})
 #       print(student_data)

        if student_data:

            firstname = student_data['firstname']
            lastname = student_data['lastname']
            level = int(student_data['level'])
            bestscore = int(student_data['bestscore'])

            password_hash = student_data['password']

            lg_usernm_entry.delete(first = 0,last = tk.END)
            lg_usr_pswd_entry.delete(first = 0,last = tk.END)
#           
            try:
                if ph.verify(password_hash,lg_usr_pswd):
          

                    details = f"""Welcome user {lg_usernm}
Firstname : {firstname}
Lastname  : {lastname}
Bestscore : {bestscore}
Level     : {level}
                    """

                    greeting_lb =tk.Label(stu_dashbrd_pg,text= details,
                        font=("Arial Bold",30)  ,  bg = '#0288d1')
                    greeting_lb.place(relheight=0.3 , relwidth=0.6 ,relx=.05 ,rely=.4)
                    stu_dashbrd_pg.tkraise()
                
            except:
                showerror('Invalid Credentials','Invalid Username or password')
        else:
            showerror('Invalid Credentials','Invalid Username or password')
    except pymongo.errors.ConnectionFailure as err:
        showerror('Connection Error','The Application could not connect to database\nmake sure your internet connection is on and strong.')
    except Exception as err:
        if str(err).startswith('All nameservers failed to answer the query'):
            showerror('Connection Error','The Application could not connect to database\nmake sure your internet connection is on and strong.')
        else:
            print(err)
            showerror('Error',str(err))
 
######### End Login functions


######### Start dashboard functions

def reset_pwrd():
    pswd1 = crt_pswd_entry1.get().strip()
    pswd2 = crt_pswd_entry2.get().strip()
    pswd3 = crt_pswd_entry3.get().strip()
 
    try:
        if ph.verify(password_hash,pswd1):
            if (len(pswd2) >=8) and (len(pswd3) >=8):
                if pswd2 == pswd3:
                    hash_pswd_new = ph.hash(pswd2)
                    try:
                        mongoc = pymongo.MongoClient(my_mongo_api)
                        db = mongoc['Students_database']
                        db['Students_coll'].update_one({'username':lg_usernm},{'$set':{'password':hash_pswd_new}})
                        showinfo("Password Reset Success","Password has been reset successfull")
                        pswd_popup.grab_release()
                        time.sleep(5)
                        pswd_popup.destroy()
                    except pymongo.errors.ConnectionFailure as err:
                        showerror('Connection Error','The Application could not connect to database\nmake sure your internet connection is on and strong.')
                    except Exception as err:
                        if str(err).startswith('All nameservers failed to answer the query'):
                            showerror('Connection Error','The Application could not connect to database\nmake sure your internet connection is on and strong.')
                        else:
                            print(err)
                            showerror('Error',str(err))
                else:
                    showerror("Password Reset Error","Passwords must be same")
            else:
                showerror("Password Reset Error","Passwords must be same")
    
    except Exception as err:
        showerror('Error',err)
    except:
        showerror('Invalid Credentials','Invalid Username or password')
                

def open_popup():

    global pswd_popup,crt_pswd_entry1,crt_pswd_entry2,crt_pswd_entry3,ps_error_msg
    pswd_popup= tk.Toplevel(my_app, bg = 'white')
    pswd_popup.geometry("750x400")
    pswd_popup.title("Create Password")

    welcome_msg =tk.Label(pswd_popup,
        text = "You can reset your password here\nPlease know that your \npassword cannot be less than 8 characters",
        font=("Arial Bold",15)  ,  bg = 'white')
    welcome_msg.place(x = 255 , y=30)

    crt_pswd_lb1 =tk.Label(pswd_popup,text = "Previous Password:",font=("Arial Bold",15)  ,  bg = 'white')
    crt_pswd_entry1 =  tk.Entry(pswd_popup,width = 25,font=("Arial Bold",15),show ='*')
    crt_pswd_lb1.place(x = 20 , y=150)
    crt_pswd_entry1.place(x = 250 , y=150)


    crt_pswd_lb2 =tk.Label(pswd_popup,text = "New Password:",font=("Arial Bold",15)  ,  bg = 'white')
    crt_pswd_entry2 =  tk.Entry(pswd_popup,width = 25,font=("Arial Bold",15),show ='*')
    crt_pswd_lb2.place(x = 20 , y=200)
    crt_pswd_entry2.place(x = 250 , y=200)

    crt_pswd_lb3 =tk.Label(pswd_popup,text = "New Password:",font=("Arial Bold",15)  ,  bg = 'white')
    crt_pswd_entry3 =  tk.Entry(pswd_popup,width = 25,font=("Arial Bold",15),show ='*')
    crt_pswd_lb3.place(x = 20 , y=250)
    crt_pswd_entry3.place(x = 250 , y=250)

    create_pswd_btn = tk.Button(pswd_popup,text='RESET PASSWORD' ,pady=10,width=18,bg='#1847f2',fg = 'white',
    font=('Bold',12), command= reset_pwrd)
    create_pswd_btn.place(x = 80 , y=300)
   
    pswd_popup.grab_set() 

def conf_erase():
    print(firstname ,lastname,level,bestscore,lg_usernm,password)


def log_out():
    global firstname,lastname,level,bestscore,lg_usernm,password,count,formatted_qlist,user_ans_list,answers_list
    
    correctn_scroll_text.config(state = 'normal')
    correctn_scroll_text.delete('4.0','end')
    correctn_scroll_text.insert(tk.END,'\n\n')
    correctn_scroll_text.config(state = 'disable')

    count = 0
    firstname ,lastname,level,bestscore,lg_usernm,password = '','','','','',None
  
    stu_login_pg.tkraise()

######### End dashboard functions


######### Start MAIN TEST functions


def neg_isdigit(str_digit):
    if str_digit.startswith('-'):
        str_digit = str_digit[1:]
    return str_digit.isdigit()

def move_next():
    global count
    if  count < len(pages)-1:
        # print(f'\ncount value before next is {count}\n')
        if neg_isdigit(ans_entry_lst[count].get()):
            count +=1
#            err_msgs[count].set('')
            pages[count].tkraise()
        else:
            showerror('Input Value Error','ANSWER CAN ONLY BE AN INTEGER')
#            err_msgs[count].set('ANSWER CAN ONLY BE AN INTEGER')
        
        # print(f'\ncount value after next is {count}\n')
        
def move_prev():
    global count
    if  count > 0:
        # print(f'\ncount value before previous button is {count}\n')
        count -=1
        pages[count].tkraise()
        # print(f'\ncount value after previous button is {count}\n')

def create_quest_pgs(pages_no = 3):
    global pages,question_str_lst,ans_entry_lst,err_msgs
    
    for i in range(pages_no):
        pages_dict[f'page{i}'] = tk.Frame(frame , bg ='white')

        pages_dict[f'page{i}'].place(relheight=0.95 , relwidth=0.95 ,relx=.025 ,rely=.025)
        
        question_no =tk.Label(pages_dict[f'page{i}'],text = f"QUESTION {i+1}:",font=("Arial Bold",20)  ,  bg = 'white', fg='black')
        question_no.place(x = 15 , y=100)
        
        str_var_dict[f'question_str{i}'] = tk.StringVar(value = "")

        question =tk.Label(pages_dict[f'page{i}'],textvariable = str_var_dict[f'question_str{i}'],font=("Arial Bold",20)  ,  bg = 'white', fg='black')
        question.place(x = 15 , y=150)

        ans_lb =tk.Label(pages_dict[f'page{i}'],text = 'ANSWER:',font=("Arial Bold",20) ,  bg = 'white', fg='black')
        ans_lb.place(x = 15 , y=300)

# tk.Entry(stu_login_pg,width = 15, )
        ans_entry_dict[f'answer{i}'] =  tk.Entry(pages_dict[f'page{i}'],width = 15,font=("Arial Bold",15))
        ans_entry_dict[f'answer{i}'].place(x = 200 , y=300)

        # err_msg_dict[f'err_msg1{i}'] = tk.StringVar(value = "")
        # err_msg1_lb =tk.Label(pages_dict[f'page{i}'],textvariable = err_msg_dict[f'err_msg1{i}'],font=("Arial Bold",20)  ,  bg = 'yellow', fg='red')
        # err_msg1_lb.place(x = 15 , y=250,height= 50)


        if i == (pages_no-pages_no):
            next_btn = tk.Button(pages_dict[f'page{i}'],text='Next' ,pady=10,width=8,bg='#1847f2',fg = 'white',
            font=('Bold',12), command= move_next)
            next_btn.place(x = 350 , y=400)

        elif i == (pages_no-1):
            previous_btn = tk.Button(pages_dict[f'page{i}'],text='Previous' ,pady=10,width=8,bg='#1877f2',fg = 'white',
            font=('Bold',12), command = move_prev)
            previous_btn.place(x = 20 , y=400)

            submit_btn = tk.Button(pages_dict[f'page{i}'],text='Submit' ,pady=10,width=8,bg='#1847f2',fg = 'white',
            font=('Bold',12), command= submit_func)
            submit_btn.place(x = 350 , y=400)

        else:
            previous_btn = tk.Button(pages_dict[f'page{i}'],text='Previous' ,pady=10,width=8,bg='#1877f2',fg = 'white',
            font=('Bold',12), command = move_prev)
            previous_btn.place(x = 20 , y=400)
    
            next_btn = tk.Button(pages_dict[f'page{i}'],text='Next' ,pady=10,width=8,bg='#1847f2',fg = 'white',
            font=('Bold',12), command= move_next)
            next_btn.place(x = 350 , y=400)

    ############ lists
    pages = list(pages_dict.values())
    question_str_lst = list(str_var_dict.values())
    ans_entry_lst = list(ans_entry_dict.values())
#    err_msgs = list(err_msg_dict.values())

    ########## End lists

def start_test():   
    
    global answers_list,question_list,formatted_qlist,start_time

    create_quest_pgs(pages_no = 3)
    formatted_qlist = []
    
    # level = level1.get()
    question_ans_dict = gen_quests(operators,level,3)
#    print('\n\n',question_ans_dict,'\n\n')

    answers_list = list(question_ans_dict.keys())

    question_list = list(question_ans_dict.values())

    for q_count in range(len(question_list)):
        question_unit = question_list[q_count]

        left_no  = question_unit[0]
        operator = ops_sign_dict[question_unit[1]]
        right_no = question_unit[2]

        question_str = f'({left_no})  {operator}  ({right_no})'

        formatted_qlist.append(question_str)
#        print('\n\n',len(question_str_lst),q_count,'\n\n')
        
        question_str_lst[q_count].set(question_str)
    # print('Formatted Questions:',formatted_qlist,'\n')
    # print('Correct Answers List:',answers_list,'\n')

    pages[count].tkraise()

    start_time =  str(datetime.now()).split('.')[0]



def submit_func():

    # start_date,start_time
    global new_result, user_ans_list,end_time
    user_ans_list = []

    if neg_isdigit(ans_entry_lst[count].get()):
        new_result = 0
        for ans_no in range(len(answers_list)):
            user_ans_list.append(int(ans_entry_lst[ans_no].get()))
            if answers_list[ans_no] == int(ans_entry_lst[ans_no].get()):
                new_result+=1
            else:
                pass
        for ii in ans_entry_lst:
            ii.delete(first = 0,last = tk.END)
#        print(answers_list,'\n')
        # print('User Answers List',user_ans_list,'\n')
        # print('New Result',new_result,'\n')
        score_.set(new_result)
        end_time =  str(datetime.now()).split('.')[0]

        upd_student_result()
        # upd_result_file()
        # score_.set(new_result)
        correctn_frame.tkraise()
        score_pg.tkraise()
    else:

        showerror('Input Value Error','ANSWER CAN ONLY BE AN INTEGER')
 #       err_msgs[count].set('ANSWER CAN ONLY BE AN INTEGER')
        
######### End MAIN TEST functions

######### Start UPDATE functions

def upd_student_result():
    mongoc = pymongo.MongoClient(my_mongo_api)
    db = mongoc['Students_database']

    db[f"{lg_usernm}_result"].insert_one({'start_time':start_time,'end_time':end_time,'score':new_result})
 #   print(best_score)
    if new_result >= bestscore:
        db['Students_coll'].update_one({'username':lg_usernm},
        {'$set':{'bestscore':new_result,'start_time':start_time,'end_time':end_time}})


def upd_correction_pg():
    global formatted_qlist,answers_list,user_ans_list
#    
    

    for i in range(len(formatted_qlist)):
        quest_corrtn_lb = formatted_qlist[i]
        if user_ans_list[i] == answers_list[i]:
            user_ans_lb = f"{user_ans_list[i]}  (correct)"
        else:
            user_ans_lb = f"{user_ans_list[i]}  (incorrect)"
        corr_ans_lb = answers_list[i]

        input_str = f' {quest_corrtn_lb}\t\t\t{user_ans_lb}\t\t\t\t{corr_ans_lb}\n\n'
        correctn_scroll_text.config(state = 'normal')
        correctn_scroll_text.insert(tk.END,input_str)
    correctn_scroll_text.config(state = 'disable')
    text_corr_frame.tkraise()
    
#goto_dashb,stu_dashbrd_pg

def goto_dashb():
    global count,formatted_qlist,user_ans_list,answers_list
    correctn_scroll_text.config(state = 'normal')
    correctn_scroll_text.delete('4.0','end')
    correctn_scroll_text.insert(tk.END,'\n\n')
    correctn_scroll_text.config(state = 'disable')
    count =0
    # formatted_qlist = []
    # user_ans_list= []
    # answers_list = []
    stu_dashbrd_pg.tkraise()

   
    
######### End UPDATE functions

#### CONTINUE FROM SHOW SCORE AND SHOW RESULT PAGE.

#################### MAIN GUI PART ################################################################################
###################################################################################################################
###################################################################################################################

my_app = tk.Tk()
my_app.title("EDUSOFT TEST APP")

canvas = tk.Canvas(my_app ,height=1500 , width=1000 ,bg='#1877f2', bd = 6)
canvas.pack()

frame = tk.Frame(canvas , bg ='grey')
frame.place(relheight=0.95 , relwidth=0.98 ,relx=.025 ,rely=.025)



########### Start student login page
stu_login_pg = tk.Frame(frame , bg ='white')
stu_login_pg.place(relheight=0.95 , relwidth=0.95 ,relx=.025 ,rely=.025)

lg_usernm_lb =tk.Label(stu_login_pg,text = "Username:",font=("Arial Bold",15)  ,  bg = 'white')
lg_usernm_entry =  tk.Entry(stu_login_pg,width = 15,font=("Arial Bold",15) )
lg_usernm_lb.place(x = 15 , y=100)
lg_usernm_entry.place(x = 150 , y=100)

# 

lg_usr_pswd_lb =tk.Label(stu_login_pg,text = "Password:",font=("Arial Bold",15)  ,  bg = 'white')
lg_usr_pswd_entry =  tk.Entry(stu_login_pg,width = 15,font=("Arial Bold",15), show = '*' )
lg_usr_pswd_lb.place(x = 15 , y=150)
lg_usr_pswd_entry.place(x = 150 , y=150)


lg_stu_btn = tk.Button(stu_login_pg,text='Login' ,pady=10,width=8,bg='#1847f2',fg = 'white',
font=('Bold',12), command= stu_login_)
lg_stu_btn.place(x = 350 , y=300)
########### End student login page


####### Start Student dashboard page 
stu_dashbrd_pg =  tk.Frame(frame , bg ='#0288d1')
stu_dashbrd_pg.place(relheight=0.95 , relwidth=0.95 ,relx=.025 ,rely=.025)

img_label2 = tk.Label(stu_dashbrd_pg)
img_label2.place(relheight=0.3 , relwidth=0.3 ,relx=.4 ,rely=.05)

img02 = Image.open("user_icon.png")
img2 = ImageTk.PhotoImage(img02)
img_label2.config(image = img2)

# greeting = tk.StringVar(value ='')
# level1 = tk.IntVar(value =0)

start_test_btn = tk.Button(stu_dashbrd_pg,text='Start test' ,pady=10,width=8,bg='#1847f2',fg = 'white',
font=('Bold',18), command=  start_test)
start_test_btn.place(relheight=0.1 , relwidth=0.2 ,relx=.45 ,rely=.8)

reset_pswd_btn = tk.Button(stu_dashbrd_pg,text='Reset\nPassword' ,pady=10,width=8,bg='#1847f2',fg = 'white',
font=('Bold',18), command= open_popup)
reset_pswd_btn.place(relheight=0.1 , relwidth=0.2 ,relx=.75 ,rely=.05)

logout_btn = tk.Button(stu_dashbrd_pg,text='LOGOUT' ,pady=10,width=8,bg='#1847f2',fg = 'white',
font=('Bold',18), command= log_out)
logout_btn.place(relheight=0.1 , relwidth=0.2 ,relx=.1 ,rely=.05)

####### End Student dashboard page 


correctn_frame = tk.Frame(frame , bg ='blue')
correctn_frame.place(relheight=0.975 , relwidth=0.975 ,relx=.015 ,rely=.015)


#### Start Show score page
score_pg = tk.Frame(correctn_frame , bg ='blue')
score_pg.place(relheight=0.8 , relwidth=0.975 ,relx=.015 ,rely=.015)

label_a =tk.Label(score_pg,text= "Your Score",font=("Arial Bold",50),bg = 'blue')# width=1,height=1)
label_a.place(relx=.3,rely=.05)

score_ = tk.IntVar(value =0)
score_lb =tk.Label(score_pg,textvariable= score_,font=("Arial Bold",150),bg = 'blue')# width=1,height=1)
score_lb.place(relx=.4,rely=.2)

#score_lb.place(x = 20+(circle_size/4)+10, y=20+(circle_size/4)-25)
corr_pg_btn = tk.Button(score_pg,text='See\nCorrection' ,pady=10,width=8,bg='white',fg = 'black',
font=('Bold',12), command= upd_correction_pg)
corr_pg_btn.place(relheight=0.1 , relwidth=0.2 ,relx=.35 ,rely=.8)

###### End Show score page

# Start correction section

text_corr_frame = tk.Frame(correctn_frame , bg ='#1877f2')
text_corr_frame.place(relheight=0.8 , relwidth=0.9 ,relx=.015 ,rely=.015)

# #Add a Vertical Scrollbar
my_scrollbary = tk.Scrollbar(text_corr_frame)
my_scrollbary.pack(side= tk.RIGHT,fill="y")

# #Add a Horizontal Scrollbar
my_scrollbarx = tk.Scrollbar(text_corr_frame, orient= tk.HORIZONTAL)
my_scrollbarx.pack(side= tk.BOTTOM, fill= "x")

correctn_scroll_text= tk.Text(text_corr_frame, height=33,width=60, yscrollcommand= my_scrollbary.set,\
 xscrollcommand = my_scrollbarx.set, wrap= tk.NONE, font=("Arial Bold",15),bg = '#1877f2')
correctn_scroll_text.pack(fill = tk.BOTH, expand=1)

my_scrollbarx.config(command = correctn_scroll_text.xview)
my_scrollbary.config(command = correctn_scroll_text.yview)

correctn_scroll_text.insert(tk.END,'\t\t\tCORRECTIONS\n\n')
correctn_scroll_text.insert(tk.END,' QUESTIONS\t\t\tUSER ANSWERS\t\t\tCORRECT ANSWERS\n\n')

logout_btn2 = tk.Button(correctn_frame,text='Log Out' ,pady=10,width=8,bg='white',fg = 'black',
font=('Bold',18), command= log_out)
logout_btn2.place(relheight=0.1 , relwidth=0.2 ,relx=.1 ,rely=.85)


goto_dashb_btn = tk.Button(correctn_frame,text='Go to\ndashboard' ,pady=10,width=8,bg='white',fg = 'black',
font=('Bold',18), command= goto_dashb)
goto_dashb_btn.place(relheight=0.1 , relwidth=0.2 ,relx=.75 ,rely=.85)

########### End Correction section



##### Question pages dict

pages_dict  = {}
str_var_dict = {}
ans_entry_dict = {}
err_msg_dict = {}


#score_pg.tkraise()
#text_corr_frame.tkraise()
stu_login_pg.tkraise()

my_app.mainloop()
