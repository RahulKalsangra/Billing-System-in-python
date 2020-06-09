from tkinter import *
import sqlite3 as sq
from tkinter import messagebox
import re
def rpmain():
    class registerPage:
        def __init__(self):
            self.name_entry=None
            self.cont_entry=None
            self.email_entry=None
            self.zone_entry=None
            self.maddress_entry=None
            self.paddress_entry=None
            self.root = None
            self.address_list=self.getAddressList()
            self.number=None
    
        def submit(self):
            
            if len( self.name_entry.get().strip() ) != 0 and len( self.cont_entry.get().strip() ) != 0 and len( self.email_entry.get().strip() ) != 0 and len( self.maddress_entry.get().strip() ) != 0 and len( self.paddress_entry.get().strip() ) != 0  :
                if self.paddress_entry.get().strip().lower() not in [x.lower() for x in self.address_list] :
                    messagebox.showerror('Error' , 'Please select address from address list')
                    self.root.focus_force()
                else:
                    
                    conn=sq.connect('register.db')
                    c=conn.cursor()
                    c.execute("""create table if not exists customer_detail(id text,name text,contact text,email text,address text)""")
                    
                    count_customer=c.execute("""select count(name) from customer_detail""").fetchall()
                    count_customer=count_customer[0]
                    for cid in count_customer:
                        customer_id=cid
        
                    c.execute("""insert into customer_detail values('{}','{}','{}','{}','{}')""".format("cust:"+str(customer_id),self.name_entry.get().strip(),self.cont_entry.get().strip(),self.email_entry.get().strip(),self.maddress_entry.get().strip()))
                    
                 
                    
                    na=self.paddress_entry.get()
                    nl=[]
                    
                    if na=='First':
                        nl.append(self.maddress_entry.get())
                    for a in range(1,len(self.address_list)):
                        nl.append(self.address_list[a])
                        if self.address_list[a]==na:
                            nl.append(self.maddress_entry.get())
                  
                    c.execute(""" drop table addresslist """)
                    c.execute(""" create table if not exists addresslist (address text) """)
                    for x in nl:
                        c.execute(""" insert into addresslist values ('{}') """.format(x))
                    conn.commit()
                    conn.close()
                    self.paddress_entry['values']=self.getAddressList()
                    self.address_list.append(self.maddress_entry.get().strip())
                    messagebox.showinfo('success','Customer registered successfully')
                    self.root.focus_force()
                    print("saved")
            else:
                messagebox.showerror('Error','Please fillout all details.')
                self.root.focus_force()
                
            
        def layout(self):
            self.root = Tk()
            self.root.title("Guru Sampoorna")
    
            title=Label(self.root,text="Register User")
            labelfont = ('courier', 30, 'bold')
            title.config(font=labelfont)
    
            title.place(x=600,y=20)
    
            label1 =Label(self.root,text="Name ")
            self.name_entry=Entry(self.root)
            self.name_entry.place(x=250,y=80)
            label1font = ('courier', 15)
            label1.config(font=label1font)
            label1.place(x=80,y=80)
    
    
            label2 =Label(self.root,text="Contact No.")
            self.cont_entry=Entry(self.root)
            self.cont_entry.place(x=250,y=160)
            label2font = ('courier', 15)
            label2.config(font=label1font)
            label2.place(x=80,y=160)
    
            label3 =Label(self.root,text="Email ")
            self.email_entry=Entry(self.root)
            self.email_entry.place(x=250,y=240)
            label3font = ('courier', 15)
            label3.config(font=label1font)
            label3.place(x=80,y=240)
    
        
            label5 =Label(self.root,text="Main Address ")
            self.maddress_entry=Entry(self.root)
            self.maddress_entry.place(x=250,y=320)
            label5font = ('courier', 15)
            label5.config(font=label1font)
            label5.place(x=80,y=320)
    
            label6 =Label(self.root,text="Address After ")
            Label(self.root,text='(note:- select address after which you want to keep current address)',font='courier').place(x=500,y=400)
            self.number= StringVar() 
            self.paddress_entry=ttk.Combobox(self.root, width=30, textvariable=self.number, state = 'readonly')
            self.paddress_entry['values']=self.getAddressList()
            
            self.paddress_entry.place(x=250,y=400)
        
            label6font = ('courier', 15)
            label6.config(font=label1font)
            label6.place(x=80,y=400)
    
            btn1=Button(self.root,text="Register",width=10,command=self.submit)
            btn1.place(x=650,y=600)
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry("%dx%d+0+0" % (w, h))
    
            self.root.mainloop()
    
        def getAddressList(self):
            conn=sq.connect('register.db')
            c=conn.cursor()
            c.execute(""" create table if not exists addresslist (address text) """)
            c.execute(""" select * from addresslist """ )
            l=c.fetchall()
            conn.commit()
            conn.close()
            al=['First']
            l=list(l)
            
            for x in l:
                for i in x:
                    al.append(i)
            
            return al
        
        def changed(self,name,index,mode):
                conn=sq.connect('register.db')
                c=conn.cursor()
                c.execute("select * from addresslist where address like '%{}%'".format(self.paddress_entry.get()))
                self.paddress_entry['values']=c.fetchall()
                conn.close()    
    
    obj=registerPage()
    obj.layout()
    obj.number.trace('w',obj.changed)
    
    
if __name__=='__main__':
    rpmain()