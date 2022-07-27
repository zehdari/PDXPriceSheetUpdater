from tkinter import filedialog, messagebox
from tkinter import *
import pandas as pd
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
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=0)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_rowconfigure(9, weight=1)

dfLabelText = StringVar()
dfLabelText.set('Please select a file')
dfLabel = Label(root, textvariable=dfLabelText).grid(row=2, column=1, columnspan=3)

psLabelText = StringVar()
psLabelText.set('Please select a file')
psLabel = Label(root, textvariable=psLabelText).grid(row=3, column=1, columnspan=3)

dbLabelText = StringVar()
dbLabelText.set('Please select a file')
dbLabel = Label(root, textvariable=dbLabelText).grid(row=4, column=1, columnspan=3)

def columnHeaders():
    global psReadList
    psReadList = list(pd.read_excel(ps, dtype=str, index_col=None))
    psRead = str('  |  '.join((psReadList))).replace('\n', ' ')
    columnRead['text'] = psRead
    columnHeader['text'] = 'Column Names on Pricesheet:'

def listMakes():
    global dbRead
    dbRead = pd.read_csv(df)
    dbRead = dbRead['MAKE'].sort_values().unique()

def onClosing():
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        root.destroy()

def checkMakes(*args):
    if 'dbRead' in globals():
        global makeCheckI
        if psMakeV.get().upper() in dbRead:
            makeCheck['text'] = ''
            makeCheck['fg'] = '#000000'
            makeCheckI = 1
        else:
            makeCheck['text'] = 'Enter a valid MAKE'
            makeCheck['fg'] = '#5F0500'
            makeCheckI = 0
    toggleState()

def checkModel(*args):
    if 'psReadList' in globals():
        global modelCheckI
        if psModelV.get().upper() in (model.upper() for model in psReadList):
            modelCheck['text'] = ''
            modelCheck['fg'] = '#000000'
            modelCheckI = 1
        else:
            modelCheck['text'] = 'INVALID'
            modelCheck['fg'] = '#5F0500'
            modelCheckI = 0
    toggleState()

def checkRetail(*args):
    if 'psReadList' in globals():
        global retailCheckI
        if psMSRPV.get().upper() in (retail.upper() for retail in psReadList):
            retailCheck['text'] = ''
            retailCheck['fg'] = '#000000'
            retailCheckI = 1
        else:
            retailCheck['text'] = 'INVALID'
            retailCheck['fg'] = '#5F0500'
            retailCheckI = 0
    toggleState()

def checkCost(*args):
    if 'psReadList' in globals():
        global costCheckI
        if psCostV.get().upper() in (cost.upper() for cost in psReadList):
            costCheck['text'] = ''
            costCheck['fg'] = '#000000'
            costCheckI = 1
        else:
            costCheck['text'] = 'INVALID'
            costCheck['fg'] = '#5F0500'
            costCheckI = 0
    toggleState()

def checkDealer(*args):
    if 'psReadList' in globals():
        global dealerCheckI
        if psWHOLESALEV.get().upper() in (dealer.upper() for dealer in psReadList):
            dealerCheck['text'] = ''
            dealerCheck['fg'] = '#000000'
            dealerCheckI = 1
        else:
            dealerCheck['text'] = 'INVALID'
            dealerCheck['fg'] = '#5F0500'
            dealerCheckI = 0
    toggleState()

def onClick(title,types,initialdir,input):
    file = filedialog.askopenfilename(initialdir=initialdir, title=title, filetypes=types)
    if len(file):
        if file.endswith('.csv') and input == 'df':
            global df
            df = file
            dfLabelText.set(df)
            listMakes()
            checkMakes()
        elif file.endswith('.xlsx') and input == 'ps':
            global ps
            ps = file
            psLabelText.set(ps)
            toggleState()
            columnHeaders()
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
        if df and ps and db and psCOST.get() and psMSRP.get() and psMake.get() and psModel.get() and modelCheckI and makeCheckI and retailCheckI and costCheckI and psWHOLESALE.get() and dealerCheckI:
            execButton['state'] = NORMAL
        else:
            execButton['state'] = DISABLED
    elif not psWActive.get():
        psWHOLESALE['state'] = DISABLED
        if df and ps and db and psCOST.get() and psMSRP.get() and psMake.get() and psModel.get() and modelCheckI and makeCheckI and retailCheckI and costCheckI:
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

columnHeader = Label (root)
columnHeader.grid(row=6,column=2, padx=5, pady=10, sticky='ew')

columnRead = Label(root)
columnRead.grid(row=7,column=2, padx=5, pady=10, sticky='ew')

makeCheck = Label(root)
makeCheck.grid(row=5,column=2, padx=5, pady=10, sticky='w')

modelCheck = Label(root)
modelCheck.grid(row=6,column=2, padx=5, pady=10, sticky='w')

retailCheck = Label(root)
retailCheck.grid(row=7,column=2, padx=5, pady=10, sticky='w')

costCheck = Label(root)
costCheck.grid(row=8,column=2, padx=5, pady=10, sticky='w')

dealerCheck = Label(root)
dealerCheck.grid(row=9,column=2, padx=5, pady=10, sticky='w')

psMakeLabel = Label(root, text='Enter MAKE (i.e. RANGER): ')
psMakeLabel.grid(row=5,column=0, padx=5, pady=10)
psMakeV = StringVar()
psMakeV.trace_add('write',checkMakes)
psMake = Entry(root, width = 25, textvariable=psMakeV)
psMake.grid(row=5,column=1, padx=5, pady=10, sticky='w')

psModelLabel = Label(root, text='Column name for model on pricesheet: ')
psModelLabel.grid(row=6,column=0, padx=5, pady=10)
psModelV = StringVar()
psModelV.trace_add('write',checkModel)
psModel = Entry(root, width = 25, textvariable=psModelV)
psModel.grid(row=6,column=1, padx=5, pady=10, sticky='w')

psMSRPLabel = Label(root, text='Column name for MSRP on pricesheet: ')
psMSRPLabel.grid(row=7,column=0, padx=5, pady=10)
psMSRPV = StringVar()
psMSRPV.trace_add('write',checkRetail)
psMSRP = Entry(root, width = 25, textvariable=psMSRPV)
psMSRP.grid(row=7,column=1, padx=5, pady=10, sticky='w')

psCOSTLabel = Label(root, text='Column name for cost on pricesheet: ')
psCOSTLabel.grid(row=8,column=0, padx=5, pady=10)
psCostV = StringVar()
psCostV.trace_add('write',checkCost)
psCOST = Entry(root, width=25, textvariable=psCostV)
psCOST.grid(row=8,column=1, padx=5, pady=10, sticky='w')

psWHOLESALELabel = Label(root, text='Column name for dealer pricing on pricesheet: ')
psWHOLESALELabel.grid(row=9,column=0, padx=5, pady=10)
psWHOLESALEV = StringVar()
psWHOLESALEV.trace_add('write',checkDealer)
psWHOLESALE = Entry(root, width = 25, textvariable=psWHOLESALEV, state=DISABLED)
psWHOLESALE.grid(row=9,column=1, padx=5, pady=10, sticky='w')

psWActive = IntVar()
psWHOLESALEActive = Checkbutton(root, text='Wholesale pricing?', variable = psWActive, command=toggleState)
psWHOLESALEActive.grid(row=9,column=2, padx=5, pady=10, sticky='w')

def runUpdate():
    res = update_db(df, ps, db, psMake.get().upper(), psModel.get().lower(), psMSRP.get().lower(), psCOST.get().lower(), psWActive.get(), psWHOLESALE.get().lower())
    res
    print(res)
    if res:
        messagebox.showinfo('Success', 'Replacement success: ' + str(res) + ' items replaced.')
        root.destroy()
    else:
        messagebox.showerror('Error', 'Something went wrong')

execButton = Button(root, text='UPDATE DB', state=DISABLED, command=runUpdate)
execButton.grid(row=10,columnspan=3, sticky='ew', padx=350, pady=10)

    
root.protocol('WM_DELETE_WINDOW', onClosing)
root.mainloop()
