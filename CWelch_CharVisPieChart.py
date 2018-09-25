# Carlton Welch
# CS 113 Afternoon
# Final Project
# 5 - 28 - 18

import tkinter as tk
import turtle


class PieChart:

    colors = ('blue', 'black', 'red', 'green', 'grey', 'orange', 'yellow', 'pink', 
              'purple', 'violet', 'snow','green yellow', 'mint cream', 'saddle brown', 
              'light coral', 'deep pink', 'chartreuse', 'cyan', 'turquoise', 
              'cadet blue', 'dodger blue', 'bisque', 'lavender', 'azure', 'maroon', 
              'rosy brown', 'thistle', 'light pink', 'dark orchid')

    def __init__(self, data_prob, data_freq, n, n_max):
        self.data_prob = data_prob
        self.data_freq = data_freq
        self.n = n
        self.n_max = n_max

    def draw_segment(self, turtle, degrees, label, color):
        radius = 250
        label_offset = 50
        turtle.ht()
        turtle.up()
        turtle.fillcolor(color)
        turtle.begin_fill()
        turtle.fd(radius)
        turtle.lt(90)
        turtle.circle(radius, degrees / 2)
        turtle.rt(90)
        turtle.fd(label_offset)
        turtle.write(label, align="center", font=("Arial", 10))
        turtle.bk(label_offset)
        turtle.lt(90)
        turtle.circle(radius, degrees - degrees / 2)
        turtle.lt(90)
        turtle.fd(radius)
        turtle.rt(180)
        turtle.end_fill()

    def draw(self):
        n_degs = 0.0
        all_other_prob = 0.0
        color_index = 0
        stan = turtle.Turtle()
        stan.speed(0)
        for key in self.data_prob:
            if self.data_prob[key] > 0:
                self.draw_segment(stan, (self.data_prob[key] * 360), 
                				  key + ', ' + str(round(self.data_prob[key], 4)),
                                  self.colors[color_index])
                n_degs += self.data_prob[key] * 360
                all_other_prob += self.data_prob[key]
                color_index += 1
        if self.n < self.n_max:
                self.draw_segment(stan, 360 - n_degs, 
                                  'All other \nletters, ' + str(round((1 - all_other_prob), 4)),
                                  self.colors[color_index])
        turtle.mainloop()


# gets slider value
def get_num(n):
    n[0] = int(S1.get())


# creates dictionary with letter frequencies
def freq_get(file):
    freq = dict()
    line = ""
    freq['white space'] = 0
    freq['symbol'] = 0
    freq['numeral'] = 0
    with open(file) as f:
        for letter in f:
            line += letter
    line = line.lower()
    for char in line:
        if char == ' ' or char == '\n':
            freq['white space'] += 1
        elif char < 'a':
            if '0' <= char <= '9':
                freq['numeral'] += 1
            else:
                freq['symbol'] += 1
        elif char > 'z':
            freq['symbol'] += 1
        else:
            freq[char] = freq.get(char, 0) + 1
    return freq


# returns dictionary containing n highest letter frequencies
def n_high_freq(l, n):
    max_dict = dict()
    i = 0
    while i < n:
        max_freq = 0.0
        high_letter = ''
        for letter in l:
            if l[letter] >= max_freq:
                max_freq = l[letter]
                high_letter = letter
        max_dict[high_letter] = l[high_letter]
        l[high_letter] = -1.0
        i += 1
    return max_dict


# MAIN BEGIN
total_frequency = 0
non_zero_entries = 0
n_display = [0]
l_prob = dict()

l_freq = freq_get("Words.txt")

for key in l_freq:
    if l_freq[key] > 0:
        non_zero_entries += 1

# check file validity
if sum(l_freq.values()) == 0:
    print("Invalid file")
    quit()

root = tk.Tk()

# center pop up window
wWidth = root.winfo_reqwidth()
wHeight = root.winfo_reqheight()
root.geometry('+{}+{}'.format(int(root.winfo_screenwidth()/2 - wWidth/2), 
              int(root.winfo_screenheight()/2 - wHeight/2)))

root.title("CWelch PieChart")
tk.Label(root, text="Please select a value for n").pack()
# slider only allows a valid n-value based on text file contents
S1 = tk.Scale(root, from_=1, to=non_zero_entries, orient='horizontal')
S1.pack()
tk.Button(root, text="Submit", command=lambda: [get_num(n_display), root.destroy()]).pack()
root.mainloop()

# sums all frequencies
for letter in l_freq:
    total_frequency += l_freq[letter]

n_highest = n_high_freq(l_freq, n_display[0])

# creates dictionary with letter probabilities
for letter in n_highest:
    l_prob[letter] = float(n_highest[letter] / total_frequency)

pc = PieChart(l_prob, l_freq, n_display[0], non_zero_entries)
pc.draw()



