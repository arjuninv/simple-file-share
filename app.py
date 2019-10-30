    try:
        import tkinter as tk
    except:
        import Tkinter as tk

    import pygubu
    import pymongo
    import webbrowser
    import os.path as path
    import json
    from tkinter import messagebox



    def add_file(uploads, file_name, file_url, file_author):
        data = { "file_name": file_name, "file_url": file_url, "file_author": file_author}
        x = uploads.insert_one(data)

    def retrieve_files(uplaods):
        return uplaods.find()

    class Application(pygubu.TkApplication):
        def __init__(self, master, uploads, backup):
            self.builder = builder = pygubu.Builder()

            builder.add_from_file('main_screen.ui')

            self.mainwindow = builder.get_object('Frame_2', master)
            self.etv = builder.get_object('editabletreeview_1')
            self.share_view = builder.get_object('Labelframe_4')
            self.etv.column("#0", width=0)
            self.uploads = uploads

            builder.connect_callbacks(self)
            
            if backup == "":
                list = retrieve_files(uploads)
                save_data = []
                for l in list:
                    self.etv.insert('', tk.END, values=(l["file_name"], l["file_url"], l["file_author"]))
                    save_data.append({"file_name": str(l["file_name"]), "file_url": str(l["file_url"]), "file_author": str(l["file_author"])})
                with open("backup.txt",'w+') as outfile:
                    json.dump(save_data, outfile)
            else:
                messagebox.showinfo("No Internet Connection", "You are currently offline. Data backup from you last session will displayed.")
                for l in backup:
                    self.etv.insert('', tk.END, values=(l["file_name"], l["file_url"], l["file_author"]))


        def share(self):
            if self.uploads == -1:
                messagebox.showinfo("No Internet Connection", "You cannot share resources while you are offline.")
            else:
                file_name = self.builder.tkvariables['file_name'].get()
                file_url = self.builder.tkvariables['file_url'].get()
                file_author = self.builder.tkvariables['file_author'].get()

                if file_name != "" and file_url != "" and file_author != "":
                    add_file(self.uploads, file_name, file_url, file_author)
                    self.etv.insert('', tk.END, values=(file_name, file_url, file_author))

        def on_row_selected(self, event):
            selected = self.etv.item(event.widget.selection(),"values")
            print(selected)
            webbrowser.open(selected[1], 2)


    def main():
        backup = ""
        uploads = -1
        try:
            myclient = pymongo.MongoClient("mongodb+srv://client:client123@dev-server-ddrnn.mongodb.net/test?retryWrites=true&w=majority")
            mydb = myclient["python_project_file_Share"]
            uploads = mydb["uploads"]
        except:
            if path.exists("backup.txt"):
                backup = json.load(open("backup.txt"))
            else:
                print("Unable to establish a connection. No backup found.")
        finally:
            root = tk.Tk()
            app = Application(root, uploads, backup)
            root.mainloop()

    if __name__ == '__main__':
        main()