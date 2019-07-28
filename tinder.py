from tkinter import filedialog
from guihelper import GUIhelper
from dbhelper import DBhelper
class Tinder(GUIhelper):

    def __init__(self):
        self.db=DBhelper()
        super(Tinder, self).__init__(self.login,self.loadRegWindow)
    def login(self):
        if self._emailInput.get()=="" or self._passwordInput.get()=="":
            self.label2.configure(text="Please fill both the fields", bg="yellow",fg="red")

        else:
            if '@' not in self._emailInput.get():
                self.label2.configure(text="Invalid email format", bg="yellow",fg="red")
            else:
                #login
                data=self.db.search('email',self._emailInput.get(),'password',self._passwordInput.get(),'users')
                if len(data)==1:
                        self.sessionId=data[0][0]
                        self.loadProfile()
                        self.label2.configure(text="Login Successful",bg="green",fg="white")
                else:
                        self.label2.configure(text="Login Failed", bg="yellow", fg="red")

    def loadRegWindow(self):
        self.regWindow(self.registrationHandler)

    def registrationHandler(self):
        if self._nameInput.get()== "" or self._emailInput.get()=="" or self._passwordInput.get()=="" or self._genderInput.get()=="" or self._ageInput.get()=="" or self._cityInput.get()=="":
            self.label2.configure(text="Please fill all the fields",bg="yellow",fg="red")
        else:
            regDict={}

            regDict['name']=self._nameInput.get()
            regDict['email'] = self._emailInput.get()
            regDict['password'] = self._passwordInput.get()
            regDict['gender']=self._genderInput.get()
            regDict['age']=self._ageInput.get()
            regDict['city']=self._cityInput.get()

            response=self.db.insert(regDict,'users')
            if response==1:
                self.label2.configure(text="Registration successful",bg="white",fg="green")
                self._root.destroy()
                self.obj=Tinder()
            else:
                self.label2.configure(text="Registration failed",bg="yellow",fg="red")

    def loadProfile(self):
        data=self.db.searchOne('user_id',self.sessionId,'users',"LIKE")
        self.mainWindow(self,data,mode=1)
    def editProfile(self):
        filename=filedialog.askopenfilename(initialdir="C:/Users\MOHIT/Desktop/project_idle/img/",title ="Select an image ",filetype=(("jpeg","*.jpg"),("All files","*.*")))
        filename=filename.split('/')[-1]
        self.db.setDp(filename,'users','user_id','dp',str(self.sessionId))
        self.loadProfile()
    def viewProfile(self,num,mode):
        if mode==3:
            data=self.db.searchMyProposals('users','user_id','juliet_id','proposals','romeo_id',str(self.sessionId))
        elif mode==4:
            data=self.db.searchMyRequests('users','user_id','romeo_id','proposals','juliet_id',str(self.sessionId))
        elif mode ==5:
            data=self.db.searchMyMatches('users','user_id','romeo_id','proposals','juliet_id',str(self.sessionId))
        else:
            data=self.db.searchOne('user_id',self.sessionId,'users',"NOT LIKE")
        if len(data)==0:
            num=-1
        new_data=[]
        if num == 0 :
                new_data.append(data[0])
                self.mainWindow(self,data,mode,num=num)
        if num<0 :
            self.message("Error "," Can not load data")
        if num >= len(data):
            self.message("Error "," Can not load data")
        else:
            new_data.append(data[num])
            self.mainWindow(self,new_data,mode,num=num)
    def propose(self,juliet_Id):
        data=self.db.search('romeo_id',str(self.sessionId),'juliet_id',str(juliet_Id),'proposals')
        if len(data) == 0:
            procDict={}
            procDict['romeo_id']=str(self.sessionId)
            procDict['juliet_id']=str(juliet_Id)
            response =  self.db.insert(procDict,'proposals',1)
            if response == 1:
                self.message("Congrats","Proposal sent successful. Fingers crossed!")
            else:
                self.message("Tough Luck","Proposal failed. Try again !")
        else:
            self.message("Error","Despo Sala")
    def logOut(self):
        #relogin
        self._root.destroy()
        self.obj=Tinder()
    
obj=Tinder()
