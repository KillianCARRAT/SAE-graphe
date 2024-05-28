import networkx as nx
import matplotlib.pyplot as plt
import re


def json_vers_nx(nom_fichier):
    Hollywood = nx.Graph()

    with open(nom_fichier, 'r') as f:
        cpt = 0
        while f.readline():
            cpt += 1
        f.close()

    with open(nom_fichier, 'r') as f:
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
    return Hollywood

Hollywood = json_vers_nx("jeux de données réduits-20240507/data.txt")

def collaborateur_commun(G,u,v):
    """Fonction renvoyant l'ensemble des acteurs en commun entre u et v. La fonction renvoie None si u ou v est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        v: le sommet de départ

    """
    if u not in G.nodes or v not in G.nodes:
        print(u, 'ou',v,"sont des illustres inconnus")
        return None
    res = set()
    collaborateur = G.adj[u]
    for colla in G.adj[v]:
        if colla in collaborateur:
            res.add(colla)
    return res


def collaborateurs_proches(G,u,k):
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
    """
    if u not in G.nodes:
        print(u,"est un illustre inconnu")
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return collaborateurs




def distance_entre_deux(G,u,v):
    if u not in G.nodes or v not in G.nodes:
        print(u, 'ou',v,"sont des illustres inconnus")
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    i = 0
    for i in range(len(G.nodes)):
        i+=1
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin == v:
                    return i
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    print('ils ne se connaissent pas')
    return None

print(collaborateur_commun(Hollywood,"Larry Mitchell","Riley Keough"))

print(collaborateurs_proches(Hollywood,"James Mapes",1))

print(distance_entre_deux(Hollywood,"James Mapes","Holly Hunter"))



print(len(Hollywood.nodes()))