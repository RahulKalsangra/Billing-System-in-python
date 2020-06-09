from tkinter import *
import sqlite3 as sq
from tkinter import messagebox


class add_product:
   def __init__(self):
       self.product_name_entry=None
       self.product_price_entry=None
       self.frame=None
       self.scroll=None
       self.listbox=None
       self.root=None
       
   def add(self):
        conn=sq.connect('register.db',)
        c=conn.cursor()
        c.execute("""create table if not exists product(id number,name text,price number)""")
        count_item=c.execute("""select count(name) from product""").fetchall()
        count_item=count_item[0]
        for cid in count_item:
            product_id=cid

        if (len(self.product_name_entry.get())==0 or len(self.product_price_entry.get()) == 0): 
            messagebox.showinfo("ALERT","Field Cant Be Empty")
            add(self)
            
                    
        
        c.execute("""insert into product values({},'{}','{}')""".format(product_id, self.product_name_entry.get(),self.product_price_entry.get()))
        

        self.frame=Frame(self.root)
        self.scroll=Scrollbar(self.frame)
        self.scroll.pack(side=RIGHT,fill=Y)
        
        c.execute("""select * from product""")
        data=c.fetchall()

        self.listbox=Listbox(self.frame,yscrollcommand=self.scroll.set,width=50,height=30)

        for x in data:
            self.listbox.insert(END,x[1])
            self.listbox.pack(side=LEFT)

        self.scroll.config(command=self.listbox.yview)
        self.frame.place(x=1000,y=130)
        





        




        conn.commit()
        conn.close()
        
        messagebox.showinfo("DONE","Item Added To list Successfully")
    


   def layout(self):
       
        self.root = Tk()
        self.root.title("Guru Sampoorna")


        title=Label(self.root,text="Add Product")
        labelfont = ('times', 30, 'bold')
        title.config(font=labelfont)
        title.place(x=650,y=10)

        label1 =Label(self.root,text="Product Name ")
        self.product_name_entry=Entry(self.root)
        self.product_name_entry.place(x=250,y=80)
        label1font = ('times', 15)
        label1.config(font=label1font)
        label1.place(x=80,y=80)

        label2 =Label(self.root,text="Product Price ")
        self.product_price_entry=Entry(self.root)
        self.product_price_entry.place(x=250,y=160)
        label2font = ('times', 15)
        label2.config(font=label1font)
        label2.place(x=80,y=160)


        add_btn=Button(self.root,text="--Add--",width=10,command=self.add)
        add_btn.place(x=650,y=400)

        modify_btn=Button(self.root,text="--Modify--",width=10)
        modify_btn.place(x=650,y=500)


        #reading data base in listBOx
        self.frame=Frame(self.root)
        self.scroll=Scrollbar(self.frame)
        self.scroll.pack(side=RIGHT,fill=Y)

        conn=sq.connect('register.db',)
        c=conn.cursor()
        c.execute("""create table if not exists product(id number,name text,price number)""")
        c.execute("""select * from product""")
        data=c.fetchall()

        self.listbox=Listbox(self.frame,yscrollcommand=self.scroll.set,width=50,height=30)

        for x in data:
            self.listbox.insert(END,x[1])
            self.listbox.pack(side=LEFT)

        self.scroll.config(command=self.listbox.yview)
        self.frame.place(x=1000,y=130)
        #list Box Ended

        
        self.root.geometry("800x3400")
        self.root.mainloop()


add_product_obj=add_product()
add_product_obj.layout()
