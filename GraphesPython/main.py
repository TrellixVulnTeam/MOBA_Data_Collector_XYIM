import matplotlib.pyplot as plt
import numpy as np


def chall_by_server_world_pie(tab):
    name = ['BR', 'EUNE', 'EUW', 'JP', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR']
    BR = int(tab[0])
    EUNE = int(tab[1])
    EUW = int(tab[2])
    JP = int(tab[3])
    KR = int(tab[4])
    LAN = int(tab[5])
    LAS = int(tab[6])
    NA = int(tab[7])
    OCE = int(tab[8])
    RU = int(tab[9])
    TR = int(tab[10])

    data = [BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, RU, TR]

    explode = (0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15)
    plt.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.axis('equal')
    #plt.show()
    plt.savefig('image_graphe/chall_by_server_world_pie.png')



def number_server_pie(tab):
    name = ['Challenger', 'GrandMaster', 'Master', 'Diamond', 'Platinum']
    Challenger = int(tab[0])
    GrandMaster = int(tab[1])
    Master = int(tab[2])
    Diamond = int(tab[3])
    Platinum = int(tab[4])

    data = [Challenger, GrandMaster, Master, Diamond, Platinum]

    explode = (0.15, 0.15, 0.15, 0.15, 0.15)
    plt.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.axis('equal')
    #plt.show()
    plt.savefig('image_graphe/chall_by_server_world_pie.png')

def number_server_hist(tab):
    x = np.arange(5)
    plt.bar(x, height=[int(tab[0]), int(tab[1]), int(tab[2]), int(tab[3]), int(tab[4])])
    plt.xticks(x, ['Challenger', 'GrandMaster', 'Master', 'Diamond', 'Platinum'])
    #plt.show()
    plt.savefig('image_graphe/chall_by_server_world_pie.png')


def chall_by_server_world_hist(tab):
    x = np.arange(11)
    plt.bar(x, height=[int(tab[0]), int(tab[1]), int(tab[2]), int(tab[3]), int(tab[4]), int(tab[5]), int(tab[6]),
                       int(tab[7]), int(tab[8]), int(tab[9]), int(tab[10])])
    plt.xticks(x, ['BR', 'EUNE', 'EUW', 'JP', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR'])
    #plt.show()
    plt.savefig('image_graphe/chall_by_server_world_pie.png')


if __name__ == '__main__':
    tab = ['100', '70', '60', '45', '0', '5', '40', '85', '45', '78', '46']
    chall_by_server_world_pie(tab)
