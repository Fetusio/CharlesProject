import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import simpledialog
from tkinter.messagebox import showinfo
from tkinter import scrolledtext
from tkinter import filedialog
import tkinter.messagebox

import os
import glob

import nltk
from nltk.corpus import stopwords
from nltk.corpus import pros_cons
from nltk import word_tokenize

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import re

import spacy
from spacy import displacy
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return "{:.1f}%\n({v:d})".format(pct, v=val)
    return my_format

from flask import Flask
app = Flask(__name__)

@app.route('/')

def hello_world():

    nlp = spacy.load("en_core_web_sm")
    # root window
    root = tk.Tk()

    root.geometry("1600x800")
    root.title("NLP Tool")
    root.resizable(1, 1)

    # configure the grid
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)

    frameLeft = Frame(root)
    frameLeft.grid(row=0, column=0, sticky=tk.NW)

    frameMid = Frame(root)
    frameMid.grid(row=0, column=1, sticky=tk.N)

    frameRight = Frame(root)
    frameRight.grid(row=0, column=2, sticky=tk.NE)

    # middle text
    midText_label = tk.Label(frameMid, text="Enter Text Here", font=("Arial", 25))
    midText_label.grid(column=1, row=0, sticky=tk.N, padx=0, pady=5)

    # middle text input
    text_area = scrolledtext.ScrolledText(frameMid, wrap=tk.WORD, width=50, height=14, font=("Times New Roman", 15))
    text_area.grid(column=1, row=1, pady=5, padx=10)

    def convertTuple(tup):
        st = ''.join(map(str, tup))
        return st

    def syllable_count(word):
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        starts = ['ou','ei','ae','ea','eu','oi']
        endings = ['es','ed','e','at']
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        #if word.endswith("le"):
        #    count+= 1
        for start in starts:
            if word.startswith(start):
                count -= 1
        for ending in endings:
            if word.endswith(ending):
                count -= 1
        if count == 0:
            count += 1
        return count

    def onClickVisualise():
        Input = text_area.get("1.0", "end-1c")
        basic_nlp(Input)

        plt.close()
        fig, axs = plt.subplots(1, 2)
        axs[0].clear()
        axs[1].clear()
       
        myLabels = ["Noun Phrases", "Verbs", "Adjectives"]
        axs[0].bar(myLabels, data1, color="royalblue", alpha=0.7)
        axs[0].grid(color="#95a5a6", linestyle="--", linewidth=2, axis="y", alpha=0.7)
        axs[1].pie(data1, labels=myLabels, autopct=autopct_format(data1))
        plt.show()

    def onClickFlesch():

        Input = text_area.get("1.0", "end-1c")
        #print("Input for flesch is " + Input)

        wordTokens = Input.split()
        #print(wordTokens)
        wordCount = len(wordTokens)
        #print(wordCount)

        syllableCount = 0
        #wordCount = 0

        for i in wordTokens:
            noSyllables = syllable_count(i)
            syllableCount += noSyllables
            #wordCount += 1
            #print(i + " has " + str(noSyllables) + " syllables.")

        #sentenceTokens = Input.split(".")
        #sentenceTokens = Input.replace(';','.',' ').replace(',',' ').split()
        sentenceTokens = list(re.split("[!?.]+", Input))
        #print(sentenceTokens)
        #sentenceTokens = re.findall(r"[\w']+", Input)
        sentenceCount = len(sentenceTokens)
        
        #print("Number of words: " + str(wordCount))
        #print("Number of syllables:" + str(syllableCount))
        #print("Total sentence count: " + str(sentenceCount) + "\n")
        #print("Sentence Tokens: " + convertTuple(sentenceTokens) + "\n\n\n\n")

        #Flesch Reading Ease#
        #206.835 − 1.015 × ( Total Words / Total Sentences ) − 84.6 × ( Total Syllables / Total Words )
        readingEase = (206.835-1.015*(int(wordCount)/int(sentenceCount))) - (84.6*(int(syllableCount)/int(wordCount)))
        #print("Unrounded reading ease: " + str(readingEase))
        readingEase = round(readingEase)
        
        if (readingEase >= 0 and readingEase < 30):
            textLevel = "Postgraduate level (More than 2l years old)"
            
        elif (readingEase >= 30 and readingEase < 50):
            textLevel = "Undergraduate level (18 - 21 years old)"
            
        elif (readingEase >= 50 and readingEase < 60):
            textLevel = "GCSE (Y11) to A-Level (Y13) (15 - 18 years old)"
            
        elif (readingEase >= 60 and readingEase < 70):
            textLevel = "Year 9-10 level (13 - 15 years old)"
            
        elif (readingEase >= 70 and readingEase < 80):
            textLevel = "Year 8 level (12 - 13 years old)"
            
        elif (readingEase >= 80 and readingEase < 90):
            textLevel = "Year 7 level (11 - 12 years old)"
            
        elif (readingEase >= 90 and readingEase < 100):
            textLevel = "Year 6 level (10 - 11 years old)"

        elif (readingEase >= 100):
            textLevel = "Year 5 level or below (Less than 10 years old)"
            
        #print("Flesch Reading Ease value: " + str(readingEase))

        #Flesch Kincaid Grade Level#
        gradeLevel = (0.39*(int(wordCount)/int(sentenceCount))) + ((11.8*(int(syllableCount)/int(wordCount))) - 15.59)
        #print("Unrounded grade level: " + str(gradeLevel))
        gradeLevel = round(gradeLevel)
        if (gradeLevel > 12):
            gradeLevel = 12
        elif (gradeLevel < 1):
            gradeLevel = 1
        #print("Flesch Kincaid Grade Level: " + str(gradeLevel))

        showinfo(title = "Flesch Kincaid Grade Level", message = "Flesch Kincaid Grade Level: \n" + str(textLevel) + "\n\nFlesch Reading Ease value: " + str(readingEase))
        
    def find(lst,a):
        result = []
        for x in lst:
            if x == (a):
                i = lst.index(x)
        return i

    def onClickWordCloud():
       
        textInput = text_area.get("1.0", "end-1c")
        #corpus = nltk.corpus.gutenberg.words("melville-moby_dick.txt")
       
        #msg1 = list_nouns(Input)
        #msg2 = list_verbs(Input)
        #msg3 = list_adjectives(Input)

        #p1 = convertTuple(msg1)
        #p2 = convertTuple(msg2)
        #p3 = convertTuple(msg3)

        #ultraP = p1 + p2 + p3
       
        #for char in "[],'":
            #ultraP = ultraP.replace(char, '')
           
        #strippedP = ultraP.replace("[],'", "")
       
        #print(strippedP)
        
        word_list = word_tokenize(textInput)
        listOfWords = [x for x in word_list if len(x)>1]

        #for char in "[],'":
        #    ultraP = listOfWords.replace(char, '')
           
        #strippedP = ultraP.replace("[],'", "")
        
        text_as_string = " ".join(listOfWords)
        wordcloud = WordCloud(max_font_size=40).generate(text_as_string)
        
        plt.close()
        
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")

        plt.show()

    def onClickCompare():
        
        Input = text_area.get("1.0", "end-1c")
        doc = nlp(Input)
        
        nPhrases = [chunk.text for chunk in doc.noun_chunks]
        countnPhrases = len(nPhrases)
        verbCount = [token.lemma_ for token in doc if token.pos_ == "VERB"]
        countVerbs = len(verbCount)
        adjCount = [token.lemma_ for token in doc if token.pos_ == "ADJ"]
        countadj = len(adjCount)
        
        data1 = [(countnPhrases), (countVerbs), (countadj)]
       
        global historical_choice
       
        try:
            # get all selected indices
            selected_indices = list_1.curselection()
            # get selected items
            selected = [list_1.get(i) for i in selected_indices]
            for character in "[]'":
                selected = (str(selected).replace(character, ''))

            selectedFinal = selected + '.txt'
            print(selectedFinal)

            f = open("texts\\" + selectedFinal, encoding="utf8")
            text = f.read()
            
        except:
            selected_indices = list_2.curselection()
            selected = [list_2.get(i) for i in selected_indices]
            text = nltk.corpus.gutenberg.raw(selected)

        #print("Historical text selected: " + text)
        historicalText_nlp(text)

        fig, axs = plt.subplots(2, 2, figsize=(20,14))
        #fig.tight_layout()
        axs[0, 0].clear()
        axs[1, 0].clear()
        axs[1, 0].clear()
        axs[1, 1].clear()
       
        myLabels = ["Noun Phrases", "Verbs", "Adjectives"]
        
        axs[0, 0].bar(myLabels, data1, color="royalblue", alpha=0.7)
        axs[0, 0].set_title('User input', bbox={'facecolor':'0.8', 'pad':2})
        axs[0, 0].grid(color="#95a5a6", linestyle="--", linewidth=2, axis="y", alpha=0.7)
        
        axs[1, 0].bar(myLabels, data2, color="royalblue", alpha=0.7)
        axs[1, 0].set_title('Historical text', bbox={'facecolor':'0.8', 'pad':2})
        axs[1, 0].grid(color="#95a5a6", linestyle="--", linewidth=2, axis="y", alpha=0.7)
        
        axs[0, 1].pie(data1, labels=myLabels, autopct=autopct_format(data1))
        axs[0, 1].set_title('User input', bbox={'facecolor':'0.8', 'pad':2})
        axs[1, 1].pie(data2, labels=myLabels, autopct=autopct_format(data2))
        axs[1, 1].set_title('Historical text', bbox={'facecolor':'0.8', 'pad':2})

        #plt.title("Graphs i guess?", bbox={'facecolor':'0.8', 'pad':5})
        plt.show()

    # open file explorer

    def onClickBrowse():
        global foundText
        
        title = ("Enter a book name")
        prompt = ("Book name: ")
        
        booklist = nltk.corpus.gutenberg.fileids()
        gutenbergList = "\n".join(booklist)
        #print(gutenbergList)

        showinfo(title = "Available Texts", message = gutenbergList)
        answer = simpledialog.askstring(title, prompt)

        file = nltk.corpus.gutenberg.raw(answer + '.txt')
        #f = open(file, encoding="utf8")
        #print(file)

        #msg1 = file.read()
        # middle text output
        midOutput = Text(frameMid, height=13, width=60, font=("Arial", 12))
        # mid scrollbar
        sbSE = Scrollbar(frameMid, orient="vertical", command=midOutput.yview)
        sbSE.grid(column=2, row=2, sticky=SE, padx=3, pady=6)
        midOutput.insert(tk.END, file)
        midOutput["yscrollcommand"] = sbSE.set
        midOutput.grid(column=1, row=2, sticky=tk.S, padx=0, pady=50)

        foundText = file

    def onClickCopy():
        try:
            # get all selected indices
            selected_indices = list_1.curselection()
            if selected_indices: 
                # get selected items
                selected = [list_1.get(i) for i in selected_indices]
                for character in "[]'":
                    selected = (str(selected).replace(character, ''))

                selectedFinal = selected + '.txt'
                #print(selectedFinal)

                f = open("texts\\" + selectedFinal, encoding="utf8")
                file = f.read()
                #print(file)
                
                #text_area.insert(tk.INSERT, file)
                print("Copied from text file!")

            else:
                selected_indices2 = list_2.curselection()
                selected = [list_2.get(i) for i in selected_indices2]
                file = nltk.corpus.gutenberg.raw(selected)

                #text_area.insert(tk.INSERT, file)
                print("Copied from Gutenberg!")

        except ValueError:
            file = foundText
            
        text_area.delete('1.0', tk.END)   
        #print(file)
        text_area.insert(tk.INSERT, file)
        
        

    # browse files button mid
    browse_button = Button(frameMid, text="Browse files...", command=onClickBrowse, height=2, width=15)
    browse_button.grid(column=1, row=2, sticky=NW, padx=10, pady=5)

    #Readability score button
    readability_button = Button(frameMid, text="Readability Score", command=onClickFlesch, height=2, width=20)
    readability_button.grid(column=1, row=2, sticky=NE, padx=10, pady=5)

    # copy text from bottom textbox to top textbox button
    copyText_button = Button(frameMid, text="Copy text", command=onClickCopy, height=2, width=20)
    copyText_button.grid(column=1, row=2, sticky=N, padx=10, pady=5)

    # right side text
    nlptechniques_label = tk.Label(frameRight, text="Select NLP Techniques", font=("Arial", 18))
    nlptechniques_label.grid(column=2, row=0, sticky=tk.W, padx=25, pady=5)

    # right side scrollbar
    sbR = Scrollbar(frameRight, orient="vertical")
    sbR.grid(column=3, row=1, sticky=NS, pady=6)

    # right side list
    list_3 = Listbox(
        frameRight,
        yscrollcommand=sbR.set,
        font=("Times", 20),
        background="white",
        foreground="black",
        selectmode=tk.SINGLE,
    )
    list_3.config(height=20, width=24)
    list_3.insert(END, "Entity Recognition")
    list_3.insert(END, "Show Noun Phrases")
    list_3.insert(END, "Show Adjectives")
    list_3.insert(END, "Show Verbs")
    list_3.insert(END, "Display Wordcloud")
    list_3.insert(END, "Visualise Text")

    #for i in range(95):
        #list_2.insert(END, "Technique " + str(i))

    list_3.grid(column=2, row=1, sticky=W, padx=0, pady=5)
    sbR.config(command=list_3.yview)

    # onclick method for submit button

    def onClickSubmit():
        selected_indices = list_3.curselection()
        choice = str(selected_indices)
        global new_choice
        new_choice = re.sub("[(),]", "", choice)
        
        if new_choice == "0":  # Entity recognition
            Input = text_area.get("1.0", "end-1c")
            #print(Input)
            msg1 = basic_nlp(Input)
            # middle text output
            midOutput = Text(frameMid, height=13, width=60, font=("Arial", 12))
            # mid scrollbar
            sbSE = Scrollbar(frameMid, orient="vertical", command=midOutput.yview)
            sbSE.grid(column=2, row=2, sticky=SE, padx=3, pady=6)
            midOutput.insert(tk.END, msg1)
            midOutput["yscrollcommand"] = sbSE.set
            midOutput.grid(column=1, row=2, sticky=tk.S, padx=0, pady=50)
            
        elif new_choice == "1":  # Show Noun Phrases
            Input = text_area.get("1.0", "end-1c")
            msg1 = list_nouns(Input)
            # middle text output
            midOutput = Text(frameMid, height=13, width=60, font=("Arial", 12))
            # mid scrollbar
            sbSE = Scrollbar(frameMid, orient="vertical", command=midOutput.yview)
            sbSE.grid(column=2, row=2, sticky=SE, padx=3, pady=6)
            midOutput.insert(tk.END, msg1)
            midOutput["yscrollcommand"] = sbSE.set
            midOutput.grid(column=1, row=2, sticky=tk.S, padx=0, pady=50)
            
        elif new_choice == "2":  # Show Adjectives
            Input = text_area.get("1.0", "end-1c")
            msg1 = list_adjectives(Input)
            # middle text output
            midOutput = Text(frameMid, height=13, width=60, font=("Arial", 12))
            # mid scrollbar
            sbSE = Scrollbar(frameMid, orient="vertical", command=midOutput.yview)
            sbSE.grid(column=2, row=2, sticky=SE, padx=3, pady=6)
            midOutput.insert(tk.END, msg1)
            midOutput["yscrollcommand"] = sbSE.set
            midOutput.grid(column=1, row=2, sticky=tk.S, padx=0, pady=50)
            
        elif new_choice == "3":  # Show Verbs
            Input = text_area.get("1.0", "end-1c")
            msg1 = list_verbs(Input)
            # middle text output
            midOutput = Text(frameMid, height=13, width=60, font=("Arial", 12))
            # mid scrollbar
            sbSE = Scrollbar(frameMid, orient="vertical", command=midOutput.yview)
            sbSE.grid(column=2, row=2, sticky=SE, padx=3, pady=6)
            midOutput.insert(tk.END, msg1)
            midOutput["yscrollcommand"] = sbSE.set
            midOutput.grid(column=1, row=2, sticky=tk.S, padx=0, pady=50)

        elif new_choice == "4": # Show wordcloud
            onClickWordCloud()

        elif new_choice == "5": # Visualise texts
            onClickVisualise()
           
    # left side upper text
    repoText_label = ttk.Label(frameLeft, text="Select Comparison Text", font=("Arial", 25))
    repoText_label.grid(column=0, row=0, sticky=tk.W, padx=25, pady=5)

    # left side lower text
    gutenbergText_label = ttk.Label(frameLeft, text="Select a text from Project Gutenberg. These may lag while loading!", font=("Arial", 12))
    gutenbergText_label.grid(column=0, row=3, sticky=tk.SW, padx=0, pady=5)

    # left side scrollbar
    sbL = Scrollbar(frameLeft, orient="vertical")
    sbL.grid(column=1, row=1, sticky=NS, pady=6)

    # left side bottom scrollbar
    sbLD = Scrollbar(frameLeft, orient="vertical")
    sbLD.grid(column=1, row=2, sticky=S, pady=6)

    # left side list
    list_1 = Listbox(
        frameLeft,
        yscrollcommand=sbL.set,
        font=("Times", 20),
        background="white",
        foreground="black",
        selectmode=tk.SINGLE,
        )

    path = "texts\\"
    textList = os.listdir(path)
    #print(textList)
        
    for i in range(len(textList)):
        currentText = textList[i]
        currentText = currentText[:-4]
        list_1.insert(END, currentText)

    list_2 = Listbox(
        frameLeft,
        yscrollcommand=sbLD.set,
        font=("Times", 20),
        background="white",
        foreground="black",
        selectmode=tk.SINGLE,
        )

    list_1.config(height=10, width=36)
    list_2.config(height=10, width=36)

    #list_1.insert(END, "Catcher in the Rye")
    #list_1.insert(END, "Crime and Punishment")
    #list_1.insert(END, "The Picture of Dorian Gray")
    #list_1.insert(END, "A Room With a View")
    #list_1.insert(END, "Romeo and Juliet")

    booklist = nltk.corpus.gutenberg.fileids()

    for i in booklist:
        list_2.insert(END, i)
        
    list_1.grid(column=0, row=1, sticky=NE, padx=0, pady=5)
    list_2.grid(column=0, row=2, sticky=SE, padx=0, pady=5)

    sbL.config(command=list_1.yview)
    sbLD.config(command=list_2.yview)

    # selecting item from list and outputting as message

    def items_selected(event):
        # get all selected indices
        selected_indices = list_1.curselection()
        # get selected items
        selected = [list_1.get(i) for i in selected_indices]
        for character in "[]'":
            selected = (str(selected).replace(character, ''))

        selectedFinal = selected + '.txt'
        print(selectedFinal)

        f = open("texts\\" + selectedFinal, encoding="utf8")
        text = f.read()
        
        # middle text output
        midOutput = Text(frameMid, height=13, width=60, font=("Arial", 12))
        # mid scrollbar
        sbSE = Scrollbar(frameMid, orient="vertical", command=midOutput.yview)
        sbSE.grid(column=2, row=2, sticky=SE, padx=3, pady=6)
        #print(text)
        midOutput.insert(tk.END, text)
        midOutput["yscrollcommand"] = sbSE.set
        midOutput.grid(column=1, row=2, sticky=tk.S, padx=0, pady=50)

    def items_selected2(event):
        # get all selected indices
        selected_indices = list_2.curselection()
        # get selected items
        #selected_langs = ",".join([list_2.get(i) for i in selected_indices])
        #print(selected_langs)

        selected = [list_2.get(i) for i in selected_indices]
        file = nltk.corpus.gutenberg.raw(selected)
        
        # middle text output
        midOutput = Text(frameMid, height=13, width=60, font=("Arial", 12))
        
        # mid scrollbar
        sbSE = Scrollbar(frameMid, orient="vertical", command=midOutput.yview)
        sbSE.grid(column=2, row=2, sticky=SE, padx=3, pady=6)
        midOutput.insert(tk.END, file)
        midOutput["yscrollcommand"] = sbSE.set
        midOutput.grid(column=1, row=2, sticky=tk.S, padx=0, pady=50)

    #def checkLength(text):
     #   if(len(text) > 1000000):
      #      showinfo(title="Warning!", message="Your text has more than 1,000,000 characters and has been trimmed down. The program may be non-responsive while your input is processed.")
       #     text = text[:1000000]
            #return text

    def list_nouns(text):
        if(len(text) > 1000000):
            showinfo(title="Warning!", message="Your text has more than 1,000,000 characters and has been trimmed down. The program may be non-responsive while your input is processed.")
            text = text[:1000000]
        
        doc = nlp(text)
        
        Messagio = ("Noun phrases:", [chunk.text for chunk in doc.noun_chunks], "\n\n\n")
        return Messagio

    def list_verbs(text):

        if(len(text) > 1000000):
            showinfo(title="Warning!", message="Your text has more than 1,000,000 characters and has been trimmed down. The program may be non-responsive while your input is processed.")
            text = text[:1000000]
            
        doc = nlp(text)
        
        Messagio = (
            "Verbs:",
            [token.lemma_ for token in doc if token.pos_ == "VERB"],
            "\n\n\n",
        )
        return Messagio

    def list_adjectives(text):
        
        if(len(text) > 1000000):
            showinfo(title="Warning!", message="Your text has more than 1,000,000 characters and has been trimmed down. The program may be non-responsive while your input is processed.")
            text = text[:1000000]
            
        doc = nlp(text)
        
        Messagio = (
            "Adjectives:",
            [token.lemma_ for token in doc if token.pos_ == "ADJ"],
            "n\n\n",
        )
        return Messagio

    def basic_nlp(text):
        
        global doc
        
        if(len(text) > 1000000):
            showinfo(title="Warning!", message="Your text has more than 1,000,000 characters and has been trimmed down. The program may be non-responsive while your input is processed.")
            text = text[:1000000]
            
        doc = nlp(text)
        
        # Analyze syntax
        Messagio = (
            "Noun phrases:",
            [chunk.text for chunk in doc.noun_chunks],
            "\n\n\n",
            "Verbs:",
            [token.lemma_ for token in doc if token.pos_ == "VERB"],
            "\n\n\n",
            "Adjectives:",
            [token.lemma_ for token in doc if token.pos_ == "ADJ"],
        )
        
        nPhrases = [chunk.text for chunk in doc.noun_chunks]
        countnPhrases = len(nPhrases)
        verbCount = [token.lemma_ for token in doc if token.pos_ == "VERB"]
        countVerbs = len(verbCount)
        adjCount = [token.lemma_ for token in doc if token.pos_ == "ADJ"]
        countadj = len(adjCount)
        global data1
        data1 = [(countnPhrases), (countVerbs), (countadj)]
        return Messagio

    def historicalText_nlp(text):
        Text = text
        global doc1
        doc1 = nlp(Text)  # come back to this (ctrl-f "doc")
        nPhrases = [chunk.text for chunk in doc1.noun_chunks]
        countnPhrases = len(nPhrases)
        verbCount = [token.lemma_ for token in doc1 if token.pos_ == "VERB"]
        countVerbs = len(verbCount)
        adjCount = [token.lemma_ for token in doc1 if token.pos_ == "ADJ"]
        countadj = len(adjCount)
        global data2
        data2 = [(countnPhrases), (countVerbs), (countadj)]

    # submit button
    submit_button = Button(frameRight, text="Submit", command=onClickSubmit, height=2, width=20)
    submit_button.grid(column=2, row=3, sticky=S, padx=5, pady=0)

    # compare button
    compare_button = Button(frameMid, text="Compare Texts", command=onClickCompare, height=2, width=20)
    compare_button.grid(column=1, row=3, sticky=S, padx=5, pady=0)

    # left search text
    #leftSearch_label = ttk.Label(frameLeft, text="Search for a text:", font=("Arial", 25))
    #leftSearch_label.grid(column=0, row=3, sticky=tk.SW, padx=5, pady=5)

    # left search text input
    #searchText_area = tk.Text(frameLeft, width=30, height=2, font=("Times New Roman", 12))
    #searchText_area.grid(column=0, row=3, pady=5, padx=10, sticky=SE)

    list_1.bind("<<ListboxSelect>>", items_selected)
    list_2.bind("<<ListboxSelect>>", items_selected2)

if __name__ == "__main__":
    app.run()
