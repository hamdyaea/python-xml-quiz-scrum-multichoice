#!/usr/local/bin/python
# Developer : Hamdy Abou El Anein

from easygui import *

import time
import math

#please use at least version 0.98  with #sudo python3 -m pip install --upgrade easygui

import sys

import pygame

pygame.init()


import xml.etree.ElementTree as ET
tree = ET.parse("./xml/scrum.xml")
root = tree.getroot()


score = 0

logo = "./images/quiz-logo.jpg"

play = ["Yes","No"]

start_title = "Welcome to The Scrum Master Quiz"
start_msg = "Would you like to play the Scrum Master Quiz?"
start = time.time()
game_start = buttonbox(title=start_title,image=logo,msg=start_msg,choices=play)
player_name = enterbox(msg="Enter your name.", title="Player name")

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
                end = time.time()
                result = end - start
                correct = ("Well done you got it right. Your score is " +str(score)+str( ". Time used until now : " +str(math.floor(result))+str(" seconds")))
                image = "./images/tick.gif"
                msgbox(title="CORRECT", image=image, msg=correct)

            elif userAnswer==None:
                sys.exit(0)
            else:
                end = time.time()
                result = end - start
                wrong = ("I'm sorry that's the wrong answer, your time used until now is " + str(math.floor(result)) +str(" seconds"))
                image = "./images/cross.gif"
                msgbox(title="Wrong Answer", image=image, msg=wrong)

        else:
            userAnswer = multchoicebox(msg,"question",ans)

            print(anstrue)
            if userAnswer==anstrue:
                score = score + 1
                end = time.time()
                result = end - start
                correct = ("Well done you got it right. Your score is " + str(score)+str( ". Time used until now : " +str(math.floor(result))+str(" seconds")))
                image = "./images/tick.gif"
                msgbox(title="CORRECT", image=image, msg=correct)

            else:
                end = time.time()
                result = end - start
                wrong = ("I'm sorry that's the wrong answer"+str(". Time used until now : " +str(math.floor(result))+str(" seconds")))
                image = "./images/cross.gif"
                msgbox(title="Wrong Answer", image=image, msg=wrong)

end = time.time()
result = end - start

gameover_good = "./images/logo-happy.gif"
gameover_bad = "./images/logo-sad.gif"

game_over_title = "Scrum Master Quiz"
msg_bad = ("You have not passed the exam ")+str(player_name)+str(" , your score is (under 85%) : ")+str(score)+str( ". Total time used :" +str(math.floor(result))+str(" seconds"))
msg_good = ("You have passed the exam ")+str(player_name)+str(" , your score is : "+str(score))+str( ". Total time used :" +str(math.floor(result))+str(" seconds"))
if score < 3: #85% of 4 questions
    game_over = msgbox(title=game_over_title,image=gameover_bad,msg= msg_bad)
else:
    game_over = msgbox(title=game_over_title,image=gameover_good,msg= msg_good)

