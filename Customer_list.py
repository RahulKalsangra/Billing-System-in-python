import sqlite3 as sq
from tkinter import *

class customer:

        def __init__(self):
            self.listbox=None
            self.root=None
            self.frame=None
            self.scroll=None
            self.top_cont_entry=None
            self.top_email_entry=None
            self.top_maddress_entry=None
            self.top_naddress_entry=None
            self.top_zone_entry=None
            self.top_name_entry=None
            

        def cust_del(self):
            #self.index = self.listbox.curselection()
            #self.listbox.delete(self.index)
            #print(type(self.index[0]))
            #print(self.index[0])
            
            mob=self.listbox.get(ACTIVE).split()
            mob_str=mob[len(mob)-1]
            
            self.listbox=self.listbox.delete(ANCHOR)
            conn=sq.connect('register.db')
            c=conn.cursor()
            c.execute("""delete from detail where contact ='{}'""".format(mob_str) )
            conn.commit()
            conn.close()
            
        def cust_mod(self):
            mob=self.listbox.get(ACTIVE).split()
            mob_str=mob[len(mob)-1]

            conn=sq.connect('register.db')
            c=conn.cursor()
            c.execute("""select * from detail where contact='{}'""".format(mob_str))
            
            data=c.fetchall()

            pop=Toplevel(self.root)

            pop.title("Guru Sampoorna")

            title=Label(pop,text="UPDATE USER DETAILS")
            labelfont = ('times', 30, 'bold')
            title.config(font=labelfont)

            title.place(x=600,y=20)

            label1 =Label(pop,text="Name ")
            self.top_name_entry=Entry(pop)
            self.top_name_entry.insert(0,data[0][1])
            self.top_name_entry.place(x=250,y=80)
            label1font = ('times', 15)
            label1.config(font=label1font)
            label1.place(x=80,y=80)


            label2 =Label(pop,text="Contact No.")
            self.top_cont_entry=Entry(pop)
            self.top_cont_entry.insert(0,data[0][2])
            self.top_cont_entry.place(x=250,y=160)
            label2font = ('times', 15)
            label2.config(font=label1font)
            label2.place(x=80,y=160)

            label3 =Label(pop,text="Email ")
            self.top_email_entry=Entry(pop)
            
            self.top_email_entry.insert(0,data[0][3])
            self.top_email_entry.place(x=250,y=240)
            label3font = ('times', 15)
            label3.config(font=label1font)
            label3.place(x=80,y=240)

            label4 =Label(pop,text="Zone ")
            self.top_zone_entry=Entry(pop)
            self.top_zone_entry.insert(0,data[0][4])
            self.top_zone_entry.place(x=250,y=320)
            label4font = ('times', 15)
            label4.config(font=label1font)
            label4.place(x=80,y=320)

            label5 =Label(pop,text="Main Address ")
            self.top_maddress_entry=Entry(pop)
            self.top_maddress_entry.insert(0,data[0][5])
            self.top_maddress_entry.place(x=250,y=400)
            label5font = ('times', 15)
            label5.config(font=label1font)
            label5.place(x=80,y=400)

            label6 =Label(pop,text="Neighbour Address ")
            self.top_naddress_entry=Entry(pop)
            self.top_naddress_entry.insert(0,data[0][6])
            self.top_naddress_entry.place(x=250,y=480)
            label6font = ('times', 15)
            label6.config(font=label1font)
            label6.place(x=80,y=480)

            save=Button(pop,text="SAVE CHANGES",width=15,command=self.top_save_changes(data))
            save.place(x=650,y=600)


            

            pop.grid()



        def Entry(self):   
            self.root = Tk()
            self.root.title("Guru Sampoorna")
            conn=sq.connect('register.db',)
            c=conn.cursor()
            c.execute("""select * from detail""")


            customer_name=Label(self.root,text="NAME",font='Helvetica 13 bold')
            customer_name.place(x=100,y=100)

            customer_mobile=Label(self.root,text="ADDRESS",font='Helvetica 13 bold')
            customer_mobile.place(x=310,y=100)

            zone=Label(self.root,text="ZONE",font='Helvetica 13 bold')
            zone.place(x=510,y=100)

            maddress=Label(self.root,text="MOBILE",font='Helvetica 13 bold')
            maddress.place(x=710,y=100)

            add_btn=Button(self.root,text="ADD",width=10)
            add_btn.place(x=1100,y=200)

            del_btn=Button(self.root,text="DELETE",width=10,command=self.cust_del)
            del_btn.place(x=1100,y=300)

            modify_btn=Button(self.root,text="MODIFY",width=10,command=self.cust_mod)
            modify_btn.place(x=1100,y=400)




            self.frame=Frame(self.root)
            self.scroll=Scrollbar(self.frame)
            self.scroll.pack(side=RIGHT,fill=Y)

            

            conn=sq.connect('register.db',)
            c=conn.cursor()
            c.execute("""select * from detail""")
            data=c.fetchall()

            self.listbox=Listbox(self.frame,yscrollcommand=self.scroll.set,width=150,height=30)
            self.listbox.pack()
            for x in data:
                
                self.listbox.insert(END,x[1],x[5],x[4],x[2])
                self.listbox.pack(side=LEFT)

            self.scroll.config(command=self.listbox.yview)
            self.frame.place(x=100,y=130)
            #list Box Ended

            conn.commit()
            conn.close()
            self.root.geometry("800x3400")
            self.root.mainloop()

        def top_save_changes(self,data):
            conn=sq.connect('register.db',)
            c=conn.cursor()
            c.execute("""select id from detail where name = '{}' and contact = '{}'""".format((data[0][1]),(data[0][2])))
            id_d = c.fetchall()

            #id=self.listbox.get(ACTIVE).split()
            #id=id[0]
            print(id_d[0][0])

            if (len(self.top_name_entry.get())==0 or len(self.top_cont_entry.get())==0 or len(self.top_email_entry.get())==0 or len(self.top_zone_entry.get()) == 0 or len(self.top_maddress_entry.get())==0 or len(self.top_naddress_entry.get())==0): 
                messagebox.showinfo("ALERT","Field Cant Be Empty")
            


            c.execute("""update detail set name='{}',contact='{}',email='{}',zone='{}',maddress='{}',naddress='{}' where id='{}'""".format(self.top_name_entry.get(),self.top_cont_entry.get(),self.top_email_entry.get(),self.top_zone_entry.get(),self.top_maddress_entry.get(),self.top_naddress_entry.get(),id_d[0][0]))
            #c.execute("""update detail set name='Rakfd' where id='A0'""")
            
            c.execute("""select * from detail where id = ?""",(id_d[0][0],))
            d= c.fetchall()
            print(self.top_name_entry.get(),self.top_cont_entry.get(),self.top_email_entry.get(),self.top_zone_entry.get(),self.top_maddress_entry.get(),self.top_naddress_entry.get(),id_d[0][0])
            conn.commit()
            conn.close()


ob=customer()
ob.Entry()
