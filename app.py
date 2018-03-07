# This Python file uses the following encoding: utf-8
from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint
 
app = Flask(__name__)
 
@app.route("/")
def index():
    insultes=['Abruti' ,'Ahuri' ,'Aigrefin','Anachorete' ,'Analphabete' ,'Andouille' ,'Anus De Poulpe' ,'Arsouille' ,'Aspirateur A Muscadet' ,'Assiste' ,'Asticot' ,'Attarde' ,'Avorton' ,'Babache' ,\
'Bachibouzouk' ,'Balai de Chiottes' ,'Baltringue' ,'Banane' ,'Bandit' ,'Barjot' ,'Batard' ,'Betterave' ,'Bigleux' ,'Blaireau' ,'Boloss' ,'Bordel' ,'Bordel a Cul' ,'Boudin','Bouffon' ,'Bougre D’ane' ,\
'Bougre D’imbecile' ,'Bougre De Congre' ,'Bougre De Conne' ,'Boule De Pus' ,'Boulet' ,'Bouricot' ,'Bourique' ,'Bourrin' ,'Boursemolle' ,'Boursouflure' ,'Bouseux' ,'Boutonneux' ,'Branleur' ,\
'Branlotin' ,'Branque' ,'Branquignole' ,'Brigand' ,'Brele' ,'Brosse a Chiottes' ,'Bubon Puant' ,'Burne' ,'Butor' ,'Becasse' ,'Begueule' ,'Belitre' ,'Beotien' ,'Bete' ,'Cageot' ,'Cagole' ,'Calice' ,\
'Canaille' ,'Canaillou' ,'Cancrelat' ,'Caprinophile' ,'Carburateur a Beaujolais' ,'Caribou' ,'Casse-pieds' ,'Cassos' ,'Catin' ,'Cave' ,'Cervelle D’huitre' ,'Chacal' ,'Chacal Puant' ,'Chafouin' ,\
'Chameau' ,'Chancreux' ,'Chancre puant' ,'Chaoui' ,'Charogne' ,'Chenapan' ,'Chiassard' ,'Chiasse De Caca Fondu' ,'Chieur' ,'Chiure De Pigeon' ,'Cingle' ,'Clampin' ,'Cloaque' ,'Cloche' ,\
'Clodo' ,'Cloporte' ,'Clown' ,'Cochon' ,'Cocu' ,'Con' ,'Conard' ,'Conchieur' ,'Concombre' ,'Connard' ,'Connasse' ,'Conne' ,'Coprolithe' ,'Coprophage' ,'Cornard' ,'Cornegidouille' ,'Corniaud' ,\
'Cornichon' ,'Couard' ,'Couille De Tetard' ,'Couille Molle' ,'Couillon' ,'Crapaud De Pissotiere' ,'Crapule' ,'Crassard','Crasspouillard!' ,'Crevard' ,'Crevure' ,'Crotte De Moineau' ,\
'Cryptorchide' ,'Crane D’obus' ,'Cretin' ,'Cretin Des Alpes' ,'Cretin Des Iles' ,'Cretin Goîtreux' ,'Cuistre' ,'Cul De Babouin' ,'Cul Terreux' ,\
'Degueulasse' ,'Don Juan De Pissotiere' ,'Ducon' ,'Dugenou' ,'Dugland' ,'Dypterosodomite' ,'Debile' ,'Decamerde' ,'Decerebre' ,'Degueulis' ,'Degenere Chromozomique' ,'Degenere Du Bulbe' ,'Deprave',\
'Detritus' ,'Ecervele' ,'Ectoplasme' ,'Emmerdeur' ,'Empaffe' ,'Emplatre' ,'Empote' ,'Enculeur De Mouches' ,'Encule' ,'Enflure' ,'Enfoire' ,'Erreur De La Nature' ,'Eunuque' ,'Face De Cul' ,'Face De Pet' ,\
'Face De Rat' ,'Faquin' ,'Faraud' ,'Faux Jeton' ,'Fesse D’huitre' ,'Fesse De Moule' ,'Fesses Molles' ,'Fiente' ,'Filou' ,'Fini a L’urine' ,'Fion' ,'Fiote' ,'Flaque De Pus' ,'Foireux' ,'Foldingue' ,\
'Fonctionnaire' ,'Fouille Merde' ,'Four a Merde' ,'Fourbe' ,'Foutriquet' ,'Frapadingue' ,'Frappe' ,'Freluquet' ,'Fricoteur' ,'Frigide' ,'Fripouille' ,'Frippon' ,'Frustre' ,'Fumier' ,'Fumiste' ,'Furoncle' ,\
'Felon' ,'Ganache' ,'Gangrene' ,'Garage A Bite' ,'Gibier De Potence' ,'Gland' ,'Glandeur' ,'Glandus' ,'Globicephale' ,'Gnome' ,'Godiche' ,'Gogol' ,'Goinfre' ,'Gommeux' ,'Gougnafier' ,'Goujat' ,'Goulu' ,\
'Gourdasse' ,'Gourgandin/e' ,'Grand Cornichon' ,'Grand Depandeur D’andouilles' ,'Gras Du Bide' ,'Graveleux' ,'Gredin' ,'Grenouille' ,'Gringalet' ,'Grognasse' ,'Gros Caca Poilu' ,'Gros Con' ,'Gros Lard' ,\
'Grosse Merde Puante' ,'Grosse Truie Violette' ,'Grue' ,'Gueulard' ,'Gueule De Fion' ,'Gueule De Raie' ,'Gueux' ,'Gugus' ,'Guignol' ,'Has-been' ,'Heretique' ,'Histrion' ,'Homoncule' ,'Hostie D’epais' ,\
'Hurluberlu' ,'Heretique' ,'Iconoclaste' ,'Idiot' ,'Ignare' ,'Illettre' ,'Imbibe' ,'Imbecile' ,'Impuissant' ,'Infame Raie De Cul' ,'Ironie De La Creation' ,'Ivrogne' ,'Jaune' ,'Jean-foutre' ,'Jobard' ,\
'Jobastre' ,'Judas' ,'Kroumir' ,'Keke' ,'Laideron' ,'Larve' ,'Lavedu' ,'Lepreux' ,'Loboto' ,'Loutre Analphabete' ,'Leche-cul' ,'Malandrin' ,'Malotru' ,'Malpropre' ,'Manant' ,'Manche a Couille' ,\
'Mange Merde' ,'Maquereau' ,'Maquerelle' ,'Maraud' ,'Marchand De Tapis' ,'Margoulin' ,'Merdaillon' ,'Merdasse' ,'Merde' ,'Merde Molle' ,'Merdophile' ,'Merlan Frit' ,'Microcephale' ,'Minable' ,'Minus' ,\
'Miteux' ,'Moins Que Rien' ,'Molasson' ,'Mongol' ,'Mononeuronal' ,'Mont De Brin' ,'Morbleu' ,'Morfale' ,'Morille' ,'Morpion' ,'Mortecouille' ,'Morue' ,'Morveux' ,'Motherfucker' ,'Mou Du Bulbe' ,\
'Mou Du Genou' ,'Mou Du Gland' ,'Moudlabite' ,'Moule a Gauffre' ,'Mouton De Panurge' ,'Mechant.' ,'Mecreant' ,'Merule' ,'Nabot' ,'Nain De Jardin' ,'Nanar' ,'Naze' ,'Nazillon' ,'Necropedophile' ,\
'Neuneu' ,'Nez De Boeuf' ,'Niais, Niaiseux' ,'Nigaud' ,'Niguedouille' ,'Noob' ,'Nounouille' ,'Necrophile' ,'Obsede' ,'Oiseau De Mauvaise Augure' ,'Olibrius' ,'Ordure Purulente' ,'Outre a Pisse' ,\
'Outrecuidant' ,'Pachyderme' ,'Paltoquet' ,'Panaris' ,'Parasite' ,'Parbleu' ,'Parvenu' ,'Patate' ,'Paume' ,'Pauvre Con' ,'Paysan' ,'Peau De Bite' ,'Peau De Vache' ,'Pecore' ,'Peigne-cul' ,'Peine a Jouir' ,\
'Pendard' ,'Pervers' ,'Pet De Moule' ,'Petite Merde' ,'Petzouille' ,'Phlegmon' ,'Pigeon' ,'Pignolo' ,'Pignouf' ,'Pimbeche' ,'Pinailleur' ,'Pine D’ours' ,'Pine D’huitre' ,'Pintade' ,'Pipistrelle Puante' ,\
'Piqueniquedouille' ,'Pisse Froid' ,'Pisse-vinaigre' ,'Pisseuse' ,'Pissure' ,'Pietre' ,'Planque' ,'Playboy De Superette' ,'Pleutre' ,'Plouc' ,'Poire' ,'Poireau' ,'Poivrot' ,'Polisson' ,'Poltron' ,\
'Pompe A Merde' ,'Porc' ,'Pot de chambre', 'Pouacreux' ,'Pouffe' ,'Pouffiasse' ,'Poufieux' ,'Pouilleux' ,'Pourceau' ,'Pourriture' ,'Pousse Megot' ,'Punaise' ,'Putassiere' ,'Pute Au Rabais' ,'Pute Borgne' ,\
'Putrefaction' ,'Pygocephale' ,'Pecore' ,'Pedale' ,'Pequenot' ,'Petasse' ,'Petassoïde Conassiforme' ,'Petochard' ,'Quadrizomique' ,'Queutard' ,'Quiche' ,'Raclure De Bidet' ,'Raclure De Chiotte' ,\
'Radasse' ,'Radin' ,'Ramassis De Chiure De Moineau' ,'Rambo De Pacotille' ,'Rastaquouere' ,'Renegat' ,'Roquet' ,'Roublard' ,'Rouge' ,'Roulure' ,'Residu De Fausse Couche' ,'Residus De Partouze' ,\
'Sabraque' ,'Sac a Brin' ,'Sac a Foutre' ,'Sac a Gnole' ,'Sac a Merde' ,'Sac a Viande' ,'Sac a Vin' ,'Sacrebleu' ,'Sacrement' ,'Sacripan' ,'Sagouin' ,'Salaud' ,'Salete' ,'Saligaud' ,'Salopard' ,\
'Salope' ,'Saloperie' ,'Salopiaud' ,'Saltinbanque' ,'Saperlipopette' ,'Saperlotte' ,'Sauvage' ,'Scaphandrier D’eau De Vaiselle' ,'Scatophile' ,'Scelerat' ,'Schnock' ,'Schpountz' ,'Serpilliere a Foutre' ,\
'Sinistrose Ambulante' ,'Sinoque' ,'Sodomite' ,'Sombre Conne' ,'Sombre Cretin' ,'Sot' ,'Souillon' ,'Sous Merde' ,'Spermatozoide Avarie' ,'Spermiducte' ,'Suintance' ,'Sybarite' ,'Syphonne' ,'Tabarnak' ,\
'Tabernacle' ,'Tacheron' ,'Tafiole' ,'Tanche' ,'Tartignole' ,'Tare' ,'Tas De Saindoux' ,'Tasse a Foutre' ,'Thon' ,'Tire Couilles' ,'Tocard' ,'Tonnerre De Brest' ,'Toque' ,'Traine' ,'Traîne Savate' ,\
'Tricard' ,'Triple Buse' ,'Tromblon' ,'Tronche De Cake' ,'Trou De Balle' ,'Trou Du Cul' ,'Troubignole' ,'Truand' ,'Trumeaux' ,'Tuberculeux' ,'Tudieu' ,'Tetard' ,'Tete D’ampoule' ,'Tete De Bite' ,\
'Tete De Chibre' ,'Tete De Con' ,'Tete De Noeud' ,'Tete a Claques' ,'Usurpateur' ,'Va Nu Pieds' ,'Va Te Faire' ,'Vandale' ,'Vaurien' ,'Vautour' ,'Ventrebleu' ,'Vermine' ,'Veule' ,'Vicelard' ,\
'Vieille Baderne' ,'Vieille Poule' ,'Vieille Taupe' ,'Vieux Chnoque' ,'Vieux Con' ,'Vieux Fossile' ,'Vieux Tableau' ,'Vieux Tromblon' ,'Vilain' ,'Vilain Comme Une Couvee De Singe' ,'Vioque' ,\
'Vipere Lubrique' ,'Voleur' ,'Vorace' ,'Voyou' ,'Verole' ,'Wisigoth' ,'Yeti Baveux' ,'Zigomar' ,'Zigoto' ,'Zonard' ,'Zouave' ,'Zoulou' ,'Zozo' ,'Zero']

    randomNumber = randint(0,len(insultes)-1) 
    insulte = insultes[randomNumber]  
    return render_template('test.html',quote=insulte)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
