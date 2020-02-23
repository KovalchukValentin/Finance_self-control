import sqlite3
import tkinter as tk
from tkinter import ttk
import time as t


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.library()
        self.init_menu()
        self.init_tree()
        self.db = db
        self.view_records(data)

    def library(self):
        self.day = [str(i) for i in range(1, 32)]
        self.month = [str(i) for i in range(1, 13)]
        self.year = [str(i) for i in range(2020, 2050)]

        for num, day in enumerate(self.day):
            if len(day) == 1:
                self.day[num] = "0" + day

        for num, month in enumerate(self.month):
            if len(month) == 1:
                self.month[num] = "0" + month

    def init_menu(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='image/add_cost_img.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.edit_img = tk.PhotoImage(file='image/edit_img.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.edit_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='image/delete_img.gif')
        btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.find_img = tk.PhotoImage(file='image/find_img.gif')
        btn_find = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.find_img,
                               compound=tk.TOP, command=self.finding)
        btn_find.pack(side=tk.LEFT)

        self.analitic_img = tk.PhotoImage(file='image/analitic_img.gif')
        btn_analitic = tk.Button(toolbar, text='Аналитика', bg='#d7d8e0', bd=0, image=self.analitic_img,
                               compound=tk.TOP, command=self.open_analitic)
        btn_analitic.pack(side=tk.LEFT)

        self.table_img = tk.PhotoImage(file='image/table_img.gif')
        btn_table = tk.Button(toolbar, text='Посмотреть другой день', bg='#d7d8e0', bd=0, image=self.table_img,
                               compound=tk.TOP, command=self.open_day)
        btn_table.pack(side=tk.LEFT)

        self.edit_type_img = tk.PhotoImage(file='image/close_img.gif')                                                  #FIX IMG
        btn_edit_type = tk.Button(toolbar, text='Редактировать группы', bg='#d7d8e0', bd=0, image=self.edit_type_img,
                               compound=tk.TOP, command=self.open_update_type)
        btn_edit_type.pack(side=tk.LEFT)

    def init_tree(self):
        self.tree = ttk.Treeview(self, columns=('ID', 'data', 'description', 'type', 'costs'), height=25,
                                 show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('data', width=100, anchor=tk.CENTER)
        self.tree.column('description', width=365, anchor=tk.CENTER)
        self.tree.column('type', width=100, anchor=tk.CENTER)
        self.tree.column('costs', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('data', text='Дата')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('type', text='Группа')
        self.tree.heading('costs', text='Сумма')

        self.tree.pack()

    def records(self, description, type, costs):
        type = type.strip()
        self.db.insert_data(description, type, costs)
        self.db.insert_type(type)
        self.view_records(data)

    def update_record(self, description, type, costs):
        self.db.c.execute('''UPDATE Finance SET description=?, type=?, costs=? WHERE ID=?''',
                          (description, type, costs, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records(data)

    def view_records(self, day):
        self.db.c.execute('''SELECT * FROM Finance WHERE data LIKE "%''' + day + '''" ''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM Finance WHERE id=''' + str(self.tree.set(selection_item, '#1')))
        self.db.conn.commit()
        self.view_records(data)

    def open_day(self):
        Day_window()

    def open_another_day(self, day):
        self.db.c.execute('''SELECT * FROM Finance WHERE data LIKE "%''' + day + '''" ''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def create_back_btn(self):
        try:
            self.back_table_btn.destroy()
        except:
            pass
        self.back_table_btn = ttk.Button(self, text='Закрыть')
        self.back_table_btn.place(x=675, y=505)
        self.back_table_btn.bind('<Button-1>', lambda event: self.back_btn())

    def back_btn(self):
        self.view_records(data)
        self.back_table_btn.destroy()

    def open_update_type(self):
        Edit_type()

    def update_type(self, type_change, type):
        self.db.c.execute('''UPDATE Finance SET type=? WHERE type=?''', (type_change, type))
        self.db.conn.commit()
        self.db.get_group_list()
        self.view_records(data)


    def finding(self):
        Find_window()

    def open_analitic(self):
        Analytic()

    def open_dialog(self):
        Dialog_window()

    def open_update_dialog(self):
        Edit_window()


class Day_window(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_day_window()
        self.grab_set()
        self.focus_set()


    def init_day_window(self):
        self.title('Введите дату')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='День')
        label_description.place(x=65, y=70)
        labe2_description = tk.Label(self, text='Месяц')
        labe2_description.place(x=130, y=70)
        labe3_description = tk.Label(self, text='Год')
        labe3_description.place(x=210, y=70)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Показать')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view_table())


        self.comb_day = ttk.Combobox(self, values=self.view.day, width=7)
        self.comb_day.current(int(t.strftime('%d')) - 1)
        self.comb_day.place(x=50, y=50)

        self.comb_month = ttk.Combobox(self, values=self.view.month, width=7)
        self.comb_month.current(int(t.strftime('%m')) - 1)
        self.comb_month.place(x=120, y=50)

        self.comb_year = ttk.Combobox(self, values=self.view.year, width=7)
        self.comb_year.current(int(t.strftime('%Y')) - 2020)
        self.comb_year.place(x=190, y=50)

    def view_table(self):
        self.comb_data = ".".join([self.comb_day.get(), self.comb_month.get(), self.comb_year.get()])
        self.view.view_records(self.comb_data)
        self.view.create_back_btn()


class Find_window(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_find()
        self.grab_set()
        self.focus_set()


    def init_find(self):
        self.title('Запрос на поиск')
        self.geometry('400x220+400+300')
        self.resizable(False, False)
        self.label = ttk.Label(self, text='Введите запрос по названию:')
        self.label.place(x=25,y=25)
        self.entry_find = ttk.Entry(self, width=30)
        self.entry_find.place(x=190, y=25)
        self.label2 = ttk.Label(self, text='Введите запрос по группе:')
        self.label2.place(x=25, y=50)
        self.entry2_find = ttk.Combobox(self, width=30, values=db.group_list)
        self.entry2_find.place(x=190, y=50)
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Найти')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view_table(self.entry_find.get(), self.entry2_find.get()))


    def view_table(self, find, find_type):
        self.view.db.c.execute('''SELECT * FROM Finance WHERE description LIKE "%''' + find + '''%" AND type lIKE "%'''
                               + find_type + '''%"''')
        [self.view.tree.delete(i) for i in self.view.tree.get_children()]
        [self.view.tree.insert('', 'end', values=row) for row in self.view.db.c.fetchall()]
        self.view.create_back_btn()


class Dialog_window(tk.Toplevel):

    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить доходы/расходы')
        self.geometry('500x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Наименование:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Группа дохода/расхода:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Сумма:')
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self, width=40)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self, width=40)
        self.entry_money.place(x=200, y=110)

        self.type = ttk.Combobox(self, values=db.group_list, width=40)
        self.type.current(0)
        self.type.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: (self.view.records(self.entry_description.get(),
                                                                        self.type.get(),
                                                                        self.entry_money.get())))
        self.grab_set()
        self.focus_set()


class Edit_window(Dialog_window):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: (self.view.update_record(self.entry_description.get(),
                                                                          self.type.get(),
                                                                          self.entry_money.get()),
                                                  self.destroy(),
                                                  Notification()))

        self.btn_ok.destroy()


class Edit_type(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.init_edit_type()

    def init_edit_type(self):
        self.title('Редактор групп')
        self.geometry('500x220+400+300')
        self.resizable(False, False)
        self.create_input()

    def create_input(self):

        self.label1 = ttk.Label(self, text='Выберете групу которую хоите редактировать:')
        self.label2 = ttk.Label(self, text='Введите новое название для группы:')
        self.label1.place(x=50, y=30)
        self.label2.place(x=50, y=90)

        self.comb_group = ttk.Combobox(self, values=db.group_list, width=40)
        self.comb_group.current(0)
        self.comb_group.place(x=50, y=50)

        self.entry_new_group = ttk.Entry(self, width=40)
        self.entry_new_group.place(x=50, y=110)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=400, y=170)

        self.btn_edit_type = ttk.Button(self, text='Редактировать')
        self.btn_edit_type.place(x=300, y=170)
        self.btn_edit_type.bind('<Button-1>', lambda event: (self.view.update_type(self.entry_new_group.get(), self.comb_group.get()), self.destroy(), Notification()))
        self.grab_set()
        self.focus_set()


class Notification(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_notification()

    def init_notification(self):
        self.title('Уведомление')
        self.geometry('500x220+400+300')
        self.resizable(False, False)
        self.label = ttk.Label(self, text='Изменено')
        self.label.place(x=50, y=50)
        self.grab_set()
        self.focus_set()


class Analytic(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.i_table = 3
        self.init_analytic()

    def init_analytic(self):
        self.title('Аналитика')
        self.geometry("1000x650+100+100")
        self.resizable(False, False)
        self.data_input_menu()
        self.grab_set()
        self.focus_set()

    def data_input_menu(self):
        self.btn_day = ttk.Button(self, text='День')
        self.btn_day.place(x=430, y=50)
        self.btn_day.bind('<Button-1>', lambda event: self.input_box_data())

        self.btn_month = ttk.Button(self, text='Месяц')
        self.btn_month.place(x=530, y=50)
        self.btn_month.bind('<Button-1>', lambda event: self.input_box_month())

        self.btn_year = ttk.Button(self, text='Год')
        self.btn_year.place(x=630, y=50)
        self.btn_year.bind('<Button-1>', lambda event: self.input_box_year())

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=730, y=50)

    def input_box_data(self):
        self.i_table -= 1
        self.comb_day = ttk.Combobox(self, values=self.view.day, width=7)
        self.comb_day.current(int(t.strftime('%d')) - 1)
        self.comb_day.place(x=50, y=50)
        self.input_box_month()

    def input_box_month(self):
        self.i_table -= 1
        self.comb_month = ttk.Combobox(self, values=self.view.month, width=7)
        self.comb_month.current(int(t.strftime('%m')) - 1)
        self.comb_month.place(x=120, y=50)
        self.input_box_year()

    def input_box_year(self):
        self.i_table -= 1
        self.comb_year = ttk.Combobox(self, values=self.view.year, width=7)
        self.comb_year.current(int(t.strftime('%Y')) - 2020)
        self.comb_year.place(x=190, y=50)
        self.btn_day.destroy()
        self.btn_month.destroy()
        self.btn_year.destroy()
        self.make_btn_result()

    def make_btn_result(self):
        self.btn_result = ttk.Button(self, text='Подщитать')
        self.btn_result.place(x=330, y=50)
        self.btn_result.bind('<Button-1>', lambda event: self.get_input())

        self.btn_back = ttk.Button(self, text='Вернуться')
        self.btn_back.place(x=430, y=50)
        self.btn_back.bind('<Button-1>', lambda event: self.btn_back_func())

    def get_input(self):
        self.comb_data = []
        try:
            self.comb_data.append(self.comb_day.get())
        except:
            pass
        try:
            self.comb_data.append(self.comb_month.get())
        except:
            pass
        self.comb_data.append(self.comb_year.get())
        self.comb_data = ".".join(self.comb_data)
        self.clear_table()
        self.table(self.comb_data)

    def btn_back_func(self):
        self.destroy()
        Analytic()

    def table(self, day):
        self.group_label = []
        x = 50
        y = 100
        count = 0
        row = 15
        gap = 20
        for num, group in enumerate(db.group_list):
            if self.summing(group, day) == 0:
                continue
            self.group_label.append([tk.Label(self, text=group + ":"), tk.Label(self, text=str(self.summing(group, day)))])
            self.group_label[count][0].place(x=x, y=y)
            self.group_label[count][1].place(x=x + 80, y=y)
            y += gap
            count += 1
            if count % row == 0:
                x += 200
                y = 100

        if len(self.group_label) >= row:
            y = (row+5) * gap
            x = 50

        self.Minus = [tk.Label(self, text="Расход:"), tk.Label(self, text=self.analytic_result(func='minus', day=day))]
        self.Minus[0].place(x=x, y=y)
        self.Minus[1].place(x=x + 80, y=y)

        self.Plus = [tk.Label(self, text="Доход:"), tk.Label(self, text=self.analytic_result('plus', day))]
        self.Plus[0].place(x=x + 200, y=y)
        self.Plus[1].place(x=x + 280, y=y)

        self.All = [tk.Label(self, text="Всего:"), tk.Label(self, text=self.analytic_result('all', day))]
        self.All[0].place(x=x + 400, y=y)
        self.All[1].place(x=x + 480, y=y)
        if self.i_table != 0:

            self.Average_month = [tk.Label(self, text="Среднее по дням:"), tk.Label(self, text=self.analytic_result(
                                                                                    'ave_month' + str(self.i_table),
                                                                                     day))]
            self.Average_month[0].place(x=x , y=y + gap)
            self.Average_month[1].place(x=x + 130, y=y + gap)

            if self.i_table == 2:
                self.Average_year = [tk.Label(self, text="Среднее по месяцам:"),
                                     tk.Label(self, text=self.analytic_result('ave_year', day))]
                self.Average_year[0].place(x=x + 200, y=y + gap)
                self.Average_year[1].place(x=x + 330, y=y + gap)

    def clear_table(self):
        try:
            for num in range(len(self.group_label)):
                self.group_label[num][0].destroy()
                self.group_label[num][1].destroy()

            self.Minus[0].destroy()
            self.Minus[1].destroy()

            self.Plus[0].destroy()
            self.Plus[1].destroy()

            self.All[0].destroy()
            self.All[1].destroy()

            self.Average_month[0].destroy()
            self.Average_month[1].destroy()
            self.Average_year[0].destroy()
            self.Average_year[1].destroy()
        except:
            pass

    def analytic_result(self, func, day):
        if func == "minus":
            result = [row for row in db.c.execute('''SELECT SUM(costs) FROM Finance WHERE data LIKE "%''' +
                                                  day + '''" AND costs LIKE "-%"''')]
        elif func == "plus":
            result = [row for row in db.c.execute('''SELECT SUM(costs) FROM Finance WHERE data LIKE "%''' +
                                                  day + '''" AND costs NOT LIKE "-%"''')]
        elif func == "all":
            result = [row for row in db.c.execute('''SELECT SUM(costs) FROM Finance WHERE data LIKE "%''' +
                                                  day + '"')]
        elif func == "ave_month1":
            result = [row for row in db.c.execute('''SELECT round(SUM(costs)/31, 2) FROM Finance WHERE data LIKE "%'''
                                                  + day + '"')]
        elif func == "ave_month2":
            result = [row for row in db.c.execute('''SELECT round(SUM(costs)/365, 2) FROM Finance WHERE data LIKE "%'''
                                                  + day + '"')]
        elif func == "ave_year":
            result = [row for row in db.c.execute('''SELECT round(SUM(costs)/12, 2) FROM Finance WHERE data LIKE "%'''
                                                  + day + '"')]
        return result[0][0] if result[0][0] != None else 0

    def summing(self, group, day):
        result = [row for row in db.c.execute('''SELECT SUM(costs) FROM Finance WHERE data LIKE "%''' +
                                             day + '''" AND type LIKE "''' + group + '"')]
        return result[0][0] if result[0][0] != None else 0


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Finance (id integer primary key, 
                                                              data text, 
                                                              description text, 
                                                              type text, 
                                                              costs real)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS Type (id integer primary key, 
                                                           name text)''')
        self.conn.commit()
        self.get_group_list()

    def get_group_list(self):
        self.group_list = [row[0] for row in self.c.execute("SELECT name FROM Type")]
        if 'Другое' not in self.group_list:
            self.group_list.append("Другое")

    def insert_data(self, description, costs, type):
        self.c.execute('''INSERT INTO Finance (data, description, type, costs) VALUES (?, ?, ?, ?)''',
                       (data, description, costs, type))
        self.conn.commit()

    def insert_type(self, name):
        if name not in self.group_list:
            self.c.execute('''INSERT INTO Type (name, name, name) VALUES (?, ?, ?)''', (name, name, name))
            self.conn.commit()
            self.group_list.append(name)


if __name__ == "__main__":
    data = t.strftime('%d.%m.%Y')
    month = t.strftime('%m.%Y')
    year = t.strftime('%Y')
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.iconbitmap("image/gui2.ico")
    root.title("Financial self-control")
    root.geometry("1000x650+100+100")
    root.resizable(False, False)
    tk.mainloop()