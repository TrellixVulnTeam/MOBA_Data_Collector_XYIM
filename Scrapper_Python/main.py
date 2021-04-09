import re
import random
import requests


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


def clean_html_string(self, raw_html):
    """Fonction enlève les caractères spéciaux d'une string
       Exemple : '<> Ca va ?!' > 'Ca va'
       """
    cleanr = re.compile('<.*?>')  # cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def extract_domain_name(self):
    """ Fonction qui extrait le nom de domaine
    Exemple 'http://www.lemonde.fr/accueil' > 'www.lemonde.fr'
    """
    m = re.search('https?://([A-Za-z_0-9.-]+).*', self.url)
    if m:
        return m.group(1)


def get_soup(self, text_response):
    """Parser la page html en utilisant BeautifulSoup pour accèder facilement aux balises et leurs contenu"""
    soup = BeautifulSoup(text_response, "lxml")
    return soup


def get_title(self, soup):
    """
    Extraire le tire de la page"""
    return soup.find('title').text


def get_all_h1(self, soup):
    """
    Extraire toutes les balises h1 de la page"""
    return [elt.text for elt in soup.findAll('h2')]


def get_imagelinks(self, soup):
    """ Extraire les images visibles dans l'url"""
    try:
        return [elt['src'] for elt in soup.findAll('img') if elt.get('src')]
    except:
        return []


def tag_visible(self, element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    return True


def get_main_text(self, soup):
    """
    Extraire le texte principal sur la page"""
    texts = soup.findAll(text=True)
    visible_texts = filter(self.tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def get_out_links(self, soup):
    """ Extraire tous les liens sortants"""
    links_list = [elt['href'] for elt in soup.findAll('a')]
    return [elt for elt in links_list if not elt.startswith(self.extract_domain_name(self.url))]


def extract_sitemap(self, soup):
    sitemapTags = soup.find_all("sitemap")
    xmlDict = {}
    for sitemap in sitemapTags:
        xmlDict[sitemap.findNext("loc").text] = sitemap.findNext('lastmod').text

        """"import json
             with open('result.json', 'w') as fp:
                 json.dump(xmlDict, fp)"""
    return xmlDict


def get_sitemap_json(self):
    domain = self.extract_domain_name()
    urls = ['http://' + domain + '/' + term for term in ['sitemap.xml', 'sitemap1.xml', 'sitemap_index.xml']]
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = self.get_soup(response.text)
            sm = self.extract_sitemap(soup)
            return sm
    return None


def main(self):
    """
    1. Appeler la méthode qui va requeter le site en question avec les bons paramètres
    2. Appeler la méthode pour la création de l'objet soup avec les bons paramètres
    3. Retourner l'objet résultat qui contient les différents éléments de la page
    ( en utilisant toutes les fonctions développées dans la classe ci-dessus)
    """
    response = self.get_response()
    soup = self.get_soup(response)
    resultat = {
        'domain_name': self.extract_domain_name(),
        'title': self.get_title(soup),
        'url': self.url,
        'images': self.get_imagelinks(soup)[:2],
        'h2': self.get_all_h1(soup)

    }
    sitemap = self.get_sitemap_json()
    return resultat

# 1. Instancier la classe scrapper avec l'url à scrapper
s = Scrapper("http://www.esiee.fr/")
#print(s.get_response())
# 2. Executer la méthode principale de la classe afin d'obtenir les résultats voulus
print(s.main())