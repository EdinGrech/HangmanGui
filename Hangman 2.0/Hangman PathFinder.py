from functools import partial
import random
import tkinter as tk
import pygame
import time

import os, sys

#path identification and presetting
APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
SoundPath = str(f"{APP_FOLDER}\Sound")
AssatsPath = str(f"{APP_FOLDER}\Assats")
pygame.mixer.init()

#path loading music and setting the volume
bg_music=pygame.mixer.Sound(os.path.join(SoundPath,'HMM.mp3'))
bg_music.set_volume(0.22)
select_effect = pygame.mixer.Sound(os.path.join(SoundPath,'selectEff.mp3'))
select_effect.set_volume(0.64)
Correct = pygame.mixer.Sound(os.path.join(SoundPath,'Correct.mp3'))
Correct.set_volume(0.45)
gameOverS = pygame.mixer.Sound(os.path.join(SoundPath,'Game Over.mp3'))
gameOverS.set_volume(0.7)
Wrong = pygame.mixer.Sound(os.path.join(SoundPath,'Wrong.mp3'))
Wrong.set_volume(1.3)
WinS=pygame.mixer.Sound(os.path.join(SoundPath,'Win.mp3'))
WinS.set_volume(0.28)
channel1 = pygame.mixer.Channel(0)
channel1.play(bg_music,-1)
channel2 = pygame.mixer.Channel(1)

#global presets
GraphiscSetting = int(1)
hangingLevel=-1


def titleLoader():

    '''THis function is given the relative file path to all the assets and loads
    the hangmanWord into a list where each like is an item so that leter we can animate it'''

    titleLoaderList=[]
    try:
        with open(os.path.join(AssatsPath,"hangmanWord.txt"),'r') as This_file:
            for line in This_file:
                #removing the \n
                titleLoaderList.append(line[:-1])
            #adding an extra item in the list so title loader has a animation buffer
            titleLoaderList.append("")
        return titleLoaderList
    except:
        #console debug 
        print("Missing file, the program is not operational, please verify")
        print("quitting")
        quit()

def wordLoader():

    '''This function is used to load all the words from the file into a list'''

    loadedWordList=[]
    try:
        with open(os.path.join(AssatsPath,"ListOfWords.txt"),'r') as This_Wfile:
            for line in This_Wfile:
                loadedWordList.append(line)
    except:
        print("Error has occured teneting back up mode")
        loadedWordList=["abruptly","buffalo","circket","duplex","fashion","galaxy"]
    return loadedWordList

def ranWordPicker(loadedWordList):
    '''This function randomly selects a word from the list and returnes just the word'''
    ranPos=random.randint(0,len(loadedWordList))
    return loadedWordList[ranPos]

def hangingLoader(spacerVal):

    '''This function loades the selected graphics the user picked (or uses the default if not selected) then it loades the apropriate
        file that corisponds to the option, using the paramiter value it separates the frames and loads them into a list to be displayed
        by the function that calls it'''

    try:
        with open(os.path.join(AssatsPath,f"hangmanDrawings{GraphiscSetting+1}.txt"),'r') as This_file:
            hangingGRAList=[]
            printLineSave=""
            x=int(0)
            for line in This_file:
                if x==spacerVal:
                    hangingGRAList.append(printLineSave)
                    printLineSave=""
                    x=-1
                else:
                    printLineSave=printLineSave+line
                x=x+1
            hangingGRAList.append(printLineSave)
        for x in hangingGRAList:
            print(x)#debug    
        return hangingGRAList
    except:
        print("Missing file, the program is not operational, please verify")
        print("quitting")
        quit()


def play():
    #function called by the music controls button to play the music
    channel1.play(bg_music,-1)

def pause():
    #function called by the music controls button to pause the music
    channel1.pause()


def newWindow():
    '''
    ~Welcome to the Main Window~

    here is where everything is created

    and all the nested functions are
    in order to not have paramiters flying everywhere nore a bunch of unnecessary golbals 
    '''

    #creating root object
    root=tk.Tk()
    #recnaming the window
    root.wm_title("Hangman")
    #loading window logo
    root.iconbitmap(os.path.join(AssatsPath,"hangman.ico"))
    #making thw window fixed
    root.resizable(width=False, height=False)

    #canvas creation and placement
    canvas = tk.Canvas(root,height=700,width=700,bg="#263D42")
    canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    #object frame for music controles
    button_fr = tk.Frame(root,bg="#c9b177")
    button_fr.place(relwidth=1,relheight=0.03,rely=0.02)

    #music lable
    button_text = tk.Label(button_fr,text="Music",font=('Arial', 10),fg="black",bg="#dbb55a")
    button_text.place(relx=0.755,rely=0.03)

    #music controles buttons
    button_1 = tk.Button(button_fr,height=1,width=5,bg="gray",text = "Play", command = play)
    button_1.place(relx=0.82,rely=0.03)

    button_2 = tk.Button(button_fr,height=1,width=5,bg="gray",text = "Pause", command = pause)
    button_2.place(relx=0.9,rely=0.03)

    def startHanging():

        #function that is called when start is pressed
        #playes select sound
        channel2.play(select_effect)

        #removes unwanted frames
        startButton.place_forget()
        grpOptBt_Fr.place_forget()
        print("Start pressed")#debug
        
        #small wait because wanted to give the effect of delay
        time.sleep(0.1)

        #calling function to load display frams to play the game
        hangerDisp()

    def dispGra(x):
        #this function is called by the graphics select buttons at the start screen to over write the global variable on what setting is selected

        #playes select sound
        channel2.play(select_effect)

        #overwriting global GraphiscSetting
        global GraphiscSetting
        GraphiscSetting = int(x)
        print(GraphiscSetting)#debug

    def hangerDisp():
        #this function takes care of the entire game, this includes placing all the letter keys, exit key, win key,game over key and display logic for the hangman graphics
        
        #these 2 boolian veriables are to make sure the program dose not creat multiple object frames and buttons unnecessary (you will see the if statements later on)
        firstRun=True
        firstRun2=True

        #loading the correct graphics and assigning the right frame separator value AND giving the text font config to the lable so the graphics look good in the Label
        if GraphiscSetting==0:
            hangingGRAList=hangingLoader(23)
            graFont2=('Consolas',8)
        elif GraphiscSetting==1:
            hangingGRAList=hangingLoader(8)
            graFont2=('Consolas',16)
        elif GraphiscSetting==2:
            hangingGRAList=hangingLoader(7)
            graFont2=('Consolas',18)

        def letterVerifire(letter,x):

            '''This function is called by the lettor buttens, it recives the letter value of the key and its position in the list of objects
                then the function uses the .find to look for the letter (not cap sencitive) and loops till it finds all the letters
                there is also a sound effect that plays if the user guess right or wrong
                
                The function also updates the dispWord veriable which is used to display the letters/spaces in the word
                it also moniters how many letters where wrong and calls a function to update the graphics'''
            letterButton[x].grid_forget()
            letterLoop=True
            letterPos=-1

            letterPosS=word.find(letter.lower())
            if letterPosS==-1:
                channel2.play(Wrong)
            else:
                channel2.play(Correct)  
            count=0
            while letterLoop==True:
                letterPos=word.find(letter.lower(),letterPos+1)
                if letterPos==-1:
                    letterLoop=False#finish this
                    if count==0:
                        hGraphicDisplayer()
                else:
                    letterPosDP=(letterPos*3)+1
                    global dispWord
                    print(dispWord)#debug 
                    dispWord=f"{dispWord[:letterPosDP]}{letter}{dispWord[letterPosDP+1:]}"
                    print(dispWord)#debug
                    HangingWordBox.config(text=(dispWord))
                    wincon=dispWord.find("_")
                    if wincon==-1:
                        winScreen()

                    count+=1

        def gameStartReset():
            #This function is used to reset the game and loads all the start screen frames 
            global hangingLevel
            hangingLevel=-1

            channel2.play(select_effect)
            lettersButton_fr.place_forget()
            HangingGra_fr.place_forget()
            HangingWordBox_Fr.place_forget()
            gameOver_fr.place_forget()
            winner_fr.place_forget()

            grpOptBt_Fr.place(relwidth=0.456,relheight=0.03,relx=0.26,rely=0.7)
            startButton.place(relx=0.29,rely=0.38)

        #creating fram and button
        gameOver_fr = tk.Frame(root,bg="#b8900f")
        gameOverBt = tk.Button(gameOver_fr,bg="#c74410",fg="#c79f10",font=('Courier',7,"bold"),relief="raised",text="  ________                        ________                      \n /  _____/_____    _____   ____   \_____  \___  __ ___________  \n/   \  ___\__  \  /     \_/ __ \   /   |   \  \/ // __ \_  __ \ \n\    \_\  \/ __ \|  Y Y  \  ___/  /    |    \   /\  ___/|  | \/ \n \______  (____  /__|_|  /\___  > \_______  /\_/  \___  >__|    \n        \/     \/      \/     \/          \/          \/        ",command=gameStartReset)

        def gameOver():
            #this function is called if the user get 8 letters wrong 

            #game over sound effect plays
            channel2.play(gameOverS)

            #global wrong guess counter reset
            global hangingLevel
            hangingLevel=-1

            #removing frames
            lettersButton_fr.place_forget()
            HangingGra_fr.place_forget()
            HangingWordBox_Fr.place_forget()

            #placing frame and button
            gameOver_fr.place(relwidth=0.65,relheight=0.24,rely=0.37,relx=0.17)
            gameOverBt.place(relwidth=0.94,relheight=0.9,rely=0.05,relx=0.031)

        #creating fram and button
        winner_fr = tk.Frame(root,bg="#a8184f")
        winnerBt = tk.Button(winner_fr,bg="#5c10c7",fg="#9c942d",font=('Courier',9,"bold"),relief="raised",text=" __      __.__                             \n/  \    /  \__| ____   ____   ___________  \n\   \/\/   /  |/    \ /    \_/ __ \_  __ \ \n \        /|  |   |  \   |  \  ___/|  | \/ \n  \__/\  / |__|___|  /___|  /\___  >__|    \n       \/          \/     \/     \/       ",command=gameStartReset)

        def winScreen():
            #function is called when user guesses all the letters 

            #playes victory music
            channel2.play(WinS)

            #global wrong guess counter reset
            global hangingLevel
            hangingLevel=-1

            #removing frames
            lettersButton_fr.place_forget()
            HangingGra_fr.place_forget()
            HangingWordBox_Fr.place_forget()

            #placing frame and win button
            winner_fr.place(relwidth=0.65,relheight=0.24,rely=0.37,relx=0.17)
            winnerBt.place(relwidth=0.94,relheight=0.9,rely=0.05,relx=0.031)

        #creating fram and button
        HangingGra_fr = tk.Frame(root,bg="#3b5463")
        HangingGra_fr.place(relwidth=0.4,relheight=0.47,rely=0.47,relx=0.55)
        
        def hGraphicDisplayer():
            #called if the letter is not in the word

            #global ranging level increment
            global hangingLevel
            hangingLevel+=1

            #depending on how many frames the graphics txt has the game will agjust, when the limit is reached then the gameOver function is called
            if hangingLevel>=len(hangingGRAList):
                hangingLevel=-1
                gameOver()
    
            #what displays the graphics
            HangingGra = tk.Label(HangingGra_fr,bg="#729bad",font=graFont2,text=hangingGRAList[hangingLevel])
            HangingGra.place(relwidth=0.9,relheight=0.9,rely=0.05,relx=0.05)

        #creation of the frame that holds the adjustable word box
        HangingWordBox_Fr = tk.Frame(root,bg="#c99077")
        HangingWordBox_Fr.place(relwidth=0.4,relheight=0.054,rely=0.38,relx=0.55)
        
        #couple of lines that call the external functions inorder to obtain the random word 
        global word
        word=ranWordPicker(wordLoader())[:-1]
        print(word)#debug

        #creating and placing the adjustable word box depending on its lenght 
        HangingWordBox = tk.Label(HangingWordBox_Fr,font=('Courier',11,"bold"))
        HangingWordBox.place(rely=0.235,relx=0.02)

        #setting up the displayWord
        if firstRun==True:
            firstRun=False
            global dispWord
            dispWord=str(" _ "*len(word))
            HangingWordBox.config(text=(dispWord))

        #creating the list of objects and placing them in the grid, also adding the exit key at the end
        if firstRun2==True:
            firstRun2=False
            lettersButton_fr = tk.Frame(root,bg="#3b4242")
            lettersButton_fr.place(relwidth=0.4,relheight=0.5185,rely=0.44,relx=0.05)

            letterList=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
            letterButton=[]
            for x,letter in enumerate(letterList):
                letterButton.append("")
                letterButton[x]=tk.Button(lettersButton_fr,height=2,width=12,bg="gray",text = letter,command=partial(letterVerifire,letter,x))
                ro=int(x/3)
                if (x%3)==0:
                    letterButton[x].grid(row=ro,column=0)
                elif(x%3)==1:
                    letterButton[x].grid(row=ro,column=1)
                elif(x%3)==2:
                    letterButton[x].grid(row=ro,column=2)
            exitButton=tk.Button(lettersButton_fr,height=2,width=12,bg="#2e4a28",fg="white",text = "EXIT",command=gameStartReset)
            exitButton.grid(row=8,column=2)
        #FUNCTION FINALLY ENDS    

    #creating start button and plaving
    startButton = tk.Button(canvas,height=8,width=40,bg="#1a3f54",fg="#ab6120",text = "  _________ __                 __   \n /   _____//  |______ ________/  |_ \n  \_____  \\\   __\__  \\\_  __ \   __\ \n /        \|  |  / __ \|  | \/|  |  \n/_______  /|__| (____  /__|   |__|  \n        \/           \/             ",font=('Courier',9,"bold"),relief="raised", command = startHanging)
    startButton.place(relx=0.29,rely=0.38)

    #creating graphics setting buttons frame 
    grpOptBt_Fr = tk.Frame(canvas)
    grpOptBt_Fr.place(relwidth=0.456,relheight=0.03,relx=0.26,rely=0.7)
    grpOptBt=[]

    #creating and placing the list of object keys
    for x in range(0,3):
        grpOptBt.append("")
        grpOptBt[x]=tk.Button(grpOptBt_Fr,height=1,width=14,bg="gray",text = f"Graphics Option {x+1}",command=partial(dispGra,x))
        grpOptBt[x].grid(row=0,column=x)
    
    #Title Frame maker (all the animated logo code)
    title_fr = tk.Frame(root,bg="white")
    title_fr.place(relwidth=1,relheight=0.22,rely=0.07)
    titelList=titleLoader()

    count = int(0)
    colours=["#96566c","#96568f","#565996","#568b96","#569673","#739656","#a1a647","#a37739","#9c3c28"]
    title=[]
    for i,x in enumerate(titelList):
        title.append("")
        title[i] = tk.Label(title_fr,font=('Courier',9,"bold"),fg=colours[i],text=x)

    while root!=None: 
        #its an infanate loop i know, satain will visit me soon
        count+=1
        #update loop
        for i,x in enumerate(titelList):
            title[i].place(relwidth=1,relheight=0.105,rely=(0.03+(i/9.1)))
            #changing each lines colour via a config, the coloures are stored in a list
            title[i].config(fg=colours[(i+count)%8],text=x)
            time.sleep(0.04)
            #the line that makes the entire program event driven and updates the graphics
            root.update()

newWindow()