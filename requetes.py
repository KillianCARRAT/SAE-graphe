import networkx as nx
import matplotlib.pyplot as plt
import re

def json_vers_nx(nom_fichier):
    Hollywood = nx.Graph()

    with open(nom_fichier, 'r') as f:
        for line in f:
            tests = eval(line)

            for actor in tests["cast"]:
                stringAc = re.sub(r"[\[\]]", "", actor).split("|")[-1]
                Hollywood.add_node(stringAc)


            for actor in tests["cast"]:
                for other_actor in tests["cast"]:
                    if actor != other_actor:
                        stringAc = re.sub(r"[\[\]]", "", actor).split("|")[-1]
                        stringLi = re.sub(r"[\[\]]", "", other_actor).split("|")[-1]
                        Hollywood.add_edge(stringAc, stringLi)

    return Hollywood

Hollywood = json_vers_nx("jeux de données réduits-20240507/data.txt")

def collaborateurs_communs(G,u,v):
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

def est_proche(G,u,v,k=1):
    return v in collaborateurs_proches(G,u,k)


def distance(G,u,v):
    if u not in G.nodes or v not in G.nodes:
        print(u, 'ou',v,"sont des illustres inconnus")
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    for j in range(len(G.nodes)):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin == v:
                    return j
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    print('ils ne se connaissent pas')
    return None


print(collaborateurs_communs(Hollywood,"James Mapes","Burt Richards"))


print(collaborateurs_proches(Hollywood,"James Mapes",1))

print(distance(Hollywood,"James Mapes","Holly Hunter"))

def centralite(G,u):
    if u not in G.nodes:
        print(u,"est un illustre inconnu")
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    for i in range(len(G.nodes)):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        if len(collaborateurs_directs)==0:
            return i    
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return None


