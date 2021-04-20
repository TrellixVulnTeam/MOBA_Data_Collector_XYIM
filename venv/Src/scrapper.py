
import re
from lxml import html
import random
import requests
from bs4 import BeautifulSoup

class Scrapper:
    def __init__(self, url):
        """ 1. Créer une liste de plusieurs User Agents (Un max de 5 est suffisant pour l'exemple)
            2. effectuer la rotation pour en choisir un aléatoirement à chaque requête
        """
        self.user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        ]
        self.headers = {'User-Agent': random.choice(self.user_agent_list)}
        self.url = url
        self.origin = url
        self.rank = 1

    ########
    #     RAJOUTER les fonctions définies dans les Excercises 1 et 2 ci dessous
    ######
    def get_response(self, timeout=10, max_retry=3):
        """
        1. Spécifier une valeur de timeout dans les paramètres de fonctions
        2. Utliser requests afin de procéder à la requeête en utilisant l'url du site web en question,
        le User Agent, et le time_out
        """
        lastException = None
        for _ in range(max_retry):
            try:
                response = requests.get(self.url, headers=self.headers, timeout=timeout)
                return response.text
            except Exception as e:
                lastException = e
        raise lastException

    def remove_white_spaces(self, x):
        """ Fonction qui enlève les espaces d'une string
        Exemple  ' hello ' > 'hello'
        """
        return x.strip()

    def get_soup(self, text_response):
        """Parser la page html en utilisant BeautifulSoup pour accèder facilement aux balises et leurs contenu"""
        soup = BeautifulSoup(text_response, "lxml")
        return soup

    def get_all_span(self, soup):
        """
        Extraire toutes les balises span de la page"""
        return [elt.text for elt in soup.findAll('span')]

    def get_all_className(self, soup):
        """
        Extraire toutes les balises class = "name" de la page"""
        return [elt.text for elt in soup.findAll(class_="name")]

    def get_all_server(self, soup):
        """
        Extraire toutes les balises class = "name" de la page"""
        #soup = soup.find_all("i", class_=False)
        return [elt.text for elt in soup.findAll("i", class_=False)]

    def get_all_classSummonerTier(self, soup):
        """
        Extraire toutes les balises class = "SummonerTier" de la page"""

        return [elt for elt in soup.findAll(class_="summonerTier")]

    def get_all_classTextCenter(self, soup):
        """
        Extraire toutes les balises class = "SummonerTier" de la page"""

        return [self.remove_white_spaces(elt.text) for elt in soup.findAll(class_="text-center")]

    def getName(self, soup):
        list = self.get_all_className(soup)
        list.remove('\n\n\n\n\n\n')
        return list

    def getServer(self, soup):
        list1 = self.get_all_server(soup)
        list2 = []
        for element in list1:
            if "(" not in element:
                list2.append(element)
        return list2

    def getStats(self, soup, number):
        list1 = [self.remove_white_spaces_split(elt.text) for elt in soup.findAll(class_="text-center")]
        list2 = []
        i = 0
        for element in list1:
            if i == 16 or i == 204:
                i = i + 1
            if i % 2 == 0 and i != 0:
                list2.append(element)
            i = i + 1
        if number == 1:
            return self.getElo(list2)
        elif number == 2:
            return self.getLP(list2)
        elif number == 3:
            return self.getWin(list2)
        elif number == 4:
            return self.getWinRate(list2)

    def getElo(self,list1):
        list2 = []
        for element in list1:
            if element:
                list2.append(element[0])
        return list2

    def getLP(self,list1):
        list2 = []
        for element in list1:
            if element:
                list2.append(element[1])
        return list2

    def getWin(self,list1):
        list2 = []
        for element in list1:
            if element:
                list2.append(element[4])
        return list2

    def getWinRate(self,list1):
        list2 = []
        for element in list1:
            if element:
                list2.append(self.remove_parenthese_strip(element[5]))
        return list2

    def remove_white_spaces_split(self, sentence):
        return sentence.split()

    def remove_parenthese_strip(self, sentence):
        return sentence.strip('()%')

    def remove_white_spaces_split(self, sentence):
        return sentence.split()


    def extract_sitemap(self, soup):
        sitemapTags = soup.find_all("sitemap")
        xmlDict = {}
        for sitemap in sitemapTags:
            xmlDict[sitemap.findNext("loc").text] = sitemap.findNext('lastmod').text

            """"import json
                 with open('result.json', 'w') as fp:
                     json.dump(xmlDict, fp)"""
        return xmlDict

    def extract_page(self):
        response = self.get_response()
        soup = self.get_soup(response)

        resultat = {
            'Name': self.getName(soup),
            'Server': self.getServer(soup),
            'Elo': self.getStats(soup,1),
            'LP': self.getStats(soup,2),
            'Win': self.getStats(soup,3),
            'Win%': self.getStats(soup,4)

        }

        data = []

        for i in range(0, len(resultat['Name'])):
            Player = {
                'Rank' : self.rank,
                'Server' : resultat['Server'][i],
                'Name' : resultat['Name'][i],
                'Elo' : resultat['Elo'][i],
                'LP': resultat['LP'][i],
                'Win': resultat['Win'][i],
                'Win%': resultat['Win%'][i]
            }
            self.rank += 1
            data.append(Player)

        return data

    def extract_pages_bulk(self, number, regions_list=None):
        concatenated_data = []

        if regions_list is not None:
            response = self.get_response()
            tree = html.fromstring(response)
            urls = [ul.xpath("li/a/@href") for ul in tree.xpath(regions_list)][0]
            for url in urls:
                #print(url)
                url_elements = url.split('/')
                if len(url_elements) < 4:
                    continue
                self.url = self.origin + '/' + url_elements[len(url_elements)-1]
                print(self.url)
                concatenated_data += self.iterate_pages(number)
            return concatenated_data

        concatenated_data = self.iterate_pages(number)

        return concatenated_data

    def iterate_pages(self, number_of_pages):
        concatenated_data = []
        for i in range(0, number_of_pages):
            data = self.extract_page()
            if(len(data) == 0):
                break
            concatenated_data += data
            #print(self.url)
            #print(data[len(data)-1])
            self.next_page()

        return concatenated_data


    def next_page(self):
        length = len(self.url)
        offset = 0
        trailing_number = []

        while(self.url[length-1-offset].isdigit()):
            trailing_number.append(self.url[length-1-offset])
            offset += 1

        indicator = self.url[length-5-offset:length-offset]

        if indicator == "page-":
            trailing_number.reverse()
            num_to_add = int(''.join(trailing_number)) + 1
            newurl = self.url[:length-offset] + str(num_to_add)
            self.url = newurl
        else :
            self.url += "/page-2"