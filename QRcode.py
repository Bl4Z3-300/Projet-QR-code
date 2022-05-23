
def QRcode(message,qrname):
    from PIL import Image
    img =Image.new(mode ="RGB", size =(21,21), color = (150,150,150))
    
    def posMdl(img,x,y):
        for j in range(7):
            for i in range(7):
                img.putpixel((x+i,y+j),(0,0,0))
        for j in range(5):
            j+=1
            for i in range(5):
                i+=1
                img.putpixel((x+i,y+j),(255,255,255))
        for j in range(3):
            j+=2
            for i in range(3):
                i+=2
                img.putpixel((x+i,y+j),(0,0,0))



    def separatorMdl(img):

        def VSeg(img,colonne,debut,fin,color=(0,0,0)):


            l=fin-debut+1
            for n in range(l):
                img.putpixel((colonne,debut),(color))
                debut+=1

        def HSeg(img,ligne,debut,fin,color=(0,0,0)):


            l=fin-debut+1
            for n in range(l):
                img.putpixel((debut,ligne),(color))
                debut+=1


        VSeg(img,7,0,6,(255,255,255))
        VSeg(img,7,14,20,(255,255,255))
        VSeg(img,13,0,6,(255,255,255))
        HSeg(img,7,0,7,(255,255,255))
        HSeg(img,7,13,20,(255,255,255))
        HSeg(img,13,0,7,(255,255,255))


    def timingMdl(img):
        #vertical
        img.putpixel((6,8),(0,0,0))
        img.putpixel((6,10),(0,0,0))
        img.putpixel((6,12),(0,0,0))
        img.putpixel((6,9),(255,255,255))
        img.putpixel((6,11),(255,255,255))

        #horizontal
        img.putpixel((8,6),(0,0,0))
        img.putpixel((10,6),(0,0,0))
        img.putpixel((12,6),(0,0,0))
        img.putpixel((9,6),(255,255,255))
        img.putpixel((11,6),(255,255,255))


    def blackMdl(img):
        img.putpixel((8,13),(0,0,0))
        
    posMdl(img,0,0)
    posMdl(img,0,14)
    posMdl(img,14,0)
    separatorMdl(img)
    timingMdl(img)
    blackMdl(img)
    
    import qr
    
    
    def formatMdl(img,format=qr.format2bits()):
        """
        les format doit être donné sous la forme d'une string ou laissé vide pour le format standard
        """
        pos1=[[20,8],[19,8],[18,8],[17,8],[16,8],[15,8],[14,8],[13,8],[8,14],[8,15],[8,16],[8,17],[8,18],[8,19],[8,20]]
        pos2=[[8,0],[8,1],[8,2],[8,3],[8,4],[8,5],[8,7],[8,8],[7,8],[5,8],[4,8],[3,8],[2,8],[1,8],[0,8]]
        for poids,value in enumerate(format):
            if value =="1":
                color = (0,0,0)
            else:
                color=(255,255,255)
            img.putpixel(pos1[poids],color)
            img.putpixel(pos2[poids],color)
            
    formatMdl(img)
    
    def encodemessage(message):
        """
        transforme le message voulu en binaire et en fait une liste
        """
        msgcode=qr.message2bits(message)
        global listemessage
        listemessage=[]
        for i in msgcode:
            listemessage.append(i)
            
    encodemessage(message)
    
    
    def masque(x,y,bit):
        if (x+y) %3 == 0:
            if bit == '0':
                return '1'
            else:
                return '0'
        else:
            return bit
    
    
    def placement(img,listemessage):
        x=20                                            #colonne
        y=20                                            #ligne
        zone = "montante"
        n=0                                             #position dans la liste contenant le message
        for k in range(421):


            if img.getpixel((x,y))==(150,150,150):              #vérifie que le pixel est gris
                #print("gray detected")               #servait a detecter si je m etais trompé dans le systeme de reco couleur
                i = listemessage[n]                         #récupère la valeur du message en binaire
                n+=1                                        #passe a la prochaine valeur pour le prochain tour de la fonction
                value = masque(x,y,i)                       #applique le masque a la valeur
                #print(i)
                #print(value)
                if value == "1":                               #1->couleur noir
                    color =(0,0,0)

                else:
                    color =(255,255,255)                      #0->couleur blanche
                img.putpixel((x,y),color)                     #place le pixel


                if x==6 and y==0:                          #partie speciale pour la 7eme colonne
                    x-=1
                    zone="descendante"

                elif x<6:                                  #mouvement de colonne 00 à colonne 05
                    if zone == "montante" and y>0:         #si zone montante et pas en haut du tableau:
                        if x%2==1:                         #si la colonne est pair, on bouge a gauche
                            x-=1
                        else:                              #si la colonne est impaire on bouge a droite et en haut
                            x+=1
                            y-=1

                    elif zone =="montante" and y==0:       #si en bout de colonne montante on va passer en descendante 
                        if x%2==1:                         #quand colonne impaire
                            x-=1
                        else:
                            x-=1
                            zone = "descendante"
                    elif zone == "descendante" and y<20:   #si en descente et pas en bas du tableau:
                        if x%2==1:                         #si colonne paire, on bouge a gauche
                            x-=1
                        else:                              #si colonne impaire on bouge a droite et on descend
                            x+=1                           
                            y+=1
                    elif zone == "descendante" and y==20:  #si zone descendante et bout de tableau on passe en descente quand la
                        if x%2==1:                         #colonne est impaire
                            x-=1
                        else:
                            x-=1
                            zone = montante
                    else:
                        print("bug dans le systeme de colonne")


                else:                                      #mouvement normal

                    if zone == "montante" and y>0:         #si zone montante et pas en haut du tableau:
                        if x%2==0:                         #si la colonne est pair, on bouge a gauche
                            x-=1
                        else:                              #si la colonne est impaire on bouge a droite et en haut
                            x+=1
                            y-=1

                    elif zone =="montante" and y==0:       #si en bout de colonne montante on va passer en descendante 
                        if x%2==0:                         #quand colonne impaire
                            x-=1
                        else:
                            x-=1
                            zone = "descendante"
                    elif zone == "descendante" and y<20:   #si en descente et pas en bas du tableau:
                        if x%2==0:                         #si colonne paire, on bouge a gauche
                            x-=1
                        else:                              #si colonne impaire on bouge a droite et on descend
                            x+=1                           
                            y+=1
                    elif zone == "descendante" and y==20:  #si zone descendante et bout de tableau on passe en descente quand la
                        if x%2==0:                         #colonne est impaire
                            x-=1
                        else:
                            x-=1
                            zone = "montante"
                    else:
                        print("bug dans le systeme de colonne")

            else:                                      #si le pixel n est pas gris
                #print("gray not detected")            #servait a detecter si je m etais trompé dans le systeme de reco couleur
                if zone == "montante" and y>0:         #si zone montante et pas en haut du tableau:
                    if x%2==0:                         #si la colonne est pair, on bouge a gauche
                        x-=1
                    else:                              #si la colonne est impaire on bouge a droite et en haut
                        x+=1
                        y-=1

                elif zone =="montante" and y==0:       #si en bout de colonne montante on va passer en descendante 
                    if x%2==0:                         #quand colonne impaire
                        x-=1
                    else:
                        x-=1
                        zone = "descendante"
                elif zone == "descendante" and y<20:   #si en descente et pas en bas du tableau:
                    if x%2==0:                         #si colonne paire, on bouge a gauche
                        x-=1
                    else:                              #si colonne impaire on bouge a droite et on descend
                        x+=1                           
                        y+=1
                elif zone == "descendante" and y==20:  #si zone descendante et bout de tableau on passe en descente quand la
                    if x%2==0:                         #colonne est impaire
                        x-=1
                    else:
                        x-=1
                        zone = "montante"
                else:
                    print("bug dans le systeme de colonne")
    placement(img,listemessage)
    qrcode=img.resize((210,210), resample=Image.BOX)
    qrcode.show()
    qrcode = qrcode.save(qrname + ".jpg")

