import customtkinter
from PIL import Image, ImageTk
import os
import json
import minecraft_launcher_lib
import subprocess
from CTkListbox import *
from CTkMessagebox import CTkMessagebox
import uuid
from setmine import ad_rp, adNewOptions
from random_username.generate import generate_username

customtkinter.set_appearance_mode("dark")

class App(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open("settings.json", "r") as sf:
            self.sett = json.load(sf)

        self.minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', f"{self.sett["minecraftDirPathName"]}")
        self.avVerList = minecraft_launcher_lib.utils.get_version_list()

        try:
            with open(f"{self.minecraft_directory}\\users.json", "r") as us:
                self.usnms = json.load(us)
        except FileNotFoundError:
            with open(f"{self.minecraft_directory}\\users.json", "w") as us:
                us.write("[]")
            self.usnms = []

        print(self.usnms)

        self.aids = []
        for i in range(len(self.avVerList)):
            if self.avVerList[i]["type"] == "release":
                self.aids.append(self.avVerList[i]["id"])

        self.title("KavasakiLauncher")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.iconbitmap(f"{self.sett["appIconFile"]}")

        # load and create background image
        current_path = self.sett["curentPath"]
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + self.sett["backgroundPath"]),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="KavasakiLauncher\nA best minecraft launcher!",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(20, 15))
        self.usnms.append("Generate Random Nickname")
        self.usnms.append("Add New Nickname")
        self.usernameCB = customtkinter.CTkComboBox(self.login_frame,values=self.usnms)
        self.usernameCB.grid(row=1, column=0, padx=30, pady=(8, 8))
        self.versionsDirectory = self.minecraft_directory + "\\versions"
        try:
            self.stVersionsList = os.listdir(self.versionsDirectory)
        except FileNotFoundError:
            self.stVersionsList = []
        self.versionsListText = "Installed versions:"
        self.version_label = customtkinter.CTkLabel(self.login_frame, text=self.versionsListText,font=customtkinter.CTkFont(size=20, weight="bold"))
        self.versionListbox = CTkListbox(self.login_frame, height=10)
        self.versionListbox.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.version_label.grid(row=2, column=0, padx=30, pady=(5, 5))
        self.vlbsize = 0
        for i in range(len(self.avVerList)):
            if self.avVerList[i]["type"] == "release":
                self.versionListbox.insert(i, f"{self.avVerList[i]["id"]}")
                self.vlbsize += 1

        for v in range(len(self.stVersionsList)):
            if self.stVersionsList[v] in self.avVerList:
                pass
            else:
                self.versionListbox.insert(self.vlbsize+1, f"{self.stVersionsList[v]}")
                self.vlbsize + 1

        self.typeVerLB = customtkinter.CTkComboBox(self.login_frame,values=["Vanilla", "Forge", "Fabric", "Quilt"])
        self.typeVerLB.grid(row=5, column=0, padx=30, pady=(5, 15))
        self.typeVerLB.set("Vanilla")

        self.login_button = customtkinter.CTkButton(self.login_frame, text="START", command=self.login_event, width=200)
        self.login_button.grid(row=6, column=0, padx=30, pady=(10, 15))
        self.insProgBar = customtkinter.CTkProgressBar(self.login_frame)
        self.insProgBar.grid(row=7, column=0, padx=30, pady=(10, 15))
        self.insProgBar.set(0/100)

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_label = customtkinter.CTkLabel(self.main_frame, text="KavasakiLauncher\nTHANC U FOR GAMING!",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=30, pady=(30, 15))

        self.tnick = customtkinter.CTkFrame(self, corner_radius=0)
        self.tnick.grid_columnconfigure(0, weight=1)
        self.tnick_label = customtkinter.CTkLabel(self.tnick, text="Type your nickname", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.tnick_label.grid(row=0, column=0, padx=30, pady=(30, 15))
        self.tnentry = customtkinter.CTkEntry(master=self.tnick, placeholder_text="NICKNAME")
        self.tnentry.grid(row=1, column=0, padx=30, pady=(10, 15))
        self.tbutton = customtkinter.CTkButton(master=self.tnick, text="SAVE", command=self.nsave)
        self.tbutton.grid(row=2, column=0, padx=30, pady=(10, 15))

    def nsave(self):
        with open(f"{self.minecraft_directory}\\users.json", "w") as us:
            self.usnms.remove("Generate Random Nickname")
            self.usnms.remove("Add New Nickname")
            self.usnms.append(self.tnentry.get())
            json.dump(self.usnms, us)
            CTkMessagebox(message="Ваш ник был сохранён!\nПерезапустите лаунчер для входа в игру!", icon="check", option_1="OK")

    def login_event(self):
        print("Start pressed - nickname:", self.usernameCB.get(), "version:", self.versionListbox.get())
        if self.usernameCB.get() == "Add New Nickname":
            self.login_frame.grid_forget()
            self.tnick.grid(row=0, column=0, sticky="nsew", padx=100)
        else:
            self.login_frame.grid_forget()
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)

        print(self.versionListbox.get())
        print(self.aids)
        if self.versionListbox.get() in self.stVersionsList:
            print("True")
        else:
            print("False")

        self.insProgBar.start()
        if not self.versionListbox.get() in self.stVersionsList:
            verlistget = self.versionListbox.get()
            vibOr = self.typeVerLB.get()
            # CTkMessagebox(title="Info", message="Установка выбранной версии началась!")
            if vibOr == "Vanilla":
                minecraft_launcher_lib.install.install_minecraft_version(versionid=verlistget,minecraft_directory=self.minecraft_directory)
            elif vibOr == "Forge":
                minecraft_launcher_lib.forge.install_forge_version(verlistget, self.minecraft_directory)
            elif vibOr == "Fabric":
                minecraft_launcher_lib.fabric.install_fabric(verlistget, self.minecraft_directory)
            elif vibOr == "Quilt":
                minecraft_launcher_lib.quilt.install_quilt(verlistget, self.minecraft_directory)
            CTkMessagebox(message="Версия успешно загружена!", icon="check", option_1="Хорошо")
        else:

            self.datalist = os.listdir(self.sett["dataPath"])
            self.rpOnData = False
            for i in range(len(self.datalist)):
                if self.datalist[i] == self.sett["rpFileName"]:
                    self.rpOnData = True
            if self.rpOnData:
                ad_rp(self.minecraft_directory, self.sett["dataPath"], self.sett["rpFileName"])
            stfilePath = self.sett["dataPath"] + "\\started.kav"
            if int(open(stfilePath, "r").read()) == 1:
                adNewOptions(self.sett["nopFileName"], self.sett["dataPath"], self.minecraft_directory)
                open(stfilePath, "w").write("0")

            if self.usernameCB.get() == "Generate Random Nickname":
                self.username = generate_username()[0]
            elif self.usernameCB.get() == "Add New Nickname":
                pass
            else:
                self.username = self.usernameCB.get()

            if self.usernameCB.get() == "Add New Nickname":
                pass

            else:
                options = {
                    'username': self.username,
                    'uuid': str(uuid.uuid1()),
                    'token': ''
                }
                print(options)
                subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=self.versionListbox.get(),minecraft_directory=self.minecraft_directory,options=options))


if __name__ == "__main__":
    app = App()
    app.mainloop()
