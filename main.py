from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication
from App_UI import Ui_MainWindow
from bs4 import BeautifulSoup
from random import shuffle
import requests

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(lambda: self.manualAdd())
        self.ui.saveToFile.clicked.connect(lambda: self.antsWrite())
        self.ui.verbsList.itemSelectionChanged.connect(lambda: self.selectionItem())
        self.ui.loadFromFile.clicked.connect(lambda: self.antsRead())
        self.antonymList = {}
        self.ui.verbsList.addItems(self.antonymList)
        self.ui.delButton.clicked.connect(lambda: self.delAnt())
        self.ui.clearAll.clicked.connect(lambda: self.clearall())
        self.ui.verbSearchButton.clicked.connect(lambda: self.findAnt())
        self.ui.interLoad.clicked.connect(lambda: self.fullParse())
        self.ui.intSearchButton.clicked.connect(lambda: self.parse(self.ui.verbSearch.text()))

    def selectionItem(self):
        try:
            self.ui.antonym.setText(self.antonymList.get(self.ui.verbsList.currentItem().text()))
        except Exception as e:
            print(e)

    def delAnt(self):
        try:
            self.antonymList.pop(self.ui.verbsList.currentItem().text())
            self.ui.verbsList.clear()
            self.ui.verbsList.addItems(self.antonymList)
        except Exception as e:
            print(e)

    def antsWrite(self, filename='antonyms.txt'):
        try:
            with open(filename, 'w') as ants:
                for x in self.antonymList:
                    ants.write(f'{x}:{self.antonymList[x]}\n')
        except Exception as e:
            print(e)

    def antsRead(self, filename='antonyms.txt'):
        try:
            with open(filename, 'r') as ants:
                for elem in ants:
                    verb, ant = elem.strip('\n').split(':')
                    self.antonymList[verb.title()] = ant.title()
            self.ui.verbsList.clear()
            self.ui.verbsList.addItems(self.antonymList)
        except Exception as e:
            print(e)

    def findAnt(self):
        try:
            items = self.ui.verbsList.findItems(self.ui.verbSearch.text().title(), Qt.MatchExactly)
            for item in items:
                self.ui.verbsList.setCurrentItem(item)
                self.ui.antonym.setText(self.antonymList.get(item.text()))
                pass
        except Exception as e:
            print(e)

    def clearall(self):
        try:
            self.ui.verbsList.clear()
            self.antonymList.clear()
            self.ui.antEntry.clear()
            self.ui.verbSearch.clear()
            self.ui.antonym.clear()
            self.ui.verbEntry.clear()
        except Exception as e:
            print(e)

    def manualAdd(self):
        try:
            verb = self.ui.verbEntry.text().title()
            ant = self.ui.antEntry.text().title()
            if len(verb) > 1 or len(ant) > 1:
                self.antonymList[verb.title()] = ant
                self.ui.verbsList.addItem(verb)
            else:
                pass
        except Exception as e:
            print(e)

    def parse(self, verb):
        try:
            url = f'https://antonimy.ru/{verb[0]}/{verb}'
            api = requests.get(url)
            content = api.text
            soup = BeautifulSoup(content, 'html.parser')
            if soup.h1.get_text() != 'Страница не найдена! :(':
                self.ui.antonym.setText(soup.li.get_text())
            else:
                pass
        except Exception as e:
            print(e)

    def fullParse(self):
        url = 'https://russkiiyazyk.ru/leksika/antonimy-primery-slov.html'
        ants = []
        try:
            api = requests.get(url)
            content = api.text
            soup = BeautifulSoup(content, 'html.parser')
            for i in soup.find_all("li"):
                if '—' in i.get_text():
                    ants.append(i.get_text().strip(';.'))
            ants = ants[::-1]
            del ants[0:23]
            shuffle(ants)
            for x in ants:
                verb, ant = x.replace('\xad', "").replace(' ', "").split('—')
                self.antonymList[verb.title()] = ant.title()
                self.ui.verbsList.addItem(verb.title())
            print(len(self.antonymList))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        app = QApplication([])
        window = MainWindow()
        window.show()
        app.exec_()
    except Exception as e:
        print('Something went wrong, i can feel it', e)