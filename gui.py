from tkinter import filedialog, messagebox
from tkinter import *
from ps_update import update_db

df = ''
db = ''
ps = ''
psMake = ''
psMSRP = ''
psCOST = ''
psWHOLESALE = ''

root = Tk()
root.geometry('1000x400')
root.title('Price sheet updater')
root.resizable(0,0)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(2, weight=2)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_rowconfigure(9, weight=1)

dfLabelText = StringVar()
dfLabelText.set('Please select a file')
dfLabel = Label(root, textvariable=dfLabelText).grid(row=2, column=1, columnspan=2)

psLabelText = StringVar()
psLabelText.set('Please select a file')
psLabel = Label(root, textvariable=psLabelText).grid(row=3, column=1, columnspan=2)

dbLabelText = StringVar()
dbLabelText.set('Please select a file')
dbLabel = Label(root, textvariable=dbLabelText).grid(row=4, column=1, columnspan=2)


def onClosing():
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        root.destroy()

def onClick(title,types,initialdir,input):
    file = filedialog.askopenfilename(initialdir=initialdir, title=title, filetypes=types)
    if len(file):
        if file.endswith('.csv') and input == 'df':
            global df
            df = file
            dfLabelText.set(df)
            toggleState()
        elif file.endswith('.xlsx') and input == 'ps':
            global ps
            ps = file
            psLabelText.set(ps)
            toggleState()
        elif file.endswith('.DB') and input == 'db':
            global db
            db = file
            dbLabelText.set(db)
            toggleState()
        elif input == 'df' or 'ps' or 'db' and file is not None:
            messagebox.showerror('Filetype Error', 'Incorrect Filetype')
            return
        

def toggleState(*args):
    if psWActive.get():
        psWHOLESALE['state'] = NORMAL
        if df and ps and db and psCOST.get() and psMSRP.get() and psMake.get() and psModel.get() and psWHOLESALE.get():
            execButton['state'] = NORMAL
        else:
            execButton['state'] = DISABLED
    elif not psWActive.get():
        psWHOLESALE['state'] = DISABLED
        if df and ps and db and psCOST.get() and psMSRP.get() and psMake.get() and psModel.get():
            execButton['state'] = NORMAL
        else:
            execButton['state'] = DISABLED

df_title = 'Select DB CSV File'
ps_title = 'Select Pricesheet Excel File'
db_title = 'Select DB .DB File'
initialdir = '/PDX price sheet updater/'

df_onClick = [df_title, (('CSV Files', '*.csv'),('All','*.*')), initialdir,'df']
ps_onClick = [ps_title, (('Excel Files', '*.xlsx'),('All','*.*')), initialdir,'ps']
db_onClick = [db_title, (('DB Files', '*.db'),('All','*.*')), initialdir,'db']

dfButton = Button(root, text=df_title, command= lambda: onClick(*df_onClick))
dfButton.grid(row=2, column=0, padx=5, pady=5)

psButton = Button(root, text=ps_title, command= lambda: onClick(*ps_onClick))
psButton.grid(row=3, column=0, padx=5, pady=5)

dbButton = Button(root, text=db_title, command= lambda: onClick(*db_onClick))
dbButton.grid(row=4, column=0, padx=5, pady=5)

psMakeLabel = Label(root, text='Enter MAKE (i.e. RANGER): ')
psMakeLabel.grid(row=5,column=0, padx=5, pady=10)
psMakeV = StringVar()
psMakeV.trace_add('write',toggleState)
psMake = Entry(root, width = 25, textvariable=psMakeV)
psMake.grid(row=5,column=1, padx=5, pady=10, sticky='w')

psModelLabel = Label(root, text='Column name for Model on pricesheet: ')
psModelLabel.grid(row=6,column=0, padx=5, pady=10)
psModelV = StringVar()
psModelV.trace_add('write',toggleState)
psModel = Entry(root, width = 25, textvariable=psModelV)
psModel.grid(row=6,column=1, padx=5, pady=10, sticky='w')

psMSRPLabel = Label(root, text='Column name for MSRP on pricesheet: ')
psMSRPLabel.grid(row=7,column=0, padx=5, pady=10)
psMSRPV = StringVar()
psMSRPV.trace_add('write',toggleState)
psMSRP = Entry(root, width = 25, textvariable=psMSRPV)
psMSRP.grid(row=7,column=1, padx=5, pady=10, sticky='w')

psCOSTLabel = Label(root, text='Column name for COST on pricesheet: ')
psCOSTLabel.grid(row=8,column=0, padx=5, pady=10)
psCostV = StringVar()
psCostV.trace_add('write',toggleState)
psCOST = Entry(root, width=25, textvariable=psCostV)
psCOST.grid(row=8,column=1, padx=5, pady=10, sticky='w')

psWHOLESALELabel = Label(root, text='Column name for WHOLESALE on pricesheet: ')
psWHOLESALELabel.grid(row=9,column=0, padx=5, pady=10)
psWHOLESALEV = StringVar()
psWHOLESALEV.trace_add('write',toggleState)
psWHOLESALE = Entry(root, width = 25, textvariable=psWHOLESALEV, state=DISABLED)
psWHOLESALE.grid(row=9,column=1, padx=5, pady=10, sticky='w')

psWActive = IntVar()
psWHOLESALEActive = Checkbutton(root, text='Wholesale pricing?', variable = psWActive, command=toggleState)
psWHOLESALEActive.grid(row=9,column=2, padx=5, pady=10, sticky='w')

def runUpdate():
    res = update_db(df, ps, db, psMake.get(), psModel.get(), psMSRP.get(), psCOST.get(), psWActive.get(), psWHOLESALE.get())
    res
    print(res)
    if res:
        messagebox.showinfo('Success', 'Replacement success, ' + str(res) + ' items replaced.')
        root.destroy()
    else:
        messagebox.showerror('Error', 'Something went wrong')

execButton = Button(root, text='Continue', state=DISABLED, command=runUpdate)
execButton.grid(row=10,columnspan=3, sticky='ew', padx=350, pady=10)

    
root.protocol('WM_DELETE_WINDOW', onClosing)
root.mainloop()