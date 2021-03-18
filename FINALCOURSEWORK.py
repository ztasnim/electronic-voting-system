from tkinter import *
import copy,csv, ctypes, datetime
import tkinter.ttk as ttk
global username, password


####Log in Window

Log= Tk()
Log.title("Voting application")
Log.geometry("500x300")
Log.resizable(0, 0)

###Function to check username and password

def Login():
    userFound = False
    passwordFound = False
    admin = False
    dateReached = False
    username1 = USERNAME.get()
    password1 = PASSWORD.get()
    username.delete(0, END)
    password.delete(0, END)
    LoginData = ReadLogIn([])



    for i in LoginData:

        if i[0] == username1:
            userFound = True
            if i[1] == password1:
                passwordFound = True
                if i[0] == "admin":
                    admin = True
    if userFound == True:
        if passwordFound == True:
            if admin == True:
                HomeWindow(True,True)
            else:
                VOTEDATE_CHECK = datetime.datetime.now()
                start = datetime.datetime(day=23,month=1,year=2020)
                end = datetime.datetime(day=12,month=2,year=2020)
                if start <= VOTEDATE_CHECK <= end:
                    HomeWindow(False,True)
        else:
            if passwordFound == 0:
                lbl_text.config(text="Incorrect username",fg = "red")
                lbl_text.grid(row = 7, columnspan = 10)
    else:
        lbl_text.config(text="Incorrect username and password",fg = "red")
        lbl_text.grid(row = 7, columnspan = 10)
        
def closeWindow():
    btn_exit = Button(Log, text = "Exit", command = closeWindow).grid(row = 9, columnspan = 12)
    Log.destroy()
             
##Function used to read LOG_DATA.csv file and split the data

def ReadLogIn(data):
    with open("LOGIN_DATA.csv") as f:
        LoginData = csv.reader(f)
        for row in LoginData:
            data.append(row)
    return data

##Function to open Main Menu window

def HomeWindow(admin,datenotReached):
    global Home
    Log.withdraw()
    Home = Toplevel()
    lbl_home = Label(Home, text="Menu", font=('times new roman', 30)).grid(row =2)
    if datenotReached == True:
        VoteButton = Button(Home,text="Vote", command=Vote).grid(row=2,column = 2,ipadx=200,ipady= 50,padx=20,pady=30)
    
    ResultsButton = Button(Home,text="Results",command=Results).grid(row=3,column = 2,ipadx=200,ipady = 50, padx =20, pady =30)
    if admin == True:
        print("ER")
        addCandButton = Button(Home,text="Add candidates",command = AddCands).grid(row=4,column=2,ipadx=200,ipady=50,padx=20,pady=30)
    btn_back = Button(Home, text='Back', command=Back).grid(row=5,column = 2,ipadx=50,ipady = 50,padx=25,pady = 30)

##Function to open Vote window

def Vote():
    global root
    Home.withdraw()
    print("VOTE")
    root = Tk()
    Vote = VoteWindow(root)
    root.mainloop()

##Function to go to results screen

def Results():#########################################################################################################
    global results
    Home.withdraw()
    results = Tk()
    Results = ResultsWindow(results)
    results.mainloop()
    
##Function to go back

def AddCands():
    position = input("What position would you like to enroll for?")
    firstName = input("What is your first name")
    surName = input("What is your sur name")
    with open('GSUCandidates.txt',"a") as txtfile:
        txtfile.write("\n"+position+" "+firstName+" "+" "+surName)
    row_contents = [position,firstName,surName,0,0,0,0]
    with open('vote_data.csv','a')as csvfile:
        csvfile.write(row_contents)

def Back():
    Home.destroy()
    Log.deiconify()

# ==============================VARIABLES======================================
USERNAME = StringVar()
PASSWORD = StringVar()

# ==============================FRAMES=========================================
Top = Frame(Log, width=200, height=150)
Top.grid(row=0,column=0)
Form = Frame(Log, width=200, height=200)
Form.grid(row=1,column=0)


# ==============================LABELS=========================================
lbl_title = Label(Top, text="Voting app", font=('arial', 15))
lbl_title.grid(row=0,sticky="n")
lbl_username = Label(Form, text="Username:", font=('arial', 14), bd=15)
lbl_username.grid(row=1, columnspan= 1, padx = 50)
lbl_password = Label(Form, text="Password:", font=('arial', 14), bd=15)
lbl_password.grid(row=2, columnspan = 1, padx = 50 )
lbl_andy = Label(Form, text = "Andy, username = admin, password = 123, "
                              "\nuse this as student not admin login"
                              "\nusername = Username, password = Password"
                 , font = ('arial', 8), bd = 15)
lbl_andy.grid(row=10, column = 0)
lbl_text = Label(Form)
lbl_text.grid(row=3, columnspan=2)

# ==============================ENTRY WIDGETS==================================
username = Entry(Form, textvariable=USERNAME, font=(14))
username.grid(row=1, column=1)
password = Entry(Form, textvariable=PASSWORD, show="*", font=(14))
password.grid(row=2, column=1)



# ==============================BUTTON WIDGETS=================================
btn_login = Button(Form, text="Login", width=45, command=Login)
btn_login.grid(pady=25, row=3, columnspan=2)
btn_login.bind('<Return>', Login)

btn_exit = Button(Form, text = "Exit", width = 45, command = closeWindow)
btn_exit.grid(padx=50, row = 5, columnspan =12)


#==============================INITIALIATION==================================



###Create the list of Candidates

CandsList = []
CandsObjectList = []

Cands = open("GSUCandidates.txt")

for line in Cands:
    temp = [x.strip("\n") for x in line.split(" ")]
    CandsList.append(temp)

#########Class for Candidates

class ApplyRole:

    def __init__(self,firstName,surName,role):
        #print("Called for ",firstName, surName)
        self.firstName = firstName
        self.surName = surName
        self.role = role
        with open('vote_data.csv', mode='r') as vData:
            csv_reader = csv.reader(vData, delimiter=',')
            for row in csv_reader:
                if self.firstName == row[0]:
                    self.firstChoice = int(row[2])
                    self.secondChoice = int(row[3])
                    self.thirdChoice = int(row[4])
                    self.fourthChoice = int(row[5])



##Main Voting window

class VoteWindow:

    def __init__(self,root):
        if root == None:
            self.CandidateObjectList = self.CreateObjList()
        else:
            self.roleCount = 0
            self.roleList = ["GSUOfficer","FacultyOfficer","President"]
            self.Title = Label(root, text="Voting for "+self.roleList[self.roleCount])
            self.Title.grid(row=0,column=2)
            self.frame = Frame(root)
            FirstPref = Label(root,text="1st preference").grid(row=1, column=1)
            SecondPref = Label(root,text="2nd preference").grid(row=1, column=2)
            ThirdPref = Label(root,text="3rd preference").grid(row=1, column=3)
            FourthPref = Label(root,text="4th preference").grid(row=1, column=4)
            self.CandidateObjectList = self.CreateObjList()
            self.selectionScreen(root,self.roleCount)


    def selectionScreen(self,root,roleCount):
        rowNum = 2
        num = 0
        self.posOfCand = []
        pref1 = StringVar(root)
        pref2 = StringVar(root)
        pref3 = StringVar(root)
        pref4 = StringVar(root)
        self.TempRows = copy.deepcopy(self.CandidateObjectList)
        roleList = ["GSUOfficer","FacultyOfficer","President"]
        for i in self.TempRows:
            if i.role == roleList[self.roleCount]:
                TempText = str(i.firstName + " " + i.surName)
                self.TempRows[num] = Label(root,text=TempText)
                self.TempRows[num].grid(row=rowNum)
                Radiobutton(root,variable=pref1,value=TempText).grid(row=rowNum,column=1)
                Radiobutton(root,variable=pref2,value=TempText).grid(row=rowNum,column=2)
                Radiobutton(root,variable=pref3,value=TempText).grid(row=rowNum,column=3)
                Radiobutton(root,variable=pref4,value=TempText).grid(row=rowNum,column=4)
                rowNum +=1
                self.posOfCand.append(num)
            num+=1

        if self.roleCount == 2:
            self.confirmButton = Button(root,text="Confirm",command=lambda: self.clicked(pref1.get(),pref2.get(),pref3.get(),pref4.get(),True))
            self.confirmButton.grid(row=rowNum,column=5)
        else:
            self.confirmButton = Button(root,text="Next",command=lambda: self.clicked(pref1.get(),pref2.get(),pref3.get(),pref4.get(),False))
            self.confirmButton.grid(row=rowNum,column=5)

    def clicked(self,pref1,pref2,pref3,pref4,confirmed):
        self.confirmButton.destroy()
        for i in self.posOfCand:
            self.TempRows[i].destroy()
        for i in self.CandidateObjectList:
            if i.firstName and i.surName in pref1:
                i.firstChoice+=1
                f = open('vote_data.csv','r')
                reader = csv.reader(f)
                mylist = list(reader)
                f.close()
                row_count = 0
                for row in mylist:
                    if row[0] == i.firstName:
                        print(i.firstName)
                        mylist[row_count][2] = i.firstChoice
                    else:
                        row_count+=1
                my_new_list = open("vote_data.csv","w",newline ='')
                csv_writer = csv.writer(my_new_list)
                csv_writer.writerows(mylist)
                my_new_list.close()
            if i.firstName and i.surName in pref2:
                i.secondChoice+=1
                f = open('vote_data.csv','r')
                reader = csv.reader(f)
                mylist = list(reader)
                f.close()
                row_count = 0
                for row in mylist:
                    if row[0] == i.firstName:
                        mylist[row_count][3] = i.secondChoice
                    else:
                        row_count+=1
                my_new_list = open("vote_data.csv","w",newline ='')
                csv_writer = csv.writer(my_new_list)
                csv_writer.writerows(mylist)
                my_new_list.close()
            if i.firstName and i.surName in pref3:
                i.thirdChoice+=1
                f = open('vote_data.csv','r')
                reader = csv.reader(f)
                mylist = list(reader)
                f.close()
                row_count = 0
                for row in mylist:
                    if row[0] == i.firstName:
                        mylist[row_count][4] = i.thirdChoice
                    else:
                        row_count+=1
                my_new_list = open("vote_data.csv","w",newline ='')
                csv_writer = csv.writer(my_new_list)
                csv_writer.writerows(mylist)
                my_new_list.close()
            if i.firstName and i.surName in pref4:
                i.fourthChoice+=1
                f = open('vote_data.csv','r')
                reader = csv.reader(f)
                mylist = list(reader)
                f.close()
                row_count = 0
                for row in mylist:
                    if row[0] == i.firstName:
                        print(i.firstName)
                        mylist[row_count][5] = i.fourthChoice
                    else:
                        row_count+=1
                my_new_list = open("vote_data.csv","w",newline ='')
                csv_writer = csv.writer(my_new_list)
                csv_writer.writerows(mylist)
                my_new_list.close()

        if confirmed == True:
            root.destroy()
            Home.deiconify()
        else:
            self.roleCount+=1
            self.Title.config(text="Voting for "+self.roleList[self.roleCount])
            self.selectionScreen(root,self.roleCount)

    def CreateObjList(self):
        if not CandsObjectList:
            for i in CandsList:
                CandsObjectList.append(str(i[1])+str(i[2]))
                CandsObjectList[-1] = ApplyRole(i[1],i[2],i[0])
        return CandsObjectList

class ResultsWindow:

    def __init__(self,results):
        self.Title = Label(results, text="Role:")
        self.Title.grid(row=1,column=40)
        self.width = 1200
        self.height = 600
        screen_width = results.winfo_screenwidth()
        screen_height = results.winfo_screenheight()
        self.x = (screen_width/2) - (self.width/2)
        self.y = (screen_height/2) - (self.height/2)
        results.geometry("%dx%d+%d+%d" % (self.width, self.height, self.x, self.y))
        TableMargin = Frame(results, width=200,bg="yellow")
        TableMargin.grid(row=3,column=4)
        self.tree = ttk.Treeview(TableMargin, columns=("First Name","Sur Name", "1st preference", "2nd preference", "3rd preference", "4th preference"), height=400)
        self.tree.heading('First Name', text="First Name", anchor=W)
        self.tree.heading('Sur Name', text="Sur Name", anchor=W)
        self.tree.heading('1st preference', text="1st preference", anchor=W)
        self.tree.heading('2nd preference', text="2nd preference", anchor=W)
        self.tree.heading('3rd preference', text="3rd preference", anchor=W)
        self.tree.heading('4th preference', text="4th preference", anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=100)
        self.tree.column('#2', stretch=NO, minwidth=0, width=100)
        self.tree.column('#3', stretch=NO, minwidth=0, width=100)
        self.tree.column('#4', stretch=NO, minwidth=0, width=100)
        self.tree.column('#5', stretch=NO, minwidth=0, width=100)
        self.tree.grid(column=0,row=0)

        self.role = StringVar(results)
        roleCombo = ttk.Combobox(results, textvariable=self.role,
                                 values=[
                                     "President",
                                     "GSUOfficer",
                                     "FacultyOfficer"])
        roleCombo.grid(column=40,row=2)
        roleCombo.current(1)
        roleCombo.bind("<<ComboboxSelected>>",self.limp())
        okbutton = Button(results, text="OK",command=self.limp)
        okbutton.grid(column=41,row=2)

        

    def limp(self):
        self.tree.delete(*self.tree.get_children())
        GetList = VoteWindow(None)
        CandidateObjList = GetList.CreateObjList()
        for i in CandidateObjList:
            if i.role == self.role.get():
                firstName = i.firstName
                surName = i.surName
                firstpreference =i.firstChoice
                secondpreference =i.secondChoice
                thirdpreference =i.thirdChoice
                fourthpreference =i.fourthChoice
                self.tree.insert("",0,values=(firstName,surName,firstpreference,secondpreference,thirdpreference,fourthpreference))
        temp1st = 0
        temp1stnum = 0
        totalVotes = 0
        for i in CandidateObjList:
            if i.role == self.role.get():
                 totalVotes = totalVotes + i.firstChoice + i.secondChoice + i.thirdChoice + i.fourthChoice
                 if int(i.firstChoice) > int(temp1stnum):
                     temp1stnum = i.firstChoice
                     temp1st = i
                 elif int(i.firstChoice) == int(temp1stnum):
                     if int(i.secondChoice) > int(temp1st.secondChoice):
                         temp1stnum = i.secondChoice
                         temp1st = i
                     elif int(i.secondChoice) == int(temp1stnum):
                         if int(i.thirdChoice)>int(temp1st.thirdChoice):
                             temp1stnum = i.thirdChoice
                             temp1st = i
                         elif int(i.thirdChoice) == int(temp1stnum):
                             if int(i.fourthChoice) > int(temp1st.thirdChoice):
                                 temp1st = i
                             elif int(i.fourthChoice) == int(temp1stnum):
                                 print("Draw")
                             
        receivedVotes = temp1st.firstChoice + temp1st.secondChoice + temp1st.thirdChoice + temp1st.fourthChoice
        WinLabel = Label(results,text=" " + temp1st.firstName+" "+temp1st.surName+" is winner for position of"+self.role.get()+"\nreceiving a total of "+str(receivedVotes) + " votes.\n" + str(round((receivedVotes/totalVotes)*100))+"%")
        WinLabel.grid(row=2,column=42)


###Show winner, How many they received, total votes, percentage of total votes received(total of winner/total votes)
        
        
        

        

            
if __name__ == '__main__':
    Log.mainloop()
