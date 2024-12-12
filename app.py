# This Python file uses the following encoding: utf-8
from flask import Flask, flash, redirect, render_template, request, session, abort,send_from_directory
from random import randint
import os
import sys
import time
import base64 


if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

app = Flask(__name__)

insultes=['Abruti' ,'Ahuri' ,'Aigrefin','Anachorète' ,'Analphabète' ,'Andouille' ,'Anus De Poulpe',\
'Arsouille' ,'Aspirateur A Muscadet' ,'Assisté' ,'Asticot' ,'Attardé' ,'Avorton' ,'Babache' ,\
'Bachibouzouk' ,'Balai de Chiottes' ,'Baltringue' ,'Banane' ,'Bandit' ,'Barjot' ,'Batârd' ,'Betterave',\
'Bigleux' ,'Blaireau' ,'Boloss' ,'Bordel' ,'Bordel à Cul' ,'Boudin','Bouffon' ,'Bougre D’âne' ,\
'Bougre D’imbécile' ,'Bougre De Congre' ,'Bougre De Conne' ,'Boule De Pus' ,'Boulet' ,'Bouricot',\
'Bourique' ,'Bourrin' ,'Boursemolle' ,'Boursouflure' ,'Bouseux' ,'Boutonneux' ,'Branleur' ,\
'Branlotin' ,'Branque' ,'Branquignole' ,'Brigand' ,'Brêle' ,'Brosse à Chiottes' ,'Bubon Puant',\
'Burne' ,'Butor' ,'Bécasse' ,'Bégueule' ,'Bélitre' ,'Béotien' ,'Bête' ,'Cageot' ,'Cagole' ,'Calice' ,\
'Canaille' ,'Canaillou' ,'Cancrelat' ,'Caprinophile' ,'Carburateur à Beaujolais' ,'Caribou',\
'Casse-pieds' ,'Cassos' ,'Catin' ,'Cave' ,'Cervelle D’huitre' ,'Chacal' ,'Chacal Puant',\
'Chafouin','Chameau' ,'Chancreux' ,'Chancre puant' ,'Chaoui' ,'Charogne' ,'Chenapan' ,'Chiassard',\
'Chiasse De Caca Fondu' ,'Chieur' ,'Chiure De Pigeon' ,'Cinglé' ,'Clampin' ,'Cloaque' ,'Cloche' ,\
'Clodo' ,'Cloporte' ,'Clown' ,'Cochon' ,'Cocu' ,'Con' ,'Conard' ,'Conchieur' ,'Concombre' ,'Connard',\
'Connasse' ,'Conne' ,'Coprolithe' ,'Coprophage' ,'Cornard' ,'Cornegidouille' ,'Corniaud' ,\
'Cornichon' ,'Couard' ,'Couille De Tétard' ,'Couille Molle' ,'Couillon' ,'Crapaud De Pissotière',\
'Crapule' ,'Crassard','Crasspouillard!' ,'Crevard' ,'Crevure' ,'Crotte De Moineau' ,\
'Cryptorchide' ,'Crâne D’obus' ,'Crétin' ,'Crétin Des Alpes' ,'Crétin Des Iles' ,'Crétin Goîtreux',\
'Cuistre' ,'Cul De Babouin' ,'Cul Terreux' ,\
'Dégueulasse' ,'Don Juan De Pissotière' ,'Ducon' ,'Dugenou' ,'Dugland' ,'Dypterosodomite' ,'Débile',\
'Décamerde' ,'Décérébré' ,'Dégueulis' ,'Dégénéré Chromozomique' ,'Dégénéré Du Bulbe' ,'Dépravé',\
'Détritus' ,'Ecervelé' ,'Ectoplasme' ,'Emmerdeur' ,'Empaffé' ,'Emplâtre' ,'Empoté' ,'Enculeur De Mouches',\
'Enculé' ,'Enflure' ,'Enfoiré' ,'Erreur De La Nature' ,'Eunuque' ,'Face De Cul' ,'Face De Pet' ,\
'Face De Rat' ,'Faquin' ,'Faraud' ,'Faux Jeton' ,'Fesse D’huitre' ,'Fesse De Moule' ,'Fesses Molles' ,\
'Fiente' ,'Filou' ,'Fini à L’urine' ,'Fion' ,'Fiote' ,'Flaque De Pus' ,'Foireux' ,'Foldingue' ,\
'Fonctionnaire' ,'Fouille Merde' ,'Four à Merde' ,'Fourbe' ,'Foutriquet' ,'Frapadingue' ,'Frappe' ,\
'Freluquet' ,'Fricoteur' ,'Frigide' ,'Fripouille' ,'Frippon' ,'Frustré' ,'Fumier' ,'Fumiste' ,'Furoncle' ,\
'Félon' ,'Ganache' ,'Gangrène' ,'Garage A Bite' ,'Gibier De Potence' ,'Gland' ,'Glandeur' ,'Glandus' ,\
'Globicéphale' ,'Gnome' ,'Godiche' ,'Gogol' ,'Goinfre' ,'Gommeux' ,'Gougnafier' ,'Goujat' ,'Goulu' ,\
'Gourdasse' ,'Gourgandin', 'Gourgandine','Grand Cornichon' ,'Grand Dépandeur D’andouilles' ,'Gras Du Bide' ,\
'Graveleux' ,'Gredin' ,'Grenouille' ,'Gringalet' ,'Grognasse' ,'Gros Caca Poilu' ,'Gros Con' ,'Gros Lard' ,\
'Grosse Merde Puante' ,'Grosse Truie Violette' ,'Grue' ,'Gueulard' ,'Gueule De Fion' ,'Gueule De Raie' ,\
'Gueux' ,'Gugus' ,'Guignol' ,'Has-been' ,'Hérétique' ,'Histrion' ,'Homoncule' ,'Hostie D’épais' ,\
'Hurluberlu' ,'Hérétique' ,'Iconoclaste' ,'Idiot' ,'Ignare' ,'Illettré' ,'Imbibé' ,'Imbécile' ,'Impuissant' ,\
'Infâme Raie De Cul' ,'Ironie De La Création' ,'Ivrogne' ,'Jaune' ,'Jean-foutre' ,'Jobard' ,\
'Jobastre' ,'Judas' ,'Kroumir' ,'Kéké' ,'Laideron' ,'Larve' ,'Lavedu' ,'Lépreux' ,'Loboto' ,'Loutre Analphabète',\
'Lèche-cul' ,'Malandrin' ,'Malotru' ,'Malpropre' ,'Manant' ,'Manche à Couille' ,\
'Mange Merde' ,'Maquereau' ,'Maquerelle' ,'Maraud' ,'Marchand De Tapis' ,'Margoulin' ,'Merdaillon' ,'Merdasse',\
'Merde' ,'Merde Molle' ,'Merdophile' ,'Merlan Frit' ,'Microcéphale' ,'Minable' ,'Minus' ,\
'Miteux' ,'Moins Que Rien' ,'Molasson' ,'Mongol' ,'Mononeuronal' ,'Mont De Brin' ,'Morbleu' ,'Morfale' ,\
'Morille' ,'Morpion' ,'Mortecouille' ,'Morue' ,'Morveux'  ,'Mou Du Bulbe' ,\
'Mou Du Genou' ,'Mou Du Gland' ,'Moudlabite' ,'Moule à Gauffre' ,'Mouton De Panurge' ,'Méchant' ,'Mécréant',\
'Mérule' ,'Nabot' ,'Nain De Jardin' ,'Nanar' ,'Naze' ,'Nazillon' ,'Necropédophile' ,\
'Neuneu' ,'Nez De Boeuf' ,'Niais', 'Niaiseux' ,'Nigaud' ,'Niguedouille' ,'Noob' ,'Nounouille' ,'Nécrophile',\
'Obsédé' ,'Oiseau De Mauvaise Augure' ,'Olibrius' ,'Ordure Purulente' ,'Outre à Pisse' ,\
'Outrecuidant' ,'Pachyderme' ,'Paltoquet' ,'Panaris' ,'Parasite' ,'Parbleu' ,'Parvenu' ,'Patate' ,'Paumé',\
'Pauvre Con' ,'Paysan' ,'Peau De Bite' ,'Peau De Vache' ,'Pecore' ,'Peigne-cul' ,'Peine à Jouir' ,\
'Pendard' ,'Pervers' ,'Pet De Moule' ,'Petite Merde' ,'Petzouille' ,'Phlegmon' ,'Pigeon' ,'Pignolo' ,'Pignouf',\
'Pimbêche' ,'Pinailleur' ,'Pine D’ours' ,'Pine D’huitre' ,'Pintade' ,'Pipistrelle Puante' ,\
'Piqueniquedouille' ,'Pisse Froid' ,'Pisse-vinaigre' ,'Pisseuse' ,'Pissure' ,'Piètre' ,'Planqué',\
'Playboy De Superette' ,'Pleutre' ,'Plouc' ,'Poire' ,'Poireau' ,'Poivrot' ,'Polisson' ,'Poltron' ,\
'Pompe A Merde' ,'Porc' ,'Pot de chambre', 'Pouacreux' ,'Pouffe' ,'Pouffiasse' ,'Poufieux' ,'Pouilleux',\
'Pourceau' ,'Pourriture' ,'Pousse Mégot' ,'Punaise' ,'Putassière' ,'Pute Au Rabais' ,'Pute Borgne' ,\
'Putréfaction' ,'Pygocéphale' ,'Pécore' ,'Pédale' ,'Péquenot' ,'Pétasse' ,'Pétassoïde Conassiforme' ,\
'Pétochard' ,'Quadrizomique' ,'Queutard' ,'Quiche' ,'Raclure De Bidet' ,'Raclure De Chiotte' ,\
'Radasse' ,'Radin' ,'Ramassis De Chiure De Moineau' ,'Rambo De Pacotille' ,'Rastaquouère' ,'Renégat',\
'Roquet' ,'Roublard' ,'Rouge' ,'Roulure' ,'Résidu De Fausse Couche' ,'Résidus De Partouze' ,\
'Sabraque' ,'Sac à Brin' ,'Sac à Foutre' ,'Sac à Gnole' ,'Sac à Merde' ,'Sac à Viande' ,'Sac à Vin',\
'Sacrebleu' ,'Sacrement' ,'Sacripan' ,'Sagouin' ,'Salaud' ,'Saleté' ,'Saligaud' ,'Salopard' ,\
'Salope' ,'Saloperie' ,'Salopiaud' ,'Saltimbanque' ,'Saperlipopette' ,'Saperlotte' ,'Sauvage' ,\
'Scaphandrier D’eau De Vaiselle' ,'Scatophile' ,'Scélérat' ,'Schnock' ,'Schpountz' ,'Serpillière à Foutre' ,\
'Sinistrose Ambulante' ,'Sinoque' ,'Sodomite' ,'Sombre Conne' ,'Sombre Crétin' ,'Sot' ,'Souillon' ,'Sous Merde',\
'Spermatozoide Avarié' ,'Spermiducte' ,'Suintance' ,'Sybarite' ,'Siphonné' ,'Tabarnak' ,\
'Tabernacle' ,'Tâcheron' ,'Tafiole' ,'Tanche' ,'Tartignole' ,'Taré' ,'Tas De Saindoux' ,'Tasse à Foutre',\
'Thon' ,'Tire Couilles' ,'Tocard' ,'Tonnerre De Brest' ,'Toqué' ,'Trainé' ,'Traîne Savate' ,\
'Tricard' ,'Triple Buse' ,'Tromblon' ,'Tronche De Cake' ,'Trou De Balle' ,'Trou Du Cul' ,'Troubignole',\
'Truand' ,'Trumeaux' ,'Tuberculeux' ,'Tudieu' ,'Tétârd' ,'Tête D’ampoule' ,'Tête De Bite' ,\
'Tête De Chibre' ,'Tête De Con' ,'Tête De Noeud' ,'Tête à Claques' ,'Usurpateur' ,'Va Nu Pieds' ,\
'Va Te Faire' ,'Vandale' ,'Vaurien' ,'Vautour' ,'Ventrebleu' ,'Vermine' ,'Veule' ,'Vicelard' ,\
'Vieille Baderne' ,'Vieille Poule' ,'Vieille Taupe' ,'Vieux Chnoque' ,'Vieux Con' ,'Vieux Fossile',\
'Vieux Tableau' ,'Vieux Tromblon' ,'Vilain' ,'Vilain Comme Une Couvée De Singe' ,'Vioque' ,\
'Vipère Lubrique' ,'Voleur' ,'Vorace' ,'Voyou' ,'Vérole' ,'Wisigoth' ,'Yéti Baveux' ,'Zigomar' ,'Zigoto',\
'Zonard' ,'Zouave' ,'Zoulou' ,'Zozo' ,'Zéro',\
'Bachi-Bouzouk des Carpathes', 'Bougre d’ectoplasme de moule à gaufres', 'Tas de cornichons','Grotesque polichinelle',\
'Vapoteur', 'Pantacourtiste', 'Tatoué', 'Influenceur', 'Totebaguiste', 'Trottinettiste', 'Uberiste', 'Millenial',\
'Bougre de faux jeton à la sauce tartare']


allImages=['i1.jpg', 'i2.jpg','i3.jpg','i4.jpg','i5.jpg', 'i6.jpg','i7.jpg','i8.jpg','i9.jpg',\
'i10.jpg','i11.jpg', 'i12.jpg','i13.jpg','i14.jpg','i15.jpg', 'i16.jpg','i17.jpg','i18.jpg','i19.jpg',\
'i20.jpg','i21.jpg','i22.jpg']

imageFolder= 'image/'

@app.route("/")

def index():
    randomNumber = randint(0,len(insultes)-1) 
    insulte = insultes[randomNumber]  
    return render_template('simple.html',quote=insulte)
 
@app.route("/api")

def api():
    randomNumber = randint(0,len(insultes)-1) 
    insulte = insultes[randomNumber]  
    return "{result: " + insulte+"}"

@app.route("/api/v1")

def apiv1():
    randomNumber = randint(0,len(insultes)-1) 
    insulte = insultes[randomNumber]
    result = "{\"insult\": { \"text\": \"" + insulte+ "\" , \"index\": "+ str(randomNumber)+"} }"
    return result


@app.route("/api/v1/img")
def apiv1img():
    try:
        randomNumber = randint(0, len(insultes) - 1)
        insulte = insultes[randomNumber]
        randomNumberImg = randint(0, len(allImages) - 1)
        centerImage = allImages[randomNumberImg]

        image_path = os.path.join('static', imageFolder, centerImage)
        with open(image_path, 'rb') as image_file:
            image_read = image_file.read()
            image_64_encode = base64.b64encode(image_read).decode('utf-8')

        result = "{\"insult\": { \"text\": \"" + insulte + "\" , \"index\": " + str(randomNumber) + "},"
        result += " \"image\": { \"data\": \"" + image_64_encode + "\", \"mimetype\" : \"image/jpg\",  \"indexImg\": "
        result += str(randomNumberImg) + "} }"

        return result
    except FileNotFoundError:
        return "Image file not found", 404
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "Internal Server Error", 500

@app.route("/img")

def img():
    randomNumber = randint(0,len(insultes)-1) 
    insulte = insultes[randomNumber]
    randomNumberImg = randint(0,len(allImages)-1) 
    centerImage=allImages[randomNumberImg]
    return render_template('img.html',quote=insulte, image=imageFolder+centerImage,ins=randomNumber,imgNumber=randomNumberImg)

@app.route("/series")

def series():
	randomNumber = randint(0,len(insultes)-1) 
	insulte = insultes[randomNumber]
	randomNumberImg = randint(0,len(allImages)-1) 
	centerImage=allImages[randomNumberImg]
	return render_template('series.html',quote=insulte, image=imageFolder+centerImage)

@app.route("/img/<int:quo>/<int:img>/")

def ins (quo, img):
	insulte = insultes[quo]
	centerImage=allImages[img]
	return render_template('img_noencore.html',quote=insulte, image=imageFolder+centerImage)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(500)
def internal_error(error):
    return "500 error",500

@app.errorhandler(404)
def not_found(error):
    return "404 error",404

@app.errorhandler(401)
def not_authorized(error):
    return "401 error",401



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
