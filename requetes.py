import time
import networkx as nx
import json
import matplotlib.pyplot as plt
import re

def json_vers_nx(nom_fichier):
    """Transforme un fichier de format JSON sous format .txt en graphe.

    Args:
        nom_fichier (str) : chemin d'accès au fichier JSON.

    Returns:
        Graph : retourne un graphique de l'ensemble des acteurs du fichier.
    """
    Hollywood = nx.Graph()

    with open(nom_fichier, 'r', encoding="utf-8") as f:
        for line in f:
            tests = json.loads(line)

            actors = {re.sub(r"[\[\]]", "", actor).split("|")[-1] for actor in tests["cast"]}

            Hollywood.add_nodes_from(actors)

            for actor in actors:
                for other_actor in actors:
                    if actor != other_actor:
                        Hollywood.add_edge(actor, other_actor)

    return Hollywood

def collaborateurs_communs(G,u,v):
    """Fonction renvoyant l'ensemble des acteurs en commun entre u et v. 
    La fonction renvoie None si u ou v est absent du graphe.
    
    Parametres:
        G : le graphe
        u : le sommet de départ
        v : le sommet d'arriver

    Returns:
        set : ensemble des acteurs en commun entre u et v.
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
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe. 
    La fonction renvoie None si u est absent du graphe.
    
    Parametres:
        G : le graphe
        u : le sommet de départ
        k : la distance depuis u

    Returns:
        set : ensemble des acteurs à distance au plus k de l'acteur u.
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
    """Fonction renvoyant True si u et v sont voisine.
    La fonction renvoie None si u ou v est absent du graphe.
    

    Args:
        G : le graphe
        u : le sommet de départ
        v : le sommet d'arriver
        k:la distance depuis u Defaults to 1

    Returns:
        bool : True si u et v sont voisine.
    """
    return v in collaborateurs_proches(G,u,k)

def distance(G,u,v):
    """Donne la distance entre les deux acteurs dans le graphe. 

    Args:
        G : le graphe
        u : le sommet de départ
        v : le sommet d'arriver

    Returns:
        int : la distance entre les deux acteurs.
    """
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
                    return j+1
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    print('ils ne se connaissent pas')
    return None

def distance_naive(G,u,v):
    """Donne la distance entre les deux acteurs dans le graphe. 
    Args:
        G : le graphe
        u : le sommet de départ
        v : le sommet d'arriver
    Returns:
        int : la distance entre les deux acteurs.
    """
    if u not in G.nodes or v not in G.nodes:
        print(u, 'ou',v,"sont des illustres inconnus")
        return None
    for i in range(len(G.nodes)):
      if v in collaborateurs_proches(G,u,i):
          return i
    print('ils ne se connaissent pas')
    return None

def centralite(G,u):
    """Donne la centralité d'un acteur dans le graphe. 

    Args:
        G : le graphe
        u : le sommet de départ

    Returns:
        int : donne ça distance avec l'acteur le plus loin de lui.
    """
    if u not in G.nodes:
        print(u,"est un illustre inconnu")
        return None
    deja_vue = set()
    deja_vue.add(u)
    collaborateurs = set()
    collaborateurs.add(u)
    for i in range(len(G.nodes)):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in deja_vue:
                    collaborateurs_directs.add(voisin)
        if len(collaborateurs_directs)==0:
            return i
        collaborateurs = collaborateurs_directs
        deja_vue = deja_vue.union(collaborateurs_directs)
    return None


def centre_hollywood_generale(G):
    """Cherche le nom de l'acteur le plus central dans le graphe.
    Args:
        G : le graphe
    Returns:
        str : le nom de l'acteur le plus central.
    """
    name = ""
    minimum = None
    for node in G.nodes():
        if len(G.adj[node]) > 1:
            stock = centralite(G, node)
            if minimum is None or stock < minimum:
                name = node
                minimum = stock
    return name


def centre_hollywood(G):
    """Cherche le nom de l'acteur le plus central dans le graphe.
    si le graph corespond a celui de la SAE 
    Args:
        G : le graphe
    Returns:
        str : le nom de l'acteur le plus central.
    """
    name = ""
    minimum = None
    for node in G.nodes():
        if len(G.adj[node]) > 1:
            if distance(G,node,"Al Pacino") is not None : ### pour verifier que node est dans le graph principale 
                 stock = centralite(G, node)
                 if minimum is None or stock < minimum:
                    name = node
                    minimum = stock
    return name

def centraliteForEloignementMax(G,u):
    """Donne la centralité d'un acteur dans le graphe. 

    Args:
        G : le graphe
        u : le sommet de départ

    Returns:
        tuple : donne ça distance avec l'acteur le plus loin de lui (int) et le nom de l'acteur le plus loin de lui (str).
    """
    if u not in G.nodes:
        print(u,"est un illustre inconnu")
        return None
    deja_vue = set()
    deja_vue.add(u)
    collaborateurs = set()
    collaborateurs.add(u)
    for i in range(len(G.nodes)):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in deja_vue:
                    collaborateurs_directs.add(voisin)
        if len(collaborateurs_directs)==0:
            return i, c
        collaborateurs = collaborateurs_directs
        deja_vue = deja_vue.union(collaborateurs_directs)
    return None

def eloignement_max(G):
    """Cherche la distance maximale entre deux acteurs dans le graphe.

    Args:
        G : le graphe

    Returns:
        int : distance maximale entre deux acteurs.
    """
    res = []
    compteur = 0
    for name in G.nodes:
        _, nom = centraliteForEloignementMax(G, name)
        distance, _ = centraliteForEloignementMax(G, nom)
        res.append(distance)
        if compteur > 4:
            break
        compteur +=1
    
    return max(res)
