#!/usr/local/bin/python
# Developer : Hamdy Abou El Anein

from easygui import *


#please use at least version 0.98  with #sudo python3 -m pip install --upgrade easygui

import sys

import pygame

pygame.init()


import xml.etree.ElementTree as ET
tree = ET.parse('questions.xml')
root = tree.getroot()


score = 0

logo = "./images/logo.gif"

play = ["Yes","No"]

start_title = "Welcome to The Scrum Master Quiz"
start_msg = "Would you like to play the Scrum Master Quiz?"
game_start = buttonbox(title=start_title,image=logo,msg=start_msg,choices=play)



print(game_start)

if game_start != "No":

    msgbox(title="Let the Scrum Master Quizz begin",image=logo,msg="Your score is "+str(score))

    for question in root:
        ans = []
        anstrue =[]
        msg = question.attrib.get("msg")
        type = question.attrib.get("type")
        for answer in question:
            ans.append(answer.attrib.get("text"))
            if answer.attrib.get("valid") == "true":
                anstrue.append(answer.attrib.get("text"))
        if type == "unique":
            userAnswer = choicebox(msg,"question",ans)
            if userAnswer in anstrue:
                score = score + 1
                correct = ("Well done you got it right. Your score is " + str(score))
                image = "./images/tick.gif"
                msgbox(title="CORRECT", image=image, msg=correct)

            elif userAnswer==None:
                sys.exit(0)
            else:
                wrong = "I'm sorry that's the wrong answer"
                image = "./images/cross.gif"
                msgbox(title="Wrong Answer", image=image, msg=wrong)

        else:
            userAnswer = multchoicebox(msg,"question",ans)
            print(userAnswer)
            print(anstrue)
            if userAnswer==anstrue:
                score = score + 1
                correct = ("Well done you got it right. Your score is " + str(score))
                image = "./images/tick.gif"
                msgbox(title="CORRECT", image=image, msg=correct)

            else:
                wrong = "I'm sorry that's the wrong answer"
                image = "./images/cross.gif"
                msgbox(title="Wrong Answer", image=image, msg=wrong)

gameover_good = "./images/logo.gif"
gameover_bad = "./images/logo.gif"

game_over_title = "Scrum Master Quiz"
msg_bad = ("You have not passed the exam, your score is (under 85%) : "+str(score))
msg_good = ("You have passed the exam, your score is : "+str(score))
if score < 3: #85% of 4
    game_over = msgbox(title=game_over_title,image=gameover_bad,msg= msg_bad)
else:
    game_over = msgbox(title=game_over_title,image=gameover_good,msg= msg_good)

