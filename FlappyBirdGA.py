# Flappy Bird with genetic algorithm
# 29/02/20
from tkinter import *
import time
import random

wn = Tk()
wn.title("Flappy Bird")
wn.geometry("850x750")
wn.configure(bg = "black")
# the main canvas, where the game plays out
canvas = Canvas(wn, width = 550, height = 750, bg = "lightblue")
canvas.place(x = 0, y = 0)
# side canvas, where the graph of score vs generation is placed
blackCanvas = Canvas(wn, width = 300, height = 260, highlightthickness = 0, relief = RIDGE, bg = "black")
blackCanvas.place(x = 555, y = 440)
times = 0
gen = 0
gene = 0
over = False
# variables related to the graph on the right
pointsWidth = 220
pointsGap = 0
# the target for the birds
target = 50
# number of birds (keep it at 4)
num = 4
# For keeping the score
score = 0
highScore = 0
# Pipe properties
pipeGap = 180
pipeSpeed = 15
pipeHeight = []
pipes = []
# these are the maximum values by which the properties of the birds can change
# 1st element - hop limit, 2nd element - reaction limit
mutationLimit = [20, 20]
theBest = 0
box = 0
birds = []
scores = []
birdBoxes = []
dead = 0
repeat = False
count = 1
# the ground
canvas.create_rectangle(0, 700, 560, 750, fill = "orange")
# the scoreboxes for the game
scoreBox = Label(canvas, text = str(score), font = ("Arial", 22), bg = "lightblue")
scoreBox.place(x = 500, y = 10)
highScoreBox = Label(canvas, text = str(highScore), font = ("Arial", 22), bg = "lightblue")
highScoreBox.place(x = 20, y = 10)
# the following lines set up the right viewport, where the details of the birds are given
genBox = Label(wn, font = ("Arial", 15), fg = "white", bg = "black")
genBox.place(x = 570, y = 20)
for i in range(num):
    birdBoxes.append(Label(wn, font = ("Arial", 11), fg = "green", bg = "black"))
    birdBoxes[i].place(x = 570, y = 60+30*i)
parentBox = Label(wn, font = ("Arial", 11), fg = "blue", bg = "black")
parentBox.place(x = 570, y = 60+30*num)
evaluationBox = Label(wn, font = ("Arial", 15), text = "Evaluation", fg = "white", bg = "black")
evaluationBox.place(x = 570, y = 100+30*num)
for i in range(num):
    birdBoxes.append(Label(wn, font = ("Arial", 11), fg = "green", bg = "black"))
    birdBoxes[i+num].place(x = 570, y = 260+30*i)
previousBest = Label(wn, font = ("Arial", 11), fg = "blue", text = "Previous best: 0", bg = "black")
previousBest.place(x = 570, y = 380)
allTimeBest = Label(wn, font = ("Arial", 11), fg = "blue", text = "All time best: 0", bg = "black")
allTimeBest.place(x = 570, y = 410)
result = Label(wn, text = "Target: " + str(target), font = ("Arial", 11), fg = "orange", bg = "black")
result.place(x = 570, y = 705)
blackCanvas.create_line(35, 10, 35, 235, fill = "white")
blackCanvas.create_line(35, 235, 280, 235, fill = "white")
blackCanvas.create_text(18, 120, angle = 90, text = "Score", font = ("Arial", 11), fill = "white")
blackCanvas.create_text(155, 252, text = "Generation", font = ("Arial", 11), fill = "white")





class Bird:

    def __init__(self, x, r):
        # hop limit
        self.x = x
        self.y1 = 360
        self.y2 = self.y1 + 30
        self.birdColor = "yellow"
        self.dy = 7.5
        self.gravity = 0.4
        self.pipe = 0
        self.count = 0
        # reaction time
        self.reaction = r
        # variable will be true when bird has died but hasn't hit the ground
        self.dead = False
        # variable will be true when bird has hit the ground
        self.halt = False

    def createBird(self):
        # creating that funny looking bird...

        canvas.create_oval(90, self.y1, 130, self.y2, fill = self.birdColor, tags = "bird")
        
        canvas.create_oval(116, self.y1 + 3, 126, self.y1 + 14, fill = "white", tags = "bird")
       

        canvas.create_oval(121, self.y1 + 5, 127, self.y1 + 11, fill = "black", tags = "bird")
        canvas.create_rectangle(112, self.y1 + 17, 138, self.y1 + 22, fill = "red", tags = "bird")
        canvas.create_rectangle(112, self.y1 + 22, 138, self.y1 + 27, fill = "red", tags = "bird")

        canvas.create_oval(80, self.y1 + 8, 104, self.y1 + 24, fill = "white", tags = "bird")

    def fly(self):
    
            global dead
            
            if not self.dead:
                
                if self.y1 <= 0:
                
                    self.dy = 0
                # if the bird is below its hop parametre, then it will jump
                if self.y1 > pipeHeight[self.pipe] - self.x and not self.dead:
                    self.dy = 9
                # if it hits one of the green pillars
                if (self.y1 <= pipeHeight[0] - pipeGap + 15 or self.y2 >= pipeHeight[0]) and pipes[0] - 8 <= 90 and pipes[0] + 108 >= 130:
                        
                        self.dead = True
                        changeColor()
                        self.birdColor = "orange"
                        self.dy = 0
                    
                self.count += 1

            # the following three lines will be constantly executed until the bird hits the ground
            self.dy -= self.gravity
            self.y1 -= self.dy
            self.y2 -= self.dy

            # if it hasn't hit the ground:
            if self.y2 < 700:

                canvas.delete("bird")
                self.createBird()
               
            
            else:
                self.halt = True
                self.dead = True
                changeColor()
                dead += 1
                self.birdColor = "orange"
                
                return

            # changing the refresh time so that the animation speed seems the same for any number of birds <= 4
            if dead < 3:
                canvas.after(2*dead+1)
            else:
                canvas.after(10)
            
            canvas.update()

# function responsible for making the graph of score vs generation
def markPoint():
    global pointsGap
    if gen > 2:
        pointsGap = pointsWidth / (gen-2)
    if gen > 3:
        blackCanvas.delete("point")
        blackCanvas.delete("line")
    for i in range(len(scores)):
        blackCanvas.create_oval(40 + pointsGap*(i), 230 - (220/target)*scores[i], 45 + pointsGap*(i), 235 - (220/target)*scores[i], fill = "white", tags = "point")
        if i > 0:
            blackCanvas.create_line(42.5 + pointsGap*(i-1), 232.5 - (220/target)*scores[i-1], 42.5 + pointsGap*(i), 232.5 - (220/target)*scores[i], fill = "white", tags = "line")
    
        
    

# triggers the preparation of the next generation
def createGen():
    global birds, gen
    gen += 1
    genBox["text"] = "Generation: " + str(gen)
    # assigning random values at the start
    if gen == 1:
        for i in range(num):
            sign = random.randint(1,2)
            birds.append(Bird(((-1)**sign)*random.random()*500, 60-random.random()*175))
            parentBox["text"] = "Parent: None"
        
    else:
        
        select()

# selects the fittest individual(s) from the last generation
def select():
    global gene, repeat, theBest
    fittest = max(birds[0].count, birds[1].count, birds[2].count, birds[3].count)
    weakest = min(birds[0].count, birds[1].count, birds[2].count, birds[3].count)
    #scores.append(fittest)
    markPoint()
    # if the previous generation birds didn't achieve much:
    if fittest - weakest < 10 and weakest < 300:
        parentBox["text"] = "Parent: None"
        
        repeat = True
    else:
        repeat = False
        
        best = []
        for i in range(num):
            if fittest == birds[i].count:
                best.append(i)
        # combines the values of the top two birds, if the top two score the same
        if len(best) > 1:
            x = (birds[best[0]].x + birds[best[1]].x)/2
            r = (birds[best[0]].reaction + birds[best[1]].reaction)/2
            gene = [x, r]
        else:
            gene = [birds[best[0]].x, birds[best[0]].reaction]

        parentBox["text"] = "Parent: (" + str(format(gene[0],".2f")) + ", " + str(format(gene[1],".2f")) + ")" 
                    
    previousBest["text"] = "Previous best: " + str(fittest)
    if fittest > theBest:
        theBest = fittest
        allTimeBest["text"] = "All time best: " + str(theBest)
        
    prepare()

# prepares the birds of the next generation
def prepare():
    global birds, repeat
    # if the previous birds didn't perform well, a new set of birds with random values is generated:
    if repeat:
        birds = []
        for i in range(num):
            sign = random.randint(1,2)
            birds.append(Bird(((-1)**sign)*random.random()*500, 80-random.random()*180))
        repeat = False
        return
    
    else:
        birds = []
        # adding mutations to the first three birds
        for i in range(num-1):
            newGene = []
            for j in range(len(mutationLimit)):
                sign = random.randint(1,2)
                newGene.append(gene[j] + ((-1)**sign)*random.random()*mutationLimit[j])
            birds.append(Bird(newGene[0], newGene[1]))
        # adding the fourth and last bird to the next generation, but this last one
        # has the same properties as the fittest bird of the last generation, since
        # it will prove to be useful in a generation whose first three birds have received
        # negative/bad mutations, hence perhaps preventing the birds from devolving, and
        # saving them from a catastrophe. This will ensure that the progress being made
        # through the generations will be positive, and that it is never lost.
        birds.append(Bird(gene[0], gene[1]))
        
                        
    
# creates a new pair of pipes with random heights
def createPipe():
    global pipeNum, count
   
    height = random.random() * 450 + 200
    
    pipes.append(700)
    pipeHeight.append(height)
    count += 1
    
    
# a key function responsible for the animation of the pipes
def movePipes():
        global count, pipes, pipeHeight, score, scoreBox, pipe, highScore

        # interval of time after another pair is made
        if count % 20 == 0:
           
            createPipe()

        for j in range(len(pipes)):
            canvas.delete("pipe" + str(j))
           

        pipes = [x - pipeSpeed for x in pipes]
        
        # creating the green rectangular pipes
        for k in range(len(pipes)):
            
            
            canvas.create_rectangle(pipes[k], pipeHeight[k], pipes[k] + 100, 700, fill = "green", width = 2, tags = "pipe" + str(k))
            canvas.create_rectangle(pipes[k] - 8, pipeHeight[k], pipes[k] + 108, pipeHeight[k] + 50, width = 2, fill = "green", tags = "pipe" + str(k)) 
            canvas.create_rectangle(pipes[k], 0, pipes[k] + 100, pipeHeight[k] - 150, fill = "green", width = 2, tags = "pipe" + str(k))
            canvas.create_rectangle(pipes[k] - 8, pipeHeight[k] - 200, pipes[k] + 108, pipeHeight[k] - 150, width = 2, fill = "green", tags = "pipe" + str(k)) 

        count += 1
        

        # if the pipe goes beyond the left side of the screen
        if pipes[0] < -115:
            canvas.delete("pipe0")
            pipes.pop(0)
            pipeHeight.pop(0)
            # all birds now focus on the first pipe in the list
            for bird in birds:
                bird.pipe = 0
            score += 1
            scoreBox["text"] = str(score)
            if score > highScore:
                highScore = score
                highScoreBox["text"] = str(highScore)
                
        else:
            for bird in birds:
                # if the foremost pipe is beyond a bird's reaction parametre,
                # then that bird will focus on the second pipe. The foremost
                # pipe has to cross a certain threshold for the bird to change focus.
                if pipes[0] < bird.reaction:
                    bird.pipe = 1
            
            
        if not(birds[0].halt and birds[1].halt and birds[2].halt and birds[3].halt):
            canvas.after(80, movePipes)
        

# resets all the variables to their initial values, and helps in restarting
def reset():
    
    global pipes, pipeHeight, pipeSpeed, count, times, score, dead, pipe, box
    for j in range(len(pipes)):
        canvas.delete("pipe" + str(j))
    for i in range(num):
        birdBoxes[i]["fg"] = "green"
        birdBoxes[i+num]["fg"] = "green"
    pipes = []
    pipeHeight = []
    pipeSpeed = 15
    score = 0
    scoreBox["text"] = str(score)
    box = 0
    dead = 0
    count = 0
    pipe = 0
    times += 1

# function responsible for writing the birds' parametres on the screen
def fillLabels():
    for i in range(num):
        birdBoxes[i]["text"] = "Bird " + str(i+1) + ": (" + str(format(birds[i].x, ".2f")) + ", " + str(format(birds[i].reaction, ".2f")) + ")"


def changeColor():
    for i in range(num):
        if birds[i].dead:
            birdBoxes[i]["fg"] = "red"
            birdBoxes[i+num]["fg"] = "red"

# function which will be executed once the target is reached
def endProcess():
    global gen
    for bird in birds:
        bird.halt = True
    result["text"] = "Target: " + str(target) + " (Achieved)"
    scores.append(score)
    gen += 1
    # marks the last point
    markPoint()
    colors = ["red", "lightgreen", "yellow", "pink", "purple", "blue", "lightblue"]
    # the background will flash some colors
    for i in range(len(colors)):
        canvas.configure(bg = colors[i])
        canvas.update()
        time.sleep(0.5)
    time.sleep(5)
    # window will close 5 seconds after the background has stopped flashing
    wn.destroy()
    
    
    

            
# the main function, which drives the whole process
def begin():
    
    global box, over

    createGen()
    fillLabels()
    createPipe()
    # movePipes has to be triggered only once, as canvas.after will take care of it from there
    if times == 0:
        movePipes()

    # continue till the target has been reached
    while score < target:
       
        for bird in birds:
            
            box += 1
            # if the bird hasn't hit the ground yet:
            if not bird.halt:
                bird.fly()
                birdBoxes[box+num-1]["text"] = "Bird " + str(box) + ": " + str(birds[box-1].count)
            
        # only if all the birds have hit the ground:
        if birds[0].halt and birds[1].halt and birds[2].halt and birds[3].halt:
            scores.append(score)
            break

        box = 0
    # if target has been reached
    if score == target:
        over = True
        
    time.sleep(2)
    
    # making the main function recursive
    if not over:
        reset()
        begin()
    else:
        endProcess()
        
        
        

if __name__ == "__main__":
    
    begin()       

wn.mainloop()  


