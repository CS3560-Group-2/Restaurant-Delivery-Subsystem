from tkinter import *
from tkinter import ttk

root = Tk()
root.title("YumRush")
root.geometry("800x600")

# Container holds all pages
container = ttk.Frame(root, padding=(3, 3, 12, 12))
container.pack(fill="both", expand=True)

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Create frames - both must have the SAME parent
mainFrame = ttk.Frame(container)
driverSignInFrame = ttk.Frame(container)
driverSignUpFrame = ttk.Frame(container)

def signInDriver():
    driverSignInFrame.tkraise()

def goBack():
    mainFrame.tkraise()

def signUpDriver():
    driverSignUpFrame.tkraise()

# Put frames in same spot
for frame in (mainFrame, driverSignInFrame, driverSignUpFrame):
    frame.grid(row=0, column=0, sticky=(N, W, E, S))

# Main frame widgets
title = ttk.Label(
    mainFrame,
    text="YumRush",
    font=("Helvetica", 36, "bold"),
)
title.pack(pady=20)
title.grid(column=0, row=0, padx=10, pady=20)
ttk.Label(mainFrame, text="Driver Sign in").grid(column=0, row=2, padx=10, pady=10)
ttk.Button(mainFrame, text="Sign in", command=signInDriver).grid(column=0, row=3, padx=10, pady=10, sticky=W)
ttk.Button(mainFrame, text="sign up", command=signUpDriver).grid(column=0, row=5, padx=10, pady=10, sticky=W)


# Driver sign-in frame widgets
ttk.Label(driverSignInFrame, text="Driver Sign In").grid(column=0, row=2, padx=10, pady=10)
ttk.Entry(driverSignInFrame).grid(column=0, row=3, padx=10, pady=5)
ttk.Entry(driverSignInFrame).grid(column=0, row=4, padx=10, pady=5)
ttk.Button(driverSignInFrame, text="Back", command=goBack).grid(column=0, row=5, padx=10, pady=10, sticky=W)

#Driver Sign-up frame widgets
ttk.Label(driverSignUpFrame, text="Driver Sign Up").grid(column=0, row=2, padx=10, pady=10)
ttk.Label(driverSignUpFrame, text= "First Name").grid(column=0, row=3, padx=10, pady=5)
ttk.Entry(driverSignUpFrame).grid(column=1, row=3, padx=10, pady=5)
ttk.Label(driverSignUpFrame, text="Last Name").grid(column=0, row=4, padx=10, pady=5)
ttk.Entry(driverSignUpFrame).grid(column=1, row=4, padx=10, pady=5)
ttk.Label(driverSignUpFrame, text="License Plate Number").grid(column=0, row=5, padx=10, pady=5)
ttk.Entry(driverSignUpFrame).grid(column=1, row=5, padx=10, pady=5)
ttk.Label(driverSignUpFrame, text="Username").grid(column=0, row=6, padx=10, pady=5)
ttk.Entry(driverSignUpFrame).grid(column=1, row=6, padx=10, pady=5)

ttk.Button(driverSignUpFrame, text="Sign Up").grid(column=1, row=7, padx=10, pady=10, sticky=W)
ttk.Button(driverSignUpFrame, text="Back", command=goBack).grid(column=0, row=7, padx=10, pady=10, sticky=W)

# Show first frame
mainFrame.tkraise()

root.mainloop()
