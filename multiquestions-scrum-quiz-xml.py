#!/usr/local/bin/python
# Developer : Hamdy Abou El Anein

from easygui import *

#please use at least version 0.98  with #sudo python3 -m pip install --upgrade easygui

import time
import math
import sys
import random
import xml.etree.ElementTree as ET
from class_questions import *


score = 0
nombre = 0 #number of questions answered

logo = "./images/quiz-logo.gif"

play = ["Yes","No"]

start_title = "Welcome to The Scrum Master Quiz"
start_msg = "Can we begin the Quiz now ?"



player_name = enterbox(msg="Enter your name.", title="Player name", default="Player")


game_xml = fileopenbox(msg="Select Your Test", title="Test Selection", default="./xml/*.xml*", multiple=False)
if game_xml == None:
    sys.exit(0)
else:
    game_start = buttonbox(title=start_title,image=logo,msg=start_msg,choices=play)

tree = ET.parse(game_xml)
root = tree.getroot()

bookmark = "Bookmark this question"

ListBookmark = []

ListQuestions=[]


for XMLquestion in root:
    msg = XMLquestion.attrib.get("msg")
    type = XMLquestion.attrib.get("type")
    question = Question(msg, type)

    ListQuestions.append(question)



    for XMLanswer in XMLquestion:
        ans=Answer(XMLanswer.attrib.get("text"),XMLanswer.attrib.get("valid") == "true")
        question.AddAnswer(ans)

random.shuffle(ListQuestions)




rate = int(root.attrib.get("success-rate"))
MaxQuestions = int(root.attrib.get("number_questions"))

start = time.time()

if game_start == "No":
    sys.exit(0)

if game_start != "No":



    msgbox(title="Let the Scrum Master Quizz begin",image=logo,msg="Your score is "+str(score))

    NumberSelected = integerbox(title="Number of questions", msg=" Enter how many questions you want for the quiz ? Max : " +str(MaxQuestions), default=MaxQuestions,lowerbound=1,upperbound=MaxQuestions)

    counter = 0
    ListCorrectQuestions = []
    ListIncorrectQuestions = []
    for question in ListQuestions:
        anstrue = []
        ans = []


        for answer in question.answer:
            ans.append(answer.text)
            random.shuffle(ans)



            if answer.valid:
                anstrue.append(answer.text)


        if question.type == "unique":
            ans.append(bookmark)

            userAnswer = choicebox(msg, "question", ans)

            if userAnswer == bookmark:
                counter = counter + 1
                ListBookmark.append(question)

            elif userAnswer in anstrue:
                score = score + 1
                nombre = nombre +1
                counter = counter +1
                end = time.time()
                result = end - start
                correct = ("Well done you got it right. Your score is " +str(score)+str( ". Time used until now : " +str(math.floor(result))+str(" seconds")))
                image = "./images/tick.gif"
                msgbox(title="CORRECT", image=image, msg=correct)
                ListCorrectQuestions.append(question)

            elif userAnswer==None:
                sys.exit(0)


            else:
                end = time.time()
                result = end - start
                nombre = nombre + 1
                counter = counter +1
                wrong = ("I'm sorry that's the wrong answer, your time used until now is " + str(math.floor(result)) +str(" seconds"))
                image = "./images/cross.gif"
                msgbox(title="Wrong Answer", image=image, msg=wrong)
                ListIncorrectQuestions.append(question)



        else:
            ans.append(bookmark)
            userAnswer = multchoicebox(msg,"question",ans)


            if userAnswer==anstrue:
                score = score + 1
                nombre = nombre +1
                end = time.time()
                result = end - start
                counter = counter +1
                correct = ("Well done you got it right. Your score is " + str(score)+str( ". Time used until now : " +str(math.floor(result))+str(" seconds")))
                image = "./images/tick.gif"
                msgbox(title="CORRECT", image=image, msg=correct)
                ListCorrectQuestions.append(question)

            elif bookmark in userAnswer:
                counter = counter + 1
                ListBookmark.append(question)

            elif userAnswer==None:
                sys.exit(0)


            else:
                end = time.time()
                result = end - start
                nombre = nombre + 1
                counter = counter +1
                wrong = ("I'm sorry that's the wrong answer"+str(". Time used until now : " +str(math.floor(result))+str(" seconds")))
                image = "./images/cross.gif"
                msgbox(title="Wrong Answer", image=image, msg=wrong)
                ListIncorrectQuestions.append(question)

        if counter == NumberSelected:
            if ListBookmark:
                question_bookmark = buttonbox(title="Bookmarked Questions", msg = "Do you want to replay the bookmarked questions ?", choices=("Yes","No"),default_choice="Yes",cancel_choice="No")
                if question_bookmark == "Yes":
                    for questionBookmark in ListBookmark:
                        anstrue = []
                        ans = []
                        for answer in questionBookmark.answer:
                            ans.append(answer.text)
                            random.shuffle(ans)

                            if answer.valid:
                                anstrue.append(answer.text)

                        if questionBookmark.type == "unique":


                            userAnswer = choicebox(msg, "question", ans)


                            if userAnswer in anstrue:
                                score = score + 1
                                nombre = nombre + 1

                                end = time.time()
                                result = end - start
                                correct = ("Well done you got it right. Your score is " + str(score) + str(
                                    ". Time used until now : " + str(math.floor(result)) + str(" seconds")))
                                image = "./images/tick.gif"
                                msgbox(title="CORRECT", image=image, msg=correct)
                                ListCorrectQuestions.append(questionBookmark)

                            elif userAnswer == None:
                                sys.exit(0)


                            else:
                                end = time.time()
                                result = end - start
                                nombre = nombre + 1

                                wrong = ("I'm sorry that's the wrong answer, your time used until now is " + str(math.floor(result)) + str(
                                    " seconds"))
                                image = "./images/cross.gif"
                                msgbox(title="Wrong Answer", image=image, msg=wrong)
                                ListIncorrectQuestions.append(questionBookmark)



                        else:
                            userAnswer = multchoicebox(msg, "question", ans)

                            if userAnswer == anstrue:
                                score = score + 1
                                nombre = nombre + 1
                                end = time.time()
                                result = end - start

                                correct = ("Well done you got it right. Your score is " + str(score) + str(
                                    ". Time used until now : " + str(math.floor(result)) + str(" seconds")))
                                image = "./images/tick.gif"
                                msgbox(title="CORRECT", image=image, msg=correct)
                                ListCorrectQuestions.append(questionBookmark)



                            else:
                                end = time.time()
                                result = end - start
                                nombre = nombre + 1

                                wrong = ("I'm sorry that's the wrong answer" + str(
                                    ". Time used until now : " + str(math.floor(result)) + str(" seconds")))
                                image = "./images/cross.gif"
                                msgbox(title="Wrong Answer", image=image, msg=wrong)
                                ListIncorrectQuestions.append(questionBookmark)

            break





end = time.time()
result = end - start

gameover_good = "./images/logo-happy.gif"
gameover_bad = "./images/logo-sad.gif"

game_over_title = "Scrum Master Quiz"

total_score = 100*score/nombre




msg_bad = ("You have not passed the exam ")+str(player_name)+str(" , your score is : ") +str(total_score)+str("\nSuccess rate = ")+str(rate) +str( "\nTotal time used : ") +str(math.floor(result))+str(" seconds")+str("\n\n\nMore details about your exam ?")
msg_good = ("You have passed the exam ")+str(player_name)+str(" , your score is : "+str(total_score))+str("\nSuccess rate = ")+str(rate) +str( "\nTotal time used : " +str(math.floor(result))+str(" seconds"))

if rate < total_score:
    game_over = msgbox(title=game_over_title, image=gameover_good, msg=msg_good)


else:
    choices_det = ("More Details", "Quit the quiz")
    game_over = buttonbox(msg=msg_bad, title=game_over_title, image=gameover_bad, choices=choices_det)

    if game_over == "More Details":
        TotalIncorAns = ""
        for IncorrectAnswered in ListIncorrectQuestions:
            IncorrectAnswered = IncorrectAnswered
            TotalIncorAns = TotalIncorAns + IncorrectAnswered.question + "\n\n"
        msgbox(ok_button="OK", title="Questions with a wrong answer", msg=TotalIncorAns)

    else:
        sys.exit(0)


