from tkinter import *
from math import *
from array import *
from tkinter import messagebox
from tkinter import font as tkFont
import json
import re
import os.path
from tkinter import filedialog
from PIL import ImageTk, Image


users_list = []
groups_list = []


class User:
    def __init__(self, username):
        self.username = username
        self.contacts = []
        self.groups = []
        self.messages = {}


class Group:
    def __init__(self, username):
        self.groupname = username
        self.posts = []
        self.members = []


def fileToArray(input_file):
    k = 0

    for i in range(len(input_file)):
        if input_file[i].split()[0] == "#users":
            continue
        else:
            if input_file[i].split()[0] == "#groups":
                k = i + 1
                break
            else:
                users_list.append(
                    User(
                        input_file[i].split(",")[0].split(":")[0],
                    )
                )

                users_list[k].contacts.append(
                    input_file[i].split(",")[0].split(":")[1].strip()
                )
                for h in range(len(input_file[i].split(",")) - 1):
                    users_list[k].contacts.append(
                        input_file[i].split(",")[h + 1].strip()
                    )
                k += 1

    for i in range(len(users_list)):
        if users_list[i].contacts[-1][-1] == "\n":
            users_list[i].contacts[-1] = users_list[i].contacts[-1][:-1]
    t = 0

    while k < len(input_file):
        groups_list.append(Group(input_file[k].split(",")[0].split(":")[0]))
        groups_list[t].members.append(input_file[k].split(",")[0].split(":")[1].strip())
        for h in range(len(input_file[k].split(",")) - 1):
            groups_list[t].members.append(input_file[k].split(",")[h + 1].strip())

        k += 1
        t += 1
    for i in range(len(groups_list)):
        if groups_list[i].members[-1][-1] == "\n":
            groups_list[i].members[-1] = groups_list[i].members[-1][:-1]
    # print(groups_list[i].groupname)
    # print(groups_list[i].members)


def userGroup():
    for singleGroup in groups_list:
        for m in singleGroup.members:
            for singleUser in users_list:
                if m == singleUser.username:

                    singleUser.groups.append(singleGroup.groupname)


def imporrt():
    f = open("messages.txt", "r")
    mess_file = f.readlines()

    for i in range(len(mess_file)):
        if mess_file[i].find("#USER") != -1:

            usa = re.sub(r"[\n\t\s]*", "", mess_file[i].split(":")[1])
            i += 1
            for singleUser in users_list:
                if singleUser.username == usa:

                    singleUser.messages = json.loads(mess_file[i].rstrip())
        if mess_file[i].find("#GROUP") != -1:
            grp = re.sub(r"[\n\t\s]*", "", mess_file[i].split(":")[1])
            for singleGroup in groups_list:
                if grp == singleGroup.groupname:
                    i += 1

                    singleGroup.posts = re.findall(r"'(.*?)'", mess_file[i], re.DOTALL)


f = open("social_network.txt", "r")
input_file = f.readlines()
f.close()


fileToArray(input_file)

if os.path.isfile("messeges.txt"):
    imporrt()

userGroup()
# ---------------------------- tkinter------------------

root = Tk()
root.title("LOG IN")
root.geometry("700x900")
name = StringVar()


Label(
    root,
    text="Welcome to Social Network",
    fg="white",
    font=("bold", "26"),
    bg="#075e54",
).pack(side=TOP, fill="x")


def nav_(frame, text_):
    return Label(
        frame,
        text=text_,
        font=("bold", "26"),
        bg="#075e54",
        fg="white",
        width="700",
        padx="5",
        pady="5",
    )


def export(main_page):
    main_page.destroy
    exp = open("messages.txt", "w")
    for singleUser in users_list:
        exp.write("#USER: ")
        exp.write(singleUser.username + "\n")
        exp.write(json.dumps(singleUser.messages))
        exp.write("\n")

    for singleGroup in groups_list:
        exp.write("#GROUP: ")
        exp.write(singleGroup.groupname + "\n")
        exp.write(str(singleGroup.posts))
        exp.write("\n")


def button_(frame, main_page):
    return Button(
        frame,
        text="Back AND EXPORT",
        command=lambda: export(main_page),
        padx="5",
        pady="5",
        bg="#075e54",
    )


def contactsList(frame, users):
    global content_contact
    content_contact = Frame(
        frame,
        bg="#2c2f33",
    )
    for user in users.contacts:
        Label(
            content_contact,
            text=user,
            bg="#2c2f33",
            fg="#fd5217",
            font=("bold", "15"),
            pady="15",
            anchor="e",
        ).pack()
    return content_contact


def groupsList(frame, users):
    global content_groups
    content_groups = Frame(
        frame,
        bg="#2c2f33",
    )
    for user in users.groups:
        Label(
            content_groups,
            text=user,
            bg="#2c2f33",
            fg="#fd5217",
            font=("bold", "15"),
            pady="15",
            anchor="w",
        ).pack()
    return content_groups


def inboxList(users, type):
    font_color = "#68FF00"

    if type == "GROUP":

        for singleGroup in users.groups:
            for g in groups_list:
                if singleGroup == g.groupname:
                    Label(
                        contents_inbox,
                        text=g.groupname,
                        bg="#99aab5",
                        fg=font_color,
                        font=("bold", "20"),
                        pady="8",
                    ).pack(fill="x")
                    if len(g.posts) == 0:
                        Label(
                            contents_inbox,
                            text="No Posts",
                            bg="#2c2f33",
                            fg=font_color,
                            font=("bold", "15"),
                            pady="5",
                            justify=LEFT,
                            anchor="w",
                        ).pack(fill="x")

                    for con in g.posts:
                        if os.path.isfile(con):
                            global iml
                            pi = Image.open(con)
                            resi = pi.resize((100, 100), Image.ANTIALIAS)
                            iml = ImageTk.PhotoImage(resi)
                            Label(
                                contents_inbox,
                                image=iml,
                            ).pack()

                        else:
                            Label(
                                contents_inbox,
                                text=con,
                                bg="#2c2f33",
                                fg=font_color,
                                font=("bold", "15"),
                                pady="5",
                                justify=LEFT,
                                anchor="w",
                            ).pack(fill="x")
    if type == "USER":
        for use in users.messages:
            Label(
                contents_inbox,
                text=use,
                bg="#99aab5",
                fg=font_color,
                font=("bold", "20"),
                pady="8",
            ).pack(fill="x")

            for i in range(len(users.messages[use])):
                if os.path.isfile(users.messages[use][i]):

                    pi = Image.open(users.messages[use][i])
                    resi = pi.resize((100, 100), Image.ANTIALIAS)
                    global im
                    im = ImageTk.PhotoImage(resi)
                    Label(
                        contents_inbox,
                        image=im,
                    ).pack()
                else:
                    Label(
                        contents_inbox,
                        text=users.messages[use][i],
                        bg="#2c2f33",
                        fg=font_color,
                        font=("bold", "15"),
                        pady="5",
                        justify=LEFT,
                        anchor="w",
                    ).pack(fill="x")

    return contents_inbox


def clrList(users, type):
    contents_inbox.pack_forget()
    for w in contents_inbox.winfo_children():
        w.destroy()

    inboxList(users, type).pack(fill="both", expand="True")


def defaultInbox(frame, users):
    global contents_inbox
    contents_inbox = Frame(
        frame,
        bg="#2c2f33",
    )
    Button(
        contents_inbox,
        text="USER",
        bg="#2c2f33",
        fg="#f56420",
        font=("bold", "15"),
        pady="15",
        borderwidth=0,
        relief=FLAT,
        command=lambda: clrList(users, "USER"),
    ).pack()
    Button(
        contents_inbox,
        text="GROUP",
        bg="#2c2f33",
        fg="#f56420",
        font=("bold", "15"),
        pady="15",
        borderwidth=0,
        relief=FLAT,
        command=lambda: clrList(users, "GROUP"),
    ).pack()
    return contents_inbox


def msg_us(gr, strt):
    if er_.get().strip() == "":
        messagebox.showinfo("BLANK MESSAGE", "You cannot send a Blank Message")
        return
    for singleUser in users_list:
        if gr == singleUser.username:

            if strt in singleUser.messages:
                singleUser.messages[strt].append(er_.get())
            else:
                singleUser.messages[strt] = []
                singleUser.messages[strt].append(er_.get())
            # print(singleUser.username)
            # print(singleUser.messages)
            messagebox.showinfo("MESSAGE SENT!", "Your Message is sent!!")

            er_.delete(0, END)


def msg_gr(gr):

    if er_.get().strip() == "":
        messagebox.showinfo("BLANK MESSAGE", "You cannot send a Blank Message")
        return
    for singleGroup in groups_list:
        if gr == singleGroup.groupname:

            singleGroup.posts.append(er_.get())
            messagebox.showinfo("MESSAGE SENT!", "Your Message is sent!!")

            er_.delete(0, END)


def img():
    root.filename = filedialog.askopenfilename(
        filetypes=(("png fles", "*.png"), ("jpg files", "*.jpg")),
    )
    er_.insert(0, root.filename)


def postsList(frame, users):
    global content_post
    font_color = "#68FF00"
    content_post = Frame(
        frame,
        bg="#2c2f33",
    )
    global er_
    global defg
    defg = StringVar()
    er_ = Entry(content_post, text="type youy message here")
    er_.pack(ipady="30", side=BOTTOM, fill="x")
    Button(
        content_post,
        text="Choose Image",
        command=img,
        padx="5",
        pady="5",
        bg="#075e54",
    ).pack(side=BOTTOM, fill="x")

    if len(users.groups) != 0:
        Label(
            content_post,
            text="GROUPS: (click on group where you want to post)",
            bg="#99aab5",
            fg=font_color,
            font=("bold", "18"),
            pady="8",
            justify=LEFT,
            anchor="w",
        ).pack(fill="x")
        for gr in users.groups:
            Button(
                content_post,
                text=gr,
                bg="#2c2f33",
                fg="#7dbeb8",
                font=("bold", "15"),
                pady="5",
                borderwidth=0,
                relief=FLAT,
                command=lambda gr=gr: msg_gr(gr),
            ).pack(fill="x")
    if len(users.contacts) != 0:
        Label(
            content_post,
            text="USERS: (click on the contact you want to share with)",
            bg="#99aab5",
            fg=font_color,
            font=("bold", "20"),
            pady="8",
            justify=LEFT,
            anchor="w",
        ).pack(fill="x")
        for gr in users.contacts:
            Button(
                content_post,
                text=gr,
                bg="#2c2f33",
                fg="#7dbeb8",
                font=("bold", "15"),
                pady="5",
                borderwidth=0,
                relief=FLAT,
                command=lambda gr=gr: msg_us(gr, users.username),
            ).pack(fill="x")

    return content_post


def newTab(users):
    main_page = Toplevel()
    main_page.geometry("550x500")
    main_page.rowconfigure(0, weight=1)
    main_page.columnconfigure(0, weight=1)
    Contacts = Frame(main_page)
    Groups = Frame(main_page)
    Inbox = Frame(main_page)
    Post = Frame(main_page)
    Contacts.p = "Contacts"
    Groups.p = "Groups"
    Inbox.p = "Inbox"
    Post.p = "Post"

    def swap(frame):
        frame.tkraise()

    # ------ drop down menu____________
    def option_(frame):
        OptionMenu_ = Frame(frame, bg="#eedc82", width=40)
        current = StringVar()
        u = []
        for i in users_list:
            u.append(i.username)
        current.set(users.username)

        userMenu = OptionMenu(OptionMenu_, current, *u)
        # --------------------Manin Part________________
        def change_dropdown(*args):
            content_contact.pack_forget()
            content_groups.pack_forget()
            contents_inbox.pack_forget()
            content_post.pack_forget()
            for w in content_contact.winfo_children():
                w.destroy()
            for wg in content_groups.winfo_children():
                wg.destroy()
            for wg in contents_inbox.winfo_children():
                wg.destroy()
            for wg in content_post.winfo_children():
                wg.destroy()

            contactsList(Contacts, users_list[u.index(current.get())]).pack(
                fill="both", expand="True"
            )
            groupsList(Groups, users_list[u.index(current.get())]).pack(
                fill="both", expand="True"
            )
            defaultInbox(Inbox, users_list[u.index(current.get())]).pack(
                fill="both", expand="True"
            )
            postsList(Post, users_list[u.index(current.get())]).pack(
                fill="both", expand="True"
            )

        current.trace("w", change_dropdown)
        helv20 = tkFont.Font(family="Helvetica", size=20)
        userMenu.config(font=helv20)

        userMenu.pack(ipady=5)

        Button(
            OptionMenu_,
            text="CONTACTS",
            bg="#eedc82",
            command=lambda: swap(Contacts),
            fg="black",
            font=("bold", "15"),
            borderwidth=0,
            relief=FLAT,
        ).pack()
        Button(
            OptionMenu_,
            text="GROUPS",
            bg="#eedc82",
            command=lambda: swap(Groups),
            fg="black",
            font=("bold", "15"),
            borderwidth=0,
            relief=FLAT,
        ).pack()
        Button(
            OptionMenu_,
            text="INBOX",
            bg="#eedc82",
            command=lambda: swap(Inbox),
            fg="black",
            font=("bold", "15"),
            borderwidth=0,
            relief=FLAT,
        ).pack()
        Button(
            OptionMenu_,
            text="POST",
            bg="#eedc82",
            command=lambda: swap(Post),
            fg="black",
            font=("bold", "15"),
            borderwidth=0,
            relief=FLAT,
        ).pack()

        return OptionMenu_

    for frame in (Contacts, Groups, Inbox, Post):
        frame.grid(row=0, column=0, sticky="nsew")
        nav_(frame, frame.p).pack(side=TOP, fill="x")
        button_(frame, main_page).pack(side=BOTTOM, fill="x")
        option_(frame).pack(side=LEFT, fill="y")

    contactsList(Contacts, users).pack(fill="both", expand="True")
    groupsList(Groups, users).pack(fill="both", expand="True")
    defaultInbox(Inbox, users).pack(fill="both", expand="True")
    postsList(Post, users).pack(fill="both", expand="True")

    Inbox.tkraise()


def plot():
    for users in users_list:
        if users.username == name.get():
            newTab(users)

            return

    messagebox.showinfo("INVALID USERNAME", "There is no user with this username")


hex_ = "#696969"

root_ = Frame(root, bg="blue", borderwidth=10, relief=RAISED)
root_.pack(expand="True")
f = Frame(root_, bg=hex_, borderwidth=14, relief=FLAT)
f.pack(expand="True", fill="both")

Label(f, text="Username", bg=hex_).pack(expand="True")
Entry(f, textvariable=name).pack(pady=10, padx=20, fill="both")


bu = Button(f, text="LOG-IN", command=plot, padx=5, pady=5, bg="blue")
bu.pack(pady=20, padx=20, fill="both")


root.mainloop()


## Galat naame k liye kuch karna hia XXXXXXX
## Contacts daale hai XXXXXX
## Groups batnane hai XXXXX
## Drop down menu for Users XXXXXXX
## Groups ka content show karna hai XXXXXXX
## Post ka GUI XXXXXX
## img ka dekhn hai XXXXX
## file handling   XXXXXXXXXX