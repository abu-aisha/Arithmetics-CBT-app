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

ph = PasswordHasher()





def add_student():
    global username
#    global first_name ,family_name,level,class_,best_score,db
#    username = usernm_entry.deletedelete///??kl

    username = usernm_entry.get().lower()
    def_pswd = def_pswd_entry.get()
    first_name = fstnm_entry.get().title()
    family_name = lstnm_entry.get().title()
    level = level_entry.get()
    levels = ['1','2','3']
    

    if level and username and def_pswd and first_name and family_name:
        if level in levels:
            try:
                mongoc = pymongo.MongoClient('mongodb+srv://abu-aisha:EeuXiZXkmiwCgEOQ@atlascluster.fkahupn.mongodb.net/?retryWrites=true&w=majority')
                db = mongoc['Students_database']

                hash_def_pswd = ph.hash(def_pswd)
                print('\n\n',username,first_name,family_name,level)

                # db['Students_coll'].drop()
                # db['password'].drop()
                # print(db.list_collection_names())

                

                # db['Students_coll'].create_index([('username')], unique = True)
                # db['password'].create_index([('pswd')],unique = True)


                # try:
                

                db['Students_coll'].insert_one({
                    'username':username,
                    'password':hash_def_pswd,
                    'firstname':first_name,
                    'lastname':family_name,
                    'level':level,
                    'bestscore':0
                    })

                db['password'].insert_one({'pswd' :def_pswd})

                usernm_entry.delete(first = 0,last = tk.END)
                def_pswd_entry.delete(first = 0,last = tk.END)
                fstnm_entry.delete(first = 0,last = tk.END)
                lstnm_entry.delete(first = 0,last = tk.END)
                level_entry.delete(first = 0,last = tk.END)
                
                for student in db['Students_coll'].find({},{'_id':0,'password':0}):
                    print(student)

                for pswd in db['password'].find({},{'_id':0}):
                    print(pswd)
                print('\n')

                showinfo('Success',"Successfully added record")

            except pymongo.errors.ConnectionFailure as err:
                # print(err)
                showerror('Connection Error','The Application could not connect to database\nmake sure your internet connection is on and strong.')
            except pymongo.errors.DuplicateKeyError as err:
                # print(err)
                showerror('Duplicate key Error',"A student with the username already exists\nplease use another username.")
            except Exception as err:
                showerror('Error',str(err))

        else:
            showerror('Data Entry Error', 'Level field must be 1,2 or 3')
    else:
        showerror('Fields Required', 'None of the fields can be empty')

def show_table():
    data_fr = tk.Frame(add_stu_pg, bg = 'white')
    data_fr.place(relheight=.5,relwidth=.3,relx=.6,rely=.3)
    try:
        mongoc = pymongo.MongoClient('mongodb+srv://abu-aisha:EeuXiZXkmiwCgEOQ@atlascluster.fkahupn.mongodb.net/?retryWrites=true&w=majority')
        db = mongoc['Students_database']
        ####################################################
        
        student_data = {}
        count = 1
        for student in db['Students_coll'].find({},{'_id':0,'password':0}):
            student_data[f'rec{count}'] = student
            # print(student)
            count+=1
        count =1
        for pswd in db['password'].find({},{'_id':0}):
            student_data[f'rec{count}']['default_password'] = pswd['pswd']
            # print(pswd)
            count +=1
        # print('\n')
        # print(student_data)
        # print('\n')

        # data = {'rec1': {'col1': 99.88, 'col2': 108.79, 'label': 'rec1'},
        #     'rec2': {'col1': 99.88, 'col2': 321.79, 'label': 'rec3'},
        #     'rec3': {'col1': 29.88, 'col2': 408.79, 'label': 'rec2'}
        #     }

        table = TableCanvas(data_fr,data = student_data,read_only=True ,editable= False)
        # print (table.model.columnNames)

        table.show()
    except pymongo.errors.ConnectionFailure as err:
        showerror('Connection Error','The Application could not connect to database\nmake sure your internet connection is on and strong.')
    except Exception as err:
        showerror('Error',str(err))
    # finally:
    #     table = TableCanvas(data_fr,read_only=True ,editable= False)
    #     # print (table.model.columnNames)

    #     table.show()

#################### MAIN GUI PART ################################################################################
###################################################################################################################
###################################################################################################################

my_app = tk.Tk()
my_app.title("EDUSOFT TEST APP")

canvas = tk.Canvas(my_app ,height=1500 , width=1000 ,bg='#1877f2', bd = 6)
canvas.pack()

frame = tk.Frame(canvas , bg ='grey')
frame.place(relheight=0.95 , relwidth=0.95 ,relx=.025 ,rely=.025)


#### Start Teacher add student page 
add_stu_pg = tk.Frame(frame , bg ='white')
add_stu_pg.place(relheight=0.95 , relwidth=0.95 ,relx=.025 ,rely=.025)

usernm_lb =tk.Label(add_stu_pg,text = "Username:",font=("Arial Bold",15)  ,  bg = 'white')
usernm_entry =  tk.Entry(add_stu_pg,width = 15,font=("Arial Bold",15) )
usernm_lb.place(x = 15 , y=100)
usernm_entry.place(x = 150 , y=100)

def_pswd_lb =tk.Label(add_stu_pg,text = "Password:",font=("Arial Bold",15)  ,  bg = 'white')
def_pswd_entry =  tk.Entry(add_stu_pg,width = 15,font=("Arial Bold",15) )
def_pswd_lb.place(x = 15 , y=150)
def_pswd_entry.place(x = 150 , y=150)

fstnm_lb =tk.Label(add_stu_pg,text = "FirstName:",font=("Arial Bold",15)  ,  bg = 'white')
fstnm_entry =  tk.Entry(add_stu_pg,width = 15,font=("Arial Bold",15) )
fstnm_lb.place(x = 15 , y=200)
fstnm_entry.place(x = 150 , y=200)

lstnm_lb =tk.Label(add_stu_pg,text = "LastName:",font=("Arial Bold",15)  ,  bg = 'white')
lstnm_entry =  tk.Entry(add_stu_pg,width = 15,font=("Arial Bold",15) )
lstnm_lb.place(x = 15 , y=250)
lstnm_entry.place(x = 150 , y=250)

level_lb =tk.Label(add_stu_pg,text = "Level:",font=("Arial Bold",15)  ,  bg = 'white')
level_entry =  tk.Entry(add_stu_pg,width = 15,font=("Arial Bold",15))
level_lb.place(x = 15 , y=300)
level_entry.place(x = 150 , y=300)

# best_scr_lb =tk.Label(add_stu_pg,text = "BestScore:",font=("Arial Bold",15)  ,  bg = 'white')
# best_scr_entry =  tk.Entry(add_stu_pg,width = 15)
# best_scr_lb.place(x = 15 , y=350)
# best_scr_entry.place(x = 150 , y=350)

add_stu_btn = tk.Button(add_stu_pg,text='Add Student' ,pady=10,width=8,bg='#1847f2',fg = 'white',
font=('Bold',12), command= add_student)
add_stu_btn.place(x = 350 , y=300)

# goto_stu_lg_pg = tk.Button(add_stu_pg,text='Go to Student Login Page' ,pady=10,width=20,bg='#1847f2',fg = 'white',
# font=('Bold',12), command= goto_stu_lg)
# goto_stu_lg_pg.place(relx=.65 ,rely=.05)

show_stu_sht_btn = tk.Button(add_stu_pg,text='View student sheets' ,pady=10,width=20,bg='#1847f2',fg = 'white',
font=('Bold',12), command= show_table)
show_stu_sht_btn.place(relx=.65 ,rely=.10)

###### End Teacher add student page


my_app.mainloop()




