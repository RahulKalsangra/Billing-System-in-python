# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 08:47:55 2019

@author: Shubh
"""

import tkinter as tk
from tkinter import *
from tkcalendar import *
from tkinter import ttk
import sqlite3 as sq
from Bill_Module import billing
from Add_customer import rpmain
import re
from datetime import date



def main():   
    def deliveryList():
        class delivery:
            def __init__(self):
                self.datepicker=None
                self.tl=None
            def generateDL(self):
                
                import sqlite3 as sq
                
                conn=sq.connect('register.db')
                c=conn.cursor()
                date=self.datepicker.get_date()
                date=str(date)
                pdate=date[-2:]+'-'+date[5:7]+'-'+date[:4]
                date=date[-2:]+'/'+date[5:7]+'/'+date[:4]
                
        
                c.execute(""" select * from bill where home_delivery=='Yes' and date=='{}' """.format(date))
                il=c.fetchall()
            
                c.execute(""" select * from addresslist """)
                al=c.fetchall()
                d={}
                cnt=0
                for a in al:
                    d[a]=cnt
                    cnt+=1
                
                dal=[]
                name=[]
                amt=[]
                for x in il:
                    c.execute(""" select address from customer_detail where id=='{}' """.format(x[1]))
                    
                    dal.append(c.fetchone())
                    c.execute(""" select name from customer_detail where id=='{}' """.format(x[1]))
                    name.append(c.fetchone())
                    amt.append(x[-1])
           
                    
                    
               
                
                for i in range(len(dal)):
                    for j in range(len(dal)-1):
                        if d.get(dal[j])>d.get(dal[j+1]):
                            temp=dal[j]
                            dal[j]=dal[j+1]
                            dal[j+1]=temp
                            
                            tempi=il[j]
                            il[j]=il[j+1]
                            il[j+1]=tempi
                            
                            tempn=name[j]
                            name[j]=name[j+1]
                            name[j+1]=tempn
                
                            tempa=amt[j]
                            amt[j]=amt[j+1]
                            amt[j+1]=tempa
                
                
                
              
                conn.commit()
                conn.close()
                
                from fpdf import FPDF
                 
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("times", size=25)
                
                pdf.cell(200, 10, txt="Guru Sampoorna", ln=1, align="C")
                pdf.set_line_width(1)
                pdf.rect(10,5,190,275)
                pdf.set_line_width(0)
                
                
                pdf.set_font('times',style='BI',size=20)
                pdf.cell(200,10,txt="Dilevery Address List",ln=1,align='C')
                pdf.set_font('times',size=12)
                pdf.cell(200,5,txt='',ln=1)
                
                
                data = [['Customer name', 'Amount','Address']]
                
                total=0
                for i in range(len(name)):
                    list1=[name[i][0],amt[i],dal[i][0]]
                    total+=float(amt[i])
                    data.append(list1)
                
                
                pdf.set_left_margin(20)
                col_width = pdf.w / 5
                row_height = pdf.font_size+1
                column_width=[1.5,0.5,2.2]
                cnt=0
                for row in data:
                        for item in row:
                            pdf.cell(col_width*column_width[cnt], row_height*1,txt=item, border=1)
                            cnt+=1
                            if cnt==3:
                                cnt=0
                        pdf.ln(row_height*1)
                pdf.set_font(family='times',style='B')
                
                
                
                listName="DL-"+pdate+".pdf"
                
                pdf.output(listName)
                
                self.tl.destroy()
                
           
            def layout(self):
                self.tl=tk.Toplevel(root)
                self.tl.title('Select Date')
                
                tk.Label(self.tl,text='Select Date',font=('courier',10)).pack()
                today=date.today()
                d = today.strftime("%d/%m/%Y")
                m=int(d[3:5])
                y=int(d[7:])
                d=int(d[:2])
                self.datepicker = DateEntry(self.tl, width=12, year=y, month=m, day=d, background='green', foreground='white', borderwidth=2)
                self.datepicker.pack(padx=10, pady=10)
                tk.Button(self.tl,text="Generate",bg="green",font=('courier',10),command=self.generateDL).pack()    
                self.tl.geometry("50x100")
        o=delivery()
        o.layout()
    def billingbtn():
        bill = billing()
        bill.layout()
    
    
        
    class addProductClass:
            def addProduct(self):
                self.tl = Toplevel()
                self.tl.focus()
                self.tl.focus_force()
                self.tl.geometry("520x400")
                self.tl.title("Add Product")
                self.tl.withdraw()
                self.tl.update_idletasks()
                number= StringVar() 
                Label(self.tl,text='Product Name',font='courier 13 bold').place(x=0,y=50)
                self.product_name=ttk.Combobox(self.tl, width=30, textvariable=number)
                self.productList = self.getProductList()
                self.product_name['values']= self.productList
                self.product_name.bind("<<ComboboxSelected>>", self.productSelected)
                self.product_name.place(x=150,y=50)
                Label(self.tl,text='(note:- Enter product name for adding new product)',font='courier').place(x=0,y=80)
                Label(self.tl,text='(note:- Select product name for Editing product)',font='courier').place(x=0,y=100)
                Label(self.tl,text='Price per Kg',font='courier 13 bold').place(x=0,y=130)
                self.price_entry = Entry(self.tl)
                self.price_entry.place(x= 150, y =130)
                Label(self.tl,text='Stock (Kg)',font='courier 13 bold ').place(x=0,y=160)
                self.stock_entry = Entry(self.tl)
                self.stock_entry.place(x=150, y= 160)
                Label(self.tl,text='(note:- In case of Editing this stock will be',font='courier').place(x=0,y=190)
                Label(self.tl,text=' addded to current stock.)',font='courier').place(x=0,y=210)

                
                addBtn = Button(self.tl ,text =  'Add Product', width = 20,command = self.addProductBtn ).place(x=50, y=300)
                edtBtn = Button (self.tl , text = 'Edit Product', width =20 , command = self.edtProductBtn).place(x=250 , y=300)
                
                x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 4
                y = (root.winfo_screenheight() - root.winfo_reqheight()) / 4
                self.tl.geometry("+%d+%d" % (x, y))
                self.tl.deiconify()
                self.tl.mainloop()
            def productSelected(self,a):
                #sql()
                n = self.product_name.get()
                conn = sq.connect('register.db')
                c = conn.cursor()
                c.execute(""" select id from product where name = '{}' """.format(n))
                self.pid  = c.fetchall()
                self.pid = self.pid[0][0]
                c.execute("select price,current_stock from product where name ='{}'".format(n))
                data = c.fetchall()
                self.price_entry.delete(0,END)
                self.price_entry.insert(0,data[0][0])
                self.stock_entry.delete(0,END)
                if data[0][1] is None:
                    self.stock_entry.insert(0,'0')
                    self.prev_stock = 0
                else:
                    self.stock_entry.insert(0,data[0][1])
                    self.prev_stock = data[0][1]
                
            def getProductList(self):
                            conn=sq.connect('register.db')
                            c=conn.cursor()
                            c.execute(""" select name from product """ )
                            l=c.fetchall()
                            conn.commit()
                            conn.close()
                            al=[]
                            l=list(l)
                            for x in l:
                                for i in x:
                                    al.append(i)
                            
                            return al
            def addProductBtn(self):
                
                if  len(self.product_name.get().strip()) == 0 :
                    messagebox.showerror("Error", "Product name cannot be empty.")
                    self.tl.focus_force()
                elif len( self.price_entry.get().strip() ) == 0  :
                    messagebox.showerror("Error", "Product price cannot be empty.")
                    self.tl.focus_force()
                elif len( self.stock_entry.get().strip()) == 0:
                    messagebox.showerror("Error", "Product stock cannot be empty.")
                    self.tl.focus_force()
                elif  self.product_name.get().strip().lower() in [ x.lower() for x in self.productList]:
                    messagebox.showwarning('Warning' , 'Cannot add product because product name already exist')
                    self.tl.focus_force()
                else:
                    conn = sq.connect('register.db')
                    c= conn.cursor()
                    c.execute(""" select id from product """)
                    l = c.fetchall()
                    c.execute(""" insert into product values ( {}, '{}' , '{}' , '{}' )  """.format(len(l),self.product_name.get(),self.price_entry.get(),self.stock_entry.get()))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Info', " Product added successfully. ")
                    self.tl.destroy()
            def edtProductBtn(self):
                if self.product_name.get().strip().lower() not in [ x.lower() for x in self.productList]:
                    messagebox.showinfo('Info', 'You are changing product name.')
                    self.tl.focus_force()
                if len( self.price_entry.get().strip() ) == 0  :
                        messagebox.showerror("Error", "Product price cannot be empty.")
                        self.tl.focus_force()
                elif len( self.stock_entry.get().strip()) == 0:
                        messagebox.showerror("Error", "Product stock cannot be empty.")
                        self.tl.focus_force()
                elif self.pid is not None:
                        conn = sq.connect('register.db')
                        c = conn.cursor()
                        current_stock = int(self.stock_entry.get()) + int(self.prev_stock)
                        c.execute(""" update product set name = '{}' , price = '{}' , current_stock = '{}' where id = {} """.format( self.product_name.get(),self.price_entry.get(),str(current_stock), self.pid  ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Info','Product Edited successfully.')
                        self.tl.destroy()
                else:
                    messagebox.showerror('Error', 'Select product from list.')
                    self.tl.focus_force()
    
        
    
    root=tk.Tk()
    addProductObj = addProductClass()
    tk.Label(root,text='Billing Portal',font=('courier',35)).place(x=550,y=10)
    tk.Button(root,text="Add Customer",bg="green",font=('courier',25),command = rpmain).place(x=100,y=200)
    tk.Button(root,text="Billing",bg="green",font=('courier',25),command = billingbtn).place(x=500,y=200)
    tk.Button(root,text="Add/Edit Product",bg="green",font=('courier',25),command = addProductObj.addProduct).place(x=800,y=200)
    tk.Button(root,text="Statistics",bg="green",font=('courier',25)).place(x=100,y=400)
    tk.Button(root,text="Delivery List",bg="green",font=('courier',25),command = deliveryList).place(x=500,y=400)
    
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    root.mainloop()
    
main()