import networkx as nx
import json
import matplotlib.pyplot as plt
import re
import time

def json_vers_nx(nom_fichier):
    """_summary_

    Args:
        nom_fichier (_type_): _description_

    Returns:
        _type_: _description_
    """
    Hollywood = nx.Graph()

    with open(nom_fichier, 'r', encoding="utf-8") as f:
        for line in f:
            tests = json.loads(line)  # Use json.loads instead of eval

            # Create a set of actors
            actors = {re.sub(r"[\[\]]", "", actor).split("|")[-1] for actor in tests["cast"]}
            
            # Add nodes (actors) to the graph
            Hollywood.add_nodes_from(actors)

            # Add edges between every pair of actors in the cast
            for actor in actors:
                for other_actor in actors:
                    if actor != other_actor:
                        Hollywood.add_edge(actor, other_actor)

    return Hollywood

start = time.time()
Hollywood = json_vers_nx("jeux de données réduits-20240507/data.txt")
end = time.time()
print(end - start)

def collaborateurs_communs(G,u,v):
    """Fonction renvoyant l'ensemble des acteurs en commun entre u et v. La fonction renvoie None si u ou v est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        v: le sommet d'arriver

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
    """Fonction renvoyant True si u et v sont voisine. La fonction renvoie None si u ou v est absent du graphe.
    

    Args:
        G: le graphe
        u: le sommet de départ
        v: le sommet d'arriver
        k:la distance depuis u Defaults to 1
    """
    return v in collaborateurs_proches(G,u,k)


def distance(G,u,v):
    """_summary_

    Args:
        G: le graphe
        u: le sommet de départ
        v: le sommet d'arriver

    Returns:
        _type_: _description_
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
    """_summary_

    Args:
        G: le graphe
        u: le sommet de départ

    Returns:
        _type_: _description_
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



def centre_hollywood(G):
    """_summary_

    Args:
        G: le graph

    Returns:
        _type_: _description_
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


def eloignement_max(G):
    """_summary_

    Args:
        G: le graph

    Returns:
        _type_: _description_
    """
    name = ""
    maximum = None
    for node in G.nodes():
        stock = centralite(G, node)
        if maximum is None or stock >maximum:
            name = node
            maximum = stock
    return name


start = time.time()
print(centralite(Hollywood,"Leonardo DiCaprio"))
end = time.time()
print(end-start)



start = time.time()
#print(eloignement_max(Hollywood))
end = time.time()
print(end-start)


