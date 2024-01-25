import datetime
import os
import glob
import random

import pandas as pd
import time
import pyperclip
from PyQt5.QtWidgets import QApplication, QDialog,QCheckBox, QVBoxLayout,QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QLCDNumber, QLabel, QWidget, QFileDialog, QListWidget, QListWidgetItem
import sys
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, QTime, QTimer, Qt

a = chr(34)
file_link = ""
files_links = []
current_folder = False
current_folder_path = ""
link = ''
nameList = []
now12 = ''
files = ''
contractions = ["aren't", "can't", "couldn't", "didn't", "don't", "doesn't", "hadn't", "haven't", "he's", "he'll", "he'd", "here's", "i'm", "i've", "i'll", "i'd", "isn't", "it's", "it'll", "mustn't", "she's", "she'll", "she'd", "shouldn't", "that's", "there's", "they're", "they've", "they'll", "they'd", "wasn't", "we're", "we've", "we'll", "we'd", "weren't", "what's", "where's", "why's", "when's", "who's", "who'll", "won't", "wouldn't", "you're", "you've", "you'll", "you'd", "shan't", "let's", "might've", "should've", "could've", "hasn't"]
data_dict = {"aren't": 'are not', "can't": "can not", "couldn't": "could not", "didn't": "did not", "don't": "do not", "doesn't": "does not", "hadn't": "had not", "haven't": "have not", "he's": "he is", "he'll": "he will", "he'd": "he had", "here's": "here is", "i'm": "i am", "i've": "i have", "i'll": "i will", "i'd": "i had", "isn't": "is not", "it's": "it is", "it'll": "it will", "mustn't": "must not", "she's": "she is", "she'll": "she will", "she'd": "she had", "shouldn't": "should not", "that's": "that is", "there's": "there is", "they're": "they are", "they've": "they have", "they'll": "they will", "they'd": "they had", "wasn't": "was not", "we're": "we are", "we've": "we have", "we'll": "we will", "we'd": "we had", "weren't": "were not", "what's": "what is", "where's": "where is", "why's": "why is", "when's": "when is", "who's": "who is", "who'll": "who will", "won't": "will not", "wouldn't": "would not", "you're": "you are", "you've": "you have", "you'll": "you will", "you'd": "you had", "shan't": "shall not", "let's": "let us", "might've": "might have", "should've": "should have", "could've": "could have", "hasn't": "has not"}

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(272, 57, 800, 600)
        # self.setFixedHeight(600)
        # self.setFixedWidth(800)
        self.setWindowTitle("\tWord Scraper")
        self.setWindowIcon(QIcon("burger.ico"))


        self.lcd_number()

    def lcd_number(self):

        vbox = QVBoxLayout()
        self.labelttl = QLabel("Text Scraper")
        self.labelttl.setAlignment(Qt.AlignCenter)
        self.labelttl.setStyleSheet("font-family:times new roman; font-size: 60px; border-radius: 1cm; border-color:cyan; border: 14px inset greenyellow; background-color:lawngreen; text-align:center;")
        self.labelttl.setFont(QFont("times new roman", 60))
        self.labelttl.setFixedHeight(120)
        vbox.addWidget(self.labelttl)

        self.label2 = QLabel("      ONLY use OPEN button i.e. file explorer for files, don't use it for selecting folders\n      OR\n"
                             "      Copy the Folder Path and paste in respective box\n"
                             "      Folder Path should be without single/double quotes\n"
                             "      Otherwise the Software won't work")

        self.label2.setStyleSheet("color:red")
        self.label2.setFont(QFont("times new roman", 12))
        self.label2.setFixedHeight(77)

        hbox = QHBoxLayout()

        self.label3 = QLabel(" NOTE  ")
        self.label3.setStyleSheet("color:Red")
        self.label3.setFont(QFont("castellar", 27))
        self.label3.setFixedHeight(72)
        self.label3.setFixedWidth(144)

        hbox.addWidget(self.label3)
        hbox.addWidget(self.label2)

        vbox.addLayout(hbox)



        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("\tEnter the Folder link here")
        self.input1.setFont(QFont("times new roman", 16))
        self.input1.setFixedHeight(60)
        self.input1.setStyleSheet("background-color:white")
        hbox12 = QHBoxLayout()
        hbox12.addWidget(self.input1)

        btn2 = QPushButton(" OPEN ")
        btn2.setFont(QFont("times new roman", 29))
        btn2.setStyleSheet("font-family:times new roman; font-size: 29px; border-radius: 1cm; border-color:cyan; border: 14px inset khaki; background-color:yellow; text-align:center;")
        btn2.setFixedWidth(120)
        btn2.clicked.connect(self.open)
        hbox12.addWidget(btn2)

        vbox.addLayout(hbox12)

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("\tEnter the Keyword here")
        self.input2.setFont(QFont("times new roman", 16))
        self.input2.setFixedHeight(60)
        self.input2.setStyleSheet("background-color:white")
        hbox1.addWidget(self.input2)

        hbox = QHBoxLayout()

        btn1 = QPushButton(" SCAN 1 ")
        btn1.setFont(QFont("times new roman", 36))
        btn1.setStyleSheet("font-family:times new roman; font-size: 36px; border-radius: 1cm; border-color:cyan; border: 14px inset violet; background-color:pink; text-align:center;")
        btn1.clicked.connect(self.one_file)
        hbox2.addWidget(btn1)

        btn3 = QPushButton(" SCAN ALL ")
        btn3.setFont(QFont("times new roman", 36))
        btn3.setStyleSheet("font-family:times new roman; font-size: 36px; border-radius: 1cm; border-color:cyan; border: 14px inset pink; background-color:lightpink; text-align:center;")
        btn3.clicked.connect(self.all_files)
        hbox2.addWidget(btn3)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

    def read_file_controller(self):
        global file_link

        a = chr(34)
        b = chr(92)
        c = chr(47)
        d = chr(39)
        splitted = file_link.split(c)
        file_link = splitted[0] + c + splitted[1] + b + splitted[2]
        self.read_file(self, file_link)

    def open(self):
        global file_link
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            file_link = path[0]
            self.input1.setPlaceholderText(file_link)

    def one_file(self):
        try:
            global file_link
            global files_links
            global current_folder
            global current_folder_path
            global files
            # print(file_link)
            b = chr(92)
            c = chr(47)
            d = chr(39)
            folder_link = self.input1.text().lstrip().rstrip()
            placeText = self.input1.placeholderText().strip()
            self.keyword = self.input2.text().lstrip().rstrip().lower()

            if current_folder == False:
                path = ''
                if len(file_link) < 1:
                    if len(folder_link) < 1:
                        return
                    else:
                        folder_link = self.input1.text().lstrip().rstrip()
                else:
                    if '.' in file_link:
                        if file_link[2] == b:
                            temp = file_link.split(b)
                            temp2 = temp.pop(len(temp) - 1)
                            folder_link = b.join(temp)
                        elif file_link[2] == c:
                            temp = file_link.split(c)
                            temp2 = temp.pop(len(temp) - 1)
                            folder_link = c.join(temp)

                if '.' in file_link:
                    path = folder_link
                    self.input1.setPlaceholderText(path)
                elif len(file_link) < 1:
                    path = self.input1.text().lstrip().rstrip()
                    if path[0] == a:
                        stripper = path.split(a)
                        path = stripper[1]
                    elif path[0] == d:
                        stripper = path.split(d)
                        path = stripper[1]
                    else:
                        path = self.input1.text().lstrip().rstrip()
                # print(path)


                if len(path) < 1:
                    return

                path3 = path + '/*.srt'
                current_folder_path = path

            else:
                path3 = current_folder_path + '/*.srt'

            if len(folder_link) > len(placeText):
                files = folder_link
            elif len(placeText) > len(folder_link):
                files = placeText
            elif len(file_link) == len(placeText):
                files = placeText

            # print(files)
            file_link = files
            files_links.append(files)
            self.read_file()
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("Oops!", sys.exc_info()[2], "occurred.")

    def all_files(self):
        try:
            global file_link
            global files_links
            global current_folder
            global current_folder_path
            # print(file_link)
            b = chr(92)
            c = chr(47)
            d = chr(39)
            folder_link = self.input1.text().lstrip().rstrip()
            self.keyword = self.input2.text().lstrip().rstrip().lower()

            if current_folder == False:
                path = ''
                if len(file_link) < 1:
                    if len(folder_link) < 1:
                        return
                    else:
                        folder_link = self.input1.text().lstrip().rstrip()
                else:
                    if '.' in file_link:
                        if file_link[2] == b:
                            temp = file_link.split(b)
                            temp2 = temp.pop(len(temp) - 1)
                            folder_link = b.join(temp)
                        elif file_link[2] == c:
                            temp = file_link.split(c)
                            temp2 = temp.pop(len(temp) - 1)
                            folder_link = c.join(temp)

                if '.' in file_link:
                    path = folder_link
                    self.input1.setPlaceholderText(path)
                elif len(file_link) < 1:
                    path = self.input1.text().lstrip().rstrip()
                    if path[0] == a:
                        stripper = path.split(a)
                        path = stripper[1]
                    elif path[0] == d:
                        stripper = path.split(d)
                        path = stripper[1]
                    else:
                        path = self.input1.text().lstrip().rstrip()
                # print(path)


                if len(path) < 1:
                    return

                path3 = path + '/*.srt'
                current_folder_path = path

            else:
                path3 = current_folder_path + '/*.srt'
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("Oops!", sys.exc_info()[2], "occurred.")



        files = glob.glob(path3)
        # print(files)
        for i in files:
            file_link = i
            files_links.append(i)
        self.read_file()

        message = QMessageBox.question(self, "Choice Message", "Do You want to continue scanning this Folder ? ",
                                       QMessageBox.Yes | QMessageBox.No)

        if message == QMessageBox.Yes:
            if len(current_folder_path) < 1:
                current_folder_path = path
                current_folder = True
            else:
                current_folder_path = current_folder_path
                current_folder = True
        elif message == QMessageBox.No:
            file_link = ""
            folder_link = ""
            current_folder_path = ""
            current_folder = False




    def read_file(self):
        try:
            global now12
            now = str(datetime.datetime.now())
            newNow = ""
            for item in now:
                if item != ":" and item != " ":
                    newNow += item
                else:
                    newNow += "_"
            now = newNow
            now12 = now
            os.system(f"mkdir {now}")
            # print("***** read file called *****")
            global file_link
            global files_links
            global nameList
            global contractions
            global data_dict
            a = chr(34)
            b = chr(92)
            c = chr(47)
            d = chr(39)
            # print('1', file_link)
            sub_link = self.input1.text().lstrip().rstrip()
            self.keyword = self.input2.text().lstrip().rstrip().lower()
            if len(file_link) < 1:
                if len(sub_link) < 1:
                    return
                else:
                    stripper = sub_link.split(a)

                    sub_link = stripper[0]

            else:
                sub_link = file_link
                # print(sub_link)

            if sub_link.split('.')[-1] != 'srt':
                self.label2.setText(
                    "\tFile Type not supported\n\tOnly MS Word (.srt) files are supported\n\tKindly select a MS Word file to Proceed")
                self.label2.setFont(QFont("times new roman", 16))
                return
            # print(2, sub_link)
            if len(files_links) < 1:
                files_links.append(sub_link)
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("Oops!", sys.exc_info()[2], "occurred.")

        try:
            settings_dialog = QDialog()
            settings_dialog.setModal(True)
            # settings_dialog.setStyleSheet("background-color:white")
            settings_dialog.setWindowTitle("\ttext file")
            settings_dialog.setGeometry(35, 50, 1300, 660)
            # settings_dialog.showFullScreen()
            vbox_layout = QVBoxLayout()

            self.label = QListWidget()
            self.label.clicked.connect(self.item_clicked)
            num = 0
            text = ""

            for link in files_links:
                overall = []
                self.label.insertItem(num, text)
                self.label.setFont(QFont("times new roman", 16))
                self.setStyleSheet("background-color:white")

                num += 1

                text = QListWidgetItem()
                name = link.split(b)[-1]
                mydata = name.split('.')

                mynum = name
                temp = mynum.split(".").pop(-1)
                mynum = "".join(mynum)
                fileName = f'{mynum}.csv'
                if "/" in fileName:
                    fileName = fileName.split("/")[-1]

                if "\\" in fileName:
                    fileName = fileName.split("\\")[-1]
                print("This is file name", fileName)
                if fileName in nameList:
                    pass
                else:
                    nameList.append(fileName)
                fhand = open(f"{now}/{fileName}", "a")
                fhand.write("Dialogue, Start Time, End Time\n")
                fhand.close()
                if "/" in name:
                    name = name.split("/")[-1]

                if "\\" in name:
                    name = name.split("\\")[-1]
                # print("my data length", len(mydata))
                text.setText("\n" + name + "\n\nName :\t" + mydata[0] + "\nYear :\t" + mydata[1] + "\nRip :\t" + mydata[3] + "\nLanguage :\t" + mydata[-2].strip().split("-")[-1])
                text.setFont(QFont("times new roman", 24))
                self.label.insertItem(num, text)
                num += 1
                doc = open(link, 'r')
                doc = doc.readlines()
                doc = ''.join(doc)
                doc = doc.strip()
                doc = doc.split('\n\n')

                for z, i in enumerate(doc):
                    printed = False
                    count = i.lower().count(self.keyword)
                    data = i.lower().split()
                    for count, myitem in enumerate(data):
                        if myitem in contractions:
                            data[count] = data_dict[myitem]
                    data = " ".join(data)
                    data = data.lower().split()
                    if "<i>" in data[0]:
                        another = ''
                        for c in range(3, len(data[0])):
                            another += data[0][c]
                        data[0] = another

                    if "</i>" in data[-1]:
                        another = ''
                        for c in range(0, len(data[-1])-4):
                            another += data[-1][c]
                        data[-1] = another

                    word_list = self.keyword.split()
                    if "<i>" in word_list[0]:
                        another = ''
                        for c in range(3, len(word_list[0])):
                            another += word_list[0][c]
                        word_list[0] = another

                    if "</i>" in word_list[-1]:
                        another = ''
                        for c in range(0, len(word_list[-1]) - 4):
                            another += word_list[-1][c]
                        word_list[-1] = another
                    for count2, myitem2 in enumerate(word_list):
                        if myitem2 in contractions:
                            word_list[count2] = data_dict[myitem2]
                    word_list = " ".join(word_list)
                    word_list = word_list.lower().split()

                    word_dict = {}
                    for aitem in word_list:
                        if aitem in contractions:
                            aitem = data_dict[aitem]
                            for term in aitem:
                                word_dict[term] = False
                        else:
                            word_dict[aitem] = False
                    phrase = []
                    for word in word_list:

                        address = []
                        for j, index in enumerate(data):
                            if word in index:
                                word_dict[word] = True
                                address.append(j + 1)


                        # print(count, "\t#\t algorithm")
                        if len(address) > 0:
                            g = ", "
                            address = [str(locat) for locat in address]
                            phrase.append(g.join(address))

                    try:
                        phrase = [set(item) for item in phrase]
                        status = True
                        for myitem in word_dict:
                            if word_dict[myitem] == False:
                                status = False
                        if status:
                            # text = "\n\nThis phrase completely exists in :\n\nparagraph {}".format(z + 1)
                            # overall.append(text)
                            # overall.append(' ')
                            # overall.append(i)
                            item = i
                            if '-->' in item:

                                fhand = open(f"{now}/{fileName}", "a")
                                startTime = item.split("\n")[1].strip().split('-->')[0].strip().split(',')[0]
                                endTime = item.split("\n")[1].strip().split('-->')[1].strip().split(',')[0]
                                temp = item.split("\n")
                                a = temp.pop(0)
                                a = temp.pop(0)
                                dialogue = " ".join(temp).strip()
                                # print(startTime, endTime, dialogue)
                                newDialogue = ""
                                for letter in dialogue:
                                    if letter != ",":
                                        newDialogue += letter
                                dialogue = newDialogue
                                newtemp = dialogue[0:3]
                                if newtemp == "<i>":
                                    another = ''
                                    for c in range(3, len(dialogue)-4):
                                        another += dialogue[c]
                                    dialogue = another
                                fhand.write(f"{dialogue}, {startTime}, {endTime}\n")
                                fhand.close()

                            phrase = []
                        status = False

                    except:
                        print("Oops!", sys.exc_info()[0], "occurred.")
                        print("Oops!", sys.exc_info()[1], "occurred.")
                        print("Oops!", sys.exc_info()[2], "occurred.")
                        return

                # try:
                #
                #
                #     # for item in overall:
                #     #     # self.label.insertItem(num, str(item))
                #     #
                #     #
                #     #
                #     #     num += 1
                # except:
                #     print("Oops!", sys.exc_info()[0], "occurred.")
                #     print("Oops!", sys.exc_info()[1], "occurred.")
                #     print("Oops!", sys.exc_info()[2], "occurred.")

                text = " "
                self.label.insertItem(num, text)
                num += 1
            vbox_layout.addWidget(self.label)

            settings_dialog.setLayout(vbox_layout)
            settings_dialog.exec_()
            files_links = []
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("Oops!", sys.exc_info()[2], "occurred.")

    def item_clicked(self):
        try:
            global now12
            global current_folder_path
            item = self.label.currentItem().text()

            if item.strip().split("\n")[0].strip().split('.')[-1] == 'srt':
                self.link = current_folder_path + "/" + item.strip().split("\n")[0].strip()
                temp = item.strip().split("\n")[0].strip()
                v1 = temp.split(".").pop(-1)
                file = pd.read_csv(f"{now12}/{temp}.csv")
                file.to_html("new.html")
                os.system('new.html')
                os.system('del new.html')
                self.query()
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("Oops!", sys.exc_info()[2], "occurred.")



    def query(self):
        try:
            settings_dialog = QDialog()
            settings_dialog.setModal(True)
            settings_dialog.setStyleSheet("background-color:#84eefa; border-radius: 1cm;")
            settings_dialog.setWindowTitle("Select Action")
            settings_dialog.setWindowIcon(QIcon("burger.ico"))
            settings_dialog.setGeometry(327, 156, 700, 200)

            vbox_master = QHBoxLayout()

            btn2 = QPushButton("VIEW\nLINKS")
            btn2.setFont(QFont("times new roman", 60))
            btn2.setStyleSheet(
                "font-family:times new roman; font-size: 60px; border-radius: 1cm; border-color:cyan; border: 14px inset greenyellow; background-color:lawngreen; text-align:center;")
            # btn2.setFixedWidth(120)
            btn2.pressed.connect(self.showLinks)
            btn2.released.connect(settings_dialog.close)
            vbox_master.addWidget(btn2)

            btn3 = QPushButton("ADD\nLINK")
            btn3.setFont(QFont("times new roman", 60))
            btn3.setStyleSheet(
                "font-family:times new roman; font-size: 60px; border-radius: 1cm; border-color:cyan; border: 14px inset skyblue; background-color:lightblue; text-align:center;")
            # btn2.setFixedWidth(120)
            btn3.pressed.connect(self.inputLinks)
            btn3.released.connect(settings_dialog.close)
            vbox_master.addWidget(btn3)

            settings_dialog.setLayout(vbox_master)
            settings_dialog.exec_()
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("Oops!", sys.exc_info()[2], "occurred.")

    def showLinks(self):
        try:

            global current_folder_path

            settings_dialog2 = QDialog()
            settings_dialog2.setModal(True)
            settings_dialog2.setStyleSheet("background-color:#84eefa; border-radius: 1cm;")
            settings_dialog2.setWindowTitle("Change Image")
            settings_dialog2.setWindowIcon(QIcon("burger.ico"))
            settings_dialog2.setGeometry(327, 156, 700, 200)

            vbox_master = QVBoxLayout()

            self.list = QListWidget()
            self.list.setFont(QFont("times new roman", 22))
            self.list.clicked.connect(lambda: pyperclip.copy(self.list.currentItem().text().strip()))
            vbox_master.addWidget(self.list)

            print(self.link)

            fhand = open(self.link, 'r')
            n = 0
            for line in fhand:
                if line.strip().split("=>")[0].strip() == "Link":
                    self.list.insertItem(n, "     ")
                    n += 1
                    self.list.insertItem(n, line.strip().split("=>")[1].strip())
                    n += 1

            settings_dialog2.setLayout(vbox_master)
            settings_dialog2.exec_()

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("Oops!", sys.exc_info()[2], "occurred.")

    def inputLinks(self):
        settings_dialog3 = QDialog()
        settings_dialog3.setModal(True)
        settings_dialog3.setStyleSheet("background-color:#84eefa; border-radius: 1cm;")
        settings_dialog3.setWindowTitle("Change Image")
        settings_dialog3.setWindowIcon(QIcon("burger.ico"))
        settings_dialog3.setGeometry(327, 156, 700, 200)

        vbox_master = QVBoxLayout()

        label = QLabel("Enter Link")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("times new roman", 48))
        label.setStyleSheet("font-family:times new roman; font-size: 48px; border-radius: 1cm; border-color:cyan; border: 14px inset blue; background-color:skyblue; text-align:center;")
        vbox_master.addWidget(label)

        label2 = QLabel()
        label2.setFixedHeight(48)
        vbox_master.addWidget(label2)


        self.linkin = QLineEdit()
        self.linkin.setAlignment(Qt.AlignCenter)
        self.linkin.setStyleSheet("background-color:white; border-radius:15px; color:black;")
        self.linkin.setFont(QFont("times new roman", 24))
        self.linkin.setPlaceholderText("Enter the Link Here")
        vbox_master.addWidget(self.linkin)

        label3 = QLabel()
        label3.setFixedHeight(48)
        vbox_master.addWidget(label3)

        hbox = QHBoxLayout()

        btn = QPushButton("     SUBMIT     ")
        btn.setFont(QFont("times new roman", 29))
        btn.setStyleSheet(
            "font-family:times new roman; font-size: 36px; border-radius: 1cm; border-color:cyan; border: 14px inset greenyellow; background-color:lawngreen; text-align:center;")
        btn.setFixedWidth(172)
        btn.pressed.connect(self.submitlink)
        btn.released.connect(settings_dialog3.close)
        hbox.addWidget(btn)
        vbox_master.addLayout(hbox)



        settings_dialog3.setLayout(vbox_master)
        settings_dialog3.exec_()

    def submitlink(self):
        text = self.linkin.text().strip()
        text = "\nLink => " + text
        fhand12 = open(self.link, 'a')
        fhand12.write(text)
        fhand12.close()



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())

