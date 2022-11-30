from tkinter import *
from tkinter import messagebox as msgbox
from win32api import GetSystemMetrics
import math





class Window():
    def __init__(self) -> None:
        self.width = 400
        self.height = 564
        self.font = ("Sans MS", 40, "bold")
        self.btn_color = "white"
        self.btn_font_color = "black"
        
        #load screen size from system
        ScreenWidth = GetSystemMetrics(0)
        ScreenHeight = GetSystemMetrics(1)

        #calculate center of the screen
        x = int((ScreenWidth/2)-(self.width/2))
        y = int((ScreenHeight/2)-(self.height/2))

        #create window
        root = Tk()
        root.title("Calculator")
        root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        root.resizable(False, False)


        
        self.var = StringVar()
        self.text_area = Entry(root, bg=self.btn_color, font = ("Sans MS", 40), textvariable = self.var)
        self.text_area.place(x=0, y=0, width=400, height=80)


                
            
        self.var.trace("w", self.callback)

        #build buttons
        self.buttons = []
        button_signs_list =['C', '±', 'π', '÷',
                            '7', '8', '9', 'x',
                            '4', '5', '6', '-',
                            '1', '2', '3', '+',
                            '√', '0', ',', '=']

        button_commands =   [self.clear_text, self.plusminus, self.pi, self.divide, 
                            self.write, self.write, self.write, self.multiply,
                            self.write, self.write, self.write, self.substract,
                            self.write, self.write, self.write, self.add,
                            self.sqrt, self.write, self.point, self.equals]


        #Loop needed to create grid of buttons
        for j in range(5):
            for i in range(4):
                index = i+4*j
                #set button properties
                button = Button(root, text=button_signs_list[index], font=self.font, background=self.btn_color, foreground=self.btn_font_color)

                #attach command to a button
                comm = button_commands[index]

                if comm == self.write:
                    button.config(command = lambda id=button.cget('text'): self.write(id))

                else:
                    button.config(command = comm)
                        

                #add button to list of buttons
                self.buttons.append(button)
                
                #place button on grid
                self.buttons[index].place(x=int(100*i) , y=(100*j + 64), width=100, height=100)

        #---------------------------------------------------------------------------

        #set temporary variables
        self.buffer = None
        self.operation = None

        #run program window
        root.mainloop()

    def callback(self, *args):
        item = self.var.get()
        item = item.replace(",",".")
            
        try:
            float(item)
        except:
            buff = ''
            for char in self.text_area.get():
                if char.isdigit() == True or char == ".":
                    buff += char

            buff = buff.replace(".",",")

            self.clear_text()
            self.text_area.insert(0,buff)


    def clear_text(self):
        self.text_area.delete(0, 'end')


    def read_text(self):
        data = self.text_area.get()
        if data == '':
            return 0

        valid = float(data.replace(',','.'))
        return valid


    def plusminus(self):
        n = self.read_text()
        self.clear_text()
        if n%1==0: n=int(n)
        self.text_area.insert(0,f"{-n}".replace('.',','))


    def pi(self):
        self.clear_text()
        self.text_area.insert(0,'3,141592')


    def divide(self):
        self.operation = 'divide'
        self.buffer = self.read_text()
        self.clear_text()


    def multiply(self):
        self.operation = 'multiply'
        self.buffer = self.read_text()
        self.clear_text()
        

    def substract(self):
        self.operation = 'substract'
        self.buffer = self.read_text()
        self.clear_text()
        

    def add(self):
        self.operation = 'add'
        self.buffer = self.read_text()
        self.clear_text()
        


    def equals(self):
        if self.buffer != None and self.operation != None:
            number = self.read_text()
            self.clear_text()

            if self.operation == 'add':
                n = self.buffer + number
                
            elif self.operation == "substract":
                n = self.buffer -number
                
            elif self.operation == "multiply":
                n = self.buffer*number

            elif self.operation == "divide":
                if number != 0:
                    n = self.buffer/number
                else:
                    msgbox.showerror("Error", "Cannot be divided by zero!")
                    self.buffer = None
                    return 1

            if n%1 ==0:
                n=int(n)

            self.text_area.insert(0,f"{n}".replace('.',','))


    def sqrt(self):
        number = self.read_text()
        if number >= 0:
            answer = math.sqrt(number)

            answer = round(answer,8)
            if answer%1==0:
                answer = int(answer)

            self.clear_text()
            self.text_area.insert(0,f"{answer}".replace('.',','))

        else:
            msgbox.showerror("Error", "Invalid input data!")


    def point(self):
        text = self.text_area.get()
        if not ',' in text:
            if text == '':
                self.text_area.insert(END,"0,")
            else:
                self.text_area.insert(END,",")


    #prints a chosen number on the output area
    def write(self, ButtonNumber:str):
        if self.text_area.get() != '0':
            self.text_area.insert(END, ButtonNumber)



if __name__ == "__main__":
    Window()