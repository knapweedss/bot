# обучение марковской модели
with open('mark.txt', encoding ='UTF-8') as f:
    file = f.read()
    text = file.split()
import markovify
m = markovify.Text(file)