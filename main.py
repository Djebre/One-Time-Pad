# Schalss Martin
import getopt
import os
import secrets
import sys
from pathlib import Path


def main(argv):
    # On recupère les paramètres ainsi que les arguments
    try:
        MS_opts_SM, MS_args_SM = getopt.getopt(argv, "h")
    except getopt.GetoptError as MS_err_SM:
        print("Erreur,", MS_err_SM)
        usage()
        sys.exit(2)
    for MS_opt_SM, MS_arg_SM in MS_opts_SM:
        # Appelle de la fonction d'aide si -h
        if MS_opt_SM in "-h":
            fhelp()
            sys.exit()
    if MS_args_SM:
        # Verification des arguments en entrees
        validargs(argv)
        #Execution en fonction des arguments
        action(argv)
        sys.exit()
    usage()
    sys.exit(2)


def fhelp():
    print("\n- - - - - - - - - - - - - PAGE D'AIDE - - - - - - - - - - - - - - - ")
    print("Voici la page d'aide sur le script de chiffrement One-Time-Pad.")
    print("Il existe differentes options de lancement pour ce script :")
    print("\n   - - - - - - - - - OPTIONS DE LANCEMENT - - - - - - - - - ")
    print("\t- \"-h\" affiche cette page d'aide.")
    print("\n   - - - - - - - - - PARAMETRES DISPONIBLES - - - - - - - -")
    print("\t~ main.py [MODE] [FICHIER] (1[PAD]) (0[SORTIE_CHIFREE]) ")
    print("\t[MODE]")
    print("\t   - 0 Chiffrement d'un fichier entre en paramètre, avec ou sans un paramètre de MS_sortie_SM. Le fichier contenant les PAD est genere automatiquement à l'emplacement liste_PAD.txt.")
    print("\t   - 1 Dechiffrement d'un fichier entre en paramètre.")
    print("\t[FICHIER]")
    print("\t   - Chemin du fichier à chiffrer / dechiffrer.")
    print("\t[PAD]")
    print("\t   - Chemin du fichier contenant les cles associees à chaque non de fichier (Si MS_mode_SM 1).")
    print("\t[SORTIE_CHIFREE]")
    print("\t   - chemin indiquant le fichier qui sera cre par le programme et contiendra le resultat de l’execution (Si MS_mode_SM 0).")
    print("\t   Par defaut \"[nom_fichier]_sortie_chiffree\".")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")


def usage():
    print("Usage: main.py [MODE] [FICHIER] (1[PAD]) (0[SORTIE_CHIFREE])")
    print("Utilisez \"main.py -h\" pour afficher l'aide.")


def validargs(MS_args_SM):
    if len(MS_args_SM) > 3 or len(MS_args_SM) < 2:      # Si il y a trop ou pas assez d'arguments, alors..
        print("Erreur, mauvais nombre de paramètres")   # On affiche une erreur
        usage()
        sys.exit(2)

    if MS_args_SM[0] == "0" or MS_args_SM[0] == "1":    # Si le mode est bien "0" ou "1", alors..
        if MS_args_SM[0] == "0":                        # Si le mode est "0"
            if len(MS_args_SM) < 3:                     # Et si le nombre d'argument > 3
                MS_sortie_SM = MS_args_SM[1] + "_" +"sortie_chiffree.txt"    # Le chemin de sortie est choisi automatiquement
            else:
                MS_sortie_SM = MS_args_SM[-1]           # Sinon il prend le nom du dernier argument de la commande
        else:
            MS_sortie_SM = ""                           # Il n'y a pas de fichier de sortie pour le mode "1"
    else:
        print("Erreur, aucun mode indique.")      # Sinon on affiche une erreur
        usage()
        sys.exit(2)

    # On verifie que l'utilisateur n'a pas entre des chemins identiques
    if len(MS_args_SM) != len(set(MS_args_SM)):
        print("Erreur, doublon detecte dans les paramètres.")
        sys.exit(2)

    for MS_element_SM in MS_args_SM:                                                            # Pour chaque argument de la liste...
        # On verifie l'existence des fichiers qui ne sont pas la MS_sortie_SM
        if MS_element_SM != MS_sortie_SM and MS_element_SM != MS_args_SM[0]:                    # Si l'argument n'est pas la sortie et le mode, alors..
            if os.path.exists(MS_element_SM) and os.path.isfile(MS_element_SM):                 # Si le fichier existe
                if Path(MS_element_SM).stat().st_size == 0:                                     # Si le fichier est vide
                    print("Erreur, le fichier \"{}\" est vide !".format(MS_element_SM))   # On affiche une erreur
                    sys.exit(2)
            else:
                print("Erreur, le fichier \"{}\" n'existe pas !".format(MS_element_SM))   # Si le fichier n'existe pas on affiche une erreur
                usage()
                sys.exit(2)
    if MS_sortie_SM != "":                                                                      # Message qui informe du chemin de sortie
        print("La sortie sera le fichier {}".format(MS_sortie_SM))


def action(MS_args_SM):
    MS_mode_SM = MS_args_SM[0]                                              # MS_mode_SM devient le mode
    MS_cfichier_SM = MS_args_SM[1]                                          # MS_cfichier_SM devient le chemin vers le fichier
    ################### MODE 0 ###################
    if MS_mode_SM == "0":                                                   # Si le mode est "0"
        if len(MS_args_SM) == 2:                                            # S'il y a plus de 2 arguments, alors..
            MS_csortie_SM = MS_cfichier_SM + "_" + "sortie_chiffree.txt"    # La sortie sera [nom_fichier]_sortie_chiffree.txt
        else:
            MS_csortie_SM = MS_args_SM[2]                                   # Sinon la sortie prend le nom de l'argument 3
        # Initialisation de differentes variables
        MS_liste_ligne_SM = []                                              # Tableau qui va contenir les lignes d'un fichier
        MS_secret_SM = []                                                   # Tableau qui va contenir les randoms
        MS_message_chiffree_SM = []                                         # Tableau qui va contenir les caractères du message chiffre
        MS_message_chiffree_final_SM = ""                                   # String pour print le message chiffré
        MS_secret_final_SM = ""                                             # String pour print le secret
        MS_fichier_SM = open(MS_cfichier_SM, 'rb')                          # On ouvre le fichier à chiffrer
        MS_ligne_SM = MS_fichier_SM.readline()                              # On parcourt les lignes
        MS_pop_SM = 0                                                       # On utilise un boolean pour plus tard

        while MS_ligne_SM:
            MS_liste_ligne_SM.append(MS_ligne_SM)                           # On enregistre les lignes dans notre tableau
            MS_ligne_SM = MS_fichier_SM.readline()
        MS_fichier_SM.close()                                               # On ferme notre "session" fichier

        for MS_ligne_SM in MS_liste_ligne_SM:                               # Pour chaque ligne dans notre liste
            for MS_element_SM in MS_ligne_SM:                               # Pour chaque element dans notre ligne
                MS_key_SM = secrets.randbelow(254)+1                        # On génère un random entre 1 et 255
                MS_secret_SM.append(MS_key_SM)                              # On ajoute notre morceau de clé dans notre liste
                MS_element_SM = MS_element_SM ^ MS_key_SM                   # On effectue le XOR entre le caractère et notre clé
                MS_message_chiffree_SM.append(chr(MS_element_SM))           # On ajoute notre caractère chiffré dans une liste

        MS_fichier_SM = open(MS_csortie_SM, "w", encoding="UTF-8")
        for MS_char_SM in MS_message_chiffree_SM:                           # Pour chaque caractère dans notre message chiffré
            MS_message_chiffree_final_SM += MS_char_SM                      # On génère un string concaténé à lui-même
            MS_fichier_SM.write(MS_char_SM)                                 # On écrit notre caractère chiffré dans le fichier de sortie
        MS_fichier_SM.close()
        print("\nMessage chiffre:\n", MS_message_chiffree_final_SM.replace("\r", "\\r"))

        for MS_char_SM in MS_secret_SM:
            MS_secret_final_SM += str(MS_char_SM) + " "                     # On génère un string concaténé à lui-même
        MS_secret_final_SM = MS_secret_final_SM[:-1]                        # On supprime l'espace en trop
        MS_new_line_SM = "\n{} : {}".format(MS_csortie_SM, MS_secret_final_SM) # On prépare la ligne à ajouter dans la liste des PAD

        MS_liste_ligne_SM = []                                              # On vide notre liste
        if os.path.exists("liste_PAD.txt") and os.path.isfile("liste_PAD.txt"): # Si le fichier "liste_PAD.txt" existe
            MS_fichier_SM = open("liste_PAD.txt", "r", encoding="utf-8")    # On l'ouvre
            MS_ligne_SM = MS_fichier_SM.readline()
            while MS_ligne_SM:                                              # Pour chaque ligne du fichier
                if MS_cfichier_SM not in MS_ligne_SM:                       # Si on ne trouve pas le nom du fichier à chiffrer dans cette ligne
                    if MS_pop_SM == 0:                                      # Si on doit l'insérer (0 = insérer, 1 = sauter la ligne en cours)
                        MS_liste_ligne_SM.append(MS_ligne_SM)               # On ajoute la ligne
                    else:
                        MS_pop_SM = 0                                       # On passe notre boolean à 0
                else:
                    del MS_liste_ligne_SM[-1]                               # On supprime la dernière ligne ajoutée (- - - BEGIN SECRET - - -)
                    MS_pop_SM = 1                                           # On passe notre boolean à 1
                MS_ligne_SM = MS_fichier_SM.readline()
            MS_fichier_SM.close()
            MS_fichier_SM = open("liste_PAD.txt", "w", encoding="utf-8")
            for MS_ligne_SM in MS_liste_ligne_SM:
                MS_fichier_SM.write(MS_ligne_SM)
            MS_fichier_SM.close()
        MS_fichier_SM = open("liste_PAD.txt", "a", encoding="utf-8")
        MS_fichier_SM.write("- - - - - - - - - - - - - BEGIN SECRET - - - - - - - - - - - - -")
        MS_fichier_SM.write(MS_new_line_SM)                                 # On ajoute notre ligne dans la liste des PAD
        MS_fichier_SM.write("\n- - - - - - - - - - - - - END SECRET - - - - - - - - - - - - - -\n")
        MS_fichier_SM.close()
    ################### MODE 1 ###################
    else:                                                                   # Si le mode est "1"
        # Initialisation de differentes variables
        MS_message_SM = ""                                                  # Sera notre message dechiffré
        MS_message_chifree_SM = []                                          # Sera notre tableau de caractère chiffré
        MS_res_SM = ""                                                      # Est un string temporaire
        MS_i_SM = 0                                                         # Est un index temporaire
        MS_cpad_SM = MS_args_SM[2]                                          # Contient le chemin de la liste des PAD

        MS_fichier_SM = open(MS_cfichier_SM, "r", encoding="UTF-8")         # Contient le chemin du fichier chiffré
        MS_ligne_SM = MS_fichier_SM.readline()
        while MS_ligne_SM:
            MS_res_SM += MS_ligne_SM
            MS_ligne_SM = MS_fichier_SM.readline()
        MS_message_chifree_SM[:] = MS_res_SM                                # On explode notre string en un tableau de char
        MS_fichier_SM.close()

        MS_fichier_SM = open(MS_cpad_SM, "r", encoding="UTF-8")
        MS_ligne_SM = MS_fichier_SM.readline()
        while MS_ligne_SM:
            if MS_cfichier_SM in MS_ligne_SM:                               # On cherche la ligne qui contient le nom du fichier chiffré
                MS_secret_SM = MS_ligne_SM.split(": ")                      # On sépare notre ligne grâce au séparateur ":"
                MS_secret_SM = MS_secret_SM[1]                              # On isole la clé de déchiffrement
                MS_secret_SM = MS_secret_SM[:-1]                            # On supprime "\n"
                MS_secret_SM = MS_secret_SM.split(" ")                      # On place dans un tableau chaque morceau de clé grâce au séparateur " "
                for MS_element_SM in MS_secret_SM:                          # Pour chaque élement de notre clé
                    message_dechifree = chr(ord(MS_message_chifree_SM[MS_i_SM]) ^ int(MS_secret_SM[MS_i_SM])) # On effectue un XOR avec le caractère chiffré et le morceau de clé correspondant
                    MS_message_SM += message_dechifree                      # On génère un string concaténé à lui-même
                    MS_i_SM += 1                                            # On incrémente l'index
                print("Message dechiffre :\n{}".format(MS_message_SM))
                break                                                       # Si on a trouvé une occurence on s'arrête
            MS_ligne_SM = MS_fichier_SM.readline()
        if MS_message_SM == "":
            print("Erreur, aucune entree de ce fichier crypte dans la liste des PAD.")
            sys.exit(2)
        MS_fichier_SM.close()


if __name__ == "__main__":
    main(sys.argv[1:])
