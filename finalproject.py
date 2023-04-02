#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 18:57:38 2022

@author: andrewliu
"""

import math

def clean_text(txt):
    """takes a string of text txt as a parameter and returns a list containing the words in txt after it has been sorted"""
    cleanTxt = ''
    for x in txt:
        if x in """.,?"'!;:""":
            x = ' '
        cleanTxt += x 
    return cleanTxt.lower().split()

def stem(s):
    """accepts a string s and returns the root of the word using a variety of if statements"""
    if s[-4:] == 'ship':
        if len(s) < 7:
            s = s
        elif s[-5] == s[-6]:
            s = s[:-5]
        else:
            s = s[:-4]
    elif s[-4:] == "tion":
        if len(s) < 8:
            s = s
        elif s[-5] == s[-6]:
            s = s[:-4]
        elif s[-6:-4] == 'at':
            s = s[:-4] + 'e'
        else:
            s = s[:-4]
    elif s[-4:] == "iers":
        if len(s) < 8:
            s = s 
        else:
            s = s[:-3]
    elif s[-3:] == "ing":
        if len(s) < 6: 
            s = s
        elif s[-4] == s[-5]:
            s = s[:-4]
        elif s[-4] == 's' or s[-4] == 't':
            s = s[-3] + 'e'
        else:
            s = s[:-3]
    elif s[-3:] == "ies":
        if len(s) < 6 :
            s = s
        elif s[-4] == [-5]:
            s = s[:-4]
        else:
            s = s[:-3]
            s += 'y'
    elif s[-2:] == 'ed':
        if len(s) < 5: 
            s = s
        elif s[-3] == s[-4]:
            s = s[-3]
        elif s[-3] == 's' or s[-3] == 't' or s[-3] == 'k':
            s = s[:-1] 
        else:
            s = s[:-2]
    elif s[-2:] == 'en':
        if len(s) < 5: 
            s = s
        elif s[-3] == s[-4]:
            s = s[-3]
        else:
            s = s[:-2]
    elif s[-1] == 'e':
        if len(s) < 4:
            s = s
        else:
            s = s[:-1]
    elif s[-1] == 'y':
        if len(s) < 5:
            s = s
        s = s[:-1] + 'i'
    elif s[-1] == 's':
        if len(s) < 3:
            s = s
        elif s[-2] == s[-1]:
            s = s
        else:
            s = s[:-1]
    else:
        s = s
    
    return s 
        
def compare_dictionaries(d1, d2):
    """produces a score of similarity from comparing the two dictionaries"""
    if d1 == {}:
        return -50
    else:
        score = 0
    
    total = sum([d1[x] for x in d1])
    
    for words in d2:
        if words in d1:
            score += d2[words]*(math.log(d1[words]/total))
        else: 
            score += d2[words] * math.log(0.5/total)
            
    return score
        

class TextModel:
    def __init__(self, model_name):
        """constructs a new TextModel Object by accepting a string Model_Name as a parameter""" 
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.big_Words = {}
        

    def __repr__(self):
        """returns a string that includes the name of the model and sizes of the dictionary"""
        textName = "text model name: " + self.name + '\n'
        textName += "  number of words: " + str(len(self.words)) + "\n"
        textName += "  number of word lengths: " + str(len(self.word_lengths)) + '\n'
        textName += "  number of stems: " + str(len(self.stems)) + '\n'
        textName += "  number of sentence lengths: " + str(len(self.sentence_lengths)) + '\n'
        textName += "  number of big words: " + str(len(self.big_Words)) + "\n"
        return textName 
    
    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
       to all of the dictionaries in this text model.
       """
        tracker = 0
        for char in range(len(s)):
            if '!' in s[char] or '?' in s[char] or '.' in s[char]:
                sentenceCount = s[tracker:char]
                numWords = len(sentenceCount.split(' '))

                if numWords not in self.sentence_lengths:
                    self.sentence_lengths[numWords] = 1
                else:
                    self.sentence_lengths[numWords] += 1
            
                tracker = char + 2
                    
        word_list = clean_text(s)
        for w in word_list: 
            if w not in self.words:
                self.words[w] = 1
            else: 
                self.words[w] += 1
            wordLength = len(w)
            if wordLength in self.word_lengths:
                self.word_lengths[wordLength] += 1
            else:
                self.word_lengths[wordLength] = 1
    
        for w in word_list:
           w = stem(w) 
           if w not in self.stems:
               self.stems[w] = 1
           else:
               self.stems[w] += 1
               
        for w in word_list:
            if len(w) > 6 :
                if w not in self.big_Words:
                    self.big_Words[w] = 1
                else:
                    self.big_Words[w] += 1
               
    def add_file(self, filename):
        """adds all of the text in the file identfied by file name to the model"""
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read() 
        self.add_string(text)
        f.close()
        
    def save_model(self):    
        """saves the TextModel object self by writing its various feature dictionaries to files""" 
        f1 = open((self.name + '_' + 'words'), 'w')
        f2 = open((self.name + '_' + 'word_lengths'), 'w')
        f3 = open((self.name + '_' + 'stems'), 'w')
        f4 = open((self.name + '_' + 'sentence_lengths'), 'w')
        f5 = open((self.name + '_' + 'big_Words'), 'w')

        f1.write(str(self.words)) 
        f2.write(str(self.word_lengths))
        f3.write(str(self.stems))
        f4.write(str(self.sentence_lengths))
        f5.write(str(self.big_Words))
        
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()
    
    def read_model(self):
        """reads stored dictionaries for TextModel object from their files and assigns them to the attributes of TextModel"""
        f1 = open((self.name + '_' + 'words'), 'r')
        words_str = f1.read()
        f1.close()
        words = dict(eval(words_str))
        self.words = words
            
        f2 = open((self.name + '_' + "word_lengths"), 'r')
        word_lengths_str = f2.read()
        f2.close()
        word_lengths = dict(eval(word_lengths_str))
        self.word_lengths = word_lengths
        
        f3 = open((self.name + '_' + "stems"), 'r')
        stems_str = f3.read()
        f3.close()
        stems = dict(eval(stems_str))
        self.stems = stems
        
        f4 = open((self.name + '_' + "sentence_lengths"), 'r')
        sentence_lengths_str = f4.read()
        f4.close()
        sentence_length = dict(eval(sentence_lengths_str))
        self.sentence_lengths = sentence_length
        
        f5 = open((self.name + '_' + "big_Words"), 'r')
        big_Words_str = f5.read()
        f5.close()
        big_Words= dict(eval(big_Words_str))
        self.big_Words = big_Words
    
    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores measuring the
        smiliarity of self and other - one score for each of the features"""
        list_Scores = []
        
        word_Scores = compare_dictionaries(other.words, self.words)
        word_LengthScores = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_Scores = compare_dictionaries(other.stems, self.stems)
        sentence_LengthScores = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        bigWord_Scores = compare_dictionaries(other.big_Words, self.big_Words)
        
        list_Scores += [word_Scores] + [word_LengthScores] + [stem_Scores] + [sentence_LengthScores] + [bigWord_Scores] 
        return list_Scores
        
    def classify(self, source1, source2):
        """compares the object, self, with two other source objects and determines
        which is more likely to be the source of the called TextModel"""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        count1 = 0
        count2 = 0
        for test in range(len(scores1)):
            if scores1[test] > scores2[test]:
                count1 += 1
            elif scores1[test] < scores2[test]:
                count2 += 1
        
        if count1 > count2:
            print(source1, "Source 1 is more likely to come from ", self.name)
        else:
            print(source2, "Source 2 is more likely to come from ", self.name)
    
    

def test():
    """ Comparing the 4 scores from the 4 essays that were calculated 
    using function classify against the two source texts from J.K rowling and 
    Shakespeare
    """
        
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
    
    
    source1 = TextModel('rowling')
    source1.add_file('sorcerers_stone.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('Shakespeare.txt')

    mystery = TextModel('Trauma Essay')
    mystery.add_file('Trauma Essay.txt')
    mystery.classify(source1, source2)
    
    mystery = TextModel('Advertising Essay')
    mystery.add_file('Advertising Impact Essay.txt')
    mystery.classify(source1, source2)
    
    mystery = TextModel('Ancient Greek Essay')
    mystery.add_file('Ancient World of Greece Essay.txt')
    mystery.classify(source1, source2)
    
    mystery = TextModel('Film Anaylsis Essay')
    mystery.add_file('Scene Analysis.txt')
    mystery.classify(source1, source2)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        