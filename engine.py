from flask import Flask, redirect, url_for, request,render_template
import nltk
import re
import heapq
import math
import os
import webbrowser
nltk.download('stopwords')
nltk.download('punkt')
stop_words=nltk.corpus.stopwords.words('english')

app = Flask(__name__) 
  
@app.route('/success/<name>') 
def success(name): 
   return  render_template('summarized.html',name=name) 
  
@app.route('/Summarizer',methods = ['POST', 'GET']) 
def login(): 
   if request.method == 'POST': 
      text = request.form['original_text'] 
      return redirect(url_for('success',name = create_summary(text))) 
   else: 
      text = request.form['original_text'] 
      return redirect(url_for('success',name = create_summary(text)))
  
def create_summary(text):
    corpus=text.lower().split('.')
    formatted_text=re.sub(r'\[[0-9]*\]',' ',str(corpus))
    formatted_text=re.sub(r'\s+',' ',str(corpus))
    formatted_text=re.sub('[^a-zA-Z]',' ',str(corpus))
    formatted_text=re.sub('\s+',' ',str(formatted_text))
    sentence_list=nltk.sent_tokenize(str(text))
    words_freq=word_frequency(formatted_text)
    max_freq=max(words_freq.values())
    #weight finding
    for word in words_freq.keys():
        words_freq[word]=(words_freq[word]/max_freq)
    score=compute_score(sentence_list,words_freq)
    #summary
    summary_sentence=heapq.nlargest(math.ceil(len(corpus)*0.15),score,key=score.get)
    summary=' '.join(summary_sentence)
    return summary


def word_frequency(formatted_text):
    #freq finding
    words_freq={}
    for word in nltk.word_tokenize(formatted_text):
        if word not in stop_words:
            if word not in words_freq.keys():
                words_freq[word]=1
            else:
                words_freq[word]+=1    
    return words_freq

def compute_score(sentence_list,words_freq):
    sentence_score={}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in words_freq.keys():
                if len(sent.split(' '))<30:
                    if sent not in sentence_score.keys():
                        sentence_score[sent]=words_freq[word]
                    else:
                        sentence_score[sent]+=words_freq[word]
    return sentence_score

if __name__ == '__main__':
   webbrowser.open(os.getcwd()+'\web\Summarizer.html')
   app.run(debug = True) 