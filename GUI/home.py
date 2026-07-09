import tkinter as tk    

root = tk.Tk()

def dothis():
    print("g")

w = int(root.winfo_screenwidth() * 0.8)
h = int(root.winfo_screenheight() * 0.8)

root.geometry(f"{w}x{h}")

button = tk.Button(root,text="click me",command = dothis)
button.grid(row = 1,column = 1)

label1 = tk.Button(root,text = "label1 , the best label")
label1.grid(column=1,row=2)
root.mainloop()
