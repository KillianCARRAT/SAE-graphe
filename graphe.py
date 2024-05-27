import networkx as nx
import matplotlib.pyplot as plt
import re



chemin_fichier = "jeux de données réduits-20240507/data_100.txt"
fic = open("dataTest.txt", "a")
Hollywood = nx.Graph()

cpt = sum(1 for _ in chemin_fichier)

with open(chemin_fichier, 'r') as f:
    for i in range(cpt):
        test = f.readline()
        tests = eval(test)


        for acteurs in tests["cast"]:
            string = re.sub("[[]", "", acteurs)
            s1 = re.sub("[]]", "", string)
            if "|" in s1:
                stock = s1.split("|")
                stringAc = stock[1]
            else:
                stringAc = s1
            Hollywood.add_node(stringAc)


        for acteur in tests["cast"]:
            for lien in tests["cast"]:
                if acteur != lien:
                    stringAc = re.sub("[[]", "", acteur)
                    stringAc2 = re.sub("[]]", "", stringAc)
                    stringLi = re.sub("[[]", "", lien)
                    stringLi2 = re.sub("[]]", "", stringLi)

                    if "|" in stringAc2:
                        stock = stringAc2.split("|")
                        stringAcAjoute = stock[1]
                    else:
                        stringAcAjoute = stringAc2

                    if "|" in stringLi2:
                        stock = stringLi2.split("|")
                        stringLiAjoute = stock[1]
                    else:
                        stringLiAjoute = stringLi2
                    Hollywood.add_edge(stringAcAjoute, stringLiAjoute)
                    #print(stringAc, stringLi)

fic.close()
#res = Hollywood.adj['[[Richard Kiley]]']
#print("Ligne lue :", res)