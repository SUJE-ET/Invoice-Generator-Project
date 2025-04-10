import tkinter as tk
import datetime
from docxtpl import DocxTemplate
from tkinter import ttk
from tkinter import messagebox

def clear_item():
    qty_spinbox.delete(0,tk.END)
    qty_spinbox.insert(0,"1")
    desc_entry.delete(0,tk.END)
    price_spinbox.delete(0,tk.END)
    price_spinbox.insert(0,"0.0")

invoice_list =[]

def add_item():
    qty = int(qty_spinbox.get())
    desc = desc_entry.get()
    price = float(price_spinbox.get())
    line_total = qty*price
    invoice_item = [qty,desc,price,line_total]
    tree.insert("","end",values=invoice_item)
    clear_item()
    invoice_list.append(invoice_item)
    
def generate_invoice():
    doc = DocxTemplate("invoice_template.docx")
    name = first_name_entry.get()+" "+last_name_entry.get()
    phone = phone_entry.get()
    subtotal = sum(item[3] for item in invoice_list)
    salestax = 0.1
    total = (subtotal*(1+salestax))
    subtotal = f"{subtotal:.2f}"
    total = f"{total:.2f}"

    doc.render({
        "name":name,
        "phone":phone,
        "invoice_list":invoice_list,
        "subtotal":subtotal,
        "salestax":salestax,
        "total":total})
    doc_name="new_invoice"+name+datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")+".docx"
    doc.save(doc_name)
    messagebox.showinfo("Invoice complete","Invoice Complete")
    new_invoice()

def new_invoice():
    first_name_entry.delete(0,tk.END)
    last_name_entry.delete(0,tk.END)
    phone_entry.delete(0,tk.END)
    clear_item()
    tree.delete(*tree.get_children())
    invoice_list.clear()

window = tk.Tk()
window.title("Invoice Generator Form")

frame = tk.Frame(window)
frame.pack(padx=20, pady=10)

first_name_label=tk.Label(frame, text="First Name")
first_name_label.grid(row=0,column=0)
last_name_label= tk.Label(frame, text="Last Name")
last_name_label.grid(row=0,column=1)

first_name_entry = tk.Entry(frame)
last_name_entry = tk.Entry(frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

phone_label = tk.Label(frame, text="Phone Number")
phone_label.grid(row=0, column=2)
phone_entry= tk.Entry(frame)
phone_entry.grid(row=1, column=2)

qty_label= tk.Label(frame, text="Qty")
qty_spinbox=tk.Spinbox(frame, from_=1, to=100)
qty_label.grid(row=2,column=0)
qty_spinbox.grid(row=3,column=0)

desc_label = tk.Label(frame, text="Description")
desc_entry = tk.Entry(frame)
desc_label.grid(row=2,column=1)
desc_entry.grid(row=3,column=1)

price_label = tk.Label(frame, text="Unit Price")
price_spinbox = tk.Spinbox(frame, from_=1, to=500, increment=0.5)
price_label.grid(row=2,column=2)
price_spinbox.grid(row=3,column=2)

add_item_button= tk.Button(frame,text="Add Item", command=add_item)
add_item_button.grid(row=4, column=2, pady=5)

columns =("qty","desc","price","total")
tree = ttk.Treeview(frame, columns=columns, show="headings")
tree.heading("qty",text="Qty")
tree.heading("desc",text="Description")
tree.heading("price",text="Price")
tree.heading("total",text="Total")
tree.grid(row=5,column=0, columnspan=3, padx=20, pady=10)

save_invoice_button = tk.Button(frame,text="Save Invoice", command=generate_invoice)
save_invoice_button.grid(row=6,column=0, columnspan=3, sticky="ewns",padx=20,pady=5)

new_invoice_button = tk.Button(frame,text="New Invoice", command=new_invoice)
new_invoice_button.grid(row=7,column=0, columnspan=3, sticky="ewns",padx=20,pady=5)



window.mainloop()