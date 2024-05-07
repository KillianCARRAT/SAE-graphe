import networkx as nx

chemin_fichier = "data.txt"
fic = open("dataTest.txt", "a")
Hollywood = nx.Graph()

with open(chemin_fichier, 'r') as f:
    for ligne in range(30):
        test = f.readline()
        tests = eval(test)
        for acteur in tests["cast"]:
            Hollywood.add_node(acteur)
        for acteur in tests["cast"]:
            for lien in tests["cast"]:
                if acteur != lien:
                    Hollywood.add_edge(acteur, lien)


for elem in Hollywood:
    print(Hollywood.adj[elem])

fic.close()
res = Hollywood.adj['[[Lillian Gish]]']
print("Ligne lue :")