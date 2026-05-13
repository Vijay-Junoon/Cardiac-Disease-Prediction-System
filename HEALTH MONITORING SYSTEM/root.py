from customtkinter import *
from tkinter import *
import mysql.connector
from PIL import Image
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
import threading
import time
from customtkinter import CTkProgressBar

crtUser = "Placeholder"

conn = mysql.connector.connect(host = "localhost",user="root",password="Lucifer545@",database="HeartMonitor")
myCursor = conn.cursor()

fileList = ["Total Cholesterol","LDL","HDL","Systolic BP","Diastolic BP"]

normalValM = {"t_chol" : 200, "ldl" : 100,"hdl" : 40,"s_bp" : 110, "d_bp" : 75}
normalValF = {"t_chol" : 200, "ldl" : 100,"hdl" : 50,"s_bp" : 110, "d_bp" : 75}

root = CTk()
root.title("Cardiac Disease Prediction System")
set_appearance_mode("System")
root.tk.call('tk', 'scaling', 1.5)
try:
    image_icon = Image.open("ecgIcon2.ico")
    #root.iconphoto(False, CTkImage(dark_image=image_icon, light_image=image_icon))
except Exception as e:
    print("Error loading icon image:", e)
root.geometry("950x600")

class Suggestions(CTkFrame):
    def __init__(self, master, items=None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.items = items if items else []
        self.labels = []
        self.render_items()

    def render_items(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.labels.clear()

        for i, item in enumerate(self.items):
            label = CTkButton(self, text=item,corner_radius=0,command=lambda i=i: self.on_item_click(i),fg_color="#BCD9FE",hover_color="#83BDF7",text_color="#002126")
            label.pack(fill="x", padx=5, pady=2)
            self.labels.append(label)

    def on_item_click(self, index):
        if self.command:
            self.command(self.items[index])

    def add_item(self, item):
        self.items.append(item)
        self.render_items()

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            self.render_items()

def show_custom_message(title,message,messagePosition):
    custom_box = Toplevel()
    custom_box.title(title)
    custom_box.geometry("300x150")
    custom_box.configure(background="#BCD9FE")
    custom_box.resizable(False,False)
    x = messagePosition[0]
    y=messagePosition[1]
    closeButton = CTkButton(custom_box, text="OK",font=("arial",12,"bold"),text_color="#222626", command=custom_box.destroy,width=45,height=2,fg_color="#E6475A",hover_color="#B6233D",corner_radius=0)
    closeButton.place(x=100,y=75)
    messageLabel = CTkLabel(custom_box,text=message,justify="center",text_color="#003D4D",font=("arial", 12,"bold"))
    messageLabel.place(x=x,y=y)

    custom_box.wait_window()

def homepage():

    def login(usernameEntry, passwordEntry, infoText):
        username = usernameEntry.get()
        password = passwordEntry.get()
        myCursor.execute("SELECT * FROM userCredentials WHERE Username = %s AND Password = %s;", (username, password))
        a = myCursor.fetchone()
        if a:
            checkValidation(1)
            global crtUser
            crtUser = username
        else:
            checkValidation(0)
            show_custom_message("An error has occurred.", "Incorrect credentials given.Try again.", [20, 25])

    def createAccount(firstNameEntry, lastNameEntry, contactEntry, emailEntry, userNameEntry, passwordEntry):
        FirstName = firstNameEntry.get()
        LastName = lastNameEntry.get()
        ContactNumber = contactEntry.get()
        Email = emailEntry.get()
        Username = userNameEntry.get()
        Password = passwordEntry.get()
        if not FirstName.isalnum() or not LastName.isalnum() or not ContactNumber.isdigit():
            show_custom_message("Error occurred.", "Please enter valid credentials.")
            checkValidation(0)
        else:
            myCursor.execute(
                "INSERT INTO userCredentials(FirstName,LastName,ContactNumber,Email,Username,Password)VALUES(%s,%s,%s,%s,%s,%s);",
                (FirstName, LastName, ContactNumber, Email, Username, Password))
            show_custom_message("Account created", "Account created successfully.", [45, 25])
            conn.commit()
            global crtUser
            crtUser = Username
            checkValidation(1)


    def createAccountPage():
        createAccountPanel = CTkCanvas(root, bg="#BCD9FE", borderwidth=0)
        createAccountPanel.place(relx=0.24, rely=0, relwidth=1, relheight=1)
        firstNameEntry = CTkEntry(createAccountPanel, corner_radius=0, placeholder_text="First Name")
        firstNameEntry.place(relx=0.24, rely=0.2, relwidth=0.26, relheight=0.04)
        lastNameEntry = CTkEntry(createAccountPanel, corner_radius=0, placeholder_text="Last Name")
        lastNameEntry.place(relx=0.24, rely=0.27, relwidth=0.26, relheight=0.04)
        contactEntry = CTkEntry(createAccountPanel, corner_radius=0, placeholder_text="Contact Number")
        contactEntry.place(relx=0.24, rely=0.34, relwidth=0.26, relheight=0.04)
        emailEntry = CTkEntry(createAccountPanel, corner_radius=0, placeholder_text="Email ID")
        emailEntry.place(relx=0.24, rely=0.41, relwidth=0.26, relheight=0.04)
        userNameEntry = CTkEntry(createAccountPanel, corner_radius=0, placeholder_text="Username")
        userNameEntry.place(relx=0.24, rely=0.48, relwidth=0.26, relheight=0.04)
        passwordEntry = CTkEntry(createAccountPanel, corner_radius=0, placeholder_text="Password")
        passwordEntry.place(relx=0.24, rely=0.55, relwidth=0.26, relheight=0.04)
        createAccountButton = CTkButton(createAccountPanel, text="CREATE ACCOUNT", font=("arial", 12, "bold"),
                                        fg_color="#83BDF7",
                                        hover_color="#1580C2", text_color="#002126", corner_radius=0,
                                        command=lambda: createAccount(firstNameEntry, lastNameEntry,
                                                                      contactEntry, emailEntry, userNameEntry,
                                                                      passwordEntry))
        createAccountButton.place(relx=0.24, rely=0.65, relwidth=0.26, relheight=0.06)

    homePagePanel = CTkCanvas(root, bg="#BCD9FE", borderwidth=0)
    homePagePanel.place(relx=0.24, rely=0, relwidth=1, relheight=1)
    userNameLabel = CTkLabel(homePagePanel,text="Username",text_color="#002126",font=("Arial",12,"bold"))
    userNameLabel.place(relx=0.24,rely=0.26)
    userNameEntry = CTkEntry(homePagePanel,bg_color="#F2F7FF",fg_color="#F2F7FF",corner_radius=0)
    userNameEntry.place(relx=0.24,rely=0.3,relwidth=0.26,relheight=0.04)
    passwordLabel = CTkLabel(homePagePanel,text="Password",text_color="#002126",font=("Arial",12,"bold"))
    passwordLabel.place(relx=0.24,rely=0.36)
    passwordEntry = CTkEntry(homePagePanel,bg_color="#F2F7FF",fg_color="#F2F7FF",corner_radius=0)
    passwordEntry.place(relx=0.24,rely=0.4,relwidth=0.26,relheight=0.04)

    dontHaveAnAccountLabel = CTkLabel(homePagePanel,text="Don't have an account?",font=("arial",12),text_color="#002126")
    dontHaveAnAccountLabel.place(relx=0.23,rely=0.57,relwidth=0.15,relheight=0.05)
    createAccountLink = CTkButton(homePagePanel,text="Create account.",border_width=0,
                                  cursor='hand2',font=("arial",12,"underline"),fg_color="transparent",
                                  hover_color="#BCD9FE",corner_radius=0,text_color=("#076B9B","#003D4D"),command=createAccountPage)
    createAccountLink.place(relx=0.41,rely=0.57,relwidth=0.1,relheight=0.05)
    loginButton = CTkButton(homePagePanel, text="Log in", font=("arial", 12, "bold"), fg_color="#83BDF7",
                            hover_color="#1580C2", text_color="#002126", corner_radius=0,
                            command=lambda: login(userNameEntry, passwordEntry, dontHaveAnAccountLabel))
    loginButton.place(relx=0.24, rely=0.5, relwidth=0.26, relheight=0.06)

def predictionpage():
    def storeHistory(age,sex,t_chol,ldl,hdl,sysBP,diaBP):
        myCursor.execute("INSERT INTO history(Username,age,sex,t_chol,ldl,hdl,s_bp,d_bp)VALUES(%s,%s,%s,%s,%s,%s,%s,%s);",(crtUser,age,sex,t_chol,ldl,hdl,sysBP,diaBP))
        conn.commit()

    def resultAnalysis(res,age,sex,t_chol,ldl,hdl,sysBP,diaBP,smoking,diabetes):
        storeHistory(age,sex,t_chol,ldl,hdl,sysBP,diaBP)
        resultAnalysisPanel = CTkCanvas(root, bg="#BCD9FE", borderwidth=0)
        resultAnalysisPanel.place(relx=0.24, rely=0, relwidth=1, relheight=1)
        if res == 0:
            resultText = CTkLabel(resultAnalysisPanel,text = "You’re in the clear — no heart issues detected.",justify="center",text_color="#003D4D",font=("arial", 18,"bold"))
            resultText.place(x=100,y=100)
        else:
            resultText = CTkLabel(resultAnalysisPanel, text="Further evaluation is recommended, as your heart may be under some strain.",
                                  justify="center", text_color="#003D4D", font=("arial", 18, "bold"))
            resultText.place(x=65, y=100)

        suggestionTitle = CTkLabel(resultAnalysisPanel,text="", text_color="#002126", font=("arial", 22, "bold"))
        suggestionTitle.place(x=275, y=175)
        suggestionText = CTkTextbox(resultAnalysisPanel,fg_color="#BCD9FE",width=398,height=200,font=("arial",16),corner_radius=0)
        suggestionText.place(x=275, y=210)
        normalText = "All Good....just do what you're doing now..."

        deteriorated_items = []

        if t_chol > 200:
            deteriorated_items.append("Total Cholesterol")
        if ldl > 130:
            deteriorated_items.append("LDL")
        if hdl < 40:
            deteriorated_items.append("HDL")
        if sysBP > 120:
            deteriorated_items.append("Systolic BP")
        if diaBP > 80:
            deteriorated_items.append("Diastolic BP")
        if smoking == "yes":
            deteriorated_items.append("Smoking")

        def displaySuggestions(item):
            suggestionTitle.configure(text=item)
            suggestionText.configure(state="normal")
            suggestionText.delete("0.0", "end")
            txt = ""
            for i in fileList:
                if i == item:
                    with open(i, "r") as fp:
                        txt = fp.read()
            suggestionText.insert("0.0", txt)
            suggestionText.configure(state="disabled")

        suggestionBox = Suggestions(resultAnalysisPanel,items=deteriorated_items,fg_color="#002126",corner_radius=0,command=displaySuggestions)
        suggestionBox.place(x=100,y=175)

    def predict(ageEntry,sexEntry,t_cholEntry,ldlEntry,hdlEntry,sysBPEntry,diaBPEntry,smokingEntry,diabetesEntry):


        age = int(ageEntry.get())
        sex = 0
        if sexEntry.get().lower().startswith("ma"):
            sex = 1
        elif sexEntry.get().lower().startswith("fe"):
            sex = 0

        t_chol = float(t_cholEntry.get())
        ldl = float(ldlEntry.get())
        hdl = float(hdlEntry.get())
        sysBP = float(sysBPEntry.get())
        diaBP = float(diaBPEntry.get())
        smoking = 0
        if smokingEntry.get().lower().startswith("non"):
            smoking = 0
        elif smokingEntry.get().lower().startswith("smoker"):
            smoking = 1
        diabetes = 0
        if diabetesEntry.get().lower().startswith("n"):
            diabetes = 0
        elif diabetesEntry.get().lower().startswith("y"):
            diabetes = 1

        genDataset = pd.read_csv("heart_disease_Dataset.csv")

        genX = genDataset.iloc[:, :-1].values  # Features
        genY = genDataset.iloc[:, -1].values  # Target

        genImputer = SimpleImputer(missing_values=np.nan, strategy="mean")
        genX = genImputer.fit_transform(genX)

        genX_train, genX_test, genY_train, genY_test = train_test_split(genX, genY, test_size=0.25, stratify=genY,
                                                                        random_state=1)

        scaler = StandardScaler()
        genX_train_scaled = scaler.fit_transform(genX_train)
        genX_test_scaled = scaler.transform(genX_test)

        genModel = LogisticRegression(solver='lbfgs', max_iter=5000, class_weight='balanced')
        genModel.fit(genX_train_scaled, genY_train)

        input_data = (age,sex,t_chol,ldl,hdl,sysBP,diaBP,smoking,diabetes)
        input_data_array = np.asarray(input_data).reshape(1, -1)

        input_data_scaled = scaler.transform(input_data_array)
        prediction = genModel.predict(input_data_scaled)
        print("Predicted class for the new input:", prediction[0])

        resultAnalysis(prediction[0],age,sex,t_chol,ldl,hdl,sysBP,diaBP,smoking,diabetes)

    predictionpagePanel = CTkCanvas(root, bg="#BCD9FE", borderwidth=0)
    predictionpagePanel.place(relx=0.24, rely=0, relwidth=1, relheight=1)

    progressbar = CTkProgressBar(predictionpagePanel,corner_radius=0);
    progressbar.configure(mode="determinate")
    progressbar.set(0)
    progressbar.place_forget()


    def help():
        helpWindow = Toplevel()
        helpWindow.title("Help")
        helpWindow.geometry("550x650")
        helpWindow.configure(background="#BCD9FE")
        pane = CTkCanvas(helpWindow, background="#BCD9FE", width=550, height=650)
        pane.pack()
        feelStuckLabel = CTkLabel(pane, wraplength=500, text="That's right...we've got your back...",
                                  font=("Coolvetica", 19, "bold"),
                                  text_color="#076B9B")
        feelStuckLabel.place(relx=0.025, rely=0.01, relwidth=1, relheight=0.2)
        ageLabel = CTkLabel(pane, justify="center", text="Age: ",
                            font=("Coolvetica", 16, "bold"), text_color="#002126")
        ageLabel.place(relx=0.05, rely=0.2, relwidth=0.1, relheight=0.05)
        ageInfoLabel = CTkLabel(pane, justify="center", text="Age(IN NUMBERS) of the user.",
                                font=("Coolvetica", 16), text_color="#454B4D")
        ageInfoLabel.place(relx=0.15, rely=0.2, relwidth=0.5, relheight=0.05)

        sexLabel = CTkLabel(pane, justify="center", text="Sex: ",
                            font=("Coolvetica", 16, "bold"), text_color="#002126")
        sexLabel.place(relx=0.05, rely=0.26, relwidth=0.1, relheight=0.05)
        sexInfoLabel = CTkLabel(pane, justify="center", text="Sex of the user(Male/Female).",
                                font=("Coolvetica", 16), text_color="#454B4D")
        sexInfoLabel.place(relx=0.15, rely=0.26, relwidth=0.5, relheight=0.05)

        tot_cholLabel = CTkLabel(pane, justify="center", text="Total Cholesterol: ",
                                 font=("Coolvetica", 16, "bold"), text_color="#002126")
        tot_cholLabel.place(relx=0.055, rely=0.32, relwidth=0.31, relheight=0.05)
        tot_chol_Info_Label = CTkLabel(pane, justify="left", wraplength=300,
                                       text="Total cholesterol level (mg/dL)",
                                       font=("Coolvetica", 16), text_color="#454B4D")
        tot_chol_Info_Label.place(relx=0.36, rely=0.305, relwidth=0.5, relheight=0.08)

        ldlLabel = CTkLabel(pane, justify="center", text="ldl: ",
                            font=("Coolvetica", 16, "bold"), text_color="#002126")
        ldlLabel.place(relx=0.06, rely=0.375, relwidth=0.06, relheight=0.05)
        ldlInfoLabel = CTkLabel(pane, justify="center",
                                text="Low-Density Lipoprotein cholesterol (bad cholesterol) level (mg/dL). ",
                                font=("Coolvetica", 16), text_color="#454B4D")
        ldlInfoLabel.place(relx=0.108, rely=0.375, relwidth=1.15, relheight=0.05)

        hdlLabel = CTkLabel(pane, justify="center", text="hdl: ",
                            font=("Coolvetica", 16, "bold"), text_color="#002126")
        hdlLabel.place(relx=0.06, rely=0.435, relwidth=0.07, relheight=0.05)
        hdlInfoLabel = CTkLabel(pane, justify="center",
                                text="High-Density Lipoprotein cholesterol (good cholesterol) level (mg/dL).",
                                font=("Coolvetica", 15), text_color="#454B4D")
        hdlInfoLabel.place(relx=0.12, rely=0.435, relwidth=1.12, relheight=0.05)

        systolic_bp_Label = CTkLabel(pane, justify="center", text="Systolic BP: ",
                                     font=("Coolvetica", 16, "bold"), text_color="#002126")
        systolic_bp_Label.place(relx=0.06, rely=0.495, relwidth=0.221, relheight=0.05)
        systolic_bp_InfoLabel = CTkLabel(pane, justify="center", text="Systolic blood pressure (mmHg).",
                                         font=("Coolvetica", 16), text_color="#454B4D")
        systolic_bp_InfoLabel.place(relx=0.27, rely=0.495, relwidth=0.55, relheight=0.05)

        diabpLabel = CTkLabel(pane, justify="center", text="Diastolic BP: ",
                              font=("Coolvetica", 16, "bold"), text_color="#002126")
        diabpLabel.place(relx=0.055, rely=0.555, relwidth=0.24, relheight=0.05)
        diabpInfoLabel = CTkLabel(pane, justify="left", wraplength=300,
                                  text="Diastolic blood pressure (mmHg).",
                                  font=("Coolvetica", 16), text_color="#454B4D")
        diabpInfoLabel.place(relx=0.3, rely=0.555, relwidth=0.523, relheight=0.05)
        smokingLabel = CTkLabel(pane, justify="center", text="Smoking: ",
                                font=("Coolvetica", 16, "bold"), text_color="#002126")
        smokingLabel.place(relx=0.06, rely=0.615, relwidth=0.17, relheight=0.05)
        smokingInfoLabel = CTkLabel(pane, justify="center", text="Smoking status  (Smoker/Non Smoker).",
                                    font=("Coolvetica", 16), text_color="#454B4D")
        smokingInfoLabel.place(relx=0.23, rely=0.615, relwidth=0.65, relheight=0.05)

        diabetesLabel = CTkLabel(pane, justify="center", text="Diabetes: ",
                                 font=("Coolvetica", 16, "bold"), text_color="#002126")
        diabetesLabel.place(relx=0.06, rely=0.675, relwidth=0.17, relheight=0.05)
        diabetesInfolabel = CTkLabel(pane, justify="left", wraplength=300,
                                     text="Diabetes status (Yes/No).",
                                     font=("Coolvetica", 16), text_color="#454B4D")
        diabetesInfolabel.place(relx=0.23, rely=0.675, relwidth=0.45, relheight=0.05)

        nextButton = CTkButton(pane, text="CLOSE", font=("arial", 12, "bold"), fg_color="#83BDF7",
                               hover_color="#1580C2", text_color="#002126", corner_radius=0
                               , command=lambda: helpWindow.destroy())
        nextButton.place(relx=0.35, rely=0.85, relwidth=0.26, relheight=0.06)

        #placeHolderPane = CTkCanvas()

    feelStuckLabel = CTkLabel(predictionpagePanel, text="Feel Stuck?", font=("Coolvetica", 38, "bold"),
                              text_color="#076B9B")
    feelStuckLabel.place(relx=0.035, rely=0.01, relwidth=0.25, relheight=0.2)
    weGotYourBackLabel = CTkLabel(predictionpagePanel, justify="left", text="We've got your back.",
                                  font=("Coolvetica", 18), text_color="#003D4D")
    weGotYourBackLabel.place(relx=0.01, rely=0.135, relwidth=0.25, relheight=0.05)
    helpButton = CTkButton(predictionpagePanel, text="Help", font=("arial", 12, "bold"),
                           fg_color="#83BDF7",
                           hover_color="#1580C2", text_color="#002126", corner_radius=0,
                           command=help)
    helpButton.place(relx=0.05, rely=0.2, relwidth=0.15, relheight=0.05)

    def predict_with_progress(ageEntry, sexEntry, t_cholEntry, ldlEntry, hdlEntry, sysBPEntry, diaBPEntry, smokingEntry,
                              diabetesEntry):
        submitButton.configure(state="disabled")

        progressbar.place(relx=0.25, rely=0.91, relwidth=0.2635, relheight=0.015)
        progressbar.set(0)

        def run_prediction():
            for i in range(1, 11):
                progressbar.set(i / 10)

            predict(ageEntry, sexEntry, t_cholEntry, ldlEntry, hdlEntry, sysBPEntry, diaBPEntry, smokingEntry,
                    diabetesEntry)

            progressbar.place_forget()
            submitButton.configure(state="normal")

        threading.Thread(target=run_prediction).start()

    ageEntry = CTkEntry(predictionpagePanel, placeholder_text="Age", corner_radius=0)
    ageEntry.place(relx=0.25, rely=0.3, relwidth=0.265, relheight=0.045)

    sexEntry = CTkEntry(predictionpagePanel, placeholder_text="Sex", corner_radius=0)
    sexEntry.place(relx=0.25, rely=0.37, relwidth=0.265, relheight=0.045)

    t_cholEntry = CTkEntry(predictionpagePanel, placeholder_text="Total cholesterol", corner_radius=0)
    t_cholEntry.place(relx=0.25, rely=0.44, relwidth=0.265, relheight=0.045)

    ldlEntry = CTkEntry(predictionpagePanel, placeholder_text="ldl cholesterol", corner_radius=0)
    ldlEntry.place(relx=0.25, rely=0.51, relwidth=0.265, relheight=0.045)

    hdlEntry = CTkEntry(predictionpagePanel, placeholder_text="hdl cholesterol", corner_radius=0)
    hdlEntry.place(relx=0.25, rely=0.58, relwidth=0.265, relheight=0.045)

    sysBPEntry = CTkEntry(predictionpagePanel, placeholder_text="Systolic BP", corner_radius=0)
    sysBPEntry.place(relx=0.25, rely=0.65, relwidth=0.265, relheight=0.045)

    diaBPEntry = CTkEntry(predictionpagePanel, placeholder_text="Diastolic BP", corner_radius=0)
    diaBPEntry.place(relx=0.25, rely=0.72, relwidth=0.265, relheight=0.045)

    smokingEntry = CTkEntry(predictionpagePanel, placeholder_text="Smoking", corner_radius=0)
    smokingEntry.place(relx=0.25, rely=0.79, relwidth=0.265, relheight=0.045)

    diabetesEntry = CTkEntry(predictionpagePanel, placeholder_text="Diabetes", corner_radius=0)
    diabetesEntry.place(relx=0.25, rely=0.86, relwidth=0.265, relheight=0.045)

    submitButton = CTkButton(predictionpagePanel, text="SUBMIT", font=("arial", 12, "bold"), fg_color="#83BDF7",
                             hover_color="#1580C2", text_color="#002126", corner_radius=0,
                             command=lambda: predict_with_progress(ageEntry, sexEntry, t_cholEntry, ldlEntry, hdlEntry,
                                                                   sysBPEntry, diaBPEntry, smokingEntry, diabetesEntry))
    submitButton.place(relx=0.25, rely=0.935, relwidth=0.26, relheight=0.06)


def history():
    historyPagePanel = CTkCanvas(root, bg="#BCD9FE", borderwidth=0)
    historyPagePanel.place(relx=0.24, rely=0, relwidth=1, relheight=1)

    def fetchHistory(username):
        uName = username.get();
        myCursor.execute("SELECT  age,sex,t_chol,ldl,hdl,s_bp,d_bp  from history where Username = %s;",(uName,))
        records = myCursor.fetchall()
        scrollable_frame = CTkScrollableFrame(historyPagePanel, width=480, height=250,fg_color="#F2F7FF",corner_radius = 0)
        scrollable_frame.place(relx=0.13,rely=0.5)

        headers = ["Age","Sex","Total Cholesterol","LDL","HDL","Systolic BP","Diastolic BP"]
        for i, header in enumerate(headers):
            label = CTkLabel(scrollable_frame, text=header, font=("Arial", 16, "bold"))
            label.grid(row=0, column=i, padx=10, pady=5)

        for row_index, row in enumerate(records, start=1):
            for col_index, value in enumerate(row):
                label = CTkLabel(scrollable_frame, text=str(value), font=("Arial", 14))
                label.grid(row=row_index, column=col_index, padx=10, pady=5)

    uNameLabel = CTkLabel(historyPagePanel,text_color="#002126",font=("Arial",13,"bold"),text="Username: ")
    uNameLabel.place(relx = 0.27,rely = 0.26)
    uName = CTkEntry(historyPagePanel,bg_color="#F2F7FF",fg_color="#F2F7FF",corner_radius=0,height=8)
    uName.place(relx=0.35,rely=0.26)
    submitButton = CTkButton(historyPagePanel, text="SUBMIT", font=("arial", 12, "bold"), fg_color="#83BDF7",
                            hover_color="#1580C2", text_color="#002126", corner_radius=0,
                            command=lambda: fetchHistory(uName))
    submitButton.place(relx=0.3, rely=0.34, relwidth=0.16, relheight=0.05)


def aboutPage():
    aboutPagePanel = CTkCanvas(root, bg="#BCD9FE", borderwidth=0)
    aboutPagePanel.place(relx=0.24, rely=0, relwidth=1, relheight=1)
    with open("aboutFile","r") as fp:
        txt = fp.read()
        fp.close()
    aboutText = CTkTextbox(aboutPagePanel, fg_color="#BCD9FE",wrap="word", width=600, height=450, font=("arial", 16),
                                corner_radius=0)
    aboutText.place(x=50, y=150)
    aboutText.insert("1.0",txt)

optionPanel=CTkCanvas(root,bg="#83BDF7",borderwidth=0)
optionPanel.place(relx=0,rely=0,relwidth=0.25,relheight=1)
mainPanel=CTkCanvas(root,bg="#BCD9FE",borderwidth=0)
mainPanel.place(relx=0.24,rely=0,relwidth=1,relheight=1)
homeButton = CTkButton(optionPanel,text="HOME",fg_color="#83BDF7",hover_color="#BCD9FE",text_color="#002126",text_color_disabled="#687073",font=("Arial", 12, "bold"),corner_radius=0)
homeButton.place(relx=0,rely=0.35,relwidth=1,relheight=0.06)
predictorButton = CTkButton(optionPanel,text="PREDICTOR",fg_color="#83BDF7",hover_color="#BCD9FE",text_color="#002126",text_color_disabled="#687073",font=("Arial", 12, "bold"),width=280,corner_radius=0,height=35,command=predictionpage)
predictorButton.place(relx=0,rely=0.42,relwidth=1,relheight=0.06)
historybutton = CTkButton(optionPanel,text="HISTORY",fg_color="#83BDF7",hover_color="#BCD9FE",text_color="#002126",text_color_disabled="#687073",width=280,font=("Arial", 12, "bold"),corner_radius=0,height=35,command = history)
historybutton.place(relx=0,rely=0.49,relwidth=1,relheight=0.06)
about = CTkButton(optionPanel,text="ABOUT",fg_color="#83BDF7",hover_color="#BCD9FE",command = aboutPage,text_color="#002126",text_color_disabled="#687073",width=280,font=("Arial", 12, "bold"),corner_radius=0,height=35)
about.place(relx=0,rely=0.56,relwidth=1,relheight=0.06)

def checkValidation(validated):
    if validated == 0:
        homeButton.configure(state="normal")
        predictorButton.configure(state="disabled")
        historybutton.configure(state="disabled")
    else:
        homeButton.configure(state="disabled")
        predictorButton.configure(state="normal")
        historybutton.configure(state="normal")

checkValidation(0)
homepage()
root.mainloop()