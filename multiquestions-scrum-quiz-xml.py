#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
"""XML-driven Scrum quiz with single- and multiple-answer questions."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET

QUESTIONS_FILE = Path(__file__).resolve().parent / "questions.xml"

@dataclass(frozen=True)
class Question:
    prompt: str
    options: tuple[str, ...]
    correct: frozenset[int]
    multi: bool

def load_questions(path: Path = QUESTIONS_FILE) -> list[Question]:
    root = ET.parse(path).getroot()
    questions = []
    for element in root.findall("question"):
        answers = element.findall("answer")
        options = tuple(answer.get("text", "") for answer in answers)
        correct = frozenset(i for i, answer in enumerate(answers) if answer.get("valid", "").lower() == "true")
        multi = element.get("type") == "multi"
        if not element.get("msg") or not options or not correct or (not multi and len(correct) != 1):
            raise ValueError("Invalid question definition")
        questions.append(Question(element.get("msg", ""), options, correct, multi))
    if not questions:
        raise ValueError("No questions found")
    return questions

def grade(questions: list[Question], answers: dict[int, set[int]]) -> tuple[int, int]:
    return sum(answers.get(i, set()) == q.correct for i, q in enumerate(questions)), len(questions)

class Quiz(ttk.Frame):
    def __init__(self, root: tk.Tk, questions: list[Question]):
        super().__init__(root, padding=20)
        self.pack(fill="both", expand=True)
        self.questions = questions
        self.index = 0
        self.answers: dict[int, set[int]] = {}
        self.title = tk.StringVar()
        self.status = tk.StringVar()
        ttk.Label(self, textvariable=self.title, wraplength=680, font=("sans", 12)).pack(pady=12)
        self.options = ttk.Frame(self)
        self.options.pack(fill="x", expand=True)
        ttk.Label(self, textvariable=self.status).pack(pady=8)
        ttk.Button(self, text="Next / Finish", command=self.next).pack()
        self.show()

    def show(self) -> None:
        q = self.questions[self.index]
        self.title.set(q.prompt)
        self.status.set(f"Question {self.index + 1}/{len(self.questions)} — " + ("select all correct" if q.multi else "select one"))
        for widget in self.options.winfo_children():
            widget.destroy()
        self.vars = []
        for i, label in enumerate(q.options):
            var = tk.BooleanVar(value=i in self.answers.get(self.index, set()))
            self.vars.append(var)
            ttk.Checkbutton(self.options, text=label, variable=var, command=self.remember).pack(anchor="w", pady=6)
    def remember(self) -> None:
        chosen = {i for i, var in enumerate(self.vars) if var.get()}
        if not self.questions[self.index].multi and len(chosen) > 1:
            last = next((i for i, var in enumerate(self.vars) if var.get() and i not in self.answers.get(self.index, set())), min(chosen))
            chosen = {last}
            for i, var in enumerate(self.vars):
                var.set(i in chosen)
        self.answers[self.index] = chosen

    def next(self) -> None:
        if self.index + 1 < len(self.questions):
            self.index += 1
            self.show()
        else:
            points, total = grade(self.questions, self.answers)
            self.title.set(f"Score: {points}/{total}")
            self.status.set("Historical training questions; consult the current Scrum Guide.")
            for widget in self.options.winfo_children():
                widget.destroy()

def main() -> None:
    questions = load_questions()
    root = tk.Tk()
    root.title("Scrum XML Quiz")
    root.geometry("800x490")
    Quiz(root, questions)
    root.mainloop()

if __name__ == "__main__":
    main()
