import tkinter as tk

root = tk.Tk()

# if you want to stack sections which both have elements inside of them then use frames
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

# now the individual elements inside of the frames
label1 = tk.Label(frame1, text="label1")
label2 = tk.Label(frame1, text="label2")
entry1 = tk.Entry(frame1)
entry2 = tk.Entry(frame1)
button1 = tk.Button(frame2, text="button1")
button2 = tk.Button(frame2, text="button2")

# packing the elements inside of the frames
label1.grid(row=0, column=0)
entry1.grid(row=0, column=1)
label2.grid(row=1, column=0)
entry2.grid(row=1, column=1)
button1.pack()
button2.pack()

# packing the frames inside of the root window
frame1.pack(side=tk.LEFT)
frame2.pack(side=tk.LEFT)


root.mainloop()

