# SI VOUS N'ETES PAS SIMON ET QUE VOUS LISEZ CE CODE, SACHEZ QUE CE N'EST PAS DU BEAU CODE
# coding: utf-8

class ClockSettings(object):

	ENABLE_COUNTDOWN_TIMER = True
	DEBUG_MODE = False
	DEBUG_LOADING_ANIMATION = False
	ANIMATION_DURATION_SECONDS = 2.5
	BACKGROUND_COLOR = [0, 0, 0]
	FRAMERATE = 60 # None = unlimited fps
	FONT = "moonget.ttf"
	FULLSCREEN = False
	WINDOWED_WIDTH = 480
	ENABLE_LOADING_ANIMATION = False
	RASPI2FB_CHECK = False
	

class AnimationLoopSettings(object):
	ENABLED = True
	DIRECTORY = 'frozen_flame'
	FPS = 30.0
	SCALE = 0.15
	# Pour la position, le chiffre est un pourcentage de l'ecran
	CENTER_X_PERCENT = 92.0
	CENTER_Y_PERCENT = 50.0
	
	
class EthermineAPI(object):
	ENABLE_ETHERMINE_STATS = True
	MINER_ADDRESS = '0x698ea061c90507b81931f9a9f8cfe6f519d8cd45'
	ADD_UP_PAYOUTS = True

# -------------------------------------LOADING SCREEN------------------------------------- #
def show_loading_screen(largeur, hauteur):
	global lift_loading_master

	loading_master = tk.Tk()

	resolution = largeur, hauteur
	
	loading_master.minsize(width=largeur, height=hauteur)
	loading_master.attributes("-fullscreen", ClockSettings.FULLSCREEN)
	loading_master.config(cursor="none")
	loading_master["bg"] = "black"
	canvas = tk.Canvas(loading_master, width=70 * size_mult, height=70 * size_mult, highlightthickness=0)
	canvas.configure(background='black')
	canvas.pack(side=tk.BOTTOM, pady=hauteur * 0.08)
	loading_arc_coordinates = 5 * size_mult, 5 * size_mult, 65 * size_mult, 65 * size_mult
	arc_extent = 0
	start_position = 0
	loading_arc = canvas.create_arc(loading_arc_coordinates, start=start_position, extent=arc_extent, width=5*size_mult, outline="cyan2", style="arc")
	loading_label = tk.Label(loading_master, font=(None, int(20 * size_mult)), text='Chargement...', fg="white", bg="black")
	loading_label.place(x=(largeur/2), y=(hauteur/2) - 20 * size_mult, anchor='center')
	status_label = tk.Label(loading_master, font=(None, int(20 * size_mult)), text=status_loading_text, fg="white", bg="black", wraplength=largeur)
	status_label.place(x=(largeur/2), y=(hauteur/2), anchor=tk.N)
	loading_master.lift()
	last_start_position = 210
	quick_lap = False
	debut_frame = time.time()
	loading_master.update()
	duree_frame = (time.time() - debut_frame)
	last_status_loading_text = ""
	while not startup_complete:
		debut_frame = time.time()
		
		arc_move_per_frame = 300.0 * duree_frame
		quick_lap_speed = arc_move_per_frame * 1.5

		if last_start_position < start_position:
			arc_extent = 250 if quick_lap else 60
			quick_lap = not quick_lap

		last_start_position = start_position
		if quick_lap:
			start_position = (start_position - quick_lap_speed) % 360
			arc_extent = arc_extent + quick_lap_speed/2 if arc_extent < 250 else 250
		else:
			start_position = (start_position - arc_move_per_frame) % 360
			arc_extent = arc_extent - quick_lap_speed/2 if arc_extent > 60 else 60

		if last_status_loading_text != status_loading_text:
			last_status_loading_text = status_loading_text
			status_label.config(text=status_loading_text)
			
		if lift_loading_master:
			loading_master.lift()
			lift_loading_master = False

		canvas.itemconfigure(loading_arc, start=start_position, extent=arc_extent)
		loading_master.update()

		duree_frame = (time.time() - debut_frame)
		duree_frame = 0 if duree_frame > 0.15 else duree_frame

	loading_master.destroy()
# ---------------------------------------------------------------------------------------- #

print("The clock has started running!")

import tkinter as tk

status_loading_text = "Modules"
startup_complete = False
lift_loading_master = False

loading_master = tk.Tk()

if ClockSettings.FULLSCREEN:
	largeur = loading_master.winfo_screenwidth()
	hauteur = loading_master.winfo_screenheight()
	
	if largeur > hauteur:
		fausse_largeur = hauteur * 1.5
		size_mult = fausse_largeur/480.0
	else:
		size_mult = hauteur/480.0
	
else:
	largeur = ClockSettings.WINDOWED_WIDTH
	hauteur = (320 * largeur)/480
	size_mult = largeur/480.0

largeur = int(largeur)
hauteur = int(hauteur)
resolution = largeur, hauteur

# Juste le texte pour afficher le plus rapidement possible
loading_master.minsize(width=largeur, height=hauteur)
loading_master.attributes("-fullscreen", ClockSettings.FULLSCREEN)
loading_master.config(cursor="none")
loading_master["bg"] = "black"
loading_label = tk.Label(loading_master, font=(None, int(20 * size_mult)), text='Chargement...', fg="white", bg="black")
loading_label.place(x=(largeur/2), y=(hauteur/2) - 20 * size_mult if ClockSettings.ENABLE_LOADING_ANIMATION else hauteur/2, anchor='center')
if ClockSettings.ENABLE_LOADING_ANIMATION:
	status_label = tk.Label(loading_master, font=(None, int(20 * size_mult)), text=status_loading_text, fg="white", bg="black")
	status_label.place(x=(largeur/2), y=(hauteur/2), anchor=tk.N)
loading_master.update()


from threading import Thread
import time

if ClockSettings.ENABLE_LOADING_ANIMATION:
	Thread(target=show_loading_screen, args=(largeur, hauteur)).start()

import os
os.system('cls' if os.name == 'nt' else 'clear')
print("Initializing...")

import math, datetime, urllib.request, urllib.error, urllib.parse, xmltodict, json, ssl, sys
from random import randint

old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')

import pygame

sys.stdout = old_stdout


if ClockSettings.DEBUG_LOADING_ANIMATION:
	time.sleep(4)
	startup_complete = True
	exit()

def seconde_a_couleur(seconde, inverser=False, couleur_random=False):
	random_number_color_local = randint(0, 59) if couleur_random else random_number_color
	
	seconde = (seconde + random_number_color_local) % 60
	
	if inverser:
		seconde = (seconde + 30) % 60 

	couleur = liste_calculs_couleurs[int(seconde/10)](seconde % 10)
	
	return couleur	
	
	
def get_data(retour_thread, get_forecast=False):
	if ClockSettings.DEBUG_MODE:
		print("SKIPPING REQUESTS FOR DEBUG")
		# retour_thread['weather_animation'] = 'vergla'
		retour_thread['thread_en_cours'] = False
		return True
	
	if retour_thread['thread_en_cours']:
		return True
	else:
		retour_thread['thread_en_cours'] = True
		
	print("Getting data")
	
	retour_thread['fetching_animation_text'] = None
	
	internet_access = False
	temp_actuelle = retour_thread['temperature'][0]
	couleur_temp_actuelle = retour_thread['temperature'][1]['couleur']
	shaking_etat_actuel = retour_thread['temperature'][1]['wiggle']
	pluie_actuelle = retour_thread['pourcent_pluie']
	detailed_info_actuelle = retour_thread['detailed_info']
	valeur_bitcoin_actuelle = retour_thread['valeur_bitcoin']
	#valeur_litecoin_actuelle = retour_thread['valeur_litecoin']
	#valeur_bitcoin_cash_actuelle = retour_thread['valeur_bitcoin_cash']
	valeur_ethereum_actuelle = retour_thread['valeur_ethereum']
	mined_ether_actuel = retour_thread['ethermine_data']
	
	internet_access = ping_this('http://google.com')
	
	if not internet_access:
		if not attempt_reconnection():
			return True
	
	
	retour_thread['fetching_animation_text'] = " "
	
	if get_forecast:
		try:
			print("Requesting forecast")
			
			retour_thread['detailed_info'] = "Rafraîchissement..."
			retour_thread['temperature'][0] = None
			retour_thread['temperature'][1]['couleur'] = couleur_fond_inverse
			retour_thread['temperature'][1]['wiggle'] = 0
			
			if retour_thread['pourcent_pluie'] != " ":
				retour_thread['pourcent_pluie'] = None
			
			xml_response = urllib.request.urlopen('https://weather.gc.ca/rss/city/qc-133_f.xml', timeout=60, context=ssl_context)
			dict_data = xmltodict.parse(xml_response.read())
			xml_response.close()
			
			forecast_pos = 0
			
			for title_num in range(0, len(dict_data['feed']['entry'])):
				if "Conditions actuelles:" in dict_data['feed']['entry'][title_num]['title']:
					forecast_pos = title_num
					break
			
			
			current_info = dict_data['feed']['entry'][forecast_pos]['title']
			
			current_info = current_info.split(" ")
			
			temperature = current_info.pop()
			
			detailed_info = ""
			
			casted_temperature = float(temperature[:-2].replace(',', '.'))

			if casted_temperature <= -15:
				# fait frette
				couleur_temperature = [102, 255, 255]
			elif casted_temperature >= 20:
				# fait chaud
				if casted_temperature > 35:
					niveau_vert = 69
				else:
					niveau_vert = int((35 - casted_temperature) * 12.4) + 69

				couleur_temperature = [255, niveau_vert, 84]
			else:
				couleur_temperature = couleur_fond_inverse
				
			if len(current_info) > 2:
				for word in current_info[2:]:
					detailed_info += word + " "
				
				detailed_info = detailed_info[:-2]
			else:
				detailed_info = 'Conditions indisponibles'
			
			
			for animation in weather_animations:
				if animation in detailed_info.lower():
					retour_thread['weather_animation'] = animation
					break
				else:
					retour_thread['weather_animation'] = ''


			pourcentage_pluie = dict_data['feed']['entry'][forecast_pos + 1]['title']
			
			if "%" in pourcentage_pluie:
				pourcentage_pluie = pourcentage_pluie.split(" ")[-1:][0]
			else:
				pourcentage_pluie = " "
					
			false_alerts = ["Aucune veille ou alerte",
							"BULLETIN",
							"TERMINÉ"]
							
			# S'il y a plusieurs alertes, on prend la premiere qui est vraie
			while forecast_pos > 0:
				alert_title = dict_data['feed']['entry'][forecast_pos - 1]['title']
								
				# Si aucune des fausses alertes ne correspond a l'alerte en cours, c'est une vraie alerte
				if not any(alert.upper() in alert_title.upper() for alert in false_alerts):
					detailed_info = dict_data['feed']['entry'][forecast_pos - 1]['title'].replace(', Québec', '')
					detailed_info = detailed_info.replace('EN VIGUEUR', '').rstrip()
					forecast_pos = 0
				else:
					forecast_pos -= 1
				
			
			if casted_temperature <= -18:
				retour_thread['temperature'][1]['wiggle'] = abs(casted_temperature + 17)/2.0
				
			retour_thread['detailed_info'] = detailed_info
			retour_thread['temperature'][0] = temperature
			retour_thread['temperature'][1]['couleur'] = couleur_temperature
			retour_thread['pourcent_pluie'] = pourcentage_pluie
			
		except ValueError:
			retour_thread['detailed_info'] = detailed_info_actuelle
			retour_thread['temperature'][0] = temp_actuelle
			retour_thread['temperature'][1]['couleur'] = couleur_temp_actuelle
			retour_thread['temperature'][1]['wiggle'] = shaking_etat_actuel
			retour_thread['pourcent_pluie'] = pluie_actuelle
		
		except Exception as erreur:
			print(erreur)
			retour_thread['detailed_info'] = str(erreur)
			retour_thread['temperature'][0] = "Erreur"
			retour_thread['temperature'][1]['couleur'] = couleur_fond_inverse
			retour_thread['temperature'][1]['wiggle'] = 0
			retour_thread['pourcent_pluie'] = ":("
			time.sleep(3)
			retour_thread['detailed_info'] = detailed_info_actuelle
			retour_thread['temperature'][0] = temp_actuelle
			retour_thread['temperature'][1]['couleur'] = couleur_temp_actuelle
			retour_thread['temperature'][1]['wiggle'] = shaking_etat_actuel
			retour_thread['pourcent_pluie'] = pluie_actuelle
			
			# retour_thread['thread_en_cours'] = False
			# get_data(retour_thread, get_forecast=True)
			# return True

	try:
		"""
		print("Requesting litecoin value")
		retour_thread['valeur_litecoin'] = None
		response = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=CAD", timeout=60)
		the_page = response.read()
		data = json.loads(the_page.decode('utf-8'))
		valeur_float_litecoin = data['CAD']
		valeur_litecoin = str(round(valeur_float_litecoin, 2)) + "$"
		retour_thread['valeur_litecoin'] = valeur_litecoin
		valeur_litecoin_actuelle = valeur_litecoin
		time.sleep(0.1)
		"""
		print("Requesting ethereum value")
		retour_thread['valeur_ethereum'] = None
		response = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=CAD", timeout=60)
		the_page = response.read()
		data = json.loads(the_page.decode('utf-8'))
		valeur_float_ethereum = data['CAD']
		valeur_ethereum = str(round(valeur_float_ethereum, 2)) + "$"
		retour_thread['valeur_ethereum'] = valeur_ethereum
		valeur_ethereum_actuelle = valeur_ethereum
		time.sleep(0.1)
		
		print("Requesting bitcoin value")
		retour_thread['valeur_bitcoin'] = None
		response = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=CAD", timeout=60)
		the_page = response.read()
		data = json.loads(the_page.decode('utf-8'))
		valeur_float_bitcoin = data['CAD']
		valeur_bitcoin = str(round(valeur_float_bitcoin, 2)) + "$"
		retour_thread['valeur_bitcoin'] = valeur_bitcoin
		valeur_bitcoin_actuelle = valeur_bitcoin
		
		if EthermineAPI.ENABLE_ETHERMINE_STATS:
			retour_thread['ethermine_data'] = [None, None, None]
			payout_total = 0
		
			if EthermineAPI.ADD_UP_PAYOUTS:
				print("Requesting ethermine payouts")
				
				request = urllib.request.Request("https://api.ethermine.org/miner/" + EthermineAPI.MINER_ADDRESS + "/payouts", headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'})
				response = urllib.request.urlopen(request, timeout=60)
				the_page = response.read()
				data = json.loads(the_page.decode('utf-8'))
				# data = {'status': 'OK', 'data': [{'start': 12406714, 'end': 12413241, 'amount': 834356589431425400, 'txHash': '0x1126c6a8588390a59291e6b1701eae3aad7dad91936b79e55e0b595441e86bf4', 'paidOn': 1620737754}, {'start': 12400230, 'end': 12406663, 'amount': 555513288702580030, 'txHash': '0xc90ef5fba01bd7f3db65d5430f190810649845ac06dd3e99d29838c331a8df08', 'paidOn': 1620650943}, {'start': 12393707, 'end': 12400188, 'amount': 645090064600998400, 'txHash': '0x2bd3e3ba15bbc62c58bf6f45d393ccb99ef1d5c2f4e2781501b273b311f41342', 'paidOn': 1620563957}, {'start': 12387159, 'end': 12393660, 'amount': 458554694654985660, 'txHash': '0x3d3d8f112c9bc665ab30744cc9e7f5cd1c88286204287f22bba0492ec671212e', 'paidOn': 1620477247}, {'start': 12380715, 'end': 12387097, 'amount': 425780021370793150, 'txHash': '0xa7a33c7d989adcc710bda831ccb4eb25fb419e0b1ea26a0cbbdff0f595734a3d', 'paidOn': 1620390476}, {'start': 12374120, 'end': 12380684, 'amount': 444826078950357200, 'txHash': '0x9b06ee407e324b3cff260d54ec504caa386341be4de27ce8a35610e0ac821622', 'paidOn': 1620303612}, {'start': 12367661, 'end': 12374108, 'amount': 418220121568648260, 'txHash': '0x77de57695a90bde416f280fdc9d06b1f1b13dd0edf772ec0c4e3cd48eb4b8e59', 'paidOn': 1620216924}, {'start': 12361120, 'end': 12367638, 'amount': 433186901673744260, 'txHash': '0x8b4e9efd30ac3b3d4520a590ce4481062324e676a405c7ee470e88050a7e29c9', 'paidOn': 1620130145}, {'start': 12354699, 'end': 12361098, 'amount': 401599760010163650, 'txHash': '0xea818db4affac370374fa647635039d14c30ff69c0a20b512f59cf4104388437', 'paidOn': 1620043450}, {'start': 12348161, 'end': 12354633, 'amount': 372013901284844700, 'txHash': '0x352d7be188fcd04ab3647e39544514b97ab609e26b98dcec8e6e6ce953dacdf0', 'paidOn': 1619956971}, {'start': 12341693, 'end': 12348133, 'amount': 440240273749722100, 'txHash': '0xe942f9b8d1ed53a8859a58a025993d574a2f533584bc9c499b9b5e5262c77b25', 'paidOn': 1619870389}, {'start': 12335207, 'end': 12341671, 'amount': 438750147301883100, 'txHash': '0xc20daa9549f051391d9626e85c7470e50a51b3aee5a322546d07053e3ba329c2', 'paidOn': 1619783846}, {'start': 12328781, 'end': 12335179, 'amount': 463160499129483100, 'txHash': '0x1662aaf5dcfb1b60c741cb55eac13df2624f124d8e7971b34691ed1b2b1ac7a5', 'paidOn': 1619697219}, {'start': 12322218, 'end': 12328750, 'amount': 464685769124625300, 'txHash': '0x78bdc76b22f31f89eb3c8cba3c8aacea5dc0f4286bcf8711ad5da20b27ed34b8', 'paidOn': 1619610504}, {'start': 12315710, 'end': 12322191, 'amount': 435199442233158700, 'txHash': '0x008ac0d1cfe60f17183c5ffebced4b47e8a030ec782500aa0ddce6fb4ff08b3c', 'paidOn': 1619523857}, {'start': 12309255, 'end': 12315691, 'amount': 437088530906237500, 'txHash': '0x87126324129b4ceb08faf536b52cacd024b6e258ef6f6ab4b8b3e64b96f9abad', 'paidOn': 1619437382}, {'start': 12302729, 'end': 12309220, 'amount': 440335824112138300, 'txHash': '0x63aef307fd36539e15f2668b58bff719688055e953228a77de0766c5c15e9ec7', 'paidOn': 1619350923}, {'start': 12296230, 'end': 12302690, 'amount': 508998304368362050, 'txHash': '0x29a23ef1a6e16472b3461f313da0c9811193dbb171ed2542e19ac08eb8447277', 'paidOn': 1619264329}, {'start': 12289751, 'end': 12296201, 'amount': 659279426835478400, 'txHash': '0x15d01751913873848e28cd9f839d502fc77142d105ce7a5771c2fde62d10f847', 'paidOn': 1619177817}, {'start': 12283329, 'end': 12289730, 'amount': 666510532168095400, 'txHash': '0xc682191d00df224e65ef7393bbd954431a3adc4ce8a252cb5d6e26f83960434a', 'paidOn': 1619091193}, {'start': 12276717, 'end': 12283298, 'amount': 771190550100570200, 'txHash': '0xee298f6e84e8fbd709b33a27e57301be758c6ac541ec072c26c546668278d4bf', 'paidOn': 1619004599}, {'start': 12270163, 'end': 12276691, 'amount': 800661688672569300, 'txHash': '0xde585ad1adcf75107715d73db66e689a90714c0b2cc65b296ee5961933e0d5f6', 'paidOn': 1618917684}, {'start': 12263754, 'end': 12270136, 'amount': 605949837715050200, 'txHash': '0x941f19207181b3d27c2c4ee39529f8889bfbf9a280e670de1324cd4ccc285dcb', 'paidOn': 1618830961}, {'start': 12257298, 'end': 12263720, 'amount': 658408728908950000, 'txHash': '0x9f2b1a570b5c7321ab486ad8c4b6aa9fbfb2c2f3129b29e8374d86031c4e741c', 'paidOn': 1618744492}, {'start': 12250744, 'end': 12257244, 'amount': 691176614122367000, 'txHash': '0x6c7265bd11b8dfea5293c7eeb013e73da852512604871c7cbfbc306f5f8fa377', 'paidOn': 1618658035}, {'start': 12244276, 'end': 12250701, 'amount': 549690415057950900, 'txHash': '0x331657ea939e50f02bdd67f07775e5de564b13f2b8e842ef413bc2b4cc24bbab', 'paidOn': 1618571088}, {'start': 12237795, 'end': 12244241, 'amount': 570614894833922700, 'txHash': '0x9bb259b7b1e22a139c91245619ff8c0774a65727b8838b420e25b1ceadfbe6e3', 'paidOn': 1618484253}, {'start': 12231286, 'end': 12237757, 'amount': 573366092723649150, 'txHash': '0x1ff09dba532786d1c0f4c8e0bf95291a22f2fd9377bb71c7c34608873a411cbb', 'paidOn': 1618397530}, {'start': 12224809, 'end': 12231248, 'amount': 555483674103140860, 'txHash': '0x6cb85e94bbc6029e6753bf9b9c63e83c9c004cf8bf6dbb83f04aaa037f71bc2a', 'paidOn': 1618310801}, {'start': 12218151, 'end': 12224781, 'amount': 506008086632875460, 'txHash': '0x8e4094d62a4c283a311d330ef0e3896a603df2fbfa08a869ebb3dc48fe3844e9', 'paidOn': 1618224141}, {'start': 12211670, 'end': 12218115, 'amount': 511187612801958300, 'txHash': '0xd682ad9681aa4dd6854cafc8f248caa68ef0b42fa2f857e4e73d127473fe4bb3', 'paidOn': 1618137606}, {'start': 12205158, 'end': 12211619, 'amount': 539986513080867500, 'txHash': '0x8b969fbae4bc51fa50c878fec0f1be8e8b6470288e2454fc33e4a4c6bc5e1e9e', 'paidOn': 1618051177}, {'start': 12198662, 'end': 12205132, 'amount': 568876353285399940, 'txHash': '0x99d28c87278d1a51738b53c7126a9fd3f5a01a8daaa0abda0c6c89e42c373cc7', 'paidOn': 1617964593}, {'start': 12192118, 'end': 12198633, 'amount': 597128665380911000, 'txHash': '0xb244d801ba7b1e928f52f45ee3a4fa2d77b197a52b5453876ac202b6320f4e9f', 'paidOn': 1617878047}, {'start': 12185615, 'end': 12192095, 'amount': 620452386552730400, 'txHash': '0x7a88e71585999094cdfe625d510e056803cd89f1126ba5481c26c93337902975', 'paidOn': 1617791278}, {'start': 12179096, 'end': 12185569, 'amount': 642672661532132700, 'txHash': '0xf5f1d2193c7c1c1ca64939f916c54e5f1336fe24cb1ed5a9f11dfc6938e2bf77', 'paidOn': 1617704534}, {'start': 12172500, 'end': 12179059, 'amount': 549183410272870100, 'txHash': '0x73aa684d16fd72683627fba0423bb1c9835ca153e21be9b9d3058abdab8e9522', 'paidOn': 1617617831}, {'start': 12165979, 'end': 12172461, 'amount': 635368839532832000, 'txHash': '0x5bccaca4343d5d76a7a03c9cf059a2ec57353ca68ccc7bf87f3891e34f84e732', 'paidOn': 1617531045}, {'start': 12159456, 'end': 12165945, 'amount': 695132993042473900, 'txHash': '0x3849459208319c32d1b05518b1a7f51d2b94aa6c95035a4d4b8fe05459d09a48', 'paidOn': 1617444422}, {'start': 12152997, 'end': 12159417, 'amount': 703335096888058400, 'txHash': '0xd84aa3880e3c0e940f1959aa788314e5800687b2dd1bfb43e7a3aa0c61e23a54', 'paidOn': 1617358004}, {'start': 12146444, 'end': 12152961, 'amount': 791407580508740000, 'txHash': '0xe4672f056eda94effe8fbf76296c9c0b8a8705995588bedafeb8797ff48846a1', 'paidOn': 1617271534}, {'start': 12139941, 'end': 12146420, 'amount': 728379276289336000, 'txHash': '0xb269adacea0b1c71108967315c396cd1ce708162d4941d9c217ae8e998f0aa2a', 'paidOn': 1617184754}, {'start': 12133430, 'end': 12139913, 'amount': 658260362309008400, 'txHash': '0x5643b0bd33032ffe8d790c8628e6a9ceb5f3b2cf5d4fd6e3c37d855db1ed0f7a', 'paidOn': 1617097988}, {'start': 12126924, 'end': 12133413, 'amount': 593583065629558300, 'txHash': '0x77f3c9fef05409a60e119fc2d71242967dc81f5c5f13197dd635217f2996bce0', 'paidOn': 1617011475}, {'start': 12120416, 'end': 12126890, 'amount': 585349926122458500, 'txHash': '0xa59834a9e3481fdf1c355e4c29c8e3cf67c0a2f2614ef26a8df5a70a49d27359', 'paidOn': 1616924697}, {'start': 12113859, 'end': 12120351, 'amount': 638402450385385900, 'txHash': '0x8683156964e960c0bb4220cb7764b65a80795ec7d8a4b2130bbfe8cb0398e855', 'paidOn': 1616838212}, {'start': 12107363, 'end': 12113829, 'amount': 694265966486183600, 'txHash': '0x66619a6ccd1171fc831bf0878a39e1bf9c567795f25ca9201f0997febd0e5bd0', 'paidOn': 1616751371}, {'start': 12100805, 'end': 12107311, 'amount': 768173360146499300, 'txHash': '0x8cc55b2d121666bb9bc837221b403d0c7b07b6b149e72e8347789e741d6b1388', 'paidOn': 1616664924}, {'start': 12094275, 'end': 12100742, 'amount': 708898420480531000, 'txHash': '0x4cb3d5ea3deca748188e3b4c7fc22a339c0447236f5fd3e082775abc0c370205', 'paidOn': 1616577899}, {'start': 12087733, 'end': 12094251, 'amount': 759617160552439200, 'txHash': '0x867de84d1c0bfe0de0271d0d36e01ee1e5385e9245629473aa6da3f5e5b2bf52', 'paidOn': 1616491149}, {'start': 12081250, 'end': 12087681, 'amount': 674334494793781000, 'txHash': '0xd814d23cec4b52bdaadb5f19cf5ead6d1b6c8a633e21bef5a5194deee6de8581', 'paidOn': 1616404389}, {'start': 12074809, 'end': 12081210, 'amount': 644647829466629400, 'txHash': '0x00f55d1efcf6ac0bbe96cde3789465e5c33819c7ca32cb8ab56af1fa0801d301', 'paidOn': 1616317883}, {'start': 12068243, 'end': 12074773, 'amount': 705715948866895900, 'txHash': '0xc33b66d6dbce633366eb44a3b98764fb504d0e8a97d3bee6f93c31d69231b005', 'paidOn': 1616231038}, {'start': 12061707, 'end': 12068203, 'amount': 767010452604572500, 'txHash': '0xc662848c92fa45ad028bc9d6e56ea948057517424030e23d4ebdf997e4a60692', 'paidOn': 1616144271}, {'start': 12055240, 'end': 12061665, 'amount': 809039902376516100, 'txHash': '0xe2d65717704d668c41b79d57be590ea7be696a0b07e549b4700888cb14e6f282', 'paidOn': 1616057764}, {'start': 12048689, 'end': 12055214, 'amount': 816860689942481300, 'txHash': '0xe936af8d06330a761345e2706fbfb77ecbbfb5bc9bb16956799e48b34463cfd9', 'paidOn': 1615971279}, {'start': 12042177, 'end': 12048660, 'amount': 798986508399683800, 'txHash': '0x4e654ea53e215b974961d57f621d50101bb9cc53e345754873ff723a7444000a', 'paidOn': 1615884541}, {'start': 12035707, 'end': 12042147, 'amount': 733859134511983900, 'txHash': '0x44edb49d2fdd11db00c806f7bf6623bd8d73cdb54f40954eb2a836b3a8496ab9', 'paidOn': 1615797995}, {'start': 12029192, 'end': 12035680, 'amount': 738940020672147000, 'txHash': '0x4ad7500115cc4468cde190947d17da6c99b74868442dc284141fbf8e653bde55', 'paidOn': 1615711563}, {'start': 12022709, 'end': 12029172, 'amount': 750786186729647200, 'txHash': '0xc3002038bf910202fd2b2bd197c2afff4b37d53962f87525589596de6f3d3bf3', 'paidOn': 1615625067}, {'start': 12016246, 'end': 12022679, 'amount': 723054019482740400, 'txHash': '0x66a0c01662c058d951a6e2d48b812effb018af1463bf4f0aa448fb6c953fa550', 'paidOn': 1615538422}, {'start': 12009738, 'end': 12016201, 'amount': 698012003191348700, 'txHash': '0x4130f028d52f182fdd24204cd10062c6b8b8dffabbb4dd5229b03331e9aa36e6', 'paidOn': 1615451661}, {'start': 12003242, 'end': 12009689, 'amount': 682406273203668400, 'txHash': '0x9b82a2f86dab2a4a1756ecb39bc44effee00256e56fe0c0f93bca79968cff0ef', 'paidOn': 1615365034}, {'start': 11996743, 'end': 12003205, 'amount': 703113363068744600, 'txHash': '0x884e3d74c676001c55720c2947c9a3e4081eb42ffa72314a295b4a44325e77c3', 'paidOn': 1615278204}, {'start': 11990252, 'end': 11996707, 'amount': 697842182975593900, 'txHash': '0x8b128e4638cd75ef79e87435085015aff913c1be6d2bcaf49b0dd9a35d59126c', 'paidOn': 1615191612}, {'start': 11983718, 'end': 11990213, 'amount': 612808950946193000, 'txHash': '0x1d125a1c5e204c2afcdfab7b7fba66898db49a06a2898fbd50baaefb77d42eed', 'paidOn': 1615105173}, {'start': 11977147, 'end': 11983683, 'amount': 663518245951817200, 'txHash': '0x2389c5377f5159bf6f14edeb5eea730ededa59afbea256301eeca1f56dbd0a6d', 'paidOn': 1615018395}, {'start': 11970608, 'end': 11977115, 'amount': 657713947114036400, 'txHash': '0xd7d6a1059ddbb03da201f997c4642d0ea4501babb36275ec7f4d80163d76d1bd', 'paidOn': 1614931559}, {'start': 11964040, 'end': 11970574, 'amount': 729934480213848300, 'txHash': '0x774bf077cb7cc0561cd867a0e40d441452bc3cd8f002b102c54d383d9aba1481', 'paidOn': 1614844757}, {'start': 11957576, 'end': 11964012, 'amount': 678343101700286100, 'txHash': '0x8ca9bbbd67f51849e6b11ce5487ce0773bd9c8203e9752d640b7ba04f16171ca', 'paidOn': 1614757926}, {'start': 11951067, 'end': 11957539, 'amount': 677743911219413000, 'txHash': '0x2fa9259baa28df9e7596d96e9bb6abfc67157886ffe4a1e46f9bafe679ea9d46', 'paidOn': 1614671261}, {'start': 11944575, 'end': 11951038, 'amount': 677444928068709100, 'txHash': '0xf2d3a931b55d0140c4220221f671b171625a258bd4e6d6ab5441fbfd90f5a21e', 'paidOn': 1614584635}, {'start': 11938056, 'end': 11944555, 'amount': 674569003296881000, 'txHash': '0xa7f31073287a7244485f2585bc929b5539905d6f19afa437c3ebf56f6238faca', 'paidOn': 1614498171}, {'start': 11931512, 'end': 11938020, 'amount': 729391147230027400, 'txHash': '0xbdb8f4ba7b562d11ef572ec1412bff385c2758c5d75712fcfbe027fc6d1a306b', 'paidOn': 1614411411}, {'start': 11924998, 'end': 11931472, 'amount': 752619268002398800, 'txHash': '0xc0d0176584ec43b6c406cec841349162c739396dc1e975b422dc4f13aab3e0bd', 'paidOn': 1614324802}, {'start': 11918508, 'end': 11924954, 'amount': 865167851837805300, 'txHash': '0x3a74eec1d49393939eb7a15dfe91618cb17f511f50fe14783ed9b3624ae9b7ab', 'paidOn': 1614238326}, {'start': 11911947, 'end': 11918476, 'amount': 1205262425791299300, 'txHash': '0xbd2c6b974c602cde42feeb8e7173dd9a5acac89a23373e6f4a27c0982c642456', 'paidOn': 1614151828}, {'start': 11905492, 'end': 11911908, 'amount': 1243063781931805400, 'txHash': '0x6c8c9e4adcdb3cfdc2006bd4a57da6115da4a9e2da8cbfbdfbc3cfd8a741bf06', 'paidOn': 1614065330}, {'start': 11898941, 'end': 11905469, 'amount': 762149606746393300, 'txHash': '0xb21e27bcdc4a1e5effdf009f98ed828780f40a4f8f1ba5205846dc86eab1cd77', 'paidOn': 1613978871}, {'start': 11892462, 'end': 11898909, 'amount': 874063358490124200, 'txHash': '0x9dea6acd068e0de6c7cca73fce257a99301a65099a88ecaa0be724358b26dc06', 'paidOn': 1613892409}, {'start': 11885952, 'end': 11892436, 'amount': 892062424051833300, 'txHash': '0x422b963feaf69b77fbc3bbf01f26987b73992d546b4fc9b757b3941b7dcbbe54', 'paidOn': 1613805725}, {'start': 11879440, 'end': 11885908, 'amount': 852648622513478300, 'txHash': '0xf3059676a9106cbdde1a335ad1ac66269a7272f7f8aba7ab1ba8d7c701ee191c', 'paidOn': 1613719306}, {'start': 11872892, 'end': 11879406, 'amount': 824119464613831400, 'txHash': '0xfdcddf2c835414a687112c80668a2a2b9823b3e7583e5768a4a3eed0c3ed81e0', 'paidOn': 1613632628}, {'start': 11866408, 'end': 11872849, 'amount': 776286500133866200, 'txHash': '0x2d824d20db5ff502bac87dc136f9a1a2031478511f190da16c18cbdaaed90ea1', 'paidOn': 1613545929}, {'start': 11859896, 'end': 11866372, 'amount': 801212212569938000, 'txHash': '0xbc36f7a2338cf51e9a0a12bb490315ecd4a91097c53d8f3bb2af458c70113f66', 'paidOn': 1613459453}, {'start': 11853392, 'end': 11859876, 'amount': 840350788362494800, 'txHash': '0x147118fca26d0061f3f061ad98bca3442a49f52f682e11a9a9f8932bc83ea4e2', 'paidOn': 1613372905}, {'start': 11846864, 'end': 11853363, 'amount': 825390004321441200, 'txHash': '0x41ea7e37c2abbd6b645fd191184d2e73d41b10c21ff927f149febc2371a485c4', 'paidOn': 1613286403}, {'start': 11840354, 'end': 11846822, 'amount': 842484702180897000, 'txHash': '0xd89778c6d921aa0319f8b565e7c012073695fece97c1c80a3b2b784930828eed', 'paidOn': 1613199855}, {'start': 11833785, 'end': 11840315, 'amount': 906035865692323000, 'txHash': '0x997d24b83154abebf724f3ea42ab993e8a5f399732b2ba99215a92b86ea5eb42', 'paidOn': 1613113351}, {'start': 11827273, 'end': 11833756, 'amount': 907374233567174100, 'txHash': '0x44c554a057a9a14607e4f8cda33a1a86ff7206b3766ce930aae17af6c4dd743e', 'paidOn': 1613026853}, {'start': 11820712, 'end': 11827242, 'amount': 999748804773943300, 'txHash': '0x46b566b70969874c84c708ba78416de57108478667004f40ca99fd80f357bec6', 'paidOn': 1612940135}, {'start': 11814318, 'end': 11820701, 'amount': 1035187995757483900, 'txHash': '0xae5ee11cda40bedb87267f5d283b85237123df508bdb768fe9fa894ac5744e6a', 'paidOn': 1612853600}, {'start': 11807799, 'end': 11814244, 'amount': 840792232914038000, 'txHash': '0x7c1a8dfaf81b8c974dacc532c0bebba83afbea6efd80f89e2ada0d6f7f701c33', 'paidOn': 1612767107}, {'start': 11801255, 'end': 11807751, 'amount': 829712741446312000, 'txHash': '0x60adf9c534f16651d4f73ebf32e96b2c4ea0977c4f046ea49b7a8b315107d002', 'paidOn': 1612680426}, {'start': 11794785, 'end': 11801178, 'amount': 1110555539967180500, 'txHash': '0x5c73dfb3b4763758530fe0aaebde6a454813034e8dfb3af22423a6126ee1bac4', 'paidOn': 1612593770}, {'start': 11788116, 'end': 11794667, 'amount': 1081612697390456800, 'txHash': '0xa7732c143609b0848283ede5ad5d39c8d31a35aa0a601154bba9497f40ed2754', 'paidOn': 1612506902}, {'start': 11781640, 'end': 11788054, 'amount': 985781931555030700, 'txHash': '0x1dccd147791b6dbcc6be20797123a1d8b1d04cac2288abd454ef3b8921129297', 'paidOn': 1612419865}, {'start': 11775155, 'end': 11781606, 'amount': 925345472224645900, 'txHash': '0x50f61f500cec82d517dec928f1658bfe45c715c53b6f40231f5bc01a961be0f1', 'paidOn': 1612333099}, {'start': 11768641, 'end': 11775051, 'amount': 867032954019236400, 'txHash': '0x5de58cb1559c23c92900f1a47eb5ca6eccb510f441e0d98f3e00bea0358d4d5d', 'paidOn': 1612246246}, {'start': 11762064, 'end': 11768589, 'amount': 838676805181087600, 'txHash': '0x3cdab5b9e4d810f8948459d50c38c59a40fc260b62659dd66d83c19d9edb5d5d', 'paidOn': 1612159582}]}
				for payout in data['data']:
					payout_total += payout['amount']
		
			print("Requesting ethermine currentStats")
			request = urllib.request.Request("https://api.ethermine.org/miner/" + EthermineAPI.MINER_ADDRESS + "/currentStats", headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'})
			response = urllib.request.urlopen(request, timeout=60)
			the_page = response.read()
			data = json.loads(the_page.decode('utf-8'))
			# data = {'status': 'OK', 'data': {'time': 1620735600, 'lastSeen': 1620735521, 'reportedHashrate': 24240470, 'currentHashrate': 19864526.8525, 'validShares': 16, 'invalidShares': 0, 'staleShares': 1, 'averageHashrate': 25524089.3757118, 'activeWorkers': 1, 'unpaid': 7390727788989035, 'unconfirmed': None, 'coinsPerMin': 1.1470426643973251e-06, 'usdPerMin': 0.004636300567787412, 'btcPerMin': 8.317206359545006e-08}}
			float_mined_ether = (data['data']['unpaid'] + payout_total) / 1000000000000000000
			float_hashrate = data['data']['currentHashrate'] / 1000000
			mined_ether = str(round(float_mined_ether, 5))
			valeur_mined_ether = str(round(float_mined_ether * valeur_float_ethereum, 2)) + '$'
			valeur_hashrate = str(round(float_hashrate, 1)) + 'MH/s'
			retour_thread['ethermine_data'][0] = mined_ether
			retour_thread['ethermine_data'][1] = valeur_mined_ether
			retour_thread['ethermine_data'][2] = valeur_hashrate
			mined_ether_actuel = [mined_ether, valeur_mined_ether, valeur_hashrate]
			time.sleep(0.1)
			
		
		"""
		print("Requesting bitcoin cash value")
		retour_thread['valeur_bitcoin_cash'] = None
		response = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=BCH&tsyms=CAD", timeout=60)
		the_page = response.read()
		data = json.loads(the_page.decode('utf-8'))
		valeur_float_bitcoin_cash = data['CAD']
		valeur_bitcoin_cash = str(round(valeur_float_bitcoin_cash, 2)) + "$"
		retour_thread['valeur_bitcoin_cash'] = valeur_bitcoin_cash
		valeur_bitcoin_cash_actuelle = valeur_bitcoin_cash
		time.sleep(0.1)
		"""
		
		
	except Exception as erreur:
		print(erreur)
		#retour_thread['valeur_litecoin'] = "Erreur"
		retour_thread['valeur_ethereum'] = "Erreur"
		#retour_thread['valeur_bitcoin_cash'] = "Erreur"
		retour_thread['valeur_bitcoin'] = "Erreur"
		retour_thread['ethermine_data'] = ['Erreur', 'Erreur']
		time.sleep(3)
		#retour_thread['valeur_litecoin'] = valeur_litecoin_actuelle
		retour_thread['valeur_ethereum'] = valeur_ethereum_actuelle
		#retour_thread['valeur_bitcoin_cash'] = valeur_bitcoin_cash_actuelle
		retour_thread['valeur_bitcoin'] = valeur_bitcoin_actuelle
		retour_thread['ethermine_data'] = mined_ether_actuel
		retour_thread['thread_en_cours'] = False
		get_data(retour_thread, get_forecast=False)

	
	retour_thread['thread_en_cours'] = False
	
	print("Done getting data")
	
	return True


def ping_this(url):
	try:
		urllib.request.urlopen(url, timeout=30)
		return True
	except Exception:
		return False
	
	
def attempt_reconnection():
	internet_access = False
	
	delais_attente = 10
	while not internet_access:
		retour_thread['fetching_animation_text'] = "Erreur"
		os.system("sudo ifconfig wlan0 down")
		os.system("sudo ifconfig wlan0 up")

		for it in range(delais_attente, 0 , -1):
			retour_thread['fetching_animation_text'] = "Attente de {secondes}s".format(secondes=str(it))
			time.sleep(1)
			if not en_fonction:
				return False
			
		retour_thread['fetching_animation_text'] = None
		
		if delais_attente < 30:
			delais_attente += 5
		
		internet_access = ping_this('http://google.com')
	
	return True
	
		
def get_text_jour_semaine_couleur():
	if num_jour_semaine == 4:
		return seconde_a_couleur(seconde_precise, couleur_random=True)
	else:
		return couleur_fond_inverse

		
def get_date_et_alignement():
	if maintenant.day == 1:
		num_jour = "1er"
	else:
		num_jour = str(maintenant.day)
	
	num_jour_semaine = maintenant.weekday()

	num_mois = maintenant.month - 1

	liste_centres = [
		font_25.size(noms_jours_semaine[num_jour_semaine])[0],
		font_40.size(num_jour)[0],
		font_17.size(noms_mois[num_mois])[0]
		]
	
	# On fait + 2 pour que ca ne soit pas colle au bord de lecran psk ca me trigger
	return num_jour_semaine, num_jour, num_mois, int((sorted(liste_centres)[-1]/2.0) + (2 * size_mult))

def render_spinning_image(vitesse_rpm=33):
	duree_un_tour = 60.0/vitesse_rpm
	correction_360 = 360.0/duree_un_tour
	degree_rotation = 360.0 - ((seconde_precise % duree_un_tour) * correction_360)

	rect_image = spinning_image.get_rect(center=(largeur*0.89, hauteur*0.75))
	rotated_surface = pygame.transform.rotozoom(spinning_image, degree_rotation, 1)
	rect_image = rotated_surface.get_rect(center=rect_image.center)

	ecran.blit(rotated_surface, rect_image)
	

def render_loop_image():
	loop_time_left = loop_end_time - maintenant
	pos_image = (loop_images_len - int(AnimationLoopSettings.FPS * loop_time_left.total_seconds())) % loop_images_len
	
	rect_image = loop_images[pos_image].get_rect(center=(loop_center_x, loop_center_y))
	ecran.blit(loop_images[pos_image], rect_image)
	
	
def get_font_ratio(font_path):
	# Sample sizes with roboto: (665, 21), 962, 1537, 3848
	measuring_sample = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890:#%$.°'
	current_size = 0
	
	created_font = pygame.font.Font(font_path, current_size)

	while created_font.size(measuring_sample)[0] <= 665 or created_font.size(measuring_sample)[1] <= 21:
		current_size += 1
		created_font = pygame.font.Font(font_path, current_size)
	
	current_size -= 1
	
	return current_size/17.0
	
def sleep_until_next_frame():
	pygame.display.update()
	# ecran.blit(surface, [0, 0])
	# clock.tick(fps)
	
	duree_frame = datetime.datetime.now() - maintenant
	duree_frame = duree_frame.total_seconds()

	if fps:
		# On diminue le sleep au cas ou la frame prends du temps a faire
		sleep_time = 1.0/fps - duree_frame

		if sleep_time > 0:
			time.sleep(sleep_time)
			duree_frame = datetime.datetime.now() - maintenant
			duree_frame = duree_frame.total_seconds()
		
	return duree_frame
			

def get_snowflake():
	mult_five = int(5 * size_mult)
	return {'pos_y': int(-randint(10, 25) * size_mult),
			'pos_x': randint(mult_five, largeur - mult_five),
			'vit_y': randint(hauteur//10, hauteur//7),
			'vit_x': randint(-largeur//15, largeur//15)}
			

def get_raindrop():
	vit_y = randint(hauteur//2, hauteur)
	return {'pos_y': int(-randint(10, 50) * size_mult),
			'pos_x': randint(-largeur//4, largeur),
			'vit_y': vit_y,
			'vit_x': vit_y//3}	
	

def render_snowing():
	if changement_seconde:
		for snowflake in snowflake_list:
			if snowflake['pos_y'] > hauteur:
				snowflake_list.remove(snowflake)
		snowflake_list.append(get_snowflake())
		
	for snowflake in snowflake_list:
		if snowflake['pos_x'] < 0 or snowflake['pos_x'] > largeur:
			snowflake['vit_x'] = - snowflake['vit_x']
		if changement_seconde:
			snowflake['vit_x'] = randint(-largeur//15, largeur//15)
			
		snowflake['pos_y'] += snowflake['vit_y'] * duree_last_frame
		snowflake['pos_x'] += snowflake['vit_x'] * duree_last_frame

		pygame.draw.circle(ecran, [255, 255, 255], [int(snowflake['pos_x']), int(snowflake['pos_y'])], int(5 * size_mult))
		

def render_raining(freezing=False):
	if len(raindrop_list) < 20:
		for it in range(0, 20 - len(raindrop_list)):
			raindrop_list.append(get_raindrop())
	else:
		for drop in raindrop_list:
			if drop['pos_y'] > hauteur or drop['pos_x'] > largeur:
				raindrop_list.remove(drop)
	
	drop_angle = 4 * size_mult
	drop_length = 15 * size_mult
	drop_thicc = int(3 * size_mult)
	drop_color = [0, 200, 255] if freezing else [0, 0, 255]
		
	for drop in raindrop_list:		
		drop['pos_y'] += drop['vit_y'] * duree_last_frame
		drop['pos_x'] += drop['vit_x'] * duree_last_frame

		pygame.draw.line(ecran, drop_color, [int(drop['pos_x']), int(drop['pos_y'])], [int(drop['pos_x'] + drop_angle), int(drop['pos_y'] + drop_length)], drop_thicc)


# START
if ClockSettings.DEBUG_MODE:
	print("DEBUGGING IS ENABLED DO NOT FORGET TO DISABLE IT")
	
status_loading_text = "Pygame"

pygame.display.init()

if ClockSettings.ENABLE_LOADING_ANIMATION:
	loading_master.destroy()
	lift_loading_master = True
else:
	loading_master.lift()
	loading_master.update()
	
pygame.mouse.set_visible(False)

ecran = pygame.display.set_mode((1, 1), pygame.NOFRAME)
lift_loading_master = True

maintenant = datetime.datetime.now()

fps = ClockSettings.FRAMERATE
debut_frame = time.time()
duree_last_frame = sleep_until_next_frame()
lift_loading_master = True

# --------------------------------LOADING SPINNING IMAGES--------------------------------- #
clock_files_folder = os.path.join(os.path.dirname(__file__), 'clock_files')
# images_filenames = ['bb0_vinyl_big.png', 'bb1_vinyl_big.png', 'mega_vinyl_big.png']
# images_filenames = ['bb0_vinyl.png', 'bb1_vinyl.png', 'mega_vinyl.png']
# images_filenames = ['cake.png', 'cake2.png', 'baloon.png']
images_filenames = []
spinning_images = []

shuffle_images = True
if len(images_filenames) < 2:
	shuffle_images = False

if len(images_filenames) > 0:
	for index in range(0, len(images_filenames)):
		status_loading_text = 'Images (' + str(index + 1) + '/' + str(len(images_filenames)) + ')'
		
		temp_image = pygame.image.load(os.path.join(clock_files_folder, images_filenames[index]))
		spinning_images.append(pygame.transform.scale(temp_image, (int(100 * size_mult), int(100 * size_mult))))

	for it in range(1, randint(1, len(spinning_images))):
		spinning_images.append(spinning_images.pop(0))

	spinning_image = spinning_images[0]
# ---------------------------------------------------------------------------------------- #
# -----------------------------------LOADING LOOP IMAGES---------------------------------- #
if AnimationLoopSettings.ENABLED:
	loop_time = 0
	loop_end_time = maintenant
	loop_center_x = int(largeur * (AnimationLoopSettings.CENTER_X_PERCENT/100.0))
	loop_center_y = int(hauteur * (AnimationLoopSettings.CENTER_Y_PERCENT/100.0))

	loop_directory = os.path.join(clock_files_folder, os.path.join('animations', AnimationLoopSettings.DIRECTORY))
	images_filenames = os.listdir(loop_directory)
	images_filenames.sort()
	
	loop_images = []
	
	for index in range(0, len(images_filenames)):
		status_loading_text = 'Images d\'animation (' + str(index + 1) + '/' + str(len(images_filenames)) + ')'

		temp_image = pygame.image.load(os.path.join(loop_directory, images_filenames[index]))
		loop_images.append(pygame.transform.rotozoom(temp_image, 0, AnimationLoopSettings.SCALE * size_mult))

	loop_images_len = len(loop_images)
	loop_time = loop_images_len/AnimationLoopSettings.FPS
# ---------------------------------------------------------------------------------------- #

surface = pygame.Surface(resolution)

status_loading_text = "Ajustement Police"

pygame.font.init()

font_path = os.path.join(clock_files_folder, ClockSettings.FONT)

font_ratio = get_font_ratio(font_path)

font_17 = pygame.font.Font(font_path, int(17 * font_ratio * size_mult))
font_25 = pygame.font.Font(font_path, int(25 * font_ratio * size_mult))
font_40 = pygame.font.Font(font_path, int(40 * font_ratio * size_mult))
font_100 = pygame.font.Font(font_path, int(100 * font_ratio * size_mult))

status_loading_text = "Touches finales"

heure = maintenant.hour

minute = maintenant.minute

seconde = maintenant.second

millisec = maintenant.microsecond

seconde_precise = seconde + millisec/1000000.0

redessiner = False

eloignement_secondes = int(10 * size_mult)

eloignement_minutes = int(45 * size_mult)

eloignement_heures = int(80 * size_mult)

if largeur > hauteur:
	rect_couleurs_secondes = [(largeur//2)-(hauteur//2)+eloignement_secondes, eloignement_secondes, hauteur-eloignement_secondes*2, hauteur-eloignement_secondes*2]
	rect_arc_secondes = [(largeur//2)-(hauteur//2)+eloignement_secondes-2, eloignement_secondes-2, hauteur-((eloignement_secondes-2)*2), hauteur-((eloignement_secondes-2)*2)]
	rect_arc_minutes = [(largeur//2)-(hauteur//2)+eloignement_minutes, eloignement_minutes, hauteur - eloignement_minutes*2, hauteur - eloignement_minutes * 2]
	rect_arc_heures = [(largeur//2)-(hauteur//2)+eloignement_heures, eloignement_heures, hauteur - eloignement_heures*2, hauteur - eloignement_heures * 2]
else:
	rect_couleurs_secondes = [eloignement_secondes, (hauteur//2)-(largeur//2)+eloignement_secondes, largeur-eloignement_secondes*2, largeur-eloignement_secondes*2]
	rect_arc_secondes = [eloignement_secondes-2, (hauteur//2)-(largeur//2)+eloignement_secondes-2, largeur-((eloignement_secondes-2)*2), largeur-((eloignement_secondes-2)*2)]
	rect_arc_minutes = [eloignement_minutes, (hauteur//2)-(largeur//2)+eloignement_minutes, largeur - eloignement_minutes*2, largeur - eloignement_minutes * 2]
	rect_arc_heures = [eloignement_heures, (hauteur//2)-(largeur//2)+eloignement_heures, largeur - eloignement_heures*2, largeur - eloignement_heures * 2]



notification_couleur_noire = False

couleur_fond = ClockSettings.BACKGROUND_COLOR

couleur_fond_inverse = [255 - couleur_fond[0], 255 - couleur_fond[1], 255 - couleur_fond[2]]

liste_calculs_couleurs = [lambda seconde: [255, int((seconde/10.0)*255), 0],
						  lambda seconde: [255 - int((seconde/10.0)*255), 255, 0],
						  lambda seconde: [0, 255, int((seconde/10.0)*255)],
						  lambda seconde: [0, 255 - int((seconde/10.0)*255), 255],
						  lambda seconde: [int((seconde/10.0)*255), 0, 255],
						  lambda seconde: [255, 0, 255 - int((seconde/10.0)*255)]]

en_fonction = True

minute_precedente = -1

heure_precedente = -1

seconde_precedente = -1

changement_heure = False

changement_seconde = False

toggle_menu = False

is_raspi2fb_active = False

animation_total_frames = round(ClockSettings.ANIMATION_DURATION_SECONDS * (ClockSettings.FRAMERATE or 1))

animation_active_frame = 0

random_number_color = randint(0, 59)

couleur_titre_countdown = couleur_fond_inverse

text_jour_semaine_couleur = couleur_fond_inverse

ssl_context = ssl._create_unverified_context()

retour_thread = {'temperature': ["##,#" + '\N{DEGREE SIGN}' + "C", {'couleur': couleur_fond_inverse, 'wiggle': 1.5 if ClockSettings.DEBUG_MODE else 0}],
				 'pourcent_pluie': "##%",
				 'detailed_info' : "Conditions actuelles",
				 'valeur_bitcoin': "####.##$",
				 #'valeur_litecoin': "##.##$",
				 #'valeur_bitcoin_cash': "###.##$",
				 'valeur_ethereum': "###.##$",
				 'ethermine_data': ['#.#####', '###.##$', '##.#MH/s'],
				 'fetching_animation_text': "",
				 'thread_en_cours': False,
				 'weather_animation' : ''}

meteo_update_recent = True

weather_animations = ['neige', 'poudre', 'vergla', 'pluie']

# clock = pygame.time.Clock()

noms_jours_semaine = [
	'Lundi',
	'Mardi',
	'Mercredi',
	'Jeudi',
	'Vendredi',
	'Samedi',
	'Dimanche',
	]
	
noms_mois = [
	'Janvier',
	'Février',
	'Mars',
	'Avril',
	'Mai',
	'Juin',
	'Juillet',
	'Août',
	'Septembre',
	'Octobre',
	'Novembre',
	'Décembre'
	]

num_jour_semaine, num_jour, num_mois, centre_date = get_date_et_alignement()

calculated_fps = '{} fps'.format(fps or 1)

#text_anim_frames = ["[oOo ]", "[ oOo]", "[o oO]", "[Oo o]"]
#text_anim_frames = ["boi", "boiii", "boiiiii", "boiiiiiii"]
#text_anim_frames = ["[\   ]", "[ \  ]", "[  \ ]", "[   \]", "[   /]", "[  / ]", "[ /  ]", "[/   ]"]
text_anim_frames = ["[.oOo.]", "[..oOo]", "[o..oO]", "[Oo..o]", "[oOo..]"]
#text_anim_frames = ["[-=-  ]", "[ -=- ]", "[  -=-]", "[-  -=]", "[=-  -]"]
#text_anim_frames = ["[do]", "[ob]", "[op]", "[qo]"]

text_anim_frame = 0

duree_last_frame = 0

snowflake_list = []

raindrop_list = []

notification_active = False

notifications = {"fps": 4,
				 "10:00": ["BANANA", "TIME"],
				 "12:00": ["À LA", "BOUFFE"]}

if ClockSettings.DEBUG_MODE:
	retour_thread['fetching_animation_text'] = None


if ClockSettings.FULLSCREEN:
	ecran = pygame.display.set_mode(resolution, pygame.FULLSCREEN | pygame.HWSURFACE)
else:
	ecran = pygame.display.set_mode(resolution)

print("Done initialising!")

if not ClockSettings.ENABLE_LOADING_ANIMATION:
	loading_master.destroy()

startup_complete = True

while en_fonction:
	debut_frame = time.time()
	
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONUP:
			pygame.mouse.set_visible(True)
			position_souris = pygame.mouse.get_pos()
			if toggle_menu:
				if position_souris[0] < largeur/3:
					#oui
					if ClockSettings.DEBUG_MODE:
						exit()
					status_loading_text = "BYE"
					en_fonction = False
				elif position_souris[0] < (2*largeur)/3:
					#non
					animation_active_frame = 0
					toggle_menu = False
					pygame.mouse.set_visible(False)
				else:
					#reboot
					status_loading_text = "À+"
					startup_complete = False
					en_fonction = False
			else:
				toggle_menu = True
				pygame.mouse.set_pos(largeur, hauteur)
		elif event.type == pygame.VIDEORESIZE and False:
			# Pour resizer, pas complet
			print("Resize detected")
			"""
			largeur = event.dict['size'][0]
			hauteur = (320 * largeur)/480
			resolution = largeur, hauteur
			size_mult = largeur/480.0
			ecran = pygame.display.set_mode(resolution, pygame.RESIZABLE)
			surface = pygame.Surface(resolution)
			animation_active_frame = 0"""

	if not toggle_menu:
	
		temps = time.strftime("%H:%M")
		
		maintenant = datetime.datetime.now()

		heure = maintenant.hour

		if heure > 11:
			heure -= 12

		minute = maintenant.minute
		
		changement_heure = ((minute < minute_precedente or heure < heure_precedente or seconde < seconde_precedente or (seconde - seconde_precedente) > 3) and seconde > 0) and minute > 0

		if changement_heure:
			print("Time change detected")
			animation_active_frame = 0
			

		heure_precedente = heure

		if minute != minute_precedente:
			# A chaque minute
			notification_active = temps in list(notifications.keys())
			couleur_titre_countdown = seconde_a_couleur(seconde_precise, couleur_random=True)
			text_jour_semaine_couleur = get_text_jour_semaine_couleur()
					

		minute_precedente = minute
		
		seconde_precedente = seconde

		seconde = maintenant.second
		
		if seconde_precedente != seconde:
			# A chaque seconde
			changement_seconde = True
			
			if ClockSettings.RASPI2FB_CHECK:
				if seconde % 15 == 0:
					if os.system("pidof raspi2fb") not in (1, 256) and not is_raspi2fb_active:
						pygame.draw.arc(surface, seconde_a_couleur(seconde_precise), rect_couleurs_secondes, math.radians(75-((360*seconde_precise)/60)), math.radians(113-((360*seconde_precise)/60)), int(30 * size_mult))
						is_raspi2fb_active = True
		else:
			changement_seconde = False

		millisec = maintenant.microsecond/1000000.0

		seconde_precise = seconde + millisec
		
		minute_changeante = minute + seconde_precise/60.0

		heure_changeante = heure + minute_changeante/60.0
		
		degree_secondes = ((360*seconde_precise)/60)
		
		degree_minutes = ((360*minute_changeante)/60)
			

		if redessiner and minute < 1:
			num_jour_semaine, num_jour, num_mois, centre_date = get_date_et_alignement()
			pygame.draw.circle(surface, [0, 0, 0], [largeur//2, hauteur//2], int(118 * size_mult))
			pygame.draw.circle(surface, [25, 25, 25], [largeur//2, hauteur//2], int(36 * size_mult))
			redessiner = False
		elif minute > 0 and not redessiner:
			redessiner = True
			
		if is_raspi2fb_active:
			if os.system("pidof raspi2fb") in (1, 256):
				is_raspi2fb_active = False
				animation_active_frame = animation_total_frames
			else:
				time.sleep(1)
				continue
			
		if not meteo_update_recent and minute % 5 == 0:
			get_forecast_too = minute % 20 == 5
			Thread(target=get_data, args=(retour_thread, get_forecast_too)).start()
			if shuffle_images:
				for it in range(0, randint(1, len(spinning_images) - 1)):
					spinning_images.append(spinning_images.pop(0))
				spinning_image = spinning_images[0]
			meteo_update_recent = True
		elif meteo_update_recent and minute % 5 != 0:
			meteo_update_recent = False
			
			
		# -------------------------------------NOTIFICATIONS------------------------------------- #
		if notification_active:
			fps = notifications['fps']
		
			big_top_text = notifications[temps][0]
			big_bottom_text = notifications[temps][1]
			
			animation_active_frame = 0
			if notification_couleur_noire:
				notification_couleur_noire = False
				midi_couleur = seconde_a_couleur(seconde_precise)
			else:
				notification_couleur_noire = True
				midi_couleur = [0, 0, 0]

			pygame.draw.rect(surface, midi_couleur, [0, 0, largeur, hauteur])
			ecran.blit(surface, [0, 0])
			midi_texte = font_100.render(big_top_text, 1, [255, 255, 255], midi_couleur)
			midi_texte_rect = midi_texte.get_rect(center=(largeur//2, int(0.3 * hauteur)))
			ecran.blit(midi_texte, midi_texte_rect)
			midi_texte = font_100.render(big_bottom_text, 1, [255, 255, 255], midi_couleur)
			midi_texte_rect = midi_texte.get_rect(center=(largeur//2, int(0.7 * hauteur)))
			ecran.blit(midi_texte, midi_texte_rect)
			sleep_until_next_frame()
			continue
		# --------------------------------------------------------------------------------------- #
			
		if animation_active_frame < animation_total_frames:
			first_frame = animation_active_frame == 0
			if first_frame:
				if ClockSettings.DEBUG_MODE:
					pygame.draw.rect(surface, [100, 100, 100], [0, 0, largeur, hauteur])
				else:
					pygame.draw.rect(surface, couleur_fond, [0, 0, largeur, hauteur])
					weather_animation = ''
				pygame.draw.circle(surface, [0, 0, 0], [largeur//2, hauteur//2], int(155 * size_mult))
				pygame.draw.circle(surface, [25, 25, 25], [largeur//2, hauteur//2], int(36 * size_mult))
				Thread(target=get_data, args=(retour_thread, True)).start()
				random_number_color = randint(0, 59)
				num_jour_semaine, num_jour, num_mois, centre_date = get_date_et_alignement()
				fps = ClockSettings.FRAMERATE
				animation_start_time = time.time()
			
			animation_temps_restant = ClockSettings.ANIMATION_DURATION_SECONDS - (animation_active_frame * ClockSettings.ANIMATION_DURATION_SECONDS) / animation_total_frames
			animation_duration = time.time() - animation_start_time
			skip_frame = False
			
			if round(animation_temps_restant + animation_duration, 1) > ClockSettings.ANIMATION_DURATION_SECONDS:
				skip_frame = True
			
			animation_seconde_fin = seconde_precise + animation_temps_restant
			
			draw_from = int(round((animation_active_frame * 120) / animation_total_frames))
			animation_active_frame += 2 if skip_frame else 1
			draw_to = int(round((animation_active_frame * 120) / animation_total_frames))


			# Secondes
			for it in range(draw_from, draw_to):
				it = int((animation_seconde_fin * 2) + it) % 120
					
				couleur_pour_secondes = seconde_a_couleur(it/2.0)

				pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes, math.radians(111-((360*(it/2.0))/60)), math.radians(123-((360*(it/2.0))/60)), int(30 * size_mult))
				pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes, math.radians(112-((360*(it/2.0))/60)), math.radians(123-((360*(it/2.0))/60)), int(30 * size_mult))
				pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes, math.radians(113-((360*(it/2.0))/60)), math.radians(123-((360*(it/2.0))/60)), int(30 * size_mult))
			
			# Pour cacher la couleur restante
			if first_frame:
				pygame.draw.arc(surface, [0, 0, 0], rect_arc_secondes, math.radians(75-degree_secondes), math.radians(130-degree_secondes), int(34 * size_mult))
				pygame.draw.arc(surface, [0, 0, 0], rect_arc_secondes, math.radians(76-degree_secondes), math.radians(130-degree_secondes), int(34 * size_mult))
				pygame.draw.arc(surface, [0, 0, 0], rect_arc_secondes, math.radians(77-degree_secondes), math.radians(130-degree_secondes), int(34 * size_mult))

			# Minutes et heures
			if draw_from:
				pygame.draw.arc(surface, seconde_a_couleur(minute_changeante, inverser=True), rect_arc_minutes, math.radians(90-((360*(minute_changeante/(120.0/draw_from))/60))), math.radians(90), int(30 * size_mult))
				pygame.draw.arc(surface, seconde_a_couleur((heure_changeante*60)/12), rect_arc_heures, math.radians(90-((360*(heure_changeante/(120.0/draw_from)))/12)), math.radians(90), int(40 * size_mult))

			
		else:
			#Couleurs secondes
			couleur_pour_secondes = seconde_a_couleur(seconde_precise)
			pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes, math.radians(111-degree_secondes), math.radians(123-degree_secondes), int(30 * size_mult))
			pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes, math.radians(112-degree_secondes), math.radians(123-degree_secondes), int(30 * size_mult))
			pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes, math.radians(113-degree_secondes), math.radians(123-degree_secondes), int(30 * size_mult))

			#Minutes
			pygame.draw.arc(surface, seconde_a_couleur(minute_changeante, inverser=True), rect_arc_minutes, math.radians(90-((360*minute_changeante)/60)), math.radians(90), int(30 * size_mult))

			#Heures
			pygame.draw.arc(surface, seconde_a_couleur((heure_changeante*60)/12), rect_arc_heures, math.radians(90-((360*heure_changeante)/12)), math.radians(90), int(40 * size_mult))
	
		
		#Arc secondes (noir)
		pygame.draw.arc(surface, [0, 0, 0], rect_arc_secondes, math.radians(75-degree_secondes), math.radians(111-degree_secondes), int(34 * size_mult))
		pygame.draw.arc(surface, [0, 0, 0], rect_arc_secondes, math.radians(76-degree_secondes), math.radians(111-degree_secondes), int(34 * size_mult))
		pygame.draw.arc(surface, [0, 0, 0], rect_arc_secondes, math.radians(77-degree_secondes), math.radians(111-degree_secondes), int(34 * size_mult))
			
		ecran.blit(surface, [0, 0])
		
		if retour_thread['thread_en_cours'] or ClockSettings.DEBUG_MODE:
			text_anim_frame = int(millisec * len(text_anim_frames))
			
		
		texte = font_25.render(temps, 1, [255, 255, 255])
		texte_rect = texte.get_rect(center=((largeur//2), (hauteur//2)))
		ecran.blit(texte, texte_rect)
		
		texte = font_25.render(str(seconde), 1, [255, 255, 255])
		texte = pygame.transform.rotozoom(texte, -degree_secondes + (180 if 45 > seconde_precise > 15 else 0), 1)
		texte_rect = texte.get_rect(center=(int((largeur/2) + math.cos(math.radians(degree_secondes - 92)) * 135 * size_mult), int((hauteur/2) + math.sin(math.radians(degree_secondes - 92)) * 135 * size_mult)))
		ecran.blit(texte, texte_rect)			
			
		texte = font_17.render(retour_thread['detailed_info'], 1, couleur_fond_inverse, couleur_fond)
		texte_rect = texte.get_rect()
		texte_rect.left = int(2 * size_mult)
		ecran.blit(texte, texte_rect)
		
		texte = font_25.render(retour_thread['temperature'][0] or text_anim_frames[text_anim_frame], 1, retour_thread['temperature'][1]['couleur'])
		texte_bottom = texte_rect.bottom
		texte_rect = texte.get_rect()
		texte_rect.top = texte_bottom
		texte_rect.left = int(2 * size_mult)
		texte_rect_final = texte_rect
		if retour_thread['temperature'][1]['wiggle'] != 0:
			texte = pygame.transform.rotate(texte, (retour_thread['temperature'][1]['wiggle'] * math.sin(millisec * 25)))
			texte_rect_final = texte.get_rect(center=texte_rect.center)
		ecran.blit(texte, texte_rect_final)

		texte = font_17.render(retour_thread['pourcent_pluie'] or text_anim_frames[text_anim_frame], 1, couleur_fond_inverse, couleur_fond)
		texte_bottom = texte_rect.bottom
		texte_rect = texte.get_rect(center=(texte_rect.center[0], 0))
		texte_rect.top = texte_bottom
		ecran.blit(texte, texte_rect)
		
		if EthermineAPI.ENABLE_ETHERMINE_STATS:
		
			texte = font_17.render(retour_thread['ethermine_data'][0] or text_anim_frames[text_anim_frame], 1, couleur_fond_inverse, couleur_fond)
			texte_top = texte_rect.top - (2 * size_mult)
			texte_rect = texte.get_rect()
			hashrate_left = int(texte_rect.right + (20 * size_mult))
			texte_rect.left = int(2 * size_mult)
			texte_rect.bottom = hauteur
			ecran.blit(texte, texte_rect)
			
			texte = font_17.render(retour_thread['ethermine_data'][1] or text_anim_frames[text_anim_frame], 1, couleur_fond_inverse, couleur_fond)
			texte_top = texte_rect.top - (2 * size_mult)
			texte_rect = texte.get_rect()
			texte_rect.left = int(2 * size_mult)
			texte_rect.bottom = int(texte_top)
			ecran.blit(texte, texte_rect)
			
			texte = font_17.render("Mining", 1, couleur_fond_inverse, couleur_fond)
			texte_top = texte_rect.top
			texte_rect = texte.get_rect(center=(texte_rect.center[0], 0))
			texte_rect.bottom = texte_top
			ecran.blit(texte, texte_rect)
		
		texte = font_17.render(retour_thread['valeur_bitcoin'] or text_anim_frames[text_anim_frame], 1, couleur_fond_inverse, couleur_fond)
		texte_top = texte_rect.top - (2 * size_mult)
		texte_rect = texte.get_rect()
		texte_rect.left = int(2 * size_mult)
		if EthermineAPI.ENABLE_ETHERMINE_STATS:
			texte_rect.bottom = int(texte_top)
		else:
			texte_rect.bottom = hauteur
		ecran.blit(texte, texte_rect)
		
		texte = font_17.render("BTC", 1, couleur_fond_inverse, couleur_fond)
		texte_top = texte_rect.top
		texte_rect = texte.get_rect(center=(texte_rect.center[0], 0))
		texte_rect.bottom = texte_top
		ecran.blit(texte, texte_rect)
		
		texte = font_17.render(retour_thread['valeur_ethereum'] or text_anim_frames[text_anim_frame], 1, couleur_fond_inverse, couleur_fond)
		texte_top = texte_rect.top - (2 * size_mult)
		texte_rect = texte.get_rect()
		texte_rect.left = int(2 * size_mult)
		texte_rect.bottom = int(texte_top)
		ecran.blit(texte, texte_rect)
		
		texte = font_17.render("ETH", 1, couleur_fond_inverse, couleur_fond)
		texte_top = texte_rect.top
		texte_rect = texte.get_rect(center=(texte_rect.center[0], 0))
		texte_rect.bottom = texte_top
		ecran.blit(texte, texte_rect)
		
		
		"""
		texte = font_17.render(retour_thread['valeur_bitcoin_cash'] or text_anim_frames[text_anim_frame], 1, couleur_fond_inverse, couleur_fond)
		texte_top = texte_rect.top - (2 * size_mult)
		texte_rect = texte.get_rect()
		texte_rect.left = int(2 * size_mult)
		texte_rect.bottom = int(texte_top)
		ecran.blit(texte, texte_rect)
		
		texte = font_17.render("BCH", 1, couleur_fond_inverse, couleur_fond)
		texte_top = texte_rect.top
		texte_rect = texte.get_rect(center=(texte_rect.center[0], 0))
		texte_rect.bottom = texte_top
		ecran.blit(texte, texte_rect)
		
		texte = font_17.render(retour_thread['valeur_litecoin'] or text_anim_frames[text_anim_frame], 1, couleur_fond_inverse, couleur_fond)
		texte_top = texte_rect.top - (2 * size_mult)
		texte_rect = texte.get_rect()
		texte_rect.left = int(2 * size_mult)
		texte_rect.bottom = int(texte_top)
		ecran.blit(texte, texte_rect)
		
		texte = font_17.render("LTC", 1, couleur_fond_inverse, couleur_fond)
		texte_top = texte_rect.top
		texte_rect = texte.get_rect(center=(texte_rect.center[0], 0))
		texte_rect.bottom = texte_top
		ecran.blit(texte, texte_rect)
		"""
		texte = font_17.render(retour_thread['fetching_animation_text'] or text_anim_frames[text_anim_frame], 1, couleur_fond_inverse, couleur_fond)
		texte_top = texte_rect.top - (20 * size_mult)
		texte_rect = texte.get_rect()
		texte_rect.left = int(2 * size_mult)
		texte_rect.bottom = int(texte_top)
		ecran.blit(texte, texte_rect)
		
		if EthermineAPI.ENABLE_ETHERMINE_STATS:
			texte = font_17.render(retour_thread['ethermine_data'][2] or text_anim_frames[text_anim_frame], 1, couleur_fond_inverse)
			texte_rect = texte.get_rect()
			texte_rect.bottom = hauteur
			texte_rect.left = hashrate_left
			ecran.blit(texte, texte_rect)
		
		texte = font_25.render(noms_jours_semaine[num_jour_semaine], 1, text_jour_semaine_couleur, couleur_fond)
		texte_rect = texte.get_rect(center=(largeur - centre_date, 0))
		texte_rect.top = 0
		ecran.blit(texte, texte_rect)
		
		texte = font_40.render(num_jour, 1, couleur_fond_inverse)
		texte_bottom = texte_rect.bottom
		texte_rect = texte.get_rect(center=(texte_rect.center[0], 0))
		texte_rect.top = int(texte_bottom - (12 * size_mult))
		ecran.blit(texte, texte_rect)
		
		texte = font_17.render(noms_mois[num_mois], 1, couleur_fond_inverse)
		texte_bottom = texte_rect.bottom
		texte_rect = texte.get_rect(center=(texte_rect.center[0], 0))
		texte_rect.top = int(texte_bottom - (10 * size_mult))
		ecran.blit(texte, texte_rect)
		
		texte = font_17.render(calculated_fps, 1, couleur_fond_inverse, couleur_fond)
		texte_rect = texte.get_rect()
		texte_rect.left = (largeur*7)//11
		ecran.blit(texte, texte_rect)

		
		# Countdown timer
		if ClockSettings.ENABLE_COUNTDOWN_TIMER:
			# Countdown normal
			temps_restant = datetime.datetime(2021, 7, 1, 10, 00) - maintenant
			# Fin de journée
			# temps_restant = datetime.datetime(maintenant.year, maintenant.month, maintenant.day, 15, 59) - maintenant
			
			temps_restant = temps_restant.days * 24 * 3600 + temps_restant.seconds
			
			temps_restant_mins, temps_restant_secs = divmod(temps_restant, 60)
			temps_restant_heures, temps_restant_mins = divmod(temps_restant_mins, 60)
			temps_restant_jours, temps_restant_heures = divmod(temps_restant_heures, 24)
			
			temps_restant_jours = "%02d" % (temps_restant_jours)
			temps_restant_heures = "%02d" % (temps_restant_heures)
			temps_restant_mins = "%02d" % (temps_restant_mins)
			temps_restant_secs = "%02d" % (temps_restant_secs)
			
			
			temps_restant = "{}:{}:{}:{}".format(temps_restant_jours, temps_restant_heures, temps_restant_mins, temps_restant_secs)
			
			texte = font_25.render(temps_restant, 1, couleur_fond_inverse, couleur_fond)
			texte_rect = texte.get_rect()
			texte_rect.right = int(largeur - (2 * size_mult))
			texte_rect.bottom = hauteur
			ecran.blit(texte, texte_rect)
			
			# Disco
			# couleur_titre_countdown = seconde_a_couleur(seconde_precise, couleur_random=True)
			# Smooth
			couleur_titre_countdown = seconde_a_couleur(seconde_precise, inverser=True)
			
			texte = font_17.render("Home :D", 1, couleur_titre_countdown, couleur_fond)
			texte_top = texte_rect.top
			texte_rect = texte.get_rect()
			texte_rect.right = int(largeur - (2 * size_mult))
			texte_rect.bottom = texte_top
			ecran.blit(texte, texte_rect)
			
			
		# End countdown timer
		
		# render_spinning_image(vitesse_rpm=15)
		
		if AnimationLoopSettings.ENABLED:
			if loop_end_time <= maintenant:
				loop_end_time = maintenant + datetime.timedelta(seconds=loop_time)

			render_loop_image()
		
		
		if retour_thread['weather_animation']:
			if retour_thread['weather_animation'] == 'neige' or retour_thread['weather_animation'] == 'poudre':
				render_snowing()
			elif retour_thread['weather_animation'] == 'vergla':
				render_raining(freezing=True)
			elif retour_thread['weather_animation'] == 'pluie':
				render_raining()
			

	else:
		#pygame.draw.rect(surface, [0, 255, 0], [0, 0, largeur/3, hauteur])
		#pygame.draw.rect(surface, [255, 0, 0], [largeur/3, 0, largeur/3, hauteur])
		#pygame.draw.rect(surface, [0, 0, 255], [(2*largeur)/3, 0, largeur/3, hauteur])
		pygame.draw.rect(surface, [0, 0, 0], [0, 0, largeur, hauteur])
		
		ecran.blit(surface, [0, 0])
		
		texte = font_25.render("Voulez-vous vraiment quitter?", 1, [255, 255, 255], [0, 0, 0])
		texte_rect = texte.get_rect(center=((largeur//2), hauteur//4))
		ecran.blit(texte, texte_rect)
		
		texte = font_40.render("Oui", 1, [0, 255, 0])
		texte_rect = texte.get_rect(center=((largeur//6), (hauteur//2)))
		ecran.blit(texte, texte_rect)
		
		texte = font_40.render("Non", 1, [255, 0, 0])
		texte_rect = texte.get_rect(center=((largeur//2), (hauteur//2)))
		ecran.blit(texte, texte_rect)
		
		texte = font_40.render("Reboot", 1, [0, 0, 255])
		texte_rect = texte.get_rect(center=((5*largeur)//6, (hauteur//2)))
		ecran.blit(texte, texte_rect)

		
	duree_last_frame = sleep_until_next_frame()
	
		
	if changement_seconde:
		calculated_fps = '{} fps'.format(int(1.0/duree_last_frame) if duree_last_frame else '--')


pygame.mouse.set_visible(False)
pygame.draw.rect(surface, couleur_fond, [0, 0, largeur, hauteur])
ecran.blit(surface, [0, 0])
texte = font_100.render(status_loading_text, 1, couleur_fond_inverse)
texte_rect = texte.get_rect(center=(largeur//2, hauteur//2))
ecran.blit(texte, texte_rect)
pygame.display.update()
time.sleep(1)

# Reusing startup_complete since its only needed during startup
if not startup_complete:
	try:
		import RPi.GPIO as GPIO
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(23, GPIO.OUT)
		GPIO.output(23, 1)
		os.system("sudo reboot")
	except Exception:
		pass
