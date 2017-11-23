class Question:
    def __init__(self,question, type):
        self.question=question
        self.type=type
        self.answer=[]

    def AddAnswer(self, answer):
        self.answer.append(answer)

class Answer:
    def __init__(self, text, valid):
        self.text=text
        self.valid=valid