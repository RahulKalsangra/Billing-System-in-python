from tkinter import *
from tkcalendar import *
import sqlite3 as sq
from tkinter import ttk
from datetime import date
class billing:
        def __init__(self):
            self.product_code=None
            self.product_name=None
            self.product_price=None
            self.product_quantity=None
            self.product_amount=None
            self.total_amount=None
            self.customer_id=None
            self.customer_name=None
            self.customer_no=None
            self.d1=None
            self.cnt=None
            self.today=None
            self.frame=None
            self.scroll=None
            self.listbox=None
            self.root=None
            self.product_label=None
            self.quatity_label=None
            self.listbox_product=None
            self.listbox_quantity=None
            self.listbox_price=None
            self.delivery_checkbox=None
            self.delivery_checkbox_value=False
            self.delivery_checkbox_state=None
            self.item_list=[]
            self.price_list=[]
            self.quantity_list=[]
        def add_cart(self):
            
            if self.current_stock >= int(self.product_quantity.get()) :
            
                self.item_list.append(self.product_name.get())
                self.quantity_list.append(self.product_quantity.get())
                self.price_list.append(float (self.product_price.get())*float(self.product_quantity.get()))
        
                self.listbox_product.insert('end',self.product_name.get())
                self.listbox_quantity.insert('end',self.product_quantity.get())
                self.listbox_price.insert('end',str(float (self.product_price.get())*float(self.product_quantity.get())))
        
        
                
                self.product_amount=Label(text="RS "+str(self.price_list[-1]))
                self.product_amount.place(x=160,y=620)
        
                total=0
                for i in range(len(self.item_list)):
                    
                    total=total+float(self.price_list[i])
                    
                
                total='%.2f'%total
                self.total_amount=Label(text="RS "+str(total))
                self.total_amount.place(x=160,y=670)
                self.product_code.delete(0,'end')
                self.product_price.delete(0,'end')
                self.product_quantity.delete(0,'end')
            else:
                messagebox.showerror('out of stock','Required quantity unavailable.\n current stock {} kg'.format(self.current_stock))
                self.root.focus_force()
    
    
    
       
        def reset(self):
            self.customer_name.delete(0, 'end')
            self.product_name.delete(0,'end')
            self.customer_id.delete(0,'end')
            self.customer_name.delete(0,'end')
            self.customer_no.delete(0,'end')
            self.product_code.delete(0,'end')
            self.product_price.delete(0,'end')
            self.product_quantity.delete(0,'end')
            self.product_name.delete(0,'end')
            self.product_amount.config(text='Rs ..........')
            
            
            
        def remove(self):
            index1 = self.listbox_price.curselection()
            index2 = self.listbox_product.curselection()
            index3 = self.listbox_quantity.curselection()
            f=0
    
            if index1:
                self.index=index1
                f=1 
            elif index2:
                self.index=index2
                f=1
            elif index3:
                self.index=index3
                f=1
            if f==1:
                removed_price=self.listbox_price.get(self.index,self.index)
                amount_price=self.total_amount.cget('text').split()
                self.total_amount['text']='Rs 00000'
                deducted_price=float(amount_price[-1])-float(removed_price[0])
                if deducted_price==0:
                    self.total_amount['text']='Rs .........'
                    amount_price.pop()
                    amount_price.append('0')
                else:
                    self.total_amount['text']='Rs 0'+str(deducted_price)
                
                self.product_amount.config(text='Rs ..........')
                print(self.index[0])
                self.listbox_product.delete(self.index)
                self.listbox_quantity.delete(self.index)
                self.listbox_price.delete(self.index)
                self.item_list.pop(self.index[0])
                self.price_list.pop(self.index[0])
                self.quantity_list.pop(self.index[0])
                
       
            
    
    
    
        def done_bill(self):
            
            conn=sq.connect('register.db')
            c=conn.cursor()
            c.execute("""create table if not exists bill(id text,customer_id text,date text,home_delivery text,total text)""")
            c.execute("""create table if not exists sales(bill_id text,product_name text,product_qty text,product_amt text)""")
            c.execute("""select count (id) from bill""")
            self.cnt=c.fetchone()
            
            total=0
            for i in range(len(self.item_list)):
                c.execute("""insert into sales values('{0}','{1}','{2}','{3}')""".format('Inv'+str(self.cnt[0]),self.item_list[i],self.quantity_list[i],str(self.price_list[i])))
            
                total+=self.price_list[i]
            home_delivery='No'
            
            if self.delivery_checkbox_value:
                home_delivery='Yes'
            else:
                home_delivery='No'
            
            c.execute("""insert into bill values('{0}','{1}','{2}','{3}','{4}')""".format('Inv'+str(self.cnt[0]),self.customer_id.get(),str(self.d1),home_delivery,str(total)))
            c.execute(""" select address from customer_detail where id=='{}' """.format(self.customer_id.get()))
            add=c.fetchone()
            add=add[0]
            conn.commit()
            
            billno=Label(self.root,text='Inv'+str(self.cnt[0]))
            billno.place(x=160,y=60)
            unitprice=[]
            
            for i in range(len(self.item_list)):
                unitprice.append(float(self.price_list[i])/float(self.quantity_list[i]))
                c.execute(""" update product set current_stock = '{}' where name = '{}' """.format(str( self.current_stock - int ( self.quantity_list[i] ) ) , self.item_list[i] ))
                conn.commit()
            conn.close() 
            self.generateInvoice('Inv'+str(self.cnt[0]),str(self.d1),self.customer_name.get(),add,self.item_list,self.quantity_list,unitprice,self.price_list)
            self.reset()
            self.listbox_price.delete(0,END)
            self.listbox_product.delete(0,END)
            self.listbox_quantity.delete(0,END)
            self.item_list=[]
            self.price_list=[]
            self.quantity_list=[]
            
            self.total_amount.config(text='Rs ..........')
            messagebox.showinfo('success' , 'Bill generated and saved to yor directory')
            self.root.destroy()
            
            
        
        def generateInvoice(self,Inid,date,name,add,item,qty,unitprice,amt):
            from fpdf import FPDF
             
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("courier", size=25)
            
            pdf.cell(200, 10, txt="Guru Sampoorna", ln=1, align="C")
            pdf.set_line_width(1)
            pdf.rect(10,5,190,275)
            pdf.set_line_width(0)
            pdf.line(10,40,200,40)
            
            pdf.set_font('courier',size=12)
           
            
            pdf.set_left_margin(150) 
            pdf.cell(200,10,txt="Bengali chouraha ",ln=1,align='F')                                  
            pdf.cell(200,10,txt="Mob No- 8962727182",ln=1,align='F')
            
            pdf.set_left_margin(10)
            pdf.cell(200,5,txt=" ",ln=1,align='F')
                
            pdf.cell(200,10,txt="    Invoice No - {}\n    ".format(Inid),ln=1,align='F')
            
            pdf.cell(200,10,txt="    Date - {}".format(date),ln=1,align='F')
            
            pdf.cell(200,10,txt="    Customer Name - {}".format(name),ln=1,align='F')
            
            pdf.cell(200,10,txt="    Customer Address - {}".format(add),ln=1,align='F')
            
            
            pdf.line(10,85,200,85)
            pdf.cell(200,5,txt=" ",ln=1,align='F')
            pdf.set_font_size(20)
            pdf.set_font('courier',style='BI',size=20)
            pdf.cell(200,10,txt="List of Items",ln=1,align='C')
            pdf.set_font('courier',size=12)
            pdf.cell(200,5,txt='',ln=1)
            
            data = [['Product', 'Amount (in Kg.)', 'Price per Kg', 'Amount']]
            total=0
            for i in range(len(item)):
                list1=[item[i],qty[i],unitprice[i],amt[i]]
                total+=float(amt[i])
                data.append(list1)
    
            pdf.set_left_margin(20)
            col_width = pdf.w / 5
            row_height = pdf.font_size+1
            for row in data:
                    for item1 in row:
                        pdf.cell(col_width, row_height,txt=str(item1), border=1)
                    pdf.ln(row_height*1)
                    
            pdf.set_font(family='courier',style='B')
            pdf.cell(col_width*3,row_height,txt='Total',border=1,align='C')
            
            pdf.cell(col_width,row_height,txt=str(total),border=1)
            pdf.set_left_margin(140)
            pdf.cell(200,15,txt='',ln=1)
            pdf.set_font('courier',style='BI',size=15)
            pdf.cell(100,10,txt='Seal (Guru Sampoorna)',ln=1)
            InvoiceName="Invoice-"+Inid+".pdf";
            pdf.output(InvoiceName)
            
        def layout(self):
            self.root = Tk()
            self.root.title("Guru Sampoorna")
          
            main_menu=Menu(self.root)
     
            #top=Toplevel(self.root)
            #cal=Calendar(top,font="Arial 14",selectmode="day")
            #cal.get_date()
            #cal.pack(fill="both",expand=True)
    
    
            file_menu=Menu(main_menu)
            file_menu = Menu(main_menu, tearoff=0)
    
            main_menu.add_cascade(label="File" , menu=file_menu)
    
    
            file_menu.add_command(label="New")
            file_menu.add_command(label="Open")
            file_menu.add_command(label="Save")
            file_menu.add_command(label="Save As")
    
            edit_menu=Menu(main_menu)
            edit_menu = Menu(main_menu, tearoff=0)
            main_menu.add_cascade(label="Edit",menu=edit_menu)
            self.root.config(menu=main_menu)
    
            frame1 = Frame(self.root, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=300, height=120, bd= 0)
    
            label1=Label(frame1,text="Invoice No :")
            label1.place(x=10,y=20)
            
            label2=Label(frame1,text="Invoice Date :")
            label2.place(x=10,y=70)
            #entry2=Entry(frame1)
            self.today=date.today()
            self.d1 = self.today.strftime("%d/%m/%Y")
            entry2=Label(self.root,text=self.d1)
            entry2.place(x=143,y=109)
    
    
    
    
            frame1.place(x=10,y=40)
    
    
    
    
    
            frame2 = Frame(self.root, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=500, height=170, bd= 0)
            
            self.customer_id=Label(frame2,text="Customer Id :")
            self.customer_id.place(x=10,y=20)
    
            self.customer_id=Entry(frame2)
            self.customer_id.place(x=140,y=20)
    
            self.customer_name=Label(frame2,text="Customer Name :")
            self.customer_name.place(x=10,y=70)
            
            
            self.number= StringVar() 
            self.customer_name=ttk.Combobox(self.root, width=30, textvariable=self.number, state = 'readonly')
            self.customer_name['values']=self.getCustomerList()
            self.number.trace('w',self.changed)
            self.customer_name.bind("<<ComboboxSelected>>", self.nameSelected)
            self.customer_name.place(x=150,y=260)
    
            self.customer_no=Label(frame2,text="Mobile No :")
            self.customer_no.place(x=10,y=120)
    
            self.customer_no=Entry(frame2)
            self.customer_no.place(x=140,y=120)
    
    
    
            frame2.place(x=10,y=190)
    
    
    
            frame3 = Frame(self.root, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=600, height=330, bd= 0)
    
            self.product_code=Label(frame3,text="Product Code :")
            self.product_code.place(x=10,y=20)
    
            self.product_code=Entry(frame3)
            self.product_code.place(x=140,y=20)
    
            self.product_name=Label(frame3,text="Product Name :")
            self.product_name.place(x=10,y=70)
    
            self.product_name=ttk.Combobox(frame3, state = 'readonly')
            self.product_name['values'] = self.getProductList()
            self.product_name.bind("<<ComboboxSelected>>", self.productSelected)
            self.product_name.place(x=140,y=70)
    
            self.product_price=Label(frame3,text="Price :")
            self.product_price.place(x=10,y=120)
    
            self.product_price=Entry(frame3)
            self.product_price.place(x=140,y=120)
    
            self.product_quantity=Label(frame3,text="Quantity :")
            self.product_quantity.place(x=10,y=170)
    
            self.product_quantity=Entry(frame3)
            self.product_quantity.place(x=140,y=170)
    
            self.product_amount=Label(frame3,text="Amount :")
            self.product_amount.place(x=10,y=220)
    
            
    
            self.total_amount=Label(frame3,text="Total Amt :")
            self.total_amount.place(x=10,y=270)
    
            
    
            self.reset_btn=Button(frame3,text="Reset",width=10,command=self.reset)
            self.reset_btn.place(x=450,y=20)
    
            self.add_cart_btn=Button(frame3,text="Add To Cart",width=10,command=self.add_cart)
            self.add_cart_btn.place(x=450,y=60)
    
            self.remove_btn=Button(frame3,text="Remove",width=10,command=self.remove)
            self.remove_btn.place(x=450,y=100)
    
            #self.update_btn=Button(frame3,text="Update",width=10)
            #self.update_btn.place(x=500,y=140)
            delivery_checkbox_value=IntVar()
            self.delivery_checkbox=Checkbutton(frame3,text="Home Delivery",variable=self.delivery_checkbox_state,command=self.set_checkbox)
            self.delivery_checkbox.place(x=450,y=140)
    
            self.done_btn=Button(self.root,text="DONE BILL",width=19,command=self.done_bill)
            self.done_btn.place(x=1140,y=700)
    
            productLabel=Label(self.root,text="Product",font='courier 13 bold').place(x=1000,y=70)
            quantityLabel=Label(self.root,text='Quantity',font='courier 13 bold').place(x=1200,y=70)
            priceLabel=Label(self.root,text="Amount",font='courier 13 bold').place(x=1350,y=70)
    
            frame3.place(x=10,y=400)
    
    
            
            frame4=Frame(self.root)
            self.scroll=Scrollbar(orient='vertical',command=self.vsb)
            self.listbox_quantity=Listbox(frame4,yscrollcommand=self.scroll.set,width=30,height=35,exportselection=0)
            self.listbox_product=Listbox(frame4,yscrollcommand=self.scroll.set,width=30,height=35,exportselection=0)
            self.listbox_price=Listbox(frame4,yscrollcommand=self.scroll.set,width=30,height=35,exportselection=0)
            
            
            self.scroll.pack(side='right',fill='y')
            self.listbox_product.pack(side='left',expand=False)
            self.listbox_quantity.pack(side='left',expand=False)
            self.listbox_price.pack(side='left',expand=False)
    
            
            frame4.place(x=950,y=100)
    
            
    
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry("%dx%d+0+0" % (w, h))
            #self.root.geometry("1020x720")
             
            self.root.mainloop()
        def productSelected(self,a):
            n = self.product_name.get()
            conn = sq.connect('register.db')
            c = conn.cursor()
            c.execute(""" select id, price, current_stock from product where name = '{}'""".format(n))
            data = c.fetchall()  
            self.product_code.delete(0,END)
            self.product_code.insert(0,data[0][0])
            self.product_price.delete(0,END)
            self.product_price.insert(0,data[0][1])
            self.current_stock = int(data[0][2])
            
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
        
        def nameSelected(self,arg):
            #sql()
            n = self.customer_name.get()
            c.execute("select contact,id from customer_detail where name ='{}'".format(n))
            data = c.fetchall()
            self.customer_no.delete(0,END)
            self.customer_no.insert(0,data[0][0])
            self.customer_id.delete(0,END)
            self.customer_id.insert(0,data[0][1])
        def changed(self , a,b,c):
                conn=sq.connect('register.db')
                c=conn.cursor()
                c.execute("select name from customer_detail where name like '%{}%'".format(self.customer_name.get()))
                self.customer_name['values']=c.fetchall()
                conn.close()  
        def getCustomerList(self):
            conn=sq.connect('register.db')
            c=conn.cursor()
            c.execute(""" select name from customer_detail """ )
            l=c.fetchall()
            conn.commit()
            conn.close()
            l=list(l)
            al=[]
            for x in l:
                for i in x:
                    al.append(i)
            
            return al
        def vsb(self,*args):
            self.listbox_product.yview(*args)
            self.listbox_quantity.yview(*args)
            self.listbox_price.yview(*args)
        def set_checkbox(self):
            if self.delivery_checkbox_value:
                self.delivery_checkbox_value=False
            else:
                self.delivery_checkbox_value=True
    
con=sq.connect('register.db')
c=con.cursor()
c.execute('select name from customer_detail')
d1 = c.fetchall()
#print(d1[0][0])
lista=[]
for i in d1:
        #print(i[0])
        lista.append(i[0])
rol =None
sur=""
sur1="aman"
def sql():
        n = bill.customer_name.get()
        print(type(n))
        #print(n)
        c.execute('select contact,id from customer_detail where name =?',(n,))
        data = c.fetchall()
        #print(data[0][1])
        rol = data[0][0]
        #sur=data[0][1]
        sur = str(sur)
        #print(type(sur))
class AutocompleteEntry(Entry):
        def __init__(self, lista, *args, **kwargs):
            
            Entry.__init__(self, *args, **kwargs)
            self.lista = lista        
            self.var = self["textvariable"]
            if self.var == '':
                self.var = self["textvariable"] = StringVar()
    
            self.var.trace('w', self.changed)
            self.bind("<Right>", self.selection)
            self.bind("<Up>", self.up)
            self.bind("<Down>", self.down)
            
            self.lb_up = False
    
        def changed(self, name, index, mode):  
    
            if self.var.get() == '':
                self.lb.destroy()
                self.lb_up = False
            else:
                words = self.comparison()
                if words:            
                    if not self.lb_up:
                        self.lb = Listbox()
                        self.lb.bind("<Double-Button-1>", self.selection)
                        self.lb.bind("<Right>", self.selection)
                        self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                        self.lb_up = True
                    
                    self.lb.delete(0, END)
                    for w in words:
                        self.lb.insert(END,w)
                else:
                    if self.lb_up:
                        self.lb.destroy()
                        self.lb_up = False
            
        def selection(self, event):
    
            if self.lb_up:
                self.var.set(self.lb.get(ACTIVE))
                self.lb.destroy()
                self.lb_up = False
                self.icursor(END)
            #sql()
            n = bill.customer_name.get()
            c.execute("select contact,id from customer_detail where name ='{}'".format(n))
            data = c.fetchall()
            bill.customer_no.delete(0,END)
            bill.customer_no.insert(0,data[0][0])
            bill.customer_id.delete(0,END)
            bill.customer_id.insert(0,data[0][1])
        def up(self, event):
    
            if self.lb_up:
                if self.lb.curselection() == ():
                    index = '0'
                else:
                    index = self.lb.curselection()[0]
                if index != '0':                
                    self.lb.selection_clear(first=index)
                    index = str(int(index)-1)                
                    self.lb.selection_set(first=index)
                    self.lb.activate(index) 
    
        def down(self, event):
    
            if self.lb_up:
                if self.lb.curselection() == ():
                    index = '0'
                else:
                    index = self.lb.curselection()[0]
                if index != END:                        
                    self.lb.selection_clear(first=index)
                    index = str(int(index)+1)        
                    self.lb.selection_set(first=index)
                    self.lb.activate(index) 
    
        def comparison(self):
            pattern = re.compile('.*' + self.var.get() + '.*')
            return [w for w in self.lista if re.match(pattern, w)]
def am():
            data= bill.customer_name.get()
            print(data)
            return data
    
    
    
   
    
    
    
if __name__=='__main__':
    bill= billing()
    bill.layout()
    
    
