#import logging
import random
import re



#log = logging.getLogger(__name__)



class Salad_bot:
    def __init__(self):
        self.reponses_mots_cles = {} # dico contenant en clé une reponse du bot et en contenu la liste des mots déclenchant cette réponse
        self.fermetures=["quit","aurevoir","bye","a+"] #liste des mots déclenchant une fin de discussion (si ils sont le seul mot de la phrase)
        self.incomprehension=["Pourriez-vous reformuler svp ?","...","Je n'ai pas compris.","Que voulez vous dire ?"] #liste des réponses possible si on ne match pas de réponse valide
        self.reponses_necessaires={} #dico : clé = réponse du bot, contenu = liste des mots nécessaires dans la question pour que la réponse soit valide

    def load(self, path):
        """Modifie les attribues du bot en lisant le fichier path
        le bot apprend les mots clés associés a chaque réponse et les mots nécessaires pour chque réponse"""
        data = open(path,'r',encoding = 'utf-8')
        contenu=data.readlines()
        for ele in contenu :
            if ele=='\n': #On s'occupe pas des lignes vides
                pass
            else:
                rep,mots,necessaires=ele.split("=") # cahque ligne de réponse est séparé en 3 blocs : la réponse , les mots déclencheurs et les mots nécessaires
                necessaires=necessaires.strip() 
                liste_mots=re.split('/|\s',mots)

                liste_necessaires=re.split('/|\s',necessaires)
                for w in liste_necessaires:
                    if len(w)==0:
                        liste_necessaires.remove(w) #On s'assure de ne pas avoir de '' dans la liste
                self.apprend_reponse(rep,liste_mots,liste_necessaires) #on fait entrer les listes dans les dictionnaires
    
    def apprend_reponse(self,bot_response, list_of_words,liste_mots_necessaires):
        """Modifie/créé une entrée dans les dictionnaires attributs
        pour une réponse bot_response, on la met en clé des dictionnaires avec en contenu les déclencheurs dans reponses_mots_cles
        et les mots necessaires dans reponses_necessaires"""
        self.reponses_mots_cles[bot_response] = list_of_words
        self.reponses_necessaires[bot_response]=liste_mots_necessaires


    def repond(self, text):
        text= text.lower()                                  #transforme texte en minuscules
        if text in self.fermetures:                         #Si le texte est un déclencher de fin de discussion, on termine la discussion
            return None
        
        text = re.sub(r'\s*\.+\s*', ' . ', text)            #on enlève de la ponctuation
        text = re.sub(r'\s*,+\s*', ' , ', text)             #on enlève de la ponctuation
        text = re.sub(r'\s*;+\s*', ' ; ', text)             #on enlève de la ponctuation
        #log.debug('After punctuation cleanup: %s', text)

        words = [w for w in text.split(' ') if w]           #On sépare les différents mots du message d'entré
        #log.debug('Input: %s', words)

        output=self.meilleure_reponse(words)                #On determine la meilleure réponse en fct de ces mots d'entré
        return output                                       #On renvoie cette réponse

    def meilleure_reponse(self,mots_question):
        """a partir d'une liste de mot on determine quelle réponse est la plus appropriée"""
        message_certainty = 0                                                           #note du meilleur message de réponse actuel
        best_rep=self.incomprehension[random.randrange(len(self.incomprehension))]      #meilleur message de réponse actuel, initialement une réponse demandant une reformulation
        for rep,liste_cles in self.reponses_mots_cles.items():          #Pour chaque réponse
            correspondance=0                                            
            veto=False
            for mot in mots_question:
                if mot in liste_cles:                                   # si un mot de la question correspond a la réponse
                    correspondance+=len(mot)                            # On augumente la note de correspondance de cette réponse
            #print(self.reponses_necessaires,mots_question)
            for ele in self.reponses_necessaires[rep] :                 #on vérifie que les mots nécessaires a cette réponse sont présents dans la question
                if not ele in mots_question:
                    veto =True
            if correspondance>message_certainty and not veto:           #Si les mots nécessaires sont présents et que la réponse correspond mieux a la question
                best_rep=rep                                            #On change de réponse a renvoyer
                message_certainty=correspondance                        #et donc la note de cette réponse
        return best_rep                                      #On renvoie la réponse ayant la meilleure note après tous ces tests

    def run(self):
        """Lance une discussion avec le bot"""
        print("SALAD: Bonjour je suis SALAD, comment puis-je vous aider ?") #Salutations
        while True:
            recu = input('> ')              #demande entrée
            repartie = self.repond(recu)    #construit une réponse a partir de l'entrée
            if repartie is None:            #Si la réponse vaut None (fin de discussion) on sort de la boucle disscussion
                break
            print("SALAD: "+repartie)       #Si on a une réponse, SALAD la renvoie
        print("A bientôt !")                #envoie un message de fin de disscussion


def main():
    SALAD = Salad_bot()         #On créé un bot
    SALAD.load('sources.txt')   #On lui apprend le contenu de source.txt
    SALAD.run()                 #On le met dans la salle de discussion

if __name__ == '__main__':
    #logging.basicConfig()
    main()
