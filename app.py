try:
    import tkinter as tk
except:
    import Tkinter as tk

import pygubu
import pymongo
import webbrowser


def add_file(uploads, file_name, file_url, file_author):
    data = { "file_name": file_name, "file_url": file_url, "file_author": file_author}
    x = uploads.insert_one(data)

def retrieve_files(uplaods):
    temp = []
    for x in uplaods.find():
        temp.append(x)
    return temp

class Application(pygubu.TkApplication):
    def __init__(self, master, uploads):
        self.builder = builder = pygubu.Builder()

        builder.add_from_file('main_screen.ui')

        self.mainwindow = builder.get_object('Frame_2', master)
        self.etv = builder.get_object('editabletreeview_1')
        self.etv.column("#0", width=0)
        self.uploads = uploads

        builder.connect_callbacks(self)
        
        list = retrieve_files(uploads)

        for l in list:
            self.etv.insert('', tk.END, values=(l["file_name"], l["file_url"], l["file_author"]))


    def share(self):
        file_name = self.builder.tkvariables['file_name'].get()
        file_url = self.builder.tkvariables['file_url'].get()
        file_author = self.builder.tkvariables['file_author'].get()

        if file_name != "" and file_url != "" and file_author != "":
            add_file(self.uploads, file_name, file_url, file_author)
            self.etv.insert('', tk.END, values=(file_name, file_url, file_author))

    def on_row_selected(self, event):
        selected = self.etv.item(event.widget.selection(),"values")
        print(selected)
        webbrowser.open(selected[1], 2) # Equivalent to: webbrowser.open_new_tab(a_website)



def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["python_project_file_Share"]
    uploads = mydb["uploads"]

    root = tk.Tk()
    app = Application(root, uploads)
    root.mainloop()

if __name__ == '__main__':
    main()