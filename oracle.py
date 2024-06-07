import requetes

# Ici vos fonctions dédiées aux interactions

# ici votre programme principal
def programme_principal():

    # Demande du jeu de données à utilisée
    cpt = 0
    test = 0
    while True:
        graphe_test = input("Quelle jeu de donner voulez-vous tester? 100 - 1000 - 10000 - plus : ")
        if graphe_test ==  "100":
            G = requetes.json_vers_nx("data_100.txt")
            test=1
            break
        elif graphe_test == "1000":
            G = requetes.json_vers_nx("data_1000.txt")
            test=2
            break
        elif graphe_test == "10000":
            G = requetes.json_vers_nx("data_10000.txt")
            test=3
            break
        elif graphe_test == "plus":
            print("La création du graphe peux prendre un peu de temps. Veuillez patienter.")
            G = requetes.json_vers_nx("data.txt")
            test=4
            break


    while True:
        autre_inf = int(input("Que voulez-vous savoir :\n1 : Les acteurs en commun entre deux acteurs,\n2 : Les acteurs à une certaine distance d'un acteur,\n3 : Savoir si deux acteurs sont proches,\n4 : A quels distance sont deux acteurs,\n5 : La centralité d'un acteur,\n6 : Le nom de l'acteur le plus au centre d'Hollywood,\n7 : La distance maximal entre les deux acteurs les plus éloignés?\n (Donner un nombre lier à la question souhaitée) : "))
        if autre_inf == 1:
            acteur1 = input("Quel acteur voulez-vous comparer ? (1 acteur)")
            acteur2 = input("Avec qui ? (1 acteur)")
            res = requetes.collaborateurs_communs(G, acteur1, acteur2)
            print("Les acteurs en commun entre ", acteur1, " et ", acteur2, " sont ", res,".")

        elif autre_inf == 2:
            acteur1 = input("Quel acteur voulez-vous consulter ? ")
            dis = input("Quel a quelle distance voulez-vous consulter? ")
            res = requetes.collaborateurs_proches(G, acteur1, dis)
            print("Les acteurs à une distance de ", dis, " de ", acteur1, " sont", res,".")

        elif autre_inf == 3:
            acteur1 = input("De quel acteur voulez-vous savoir si ils sont voisins ? (1 acteur)")
            acteur2 = input("Avec qui ? (1 acteur)")
            res = requetes.est_proche(G, acteur1, acteur2)
            if res:
                print("Les acteurs", acteur1, acteur2, " sont voisins.")
            else:
                print("Les acteurs", acteur1, acteur2, " ne sont pas voisins.")

        elif autre_inf == 4:
            acteur1 = input("De quel acteur voulez-vous avoir sa distance ? (1 acteur)")
            acteur2 = input("Avec qui ? (1 acteur)")
            res = requetes.distance(G, acteur1, acteur2)
            print("La distance entre ", acteur1, " et ", acteur2, " est de ", res,".")

        elif autre_inf == 5:
            acteur1 = input("De quel acteur voulez-vous avoir sa centralite ? (1 acteur)")
            res = requetes.centralite(G, acteur1)[0]
            print("La centralité de ", acteur1, " est de ", res,".")

        elif autre_inf == 6:
            res = requetes.centre_hollywood(G)

            if test > 1:
                print("Le test prend trop de temps à être effectué. Il n'est pas possible de le faire.")
            else:
                print("L'acteur  centre de Hollywood est ", res,".")
        
        elif autre_inf == 7:
            res = requetes.eloignement_max(G)
            print("Cela peut prendre un peu de temps à être effectué.")
            print("La distance maximale entre deux acteurs est de ", res,".")
        
        continu = str(input("Voulez-vous une nouvelle réponse question?(O/N)"))
        if continu != "O" and continu != "o":
            break


programme_principal()
