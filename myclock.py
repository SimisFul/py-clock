# SI VOUS N'ETES PAS SIMON ET QUE VOUS LISEZ CE CODE, SACHEZ QUE CE N'EST PAS DU BEAU CODE
# coding: utf-8

class ClockSettings(object):

	ENABLE_COUNTDOWN_TIMER = True
	DEBUG_MODE = False
	DEBUG_LOADING_ANIMATION = False
	ANIMATION_DURATION_SECONDS = 2.5
	BACKGROUND_COLOR = [0, 0, 0]
	FRAMERATE = 70 # None = unlimited fps
	FONT = "moonget.ttf"
	FULLSCREEN = True
	WINDOWED_WIDTH = 480
	ENABLE_LOADING_ANIMATION = True
	RASPI2FB_CHECK = False
	

class AnimationLoopSettings(object):
	ENABLED = True
	DIRECTORY = 'frozen_flame'
	FPS = 30.0
	SCALE = 0.15
	# Pour la position, le chiffre est un pourcentage de l'ecran
	CENTER_X_PERCENT = 92.0
	CENTER_Y_PERCENT = 50.0

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
	valeur_litecoin_actuelle = retour_thread['valeur_litecoin']
	valeur_bitcoin_cash_actuelle = retour_thread['valeur_bitcoin_cash']
	valeur_ethereum_actuelle = retour_thread['valeur_ethereum']
	
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
			
			retour_thread['thread_en_cours'] = False
			get_data(retour_thread, get_forecast=True)
			return True

	try:
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
		
		print("Requesting bitcoin value")
		retour_thread['valeur_bitcoin'] = None
		response = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=CAD", timeout=60)
		the_page = response.read()
		data = json.loads(the_page.decode('utf-8'))
		valeur_float_bitcoin = data['CAD']
		valeur_bitcoin = str(round(valeur_float_bitcoin, 2)) + "$"
		retour_thread['valeur_bitcoin'] = valeur_bitcoin
		valeur_bitcoin_actuelle = valeur_bitcoin
		
	except Exception as erreur:
		print(erreur)
		retour_thread['valeur_litecoin'] = "Erreur"
		retour_thread['valeur_ethereum'] = "Erreur"
		retour_thread['valeur_bitcoin_cash'] = "Erreur"
		retour_thread['valeur_bitcoin'] = "Erreur"
		time.sleep(3)
		retour_thread['valeur_litecoin'] = valeur_litecoin_actuelle
		retour_thread['valeur_ethereum'] = valeur_ethereum_actuelle
		retour_thread['valeur_bitcoin_cash'] = valeur_bitcoin_cash_actuelle
		retour_thread['valeur_bitcoin'] = valeur_bitcoin_actuelle
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
				 'valeur_litecoin': "##.##$",
				 'valeur_bitcoin_cash': "###.##$",
				 'valeur_ethereum': "###.##$",
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
		if event.type == 6:
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
			pygame.draw.arc(surface, seconde_a_couleur(minute_changeante, inverser=True), rect_arc_minutes, math.radians(90-(degree_minutes)), math.radians(90), int(30 * size_mult))

			#Heures
			pygame.draw.arc(surface, seconde_a_couleur((heure_changeante*60)/12), rect_arc_heures, math.radians(90-((360*heure_changeante)/12)), math.radians(90), int(40 * size_mult))
	
		
		#Arc secondes (noir)
		pygame.draw.arc(surface, [0, 0, 0], rect_arc_secondes, math.radians(74-degree_secondes), math.radians(110-degree_secondes), int(34 * size_mult))
		pygame.draw.arc(surface, [0, 0, 0], rect_arc_secondes, math.radians(75-degree_secondes), math.radians(110-degree_secondes), int(34 * size_mult))
		pygame.draw.arc(surface, [0, 0, 0], rect_arc_secondes, math.radians(76-degree_secondes), math.radians(110-degree_secondes), int(34 * size_mult))
			
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
		
		texte = font_17.render(retour_thread['valeur_bitcoin'] or text_anim_frames[text_anim_frame], 1, couleur_fond_inverse, couleur_fond)
		texte_rect = texte.get_rect()
		texte_rect.left = int(2 * size_mult)
		texte_rect.bottom = hauteur
		ecran.blit(texte, texte_rect)
		
		texte = font_17.render("BTC", 1, couleur_fond_inverse, couleur_fond)
		texte_top = texte_rect.top
		texte_rect = texte.get_rect(center=(texte_rect.center[0], 0))
		texte_rect.bottom = texte_top
		ecran.blit(texte, texte_rect)
		
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
		
		texte = font_17.render(retour_thread['fetching_animation_text'] or text_anim_frames[text_anim_frame], 1, couleur_fond_inverse, couleur_fond)
		texte_top = texte_rect.top - (20 * size_mult)
		texte_rect = texte.get_rect()
		texte_rect.left = int(2 * size_mult)
		texte_rect.bottom = int(texte_top)
		ecran.blit(texte, texte_rect)
		
		texte = font_17.render(calculated_fps, 1, couleur_fond_inverse, couleur_fond)
		texte_rect = texte.get_rect()
		texte_rect.bottom = hauteur
		texte_rect.right = largeur//3
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

		
		# Countdown timer
		if ClockSettings.ENABLE_COUNTDOWN_TIMER:
			# Countdown normal
			temps_restant = datetime.datetime(2021, 3, 31, 10, 00) - maintenant
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
			
			texte = font_17.render("Fête Phil <3", 1, couleur_titre_countdown, couleur_fond)
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
