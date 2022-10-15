from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from save import *
from testing import *
import interpreter as inte
from directories import *

TITLE = 'Interpretej notacji algorytmicznej'
#inicjacja okna
root = Tk()
root.title(TITLE)
#stale
SZEROKOSC = 1200
WYSOKOSC = 700
FONT = "Times New Roman"

#index operowanego pliku
index=0

root.geometry(str(SZEROKOSC)+"x"+str(WYSOKOSC))

#Wypisywanie notacji
code_list = []
labelcode_list=[]
# ------------------------------------------------------
#Segment ocen
marks = ("2", "2.5", "2,5", "3", "3,5", "3.5", "4", "4,5", "4.5", "5", "nzal", "zal")
# ------------------------------------------------------
#Next Step
step = -1
# ------------------------------------------------------
#flaga kompilacji
compilated=0
#inicjacja we
input_list=[]
labelinput_list=[]
secondinput_list=[]
variableframe_list=[]
#inicjacja zmienne
variable_list=[]
variable_label_list=[]
variable_labelval_list=[]
#flaga swap second input variable
swap=0

#wczytanie danych z pliku tylko do pierwszego wyswietlenia
def f_readfile():
    global code_list
    global labelcode_list
    if (files_list):
        with open(files_list[index]) as f:
            for line in f:
                code_list.append(line)

#Dodaje ocene 
def f_addmark():
    grade = mark.get()
    komentarz = comment.get() 
    if(grade in marks):
        #zapisuje w pliku excel - ocena + komentarz
        save(person.cget("text"), grade, komentarz)
        pass
    else:
        messagebox.showwarning(title="Warning!" , message="To nie jest ocena")
    comment.delete(0,END)
    mark.delete(0, END)

#Resetuje zmienne

def f_setnew():
    global compilated
    global step
    global swap
    global code_list
    global labelcode_list
    global input_list
    global labelinput_list
    global secondinput_list
    global variableframe_list
    global variable_list
    global variable_label_list
    global variable_labelval_list
    compilated=0
    step = -1
    swap=0
    status.config(text="Nie skompilowano", bg="#f3a2ad")
    labelcode_list.clear()
    code_list.clear()
    input_list.clear()
    labelinput_list.clear()
    secondinput_list.clear()
    variableframe_list.clear()
    variable_list.clear()
    variable_label_list.clear()
    variable_labelval_list.clear()

#Pokazuje dane w polu notacji po lewej

def f_showcode():
    global code_list
    global labelcode_list
    i=1
    for element in code_list:
        labelcode_list.append(Label(frameframe_code, text = element))
        labelcode_list[-1].config(font=(FONT, 12))
        labelcode_list[-1].grid(row = i, column = 1, stick = W)
        i+=1

#Usuwa dane w polu notacji po lewej

def f_forgetcode():
    global code_list
    global labelcode_list
    for element in labelcode_list:
        element.grid_forget()
    code_list.clear()
    labelcode_list.clear()
   
#Usuwa wszyztkie zmienne w polu po prawej

def f_forgetvariable(flag=True):
    global variable_list
    global variable_label_list
    global variable_labelval_list
    global input_list
    global labelinput_list
    global secondinput_list
    global variableframe_list
    for element in variableframe_list:
        element.pack_forget()
    labelinput_list.clear()
    secondinput_list.clear()
    variableframe_list.clear()
    variable_label_list.clear()
    variable_labelval_list.clear()
    #Domyslnie przygotuwje program do ponownej kompilacji
    if flag:
        input_list.clear()
        variable_list.clear()

#Zamyka inputy na czas wyknywania programu przez interpreter
def f_swapEntryWithLabel():
    global secondinput_list
    global labelinput_list
    global swap
    #Sprawdza czy wprowadzono poprawne znaki
    for i in range (len(secondinput_list)):
        try:
            zmienna = int(secondinput_list[i].get())
        except ValueError:
            if (secondinput_list[i].get()==""):
                secondinput_list[i].insert(0,0)
            #Specjalny wyjatek dla tablic
            elif(labelinput_list[i].cget("text")[-1]=='#'):
                for char in secondinput_list[i].get():
                    if not(char.isdigit() or char.isspace()):
                        secondinput_list[i].delete(0, END)
                        messagebox.showwarning(title="Warning!" , message="Jeden z inputow jest niepoprawny")
                        return 0
            else:
                secondinput_list[i].delete(0, END)
                messagebox.showwarning(title="Warning!" , message="Jeden z inputow jest niepoprawny")
                return 0
    #Pobierane dane do interpretera i zamyka mozliwosc modyfikacji danych
    for i in range (len(secondinput_list)):
        varl = secondinput_list[i].get()
        secondinput_list[i].pack_forget()
        secondinput_list[i] = Label(variableframe_list[i], text=varl)
        secondinput_list[i].pack(side=RIGHT, padx=30)
        secondinput_list[i].config(font=(FONT, 10))
    swap = 1
    return 1

#Przywraca mozliwosc modyfikacji inputow
def f_swapLabelWithEntry():
    global swap
    global secondinput_list
    for i in range (len(secondinput_list)):
        varl = secondinput_list[i].cget("text")
        secondinput_list[i].pack_forget()
        secondinput_list[i] = Entry(variableframe_list[i], width=10)
        secondinput_list[i].pack(side=RIGHT, padx=20)
        secondinput_list[i].config(font=(FONT, 10))
        try:
            x = int(varl)
            secondinput_list[i].insert(0, varl)
        except:
            temp = varl.find(',')+1
            if not temp:
                varl = ''
            else:
                varl = varl[temp:-1]
                varl = ' '.join(varl.split(','))
            secondinput_list[i].insert(0, varl)
    swap = 0

#Ustawia kolor domyślny notacji po lewej
def f_normalizeColor():
    global labelcode_list
    defaultbg = root.cget("bg")
    for element in labelcode_list:
        element.config(bg=defaultbg)

#Wywołuje kompilację programu
def f_compilation(flag=True):
    global code_list
    global labelcode_list
    global input_list
    global labelinput_list
    global secondinput_list
    global variableframe_list
    global step
    global swap
    global variable_list
    #kompiluje
    compilation = inte.Compile(files_list[index])
    step = -1
    #kompilacja się nie powiodła
    if(compilation == 0):
        f_forgetcode()
        code_list = inte.user_commands[2:]
        f_showcode()
        for k in inte.wrong_commands:
            labelcode_list[k-1].config(bg = "#ed5b6b")
        status.pack_forget()
        status.config(text="Error", bg="#f00e2c")
        status.pack(pady = 5)
    #kompilacja się powiodła, zatem domyslnie wprowadzam zmiany widoczne
    elif flag:
        swap = 0
        f_forgetvariable()
        for element in inte.input_vars:
            if (element!=""):
                input_list.append(element)
        f_showvariable_input()
        f_forgetcode()
        code_list = inte.user_commands[2:]
        f_showcode()
        status.pack_forget()
        status.config(text="Skompilowano", bg= "#58f52e")
        status.pack(pady = 5)
        global compilated
        compilated = 1
 
#Wczytuje inputy podane przez uzytkownika
def f_loaddata():
    global secondinput_list
    global labelinput_list
    #Najpierw wczytuje zwykle zmienne
    for i in range (len(secondinput_list)):
        key = labelinput_list[i].cget("text")
        if(key[-1]=="#"):
            continue
        val = int(secondinput_list[i].cget("text"))
        inte.variables[key]=val
    
    #Teraz wczytuje ciagi
    for i in range (len(secondinput_list)):
        key = labelinput_list[i].cget("text")
        if not(key[-1]=="#"):
            continue
        key='#' + key[:-1]
        val = [int(x) for x in secondinput_list[i].cget("text").split()]
        print(key)
        inte.variables[key].extend(val)
        #Uptade robi wielkosci ciagu
        inte.ciag_rozmiar_update(key[1:])
        #Przycina ciag do odpowiedniej wielkosci lub uzupelnia zerami
        while(True):
            if (inte.variables[key][0] > len(inte.variables[key])-1 ):
                inte.variables[key].extend([0])
            elif(inte.variables[key][0] < len(inte.variables[key])-1):
                inte.variables[key].pop()
            else:
                break
        secondinput_list[i].config(text = inte.variables[key][1:])  

#Wywoluje natepny krok
def f_nextstep():
    global code_list
    global labelcode_list
    global swap
    global input_list
    global labelinput_list
    global secondinput_list
    global variableframe_list
    #Przerwie, bo nieskompilowano
    if (compilated==0):
        messagebox.showwarning(title="Warning!" , message="Skompiluj najpierw program!")
        return
    global step
    if (step == -1):
        if(swap==0):
            x = f_swapEntryWithLabel()
            if(x==0):
                return
            f_loaddata()
    #Podkresla wykonano linike
    f_normalizeColor()  
    step=inte.command_id-1
    labelcode_list[step].config(bg="#77f180")
    #Zmienia status
    status.pack_forget()
    status.config(text="Zrobiono krok", bg= "#e8f179")
    status.pack(pady = 5)
    #Kiedy krok konczy program
    if(step==len(labelcode_list)-1):
        f_compilation(flag=False)
        step = -1
        status.pack_forget()
        status.config(text="Wykonano", bg= "#799cf1")
        status.pack(pady = 5)
        f_normalizeColor()
        if(swap == 1):
            f_swapLabelWithEntry()
        variable_list.clear()
        return
    #Robi krok
    make_step = inte.make_step()
    #Jesli wykonanie kroku sie nie powiodlo
    if not make_step:
        status.pack_forget()
        status.config(text="Error wykonania", bg= "#f00e2c")
        status.pack(pady = 5)
        labelcode_list[inte.command_id-1].config(bg = "#ed5b6b")
    #Aktualizacja listy zmiennych
    variable_list.clear()
    for element in set(inte.variables.keys()).difference(inte.input_vars):
        if not element[0]=='&':
            if element[0] == '#':
                element = element[1:] + '#'
            variable_list.append(element)
    #Aktualizuje zmienne wyswietlane
    f_forgetvariable(flag=False)
    f_showvariable_input(flag=False)
    f_showvariable()
 
#Wykonuje program
def f_run():
    global code_list
    global labelcode_list
    global swap
    global step
    global input_list
    global labelinput_list
    global secondinput_list
    global variableframe_list
    global variable_list
    f_normalizeColor()
    #Jesli nie skompilowano to przerwie
    if (compilated==0):
        messagebox.showwarning(title="Warning!" , message="Skompiluj najpierw program!")
        return
    #Zamyka pola, aby wczytac dane i wykonac program
    if(swap==0):
        x = f_swapEntryWithLabel()
        if(x==0):
            return
        f_loaddata()   
    #Zmiana statusu
    status.pack_forget()
    status.config(text="Wykonano", bg= "#799cf1")
    status.pack(pady = 5)
    execution = inte.Execute()
    #B L A D  N I E S K O N C Z O N E J  P E T L I
    if execution == -1:
        status.pack_forget()
        status.config(text="NIESKONCZONA  P E T L A ! !", bg= "#f00e2c")
        status.pack(pady = 5)
    #Bledy inne
    elif not execution:
        status.pack_forget()
        status.config(text="Error wykonania", bg= "#f00e2c")
        status.pack(pady = 5)
        labelcode_list[inte.command_id-1].config(bg = "#ed5b6b")
    else:
        status.pack_forget()
        status.config(text="Wykonano w " + str(execution) + " krokow", bg= "#799cf1")
        status.pack(pady = 5)
        execution = inte.Execute()
    #Wczytuje dane, ale jesli jest na poczatku programu tylko, bo inaczej zostaly wczytane przez zrob krok
    if (inte.command_id<2 or step == -1):
        for element in set(inte.variables.keys()).difference(inte.input_vars):
            if not element[0]=='&':
                if element[0] == '#':
                    element = element[1:] + '#'
                variable_list.append(element)
    #Aktualizacja danych i kompilacja z tylu aby zresetowac zmienne
    f_forgetvariable(flag=False)
    f_showvariable_input(flag=False)
    f_showvariable()
    variable_list.clear()
    if(swap == 1):
        f_swapLabelWithEntry()
    step = -1
    f_compilation(flag=False)

#Guzik do tylu
def f_back():
    global index
    global person
    if(index!=0):
        index-=1
        person.config(text = files_list[index].split("/")[-1][:-4])
        f_forgetcode()
        f_forgetvariable()
        f_setnew()
        comment.delete(0,END)
        mark.delete(0, END)
        f_readfile()
        f_firstload()
    
#Guzik do przodu    
def f_forward():
    global index
    global person
    if(index!=len(files_list)-1):
        index+=1
        person.config(text = files_list[index].split("/")[-1][:-4])
        f_forgetcode()
        f_forgetvariable()
        f_setnew()
        comment.delete(0,END)
        mark.delete(0, END)
        f_readfile()
        f_firstload()
    
#Pokaz zmienne wejscia   
def f_showvariable_input(flag=True):
    global input_list
    global labelinput_list
    global secondinput_list
    global variableframe_list
    for element in input_list:
        if element[0] == '#':
            temporary_name = element[1:] + '#' 
        else:
            temporary_name = element
        variableframe_list.append(Frame(frame_variable))
        variableframe_list[-1].pack(side= TOP, fill="x")

        labelinput_list.append(Label(variableframe_list[-1], text = temporary_name))
        labelinput_list[-1].pack(side=LEFT, padx=30)
        labelinput_list[-1].config(font=(FONT, 10))
        if flag:
            secondinput_list.append(Entry(variableframe_list[-1], width=10))
            secondinput_list[-1].pack(side=RIGHT, padx=30)
            secondinput_list[-1].config(font=(FONT, 10))
        else:
            secondinput_list.append(Label(variableframe_list[-1], text = "{}".format( inte.variables[element] )))
            secondinput_list[-1].pack(side=RIGHT, padx=30)
            secondinput_list[-1].config(font=(FONT, 10))
#Pokaz zmienne
def f_showvariable():
    global variable_list
    global variable_label_list
    global variableframe_list
    global variable_labelval_list

    for element in variable_list:
        variableframe_list.append(Frame(frame_variable))
        variableframe_list[-1].pack(side= TOP, fill="x")

        variable_label_list.append(Label(variableframe_list[-1], text = element))
        variable_label_list[-1].pack(side=LEFT, padx=30)

        variable_labelval_list.append(Label(variableframe_list[-1], text = inte.variables[element]))
        variable_labelval_list[-1].pack(side=RIGHT, padx=30)
#Uruchom po zalowadniu pliku
def f_firstload():
    f_showcode()

#Pobierz sciezke
dir = filedialog.askdirectory()
files_list = directories(dir)
#Przeczytaj plik
f_readfile()
#Zbuduj na nowo okno, aby uniknac bugow z wczytania sciezki
root.destroy()
root = Tk()
root.title(TITLE)

root.geometry(str(SZEROKOSC)+"x"+str(WYSOKOSC))
#Easter eggi
#messagebox.showinfo(title="Witaj" , message="Witaja Cie: Lewi, Marcin, Piotrek")
#messagebox.showinfo(title="Witaj" , message="Klikin ok, aby rozpoczac sprawdzanie. Pracuj Madrze, nie Ciezko ;-)")

#Zapis Notacji
# ------------------------------------------------------
frame_code = LabelFrame(root, text="Zapis w notacji", height = WYSOKOSC, width=SZEROKOSC*4/10)

canvas_code = Canvas(frame_code)
canvas_code.pack(side=LEFT, fill="y")

scrollbar_code = Scrollbar(frame_code, orient="vertical", command=canvas_code.yview)
scrollbar_code.pack(side = RIGHT, fill="y")

canvas_code.configure(yscrollcommand=scrollbar_code.set)
canvas_code.bind('<Configure>', lambda e: canvas_code.configure(scrollregion = canvas_code.bbox('all')))

frame_code.grid(row = 1, column = 1, rowspan = 3, stick=N+S+W)
frame_code.pack_propagate(0)
frame_code.grid_propagate(0)

frameframe_code = Frame(canvas_code)
canvas_code.create_window((0,0), window = frameframe_code, anchor=N+W)


#Funkcjonalność
# ------------------------------------------------------
frame_option = LabelFrame(root, text = "Funkcjonalnosc", height = WYSOKOSC*2/5, width=SZEROKOSC*4/10)
frame_option.grid(row = 1, column = 2,stick=N+W+E)
#frame_option.pack_propagate(0)
#frame_option.grid_propagate(0)

button_compilation = Button(frame_option, text= "Kompiluj", width=12, height = 1, bg="#77f180", activebackground="#77f180", command=f_compilation)
button_nextstep = Button(frame_option, text= "Zrob krok", width=12, height = 1, bg="#77f180", activebackground="#77f180", command=f_nextstep)
button_run = Button(frame_option, text= "Wykonaj", width=24, height = 1, bg="#77f180", activebackground="#77f180", command=f_run)

button_compilation.grid(row=1, column=1, padx= 20, pady = 15, sticky=W )
button_compilation.config(font=(FONT, 20))

button_nextstep.grid(row=1, column=2, padx= 20, pady = 15, sticky=E )
button_nextstep.config(font=(FONT, 20))

button_run.grid(row=2, column=1, columnspan=2, padx= 40, pady = 15 )
button_run.config(font=(FONT, 20))


#Stan
# ------------------------------------------------------
frame_status = LabelFrame(root, text="Stan", height = WYSOKOSC*2/10, width=SZEROKOSC*4/10)
frame_status.grid(row=2, column = 2)
frame_status.pack_propagate(0)
frame_status.grid_propagate(0)

status=Label(frame_status, text="Nie skompilowano", width=50, height = 20, relief= SUNKEN, bg="#f3a2ad")
status.config(font=(FONT, 20))
status.pack(pady = 5)


#Wystawianie ocen
# ------------------------------------------------------


frame_mark = LabelFrame(root, text = "Panel Studenta", height = WYSOKOSC*5/10, width=SZEROKOSC*4/10 )
frame_mark.grid(row = 3, column = 2, stick=S+W+E)
frame_mark.pack_propagate(0)
frame_mark.grid_propagate(0)

subframe_person = Frame(frame_mark)
subframe_person.pack()

person = Label(subframe_person, text = files_list[index].split("/")[-1][:-4])
person.config(font=(FONT, 20))
person.pack()

subframe_mark = Frame(frame_mark)
subframe_mark.pack()

marklabel = Label(subframe_mark, text="Ocena: ")
marklabel.config(font=(FONT, 12))
marklabel.grid(row=1, column=1)

mark=Entry(subframe_mark, width=3)
mark.config(font=(FONT, 20))
mark.grid(row = 1, column = 2)

add_mark=Button(frame_mark, text = "Dodaj ocene i komentarz", bg= "#ecdddf", activebackground="#ecdddf", command = f_addmark)
add_mark.config(font=(FONT, 12))
add_mark.pack(pady = 10)

comlabel = Label(frame_mark, text = "Komentarz:")
comlabel.config(font=(FONT, 12))
comlabel.pack()

comment=Entry(frame_mark, width=50)
comment.config(font=(FONT, 12))
comment.pack()


buttonleft = Button(frame_mark, text="<<", bg= "#ecdddf", activebackground="#ecdddf", width = 10, height = 2, command = f_back)
buttonright = Button(frame_mark, text=">>", bg= "#ecdddf", activebackground="#ecdddf", width = 10, height = 2, command = f_forward )
buttonleft.pack(side=LEFT, padx = 10, pady = 10)
buttonright.pack(side=RIGHT, padx = 10, pady = 10)

#Autorzy, aby w momencie kiedy rozpowszczechnimy program to bylo wiadomo czyj
frame_autorzy = Frame(frame_mark)
frame_autorzy.pack(side=BOTTOM)
tytul = Label(frame_autorzy, text = 'Autorzy: ')
tytul.grid(row = 1, column = 1)
lewi = Label(frame_autorzy, text="Lewi, ")
lewi.config(font=("Comic Sans MS", 12))
lewi.grid(row = 1, column = 2)
piotrus = Label(frame_autorzy, text="Piotrek")
piotrus.config(font=("Wingdings", 12))
piotrus.grid(row = 1, column = 3) 
marcin = Label(frame_autorzy, text="i Makulec")
marcin.config(font=(FONT, 12))
marcin.grid(row = 1, column = 4) 

#Zmienne
# ------------------------------------------------------
frame_variable = LabelFrame(root, text="Zmienne", height = WYSOKOSC, width=SZEROKOSC*2/10-5)
frame_variable.grid(row = 1, column = 3, rowspan = 3, stick=N+S+E)
frame_variable.pack_propagate(0)
frame_variable.grid_propagate(0)

titleframe_variable = Frame(frame_variable)
titleframe_variable.pack(side= TOP, fill="x")

name = Label(titleframe_variable, text="Nazwa")
name.pack(side=LEFT, padx=20)
#name.grid(row=1, column=1, stick=W+E, padx = 40)
name.config(font=(FONT, 12))

value = Label(titleframe_variable, text="Wartosc")
value.pack(side=RIGHT, padx=20)
#value.grid(row=1, column=2, stick=W+E)
value.config(font=(FONT, 12))

# ------------------------------------------------------

f_firstload()
mainloop()

