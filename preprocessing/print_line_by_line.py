from os import system

with open('test_puzzles.txt', 'r') as f:
    text = f.readlines()

for i in filter(lambda s: s not in('', '\n'), text):
    print(i, end='')
    t = input(".")
