# coding: utf-8

class ClockSettings(object):
    ENABLE_COUNTDOWN_TIMER = False
    DEBUG_MODE = False
    BACKGROUND_COLOR = [0, 0, 0]
    FRAMERATE = None  # None = unlimited fps
    LOW_FRAMERATE_MODE = False
    FONT = "moonget-fixed.ttf"
    ENABLE_LOADING_ANIMATION = True
    LOADING_ANIMATION_SELECTION = 'peek'  # Choices: progress, peek, peek_lite
    DEBUG_LOADING_ANIMATION = False
    ANDROID_MODE = False
    FETCH_RELAIS_DATA = False
    SHOW_MINING_INFO = True


class DisplaySettings(object):
    SCREEN_WIDTH = 960
    SCREEN_HEIGHT = 600
    FULLSCREEN = False
    AUTOMATIC_RESOLUTION = True
    BORDERLESS_WINDOW = True
    X_POS = '0'
    Y_POS = '0'


class AnimationLoopSettings(object):
    ENABLED = True
    DIRECTORY = 'smug_dance'
    FPS = 60.0
    SCALE = 0.6
    ANTIALIASING = True
    # Pour la position, le chiffre est un pourcentage de l'ecran
    CENTER_X_PERCENT = 90.0
    CENTER_Y_PERCENT = 50.0


class WeatherSettings(object):
    RAINDROP_AMOUNT = 20


# -------------------------------------LOADING SCREEN------------------------------------- #
def show_progress_loading_screen(largeur, hauteur):
    global lift_loading_master

    loading_master = tk.Tk()

    loading_master.geometry(
        str(largeur) + "x" + str(hauteur) + "+" + DisplaySettings.X_POS + "+" + DisplaySettings.Y_POS)
    loading_master.overrideredirect(DisplaySettings.BORDERLESS_WINDOW and not DisplaySettings.FULLSCREEN)
    loading_master.attributes("-fullscreen", DisplaySettings.FULLSCREEN)
    loading_master.config(cursor="none")
    loading_master["bg"] = "black"
    canvas = tk.Canvas(loading_master, width=70 * size_mult, height=70 * size_mult, highlightthickness=0)
    canvas.configure(background='black')
    canvas.pack(side=tk.BOTTOM, pady=hauteur * 0.08)
    loading_arc_coordinates = 5 * size_mult, 5 * size_mult, 65 * size_mult, 65 * size_mult
    arc_extent = 0
    start_position = 0
    loading_arc = canvas.create_arc(loading_arc_coordinates, start=start_position, extent=arc_extent,
                                    width=5 * size_mult, outline="cyan2", style="arc")
    loading_label = tk.Label(loading_master, font=(None, int(20 * size_mult)), text='Chargement...', fg="white",
                             bg="black")
    loading_label.place(x=(largeur / 2), y=(hauteur / 2) - 20 * size_mult, anchor='center')
    status_label = tk.Label(loading_master, font=(None, int(20 * size_mult)), text=status_loading_text, fg="white",
                            bg="black", wraplength=largeur)
    status_label.place(x=(largeur / 2), y=(hauteur / 2), anchor=tk.N)
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
            arc_extent = arc_extent + quick_lap_speed / 2 if arc_extent < 250 else 250
        else:
            start_position = (start_position - arc_move_per_frame) % 360
            arc_extent = arc_extent - quick_lap_speed / 2 if arc_extent > 60 else 60

        if last_status_loading_text != status_loading_text:
            last_status_loading_text = status_loading_text
            status_label.config(text=status_loading_text)

        if lift_loading_master and not startup_complete:
            loading_master.lift()
            lift_loading_master = False

        canvas.itemconfigure(loading_arc, start=start_position, extent=arc_extent)
        loading_master.update()

        duree_frame = (time.time() - debut_frame)
        duree_frame = 0.1 if duree_frame > 0.1 else duree_frame

    loading_master.withdraw()
    lift_loading_master = False
    time.sleep(0.2)
    loading_master.destroy()


def show_peek_loading_screen(largeur, hauteur):
    global lift_loading_master
    global wait_for_peek_animation
    global loading_start_time

    lite_mode = ClockSettings.LOADING_ANIMATION_SELECTION == 'peek_lite'

    loading_master = tk.Tk()

    loading_master.geometry(
        str(largeur) + "x" + str(hauteur) + "+" + DisplaySettings.X_POS + "+" + DisplaySettings.Y_POS)
    loading_master.overrideredirect(DisplaySettings.BORDERLESS_WINDOW and not DisplaySettings.FULLSCREEN)
    loading_master.attributes("-fullscreen", DisplaySettings.FULLSCREEN)
    loading_master.config(cursor="none")
    loading_master["bg"] = "black"
    # loading_master.update()
    canvas = tk.Canvas(loading_master, width=hauteur, height=hauteur, highlightthickness=0)
    background = 'black'
    canvas.configure(background=background)
    canvas.pack(side=tk.BOTTOM)
    circle_secs = canvas.create_oval(int(8 * size_mult),
                                     int(8 * size_mult),
                                     hauteur - (8 * size_mult),
                                     hauteur - (8 * size_mult),
                                     fill='black',
                                     width=0)
    circle_mins = canvas.create_oval(int(42 * size_mult),
                                     int(42 * size_mult),
                                     hauteur - (42 * size_mult),
                                     hauteur - (42 * size_mult),
                                     fill='black',
                                     outline=background,
                                     width=int(5 * size_mult))
    circle_hours = canvas.create_oval(int(78 * size_mult),
                                      int(78 * size_mult),
                                      hauteur - (78 * size_mult),
                                      hauteur - (78 * size_mult),
                                      fill='black',
                                      outline=background,
                                      width=int(5 * size_mult))
    circle_time = canvas.create_oval((hauteur / 2) - int(38 * size_mult),
                                     (hauteur / 2) - int(38 * size_mult),
                                     (hauteur / 2) + int(38 * size_mult),
                                     (hauteur / 2) + int(38 * size_mult),
                                     fill='black',
                                     outline=background,
                                     width=int(5 * size_mult))
    circle_list = [circle_time, circle_hours, circle_mins, circle_secs, circle_secs]
    peek_progress_background = canvas.create_rectangle(0,
                                                       hauteur - peek_progress_height,
                                                       hauteur,
                                                       hauteur,
                                                       fill='#191919' if lite_mode else 'black',
                                                       outline='')
    peek_progress = canvas.create_rectangle(0,
                                            hauteur - peek_progress_height,
                                            int((hauteur * loading_progress_status) / 100),
                                            hauteur,
                                            fill='#404040',
                                            outline='')
    loading_master.update()
    last_loading_progress_status = 0
    smooth_progress_status = 0
    progress_catchup_mode = False
    duree_frame = 0
    color_strength = 0.0
    color_strength_lowest = 19.0
    color_strength_limit = 40.0
    active_circle = 0
    first_loop = True
    animation_paused = False
    pause_start = time.time()
    while not startup_complete:
        debut_frame = time.time()

        if lite_mode and not first_loop:
            wait_for_peek_animation = False

        if not animation_paused:
            color_strength = color_strength + duree_frame * (200 if first_loop else 100)

            if color_strength > color_strength_limit:
                color_strength = color_strength_limit

            color_strength_reversed = (color_strength_limit + color_strength_lowest) - (
                color_strength if color_strength >= color_strength_lowest else color_strength_lowest)

            color_string = str(int(color_strength)).zfill(2)
            color_string = '#' + color_string + color_string + color_string
            color_string_reversed = str(int(color_strength_reversed)).zfill(2)
            color_string_reversed = '#' + color_string_reversed + color_string_reversed + color_string_reversed

            if lite_mode:
                if first_loop:
                    if color_strength != color_strength_limit:
                        color_strength = color_strength - duree_frame * 100
                    else:
                        canvas.itemconfigure(circle_list[active_circle], fill='#191919')
            else:
                canvas.itemconfigure(circle_list[active_circle], fill=color_string)

                if active_circle != 0:
                    canvas.itemconfigure(circle_list[active_circle - 1],
                                         fill=color_string_reversed)

        if loading_progress_status <= loading_smooth_checkpoints[-1]:
            if smooth_progress_status < loading_progress_status:
                smooth_progress_status += (loading_progress_status - smooth_progress_status) * duree_frame
            if smooth_progress_status < loading_smooth_checkpoints[loading_checkpoint]:
                if loading_speed < loading_smooth_checkpoints[loading_checkpoint] - smooth_progress_status:
                    smooth_progress_status += loading_speed * duree_frame
                else:
                    smooth_progress_status += (loading_smooth_checkpoints[
                                                   loading_checkpoint] - smooth_progress_status) * duree_frame

            # Wait for loading
            if smooth_progress_status > loading_smooth_checkpoints[loading_checkpoint]:
                smooth_progress_status = loading_smooth_checkpoints[loading_checkpoint]
        # Catch up with loading
        else:
            if smooth_progress_status < loading_progress_status and smooth_progress_status < loading_smooth_checkpoints[
                -1] and not progress_catchup_mode:
                progress_catchup_mode = True

            if progress_catchup_mode:
                smooth_progress_status += (100 - smooth_progress_status) * duree_frame

                if smooth_progress_status >= loading_progress_status:
                    progress_catchup_mode = False
                    smooth_progress_status = loading_progress_status
            else:
                smooth_progress_status = loading_progress_status

        if last_loading_progress_status != smooth_progress_status:
            last_loading_progress_status = smooth_progress_status
            canvas.coords(peek_progress,
                          0,
                          hauteur - peek_progress_height,
                          int((hauteur * last_loading_progress_status) / 100),
                          hauteur)

            if animation_paused:
                loading_master.update()
        elif animation_paused:
            time.sleep(0.01)

        if first_loop and not lite_mode:
            if active_circle == 0:
                if color_strength <= 19:
                    canvas.itemconfigure(peek_progress_background, fill=color_string)
                else:
                    canvas.itemconfigure(peek_progress_background, fill='#191919')

        if startup_complete and time.time() - pause_start >= 0.2:
            break

        if time.time() - pause_start >= 1 and animation_paused:
            if wait_for_peek_animation:
                # wait_for_peek_animation set to True by main thread, don't start another loop. Prevents animation from looping again on horrendously slow hardware
                if ClockSettings.DEBUG_MODE:
                    canvas.itemconfigure(circle_list[0], fill='#ff4d4d')
                    loading_master.update()
                while not startup_complete:
                    time.sleep(0.05)
                break
            elif loading_progress_status < 100:  # Don't start another loop if we're about to be done
                wait_for_peek_animation = True
                animation_paused = False

        if not animation_paused:
            loading_master.update()

        if color_strength == color_strength_limit:
            active_circle += 1
            if active_circle == len(circle_list) and not animation_paused:
                animation_paused = True
                active_circle = 0
                first_loop = False
                pause_start = time.time()
                wait_for_peek_animation = False
                loading_master.lift()

            color_strength = 0.0 if first_loop else 19.0

        duree_frame = (time.time() - debut_frame)
        duree_frame = 0.1 if duree_frame > 0.1 else duree_frame

        if duree_frame > 5:
            # Time probably changed, compensating
            loading_start_time += duree_frame
            pause_start += duree_frame

    if lite_mode:
        # Makes the tft screen have to refresh a large enough area so that it can't display the black flicker when switching from tkinter to pygame
        canvas.itemconfigure(circle_secs, fill='#181818')
        loading_master.update()
    # loading_master.withdraw()
    lift_loading_master = False
    loading_master.withdraw()
    time.sleep(0.2)
    loading_master.destroy()


# ---------------------------------------------------------------------------------------- #

print('The clock has started running!')

if ClockSettings.ANDROID_MODE:
    print(
        'ANDROID_MODE enabled, this feature is meant to be used when this clock is used inside a buildozer made application.')
    ClockSettings.ENABLE_LOADING_ANIMATION = False

if ClockSettings.ENABLE_LOADING_ANIMATION:
    import tkinter as tk

import os, sys

clock_files_folder = os.path.abspath('.') + '/clock_files' if ClockSettings.ANDROID_MODE else os.path.join(
    os.path.dirname(__file__), 'clock_files')

if os.name == "nt":
    from ctypes import windll

    windll.user32.SetProcessDPIAware()

os.environ['SDL_VIDEO_WINDOW_POS'] = DisplaySettings.X_POS + ',' + DisplaySettings.Y_POS

desktop_img = None

if not os.path.exists(os.path.join(clock_files_folder, 'exit_splash.png')):
    try:
        import mss

        with mss.mss() as desktop_img:
            desktop_img = desktop_img.grab(desktop_img.monitors[0])
    except Exception:
        print('Screenshot failed!')
        desktop_img = None

status_loading_text = "Pygame: 1/2"
startup_complete = False
lift_loading_master = False
loading_progress_status = 0
loading_speed = 1
loading_smooth_checkpoints = [25, 28, 68, 69, 70]
loading_checkpoint = 0
wait_for_peek_animation = ClockSettings.LOADING_ANIMATION_SELECTION.startswith(
    'peek') and ClockSettings.ENABLE_LOADING_ANIMATION

if ClockSettings.ANDROID_MODE or not ClockSettings.ENABLE_LOADING_ANIMATION:
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    import pygame

    sys.stdout = old_stdout

    pygame.display.init()
    AutoRes = pygame.display.Info()
    largeur_ecran = AutoRes.current_w
    hauteur_ecran = AutoRes.current_h
else:
    tk_root = tk.Tk()
    largeur_ecran = tk_root.winfo_screenwidth()
    hauteur_ecran = tk_root.winfo_screenheight()
    tk_root.destroy()

if DisplaySettings.AUTOMATIC_RESOLUTION:
    largeur = int((largeur_ecran / 2) if ClockSettings.ANDROID_MODE else largeur_ecran)
    hauteur = int((hauteur_ecran / 2) if ClockSettings.ANDROID_MODE else hauteur_ecran)

else:
    largeur = DisplaySettings.SCREEN_WIDTH
    hauteur = DisplaySettings.SCREEN_HEIGHT

if largeur > hauteur:
    fausse_largeur = hauteur * 1.5
    size_mult = fausse_largeur / 480.0
else:
    size_mult = hauteur / 480.0

resolution = int(largeur), int(hauteur)

peek_progress_height = 2 if int(2 * size_mult) < 2 else int(2 * size_mult)

if ClockSettings.ENABLE_LOADING_ANIMATION and ClockSettings.LOADING_ANIMATION_SELECTION == 'progress':
    # Juste le texte pour afficher le plus rapidement possible
    loading_master = tk.Tk()
    loading_master.geometry(
        str(largeur) + "x" + str(hauteur) + "+" + DisplaySettings.X_POS + "+" + DisplaySettings.Y_POS)
    loading_master.overrideredirect(DisplaySettings.BORDERLESS_WINDOW and not DisplaySettings.FULLSCREEN)
    loading_master.attributes("-fullscreen", DisplaySettings.FULLSCREEN)
    loading_master.config(cursor="none")
    loading_master["bg"] = "black"
    loading_label = tk.Label(loading_master, font=(None, int(20 * size_mult)), text='Chargement...', fg="white",
                             bg="black")
    loading_label.place(x=(largeur / 2),
                        y=(hauteur / 2) - 20 * size_mult,
                        anchor='center')
    status_label = tk.Label(loading_master, font=(None, int(20 * size_mult)), text=status_loading_text, fg="white",
                            bg="black")
    status_label.place(x=(largeur / 2), y=(hauteur / 2), anchor=tk.N)

    loading_master.update()

from threading import Thread
import time

loading_start_time = time.time()

if ClockSettings.ENABLE_LOADING_ANIMATION:
    if ClockSettings.LOADING_ANIMATION_SELECTION == 'progress':
        Thread(target=show_progress_loading_screen, args=(largeur, hauteur), daemon=True).start()
    elif ClockSettings.LOADING_ANIMATION_SELECTION.startswith('peek'):
        Thread(target=show_peek_loading_screen, args=(largeur, hauteur), daemon=True).start()

os.system('cls' if os.name == 'nt' else 'clear')
print("Initializing...")

if ClockSettings.ENABLE_LOADING_ANIMATION and ClockSettings.LOADING_ANIMATION_SELECTION.startswith('peek'):
    loading_speed_file_path = os.path.join(clock_files_folder, 'loading_speed.txt')

    if os.path.exists(loading_speed_file_path):
        try:
            with open(loading_speed_file_path) as f:
                loading_speed = float(f.read())

            if loading_speed < 1:
                loading_speed = 1
        except Exception:
            # os.remove(loading_speed_file_path)
            loading_speed = 2

if ClockSettings.DEBUG_LOADING_ANIMATION:
    time.sleep(1)
    loading_progress_status = 25
    time.sleep(1)
    loading_progress_status = 50
    time.sleep(1)
    loading_progress_status = 75
    time.sleep(1)
    loading_progress_status = 100
    time.sleep(1)
    startup_complete = True
    exit()

old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')

import pygame

sys.stdout = old_stdout

loading_progress_status = loading_smooth_checkpoints[loading_checkpoint]
loading_checkpoint += 1


def seconde_a_couleur(seconde, inverser=False, couleur_random=False):
    color_offset_local = uniform(0, 59) if couleur_random else color_offset

    seconde = (seconde + color_offset_local) % 60

    if inverser:
        seconde = (seconde + 30) % 60

    couleur = liste_calculs_couleurs[int(seconde / 10)](seconde % 10)

    return couleur


def get_data(retour_thread, get_forecast=False):
    if ClockSettings.DEBUG_MODE:
        print("SKIPPING REQUESTS FOR DEBUG")
        retour_thread['weather_animation'] = 'pluie'
        retour_thread['fetching_animation_text'] = None
        retour_thread['thread_en_cours'] = False
        return True

    if retour_thread['thread_en_cours']:
        return True
    else:
        retour_thread['thread_en_cours'] = True

    print("Getting data")

    retour_thread['fetching_animation_text'] = None

    temp_actuelle = retour_thread['temperature'][0]
    couleur_temp_actuelle = retour_thread['temperature'][1]['couleur']
    shaking_etat_actuel = retour_thread['temperature'][1]['wiggle']
    pluie_actuelle = retour_thread['pourcent_pluie']
    detailed_info_actuelle = retour_thread['detailed_info']
    weather_icon_actuel = retour_thread['weather_icon']
    pistes_soir_actuel = retour_thread['pistes_soir']
    valeur_bitcoin_actuelle = retour_thread['valeur_bitcoin']
    # valeur_litecoin_actuelle = retour_thread['valeur_litecoin']
    # valeur_bitcoin_cash_actuelle = retour_thread['valeur_bitcoin_cash']
    valeur_ethereum_actuelle = retour_thread['valeur_ethereum']
    dict_data = {}

    internet_access = ping_this('http://google.com')

    if not internet_access:
        if not attempt_reconnection():
            return True

    retour_thread['fetching_animation_text'] = " "

    if get_forecast:
        try:
            print("Requesting forecast")

            retour_thread['detailed_info'] = "Géolocalisation..." if not retour_thread['geolocate_success'] else \
                retour_thread['city_name']
            retour_thread['temperature'][0] = None
            retour_thread['temperature'][1]['couleur'] = couleur_fond_inverse
            retour_thread['temperature'][1]['wiggle'] = 0
            retour_thread['weather_icon'] = ''

            if retour_thread['pourcent_pluie'] != ' ' or not retour_thread['geolocate_success']:
                retour_thread['pourcent_pluie'] = None

            if not retour_thread['geolocate_success']:
                response = urllib.request.urlopen("http://ipinfo.io/json",
                                                  timeout=60,
                                                  context=ssl_context)
                the_page = response.read()
                data = json.loads(the_page.decode('utf-8'))
                coordinates = data['loc'].split(',')
                coordinates[0], coordinates[1] = float(coordinates[0]), float(coordinates[1])

                city_list = []

                url_response = urllib.request.urlopen('https://dd.weather.gc.ca/citypage_weather/docs/site_list_fr.csv',
                                                      timeout=60,
                                                      context=ssl_context)

                csv_reader = csv.DictReader(url_response.read().decode('utf-8').splitlines()[1:])

                if not en_fonction:
                    return False

                for city in csv_reader:
                    if city['Code de province'] != 'HEF':
                        city['Latitude'] = float(city['Latitude'].replace('N', ''))
                        city['Longitude'] = -1 * float(city['Longitude'].replace('O', ''))
                        city['Distance'] = math.sqrt(
                            (coordinates[0] - city['Latitude']) ** 2.0 + (coordinates[1] - city['Longitude']) ** 2.0)
                        city_list.append(city)

                def city_distance(site):
                    return site['Distance']

                city_list.sort(key=city_distance)
                for city in city_list:
                    retour_thread['temperature'][0] = city['Noms français']
                    retour_thread['city_id'] = city['Codes']

                    # Québec
                    # url_response = urllib.request.urlopen('https://dd.weather.gc.ca/citypage_weather/xml/QC/s0000620_f.xml',
                    # Montmagny
                    # url_response = urllib.request.urlopen('https://dd.weather.gc.ca/citypage_weather/xml/QC/s0000334_f.xml',
                    # Automatique

                    # Québec
                    # dict_data = xmltodict.parse(b'<?xml version=\'1.0\' encoding=\'ISO-8859-1\'?>\n <siteData xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://dd.meteo.gc.ca/citypage_weather/schema/site.xsd">\n <license>https://dd.meteo.gc.ca/doc/LICENCE_GENERAL.txt</license>\n <dateTime name="xmlCreation" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>16</hour>\n <minute>37</minute>\n <timeStamp>20220321163700</timeStamp>\n <textSummary>21 mars 2022 16h37 UTC</textSummary>\n </dateTime>\n <dateTime name="xmlCreation" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>12</hour>\n <minute>37</minute>\n <timeStamp>20220321123700</timeStamp>\n <textSummary>21 mars 2022 12h37 HAE</textSummary>\n </dateTime>\n <location>\n <continent>Am\xe9rique du Nord</continent>\n <country code="ca">Canada</country>\n <province code="qc">Qu\xe9bec</province>\n <name code="s0000620" lat="46.82N" lon="71.22O">Qu\xe9bec</name>\n <region>Qu\xe9bec</region>\n </location>\n <warnings/>\n <currentConditions>\n <station code="yqb" lat="46.79N" lon="71.39O">A\xe9roport int. Lesage de Qu\xe9bec</station>\n <dateTime name="observation" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>16</hour>\n <minute>32</minute>\n <timeStamp>20220321163200</timeStamp>\n <textSummary>21 mars 2022 16h32 UTC</textSummary>\n </dateTime>\n <dateTime name="observation" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>12</hour>\n <minute>32</minute>\n <timeStamp>20220321123200</timeStamp>\n <textSummary>21 mars 2022 12h32 HAE</textSummary>\n </dateTime>\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="gif">03</iconCode>\n <temperature unitType="metric" units="C">-25.4</temperature>\n <dewpoint unitType="metric" units="C">-4.8</dewpoint>\n <pressure unitType="metric" units="kPa" change="0.01" tendency="\xe0 la baisse">101.0</pressure>\n <visibility unitType="metric" units="km">48.3</visibility>\n <relativeHumidity units="%">65</relativeHumidity>\n <wind>\n <speed unitType="metric" units="km/h">12</speed>\n <gust unitType="metric" units="km/h">28</gust>\n <direction>ONO</direction>\n <bearing units="degrees">300.0</bearing>\n </wind>\n </currentConditions>\n <forecastGroup>\n <dateTime name="forecastIssue" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>15</hour>\n <minute>30</minute>\n <timeStamp>20220321153000</timeStamp>\n <textSummary>21 mars 2022 15h30 UTC</textSummary>\n </dateTime>\n <dateTime name="forecastIssue" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>11</hour>\n <minute>30</minute>\n <timeStamp>20220321113000</timeStamp>\n <textSummary>21 mars 2022 11h30 HAE</textSummary>\n </dateTime>\n <regionalNormals>\n <textSummary>Minimum moins 6. Maximum plus 2.</textSummary>\n <temperature unitType="metric" units="C" class="high">2</temperature>\n <temperature unitType="metric" units="C" class="low">-6</temperature>\n </regionalNormals>\n <forecast>\n <period textForecastName="Aujourd\'hui">lundi</period>\n <textSummary>G\xe9n\xe9ralement nuageux avec 40 pour cent de probabilit\xe9 d\'averses de neige ou de pluie. Vents d\'ouest de 20 km/h avec rafales \xe0 40. Maximum plus 2. Indice UV de 3 ou mod\xe9r\xe9.</textSummary>\n <cloudPrecip>\n <textSummary>G\xe9n\xe9ralement nuageux avec 40 pour cent de probabilit\xe9 d\'averses de neige ou de pluie.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">07</iconCode>\n <pop units="%">0</pop>\n <textSummary>Possibilit\xe9 d\'averses de neige ou de pluie</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum plus 2.</textSummary>\n <temperature unitType="metric" units="C" class="high">2</temperature>\n </temperatures>\n <winds>\n <textSummary>Vents d\'ouest de 20 km/h avec rafales \xe0 40.</textSummary>\n <wind index="1" rank="major">\n <speed unitType="metric" units="km/h">20</speed>\n <gust unitType="metric" units="km/h">40</gust>\n <direction>O</direction>\n <bearing units="degrees">27</bearing>\n </wind>\n </winds>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="16" end="22"/>\n </precipitation>\n <uv category="mod\xe9r\xe9">\n <index>3</index>\n <textSummary>Indice UV de 3 ou mod\xe9r\xe9.</textSummary>\n </uv>\n <relativeHumidity units="%">55</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Ce soir et cette nuit">ce soir et cette nuit</period>\n <textSummary>G\xe9n\xe9ralement nuageux. Vents d\'ouest de 20 km/h avec rafales \xe0 40. Minimum moins 6. Refroidissement \xe9olien moins 13 au cours de la nuit.</textSummary>\n <cloudPrecip>\n <textSummary>G\xe9n\xe9ralement nuageux.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">33</iconCode>\n <pop units="%"/>\n <textSummary>G\xe9n\xe9ralement nuageux</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum moins 6.</textSummary>\n <temperature unitType="metric" units="C" class="low">-6</temperature>\n </temperatures>\n <winds>\n <textSummary>Vents d\'ouest de 20 km/h avec rafales \xe0 40.</textSummary>\n <wind index="1" rank="major">\n <speed unitType="metric" units="km/h">20</speed>\n <gust unitType="metric" units="km/h">40</gust>\n <direction>O</direction>\n <bearing units="degrees">27</bearing>\n </wind>\n </winds>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <windChill>\n <textSummary>Refroidissement \xe9olien moins 13 au cours de la nuit.</textSummary>\n <calculated unitType="metric" class="nuit">-13</calculated>\n <frostbite/>\n </windChill>\n <relativeHumidity units="%">55</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Mardi">mardi</period>\n <textSummary>G\xe9n\xe9ralement nuageux. Vents d\'ouest de 20 km/h avec rafales \xe0 40. Maximum z\xe9ro. Refroidissement \xe9olien moins 13 le matin. Indice UV de 2 ou bas.</textSummary>\n <cloudPrecip>\n <textSummary>G\xe9n\xe9ralement nuageux.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">03</iconCode>\n <pop units="%"/>\n <textSummary>G\xe9n\xe9ralement nuageux</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum z\xe9ro.</textSummary>\n <temperature unitType="metric" units="C" class="high">0</temperature>\n </temperatures>\n <winds>\n <textSummary>Vents d\'ouest de 20 km/h avec rafales \xe0 40.</textSummary>\n <wind index="1" rank="major">\n <speed unitType="metric" units="km/h">20</speed>\n <gust unitType="metric" units="km/h">40</gust>\n <direction>O</direction>\n <bearing units="degrees">27</bearing>\n </wind>\n </winds>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <windChill>\n <textSummary>Refroidissement \xe9olien moins 13 le matin.</textSummary>\n <calculated unitType="metric" class="matin">-13</calculated>\n <frostbite/>\n </windChill>\n <uv category="bas">\n <index>2</index>\n <textSummary>Indice UV de 2 ou bas.</textSummary>\n </uv>\n <relativeHumidity units="%">55</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Mardi soir et nuit">mardi soir et nuit</period>\n <textSummary>D\xe9gag\xe9. Minimum moins 8.</textSummary>\n <cloudPrecip>\n <textSummary>D\xe9gag\xe9.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">30</iconCode>\n <pop units="%"/>\n <textSummary>D\xe9gag\xe9</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum moins 8.</textSummary>\n <temperature unitType="metric" units="C" class="low">-8</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">85</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Mercredi">mercredi</period>\n <textSummary>Ensoleill\xe9. Maximum plus 3.</textSummary>\n <cloudPrecip>\n <textSummary>Ensoleill\xe9.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">00</iconCode>\n <pop units="%"/>\n <textSummary>Ensoleill\xe9</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum plus 3.</textSummary>\n <temperature unitType="metric" units="C" class="high">3</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">60</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Mercredi soir et nuit">mercredi soir et nuit</period>\n <textSummary>Nuageux. Minimum moins 3.</textSummary>\n <cloudPrecip>\n <textSummary>Nuageux.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">10</iconCode>\n <pop units="%"/>\n <textSummary>Nuageux</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum moins 3.</textSummary>\n <temperature unitType="metric" units="C" class="low">-3</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">75</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Jeudi">jeudi</period>\n <textSummary>Neige intermittente. Maximum plus 1.</textSummary>\n <cloudPrecip>\n <textSummary>Neige intermittente.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">16</iconCode>\n <pop units="%"/>\n <textSummary>Neige intermittente</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum plus 1.</textSummary>\n <temperature unitType="metric" units="C" class="high">1</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="87" end="94">neige</precipType>\n </precipitation>\n <relativeHumidity units="%">80</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Jeudi soir et nuit">jeudi soir et nuit</period>\n <textSummary>Neige. Minimum moins 1.</textSummary>\n <cloudPrecip>\n <textSummary>Neige.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">17</iconCode>\n <pop units="%"/>\n <textSummary>Neige</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum moins 1.</textSummary>\n <temperature unitType="metric" units="C" class="low">-1</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="94" end="106">neige</precipType>\n </precipitation>\n <relativeHumidity units="%">100</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Vendredi">vendredi</period>\n <textSummary>Neige ou pluie. Maximum plus 3.</textSummary>\n <cloudPrecip>\n <textSummary>Neige ou pluie.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">15</iconCode>\n <pop units="%"/>\n <textSummary>Neige ou pluie</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum plus 3.</textSummary>\n <temperature unitType="metric" units="C" class="high">3</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="106" end="111">neige</precipType>\n <precipType start="111" end="114">pluie et neige</precipType>\n <precipType start="114" end="118">pluie</precipType>\n </precipitation>\n <relativeHumidity units="%">100</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Vendredi soir et nuit">vendredi soir et nuit</period>\n <textSummary>Pluie ou neige. Minimum plus 1.</textSummary>\n <cloudPrecip>\n <textSummary>Pluie ou neige.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">15</iconCode>\n <pop units="%"/>\n <textSummary>Pluie ou neige</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum plus 1.</textSummary>\n <temperature unitType="metric" units="C" class="low">1</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="118" end="126">pluie</precipType>\n <precipType start="126" end="129">pluie et neige</precipType>\n <precipType start="129" end="130">neige</precipType>\n </precipitation>\n <relativeHumidity units="%">100</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Samedi">samedi</period>\n <textSummary>Nuageux avec 60 pour cent de probabilit\xe9 d\'averses de neige ou de pluie. Maximum plus 5.</textSummary>\n <cloudPrecip>\n <textSummary>Nuageux avec 60 pour cent de probabilit\xe9 d\'averses de neige ou de pluie.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">15</iconCode>\n <pop units="%">60</pop>\n <textSummary>Possibilit\xe9 d\'averses de neige ou de pluie</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum plus 5.</textSummary>\n <temperature unitType="metric" units="C" class="high">5</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="130" end="132">neige</precipType>\n <precipType start="138" end="142">pluie</precipType>\n </precipitation>\n <relativeHumidity units="%">70</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Samedi soir et nuit">samedi soir et nuit</period>\n <textSummary>Nuageux avec 30 pour cent de probabilit\xe9 d\'averses de pluie ou de neige. Minimum moins 7.</textSummary>\n <cloudPrecip>\n <textSummary>Nuageux avec 30 pour cent de probabilit\xe9 d\'averses de pluie ou de neige.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">15</iconCode>\n <pop units="%">30</pop>\n <textSummary>Possibilit\xe9 d\'averses de pluie ou de neige</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum moins 7.</textSummary>\n <temperature unitType="metric" units="C" class="low">-7</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="142" end="147">pluie</precipType>\n <precipType start="147" end="150">neige</precipType>\n </precipitation>\n <relativeHumidity units="%">65</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Dimanche">dimanche</period>\n <textSummary>Alternance de soleil et de nuages. Maximum moins 2.</textSummary>\n <cloudPrecip>\n <textSummary>Alternance de soleil et de nuages.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">02</iconCode>\n <pop units="%"/>\n <textSummary>Alternance de soleil et de nuages</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum moins 2.</textSummary>\n <temperature unitType="metric" units="C" class="high">-2</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">40</relativeHumidity>\n </forecast>\n </forecastGroup>\n <hourlyForecastGroup>\n <dateTime name="forecastIssue" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>15</hour>\n <minute>30</minute>\n <timeStamp>20220321153000</timeStamp>\n <textSummary>21 mars 2022 15h30 UTC</textSummary>\n </dateTime>\n <dateTime name="forecastIssue" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>11</hour>\n <minute>30</minute>\n <timeStamp>20220321113000</timeStamp>\n <textSummary>21 mars 2022 11h30 HAE</textSummary>\n </dateTime>\n <hourlyForecast dateTimeUTC="202203211700">\n <condition>Possibilit\xe9 d\'averses de neige ou de pluie</condition>\n <iconCode format="png">07</iconCode>\n <temperature unitType="metric" units="C">2</temperature>\n <lop category="Basse" units="%">40</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203211800">\n <condition>Possibilit\xe9 d\'averses de neige ou de pluie</condition>\n <iconCode format="png">07</iconCode>\n <temperature unitType="metric" units="C">2</temperature>\n <lop category="Basse" units="%">40</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203211900">\n <condition>Possibilit\xe9 d\'averses de neige ou de pluie</condition>\n <iconCode format="png">07</iconCode>\n <temperature unitType="metric" units="C">2</temperature>\n <lop category="Basse" units="%">40</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203212000">\n <condition>Possibilit\xe9 d\'averses de neige ou de pluie</condition>\n <iconCode format="png">07</iconCode>\n <temperature unitType="metric" units="C">1</temperature>\n <lop category="Basse" units="%">40</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203212100">\n <condition>Possibilit\xe9 d\'averses de neige ou de pluie</condition>\n <iconCode format="png">07</iconCode>\n <temperature unitType="metric" units="C">1</temperature>\n <lop category="Basse" units="%">40</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203212200">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">0</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203212300">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">0</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203220000">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">-1</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-7</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203220100">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">-1</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-7</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203220200">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">-2</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-7</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203220300">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">-2</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-8</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203220400">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">-3</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-9</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203220500">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">-4</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-10</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203220600">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">-5</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-12</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203220700">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">-5</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-12</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203220800">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">-6</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-12</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203220900">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">-6</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-13</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203221000">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">33</iconCode>\n <temperature unitType="metric" units="C">-6</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-13</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203221100">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">-6</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-13</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203221200">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">-6</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-13</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203221300">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">-5</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-12</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203221400">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">-5</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-11</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203221500">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">-4</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-10</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202203221600">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">-3</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric">-9</windChill>\n <humidex unitType="metric"/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Ouest">O</direction>\n <gust unitType="metric" units="km/h">40</gust>\n </wind>\n </hourlyForecast>\n </hourlyForecastGroup>\n <yesterdayConditions>\n <temperature unitType="metric" units="C" class="high">2.8</temperature>\n <temperature unitType="metric" units="C" class="low">-0.3</temperature>\n <precip unitType="metric" units="mm">7.4</precip>\n </yesterdayConditions>\n <riseSet>\n <disclaimer>Les heures de lever et coucher du soleil sont une estimation seulement et peuvent \xeatre diff\xe9rentes des heures officielles de lever et coucher du soleil disponibles ici ( http://hia-iha.nrc-cnrc.gc.ca/sunrise_f.html )</disclaimer>\n <dateTime name="sunrise" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>10</hour>\n <minute>46</minute>\n <timeStamp>20220321104600</timeStamp>\n <textSummary>21 mars 2022 10h46 UTC</textSummary>\n </dateTime>\n <dateTime name="sunrise" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>06</hour>\n <minute>46</minute>\n <timeStamp>20220321064600</timeStamp>\n <textSummary>21 mars 2022 06h46 HAE</textSummary>\n </dateTime>\n <dateTime name="sunset" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>22</hour>\n <minute>58</minute>\n <timeStamp>20220321225800</timeStamp>\n <textSummary>21 mars 2022 22h58 UTC</textSummary>\n </dateTime>\n <dateTime name="sunset" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="mars">03</month>\n <day name="lundi">21</day>\n <hour>18</hour>\n <minute>58</minute>\n <timeStamp>20220321185800</timeStamp>\n <textSummary>21 mars 2022 18h58 HAE</textSummary>\n </dateTime>\n </riseSet>\n <almanac>\n <temperature class="extremeMax" period="1993-2021" unitType="metric" units="C" year="2012">18.3</temperature>\n <temperature class="extremeMin" period="1993-2021" unitType="metric" units="C" year="2007">-19.9</temperature>\n <temperature class="normalMax" unitType="metric" units="C"/>\n <temperature class="normalMin" unitType="metric" units="C"/>\n <temperature class="normalMean" unitType="metric" units="C"/>\n <precipitation class="extremeRainfall" period="1993-2013" unitType="metric" units="mm" year="1993">0.0</precipitation>\n <precipitation class="extremeSnowfall" period="1993-2013" unitType="metric" units="cm" year="1993">8.8</precipitation>\n <precipitation class="extremePrecipitation" period="1993-2021" unitType="metric" units="mm" year="2003">10.4</precipitation>\n <precipitation class="extremeSnowOnGround" period="1993-2021" unitType="metric" units="cm" year="2008">97.0</precipitation>\n <pop units="%"/>\n </almanac>\n </siteData>\n\n')
                    # Montmagny
                    # dict_data = xmltodict.parse(b'<?xml version=\'1.0\' encoding=\'ISO-8859-1\'?>\n <siteData xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://dd.meteo.gc.ca/citypage_weather/schema/site.xsd">\n <license>https://dd.meteo.gc.ca/doc/LICENCE_GENERAL.txt</license>\n <dateTime name="xmlCreation" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="lundi">08</day>\n <hour>23</hour>\n <minute>08</minute>\n <timeStamp>20220808230800</timeStamp>\n <textSummary>08 ao\xfbt 2022 23h08 UTC</textSummary>\n </dateTime>\n <dateTime name="xmlCreation" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="lundi">08</day>\n <hour>19</hour>\n <minute>08</minute>\n <timeStamp>20220808190800</timeStamp>\n <textSummary>08 ao\xfbt 2022 19h08 HAE</textSummary>\n </dateTime>\n <location>\n <continent>Am\xe9rique du Nord</continent>\n <country code="ca">Canada</country>\n <province code="qc">Qu\xe9bec</province>\n <name code="s0000334" lat="46.98N" lon="70.55O">Montmagny</name>\n <region>Montmagny - L\'Islet</region>\n </location>\n <warnings/>\n <currentConditions>\n <station code="wst" lat="47.36N" lon="70.03O">La Pocati\xe8re</station>\n <dateTime name="observation" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="lundi">08</day>\n <hour>23</hour>\n <minute>00</minute>\n <timeStamp>20220808230000</timeStamp>\n <textSummary>08 ao\xfbt 2022 23h00 UTC</textSummary>\n </dateTime>\n <dateTime name="observation" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="lundi">08</day>\n <hour>19</hour>\n <minute>00</minute>\n <timeStamp>20220808190000</timeStamp>\n <textSummary>08 ao\xfbt 2022 19h00 HAE</textSummary>\n </dateTime>\n <condition/>\n <iconCode format="gif"/>\n <temperature unitType="metric" units="C">14.9</temperature>\n <dewpoint unitType="metric" units="C">12.9</dewpoint>\n <pressure unitType="metric" units="kPa" change="0.13" tendency="\xe0 la baisse">101.3</pressure>\n <visibility unitType="metric" units="km"/>\n <relativeHumidity units="%">87</relativeHumidity>\n <wind>\n <speed unitType="metric" units="km/h">5</speed>\n <gust unitType="metric" units="km/h"/>\n <direction>SE</direction>\n <bearing units="degrees">133.2</bearing>\n </wind>\n </currentConditions>\n <forecastGroup>\n <dateTime name="forecastIssue" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="lundi">08</day>\n <hour>19</hour>\n <minute>45</minute>\n <timeStamp>20220808194500</timeStamp>\n <textSummary>08 ao\xfbt 2022 19h45 UTC</textSummary>\n </dateTime>\n <dateTime name="forecastIssue" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="lundi">08</day>\n <hour>15</hour>\n <minute>45</minute>\n <timeStamp>20220808154500</timeStamp>\n <textSummary>08 ao\xfbt 2022 15h45 HAE</textSummary>\n </dateTime>\n <regionalNormals>\n <textSummary>Minimum 11. Maximum 23.</textSummary>\n <temperature unitType="metric" units="C" class="high">23</temperature>\n <temperature unitType="metric" units="C" class="low">11</temperature>\n </regionalNormals>\n <forecast>\n <period textForecastName="Ce soir et cette nuit">ce soir et cette nuit</period>\n <textSummary>Pluie. Hauteur pr\xe9vue de 30 mm. Vents devenant du nord-est \xe0 30 km/h ce soir. Minimum 12.</textSummary>\n <cloudPrecip>\n <textSummary>Pluie.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">12</iconCode>\n <pop units="%"/>\n <textSummary>Pluie</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum 12.</textSummary>\n <temperature unitType="metric" units="C" class="low">12</temperature>\n </temperatures>\n <winds>\n <textSummary>Vents devenant du nord-est \xe0 30 km/h ce soir.</textSummary>\n <wind index="1" rank="minor">\n <speed unitType="metric" units="km/h">10</speed>\n <gust unitType="metric" units="km/h">00</gust>\n <direction>NE</direction>\n <bearing units="degrees">04</bearing>\n </wind>\n <wind index="2" rank="major">\n <speed unitType="metric" units="km/h">20</speed>\n <gust unitType="metric" units="km/h">00</gust>\n <direction>NE</direction>\n <bearing units="degrees">04</bearing>\n </wind>\n <wind index="3" rank="major">\n <speed unitType="metric" units="km/h">30</speed>\n <gust unitType="metric" units="km/h">00</gust>\n <direction>NE</direction>\n <bearing units="degrees">04</bearing>\n </wind>\n </winds>\n <humidex/>\n <precipitation>\n <textSummary>Hauteur pr\xe9vue de 30 mm.</textSummary>\n <precipType start="20" end="34">pluie</precipType>\n <accumulation>\n <name>pluie</name>\n <amount unitType="metric" units="mm">30</amount>\n </accumulation>\n </precipitation>\n <relativeHumidity units="%">100</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Mardi">mardi</period>\n <textSummary>Pluie intermittente m\xeal\xe9e de bruine cessant le matin. Nuageux par la suite. Vents du nord-est de 30 km/h. Maximum 18. Indice UV de 5 ou mod\xe9r\xe9.</textSummary>\n <cloudPrecip>\n <textSummary>Pluie intermittente m\xeal\xe9e de bruine cessant le matin. Nuageux par la suite.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">12</iconCode>\n <pop units="%"/>\n <textSummary>Pluie intermittente ou bruine</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum 18.</textSummary>\n <temperature unitType="metric" units="C" class="high">18</temperature>\n </temperatures>\n <winds>\n <textSummary>Vents du nord-est de 30 km/h.</textSummary>\n <wind index="1" rank="major">\n <speed unitType="metric" units="km/h">30</speed>\n <gust unitType="metric" units="km/h">00</gust>\n <direction>NE</direction>\n <bearing units="degrees">04</bearing>\n </wind>\n <wind index="2" rank="major">\n <speed unitType="metric" units="km/h">20</speed>\n <gust unitType="metric" units="km/h">00</gust>\n <direction>NE</direction>\n <bearing units="degrees">04</bearing>\n </wind>\n </winds>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="34" end="38">pluie et bruine</precipType>\n </precipitation>\n <uv category="mod\xe9r\xe9">\n <index>5</index>\n <textSummary>Indice UV de 5 ou mod\xe9r\xe9.</textSummary>\n </uv>\n <relativeHumidity units="%">80</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Mardi soir et nuit">mardi soir et nuit</period>\n <textSummary>G\xe9n\xe9ralement nuageux. Minimum 13.</textSummary>\n <cloudPrecip>\n <textSummary>G\xe9n\xe9ralement nuageux.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">33</iconCode>\n <pop units="%"/>\n <textSummary>G\xe9n\xe9ralement nuageux</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum 13.</textSummary>\n <temperature unitType="metric" units="C" class="low">13</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">95</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Mercredi">mercredi</period>\n <textSummary>Nuageux. Maximum 23.</textSummary>\n <cloudPrecip>\n <textSummary>Nuageux.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">10</iconCode>\n <pop units="%"/>\n <textSummary>Nuageux</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum 23.</textSummary>\n <temperature unitType="metric" units="C" class="high">23</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">70</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Mercredi soir et nuit">mercredi soir et nuit</period>\n <textSummary>Nuageux. Minimum 17.</textSummary>\n <cloudPrecip>\n <textSummary>Nuageux.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">10</iconCode>\n <pop units="%"/>\n <textSummary>Nuageux</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum 17.</textSummary>\n <temperature unitType="metric" units="C" class="low">17</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">80</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Jeudi">jeudi</period>\n <textSummary>Alternance de soleil et de nuages. Maximum 25.</textSummary>\n <cloudPrecip>\n <textSummary>Alternance de soleil et de nuages.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">02</iconCode>\n <pop units="%"/>\n <textSummary>Alternance de soleil et de nuages</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum 25.</textSummary>\n <temperature unitType="metric" units="C" class="high">25</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">75</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Jeudi soir et nuit">jeudi soir et nuit</period>\n <textSummary>Passages nuageux. Minimum 16.</textSummary>\n <cloudPrecip>\n <textSummary>Passages nuageux.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">32</iconCode>\n <pop units="%"/>\n <textSummary>Passages nuageux</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum 16.</textSummary>\n <temperature unitType="metric" units="C" class="low">16</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">95</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Vendredi">vendredi</period>\n <textSummary>Alternance de soleil et de nuages. Maximum 19.</textSummary>\n <cloudPrecip>\n <textSummary>Alternance de soleil et de nuages.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">02</iconCode>\n <pop units="%"/>\n <textSummary>Alternance de soleil et de nuages</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum 19.</textSummary>\n <temperature unitType="metric" units="C" class="high">19</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">75</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Vendredi soir et nuit">vendredi soir et nuit</period>\n <textSummary>Passages nuageux. Minimum 10.</textSummary>\n <cloudPrecip>\n <textSummary>Passages nuageux.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">32</iconCode>\n <pop units="%"/>\n <textSummary>Passages nuageux</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum 10.</textSummary>\n <temperature unitType="metric" units="C" class="low">10</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">95</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Samedi">samedi</period>\n <textSummary>Alternance de soleil et de nuages. Maximum 24.</textSummary>\n <cloudPrecip>\n <textSummary>Alternance de soleil et de nuages.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">02</iconCode>\n <pop units="%"/>\n <textSummary>Alternance de soleil et de nuages</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum 24.</textSummary>\n <temperature unitType="metric" units="C" class="high">24</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">50</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Samedi soir et nuit">samedi soir et nuit</period>\n <textSummary>Passages nuageux. Minimum 11.</textSummary>\n <cloudPrecip>\n <textSummary>Passages nuageux.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">32</iconCode>\n <pop units="%"/>\n <textSummary>Passages nuageux</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Minimum 11.</textSummary>\n <temperature unitType="metric" units="C" class="low">11</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">95</relativeHumidity>\n </forecast>\n <forecast>\n <period textForecastName="Dimanche">dimanche</period>\n <textSummary>Alternance de soleil et de nuages. Maximum 22.</textSummary>\n <cloudPrecip>\n <textSummary>Alternance de soleil et de nuages.</textSummary>\n </cloudPrecip>\n <abbreviatedForecast>\n <iconCode format="gif">02</iconCode>\n <pop units="%"/>\n <textSummary>Alternance de soleil et de nuages</textSummary>\n </abbreviatedForecast>\n <temperatures>\n <textSummary>Maximum 22.</textSummary>\n <temperature unitType="metric" units="C" class="high">22</temperature>\n </temperatures>\n <winds/>\n <humidex/>\n <precipitation>\n <textSummary/>\n <precipType start="" end=""/>\n </precipitation>\n <relativeHumidity units="%">55</relativeHumidity>\n </forecast>\n </forecastGroup>\n <hourlyForecastGroup>\n <dateTime name="forecastIssue" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="lundi">08</day>\n <hour>19</hour>\n <minute>45</minute>\n <timeStamp>20220808194500</timeStamp>\n <textSummary>08 ao\xfbt 2022 19h45 UTC</textSummary>\n </dateTime>\n <dateTime name="forecastIssue" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="lundi">08</day>\n <hour>15</hour>\n <minute>45</minute>\n <timeStamp>20220808154500</timeStamp>\n <textSummary>08 ao\xfbt 2022 15h45 HAE</textSummary>\n </dateTime>\n <hourlyForecast dateTimeUTC="202208090000">\n <condition>Pluie</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">14</temperature>\n <lop category="\xc9lev\xe9e" units="%">100</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208090100">\n <condition>Pluie</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">14</temperature>\n <lop category="\xc9lev\xe9e" units="%">100</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208090200">\n <condition>Pluie</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">13</temperature>\n <lop category="\xc9lev\xe9e" units="%">100</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208090300">\n <condition>Pluie</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">13</temperature>\n <lop category="\xc9lev\xe9e" units="%">100</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208090400">\n <condition>Pluie</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">13</temperature>\n <lop category="\xc9lev\xe9e" units="%">100</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208090500">\n <condition>Pluie</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">13</temperature>\n <lop category="\xc9lev\xe9e" units="%">100</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208090600">\n <condition>Pluie</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">13</temperature>\n <lop category="\xc9lev\xe9e" units="%">100</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">30</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208090700">\n <condition>Pluie</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">13</temperature>\n <lop category="\xc9lev\xe9e" units="%">100</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">30</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208090800">\n <condition>Pluie</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">12</temperature>\n <lop category="\xc9lev\xe9e" units="%">100</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">30</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208090900">\n <condition>Pluie</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">12</temperature>\n <lop category="\xc9lev\xe9e" units="%">100</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">30</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208091000">\n <condition>Pluie intermittente ou bruine</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">12</temperature>\n <lop category="\xc9lev\xe9e" units="%">80</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">30</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208091100">\n <condition>Pluie intermittente ou bruine</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">13</temperature>\n <lop category="\xc9lev\xe9e" units="%">80</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">30</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208091200">\n <condition>Pluie intermittente ou bruine</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">13</temperature>\n <lop category="\xc9lev\xe9e" units="%">80</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208091300">\n <condition>Pluie intermittente ou bruine</condition>\n <iconCode format="png">12</iconCode>\n <temperature unitType="metric" units="C">13</temperature>\n <lop category="\xc9lev\xe9e" units="%">80</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208091400">\n <condition>Couvert</condition>\n <iconCode format="png">10</iconCode>\n <temperature unitType="metric" units="C">14</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208091500">\n <condition>Couvert</condition>\n <iconCode format="png">10</iconCode>\n <temperature unitType="metric" units="C">14</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208091600">\n <condition>Couvert</condition>\n <iconCode format="png">10</iconCode>\n <temperature unitType="metric" units="C">14</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208091700">\n <condition>Couvert</condition>\n <iconCode format="png">10</iconCode>\n <temperature unitType="metric" units="C">15</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208091800">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">15</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208091900">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">16</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208092000">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">17</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208092100">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">18</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">20</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208092200">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">17</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">10</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n <hourlyForecast dateTimeUTC="202208092300">\n <condition>G\xe9n\xe9ralement nuageux</condition>\n <iconCode format="png">03</iconCode>\n <temperature unitType="metric" units="C">17</temperature>\n <lop category="Nulle" units="%">0</lop>\n <windChill unitType="metric"/>\n <humidex/>\n <wind>\n <speed unitType="metric" units="km/h">10</speed>\n <direction windDirFull="Nord-est">NE</direction>\n <gust unitType="metric" units="km/h"/>\n </wind>\n </hourlyForecast>\n </hourlyForecastGroup>\n <yesterdayConditions>\n <temperature unitType="metric" units="C" class="high">28.2</temperature>\n <temperature unitType="metric" units="C" class="low">13.2</temperature>\n <precip unitType="metric" units="mm">0.0</precip>\n </yesterdayConditions>\n <riseSet>\n <disclaimer>Les heures de lever et coucher du soleil sont une estimation seulement et peuvent \xeatre diff\xe9rentes des heures officielles de lever et coucher du soleil disponibles ici ( http://hia-iha.nrc-cnrc.gc.ca/sunrise_f.html )</disclaimer>\n <dateTime name="sunrise" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="lundi">08</day>\n <hour>09</hour>\n <minute>30</minute>\n <timeStamp>20220808093000</timeStamp>\n <textSummary>08 ao\xfbt 2022 09h30 UTC</textSummary>\n </dateTime>\n <dateTime name="sunrise" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="lundi">08</day>\n <hour>05</hour>\n <minute>30</minute>\n <timeStamp>20220808053000</timeStamp>\n <textSummary>08 ao\xfbt 2022 05h30 HAE</textSummary>\n </dateTime>\n <dateTime name="sunset" zone="UTC" UTCOffset="0">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="mardi">09</day>\n <hour>00</hour>\n <minute>05</minute>\n <timeStamp>20220809000500</timeStamp>\n <textSummary>09 ao\xfbt 2022 00h05 UTC</textSummary>\n </dateTime>\n <dateTime name="sunset" zone="HAE" UTCOffset="-4">\n <year>2022</year>\n <month name="ao\xfbt">08</month>\n <day name="lundi">08</day>\n <hour>20</hour>\n <minute>05</minute>\n <timeStamp>20220808200500</timeStamp>\n <textSummary>08 ao\xfbt 2022 20h05 HAE</textSummary>\n </dateTime>\n </riseSet>\n <almanac>\n <temperature class="extremeMax" period="1996-2021" unitType="metric" units="C" year="1998">31.1</temperature>\n <temperature class="extremeMin" period="1996-2021" unitType="metric" units="C" year="2009">7.9</temperature>\n <temperature class="normalMax" unitType="metric" units="C"/>\n <temperature class="normalMin" unitType="metric" units="C"/>\n <temperature class="normalMean" unitType="metric" units="C"/>\n <precipitation class="extremeRainfall" period="-" unitType="metric" units="mm" year=""/>\n <precipitation class="extremeSnowfall" period="-" unitType="metric" units="cm" year=""/>\n <precipitation class="extremePrecipitation" period="1996-2021" unitType="metric" units="mm" year="2019">57.7</precipitation>\n <precipitation class="extremeSnowOnGround" period="-" unitType="metric" units="cm" year=""/>\n <pop units="%"/>\n </almanac>\n </siteData>\n\n')

                    start_time = time.time()
                    sleep_time = 0.5

                    try:
                        url_response = urllib.request.urlopen(
                            'https://dd.weather.gc.ca/citypage_weather/xml/QC/' + retour_thread['city_id'] + '_f.xml',
                            timeout=60,
                            context=ssl_context)
                        dict_data = xmltodict.parse(url_response.read())
                        url_response.close()
                        end_time = (time.time() - start_time)
                        sleep_time = sleep_time - end_time if end_time <= sleep_time else 0
                    except urllib.error.HTTPError:
                        time.sleep(sleep_time)
                        continue

                    if not en_fonction:
                        return False

                    if dict_data['siteData']['currentConditions']:
                        detailed_info = dict_data['siteData']['currentConditions']['condition']
                        weather_icon = dict_data['siteData']['currentConditions']['iconCode']

                        if '#text' not in weather_icon or not detailed_info:
                            time.sleep(sleep_time)
                        else:
                            retour_thread['detailed_info'] = 'Location sélectionnée'
                            retour_thread['weather_icon'] = 'checkmark.png'
                            retour_thread['pourcent_pluie'] = ' '
                            retour_thread['geolocate_success'] = True
                            print('Geolocated successfully')

                            if detailed_info:
                                for animation in weather_animations:
                                    if animation in detailed_info.lower():
                                        retour_thread['weather_animation'] = animation
                                        break
                                    else:
                                        retour_thread['weather_animation'] = ''

                            time.sleep(1)
                            break
                    else:
                        time.sleep(sleep_time)

            else:
                url_response = urllib.request.urlopen(
                    'https://dd.weather.gc.ca/citypage_weather/xml/QC/' + retour_thread['city_id'] + '_f.xml',
                    timeout=60,
                    context=ssl_context)
                dict_data = xmltodict.parse(url_response.read())
                url_response.close()

                if not en_fonction:
                    return False

            detailed_info = dict_data['siteData']['currentConditions']['condition']
            weather_icon = dict_data['siteData']['currentConditions']['iconCode']
            temperature = dict_data['siteData']['currentConditions']['temperature']['#text']
            pourcentage_pluie = dict_data['siteData']['forecastGroup']['forecast'][0]['abbreviatedForecast']['pop']
            retour_thread['city_name'] = dict_data['siteData']['location']['name']['#text']

            if '#text' in pourcentage_pluie:
                pourcentage_pluie = pourcentage_pluie['#text']
            else:
                pourcentage_pluie = 0

            if '#text' in weather_icon:
                weather_icon = weather_icon['#text']
            else:
                weather_icon = -1

            casted_temperature = float(temperature)

            shaking_etat_actuel = 0

            if casted_temperature <= -15:
                # fait frette
                couleur_temperature = [102, 255, 255]

                if casted_temperature <= -18:
                    shaking_etat_actuel = abs(casted_temperature + 17) / 2.0
            elif casted_temperature >= 20:
                # fait chaud
                if casted_temperature > 30:
                    niveau_vert = 68
                else:
                    niveau_vert = int((30 - casted_temperature) * 18.7) + 68

                couleur_temperature = [255, niveau_vert, 68]
            else:
                couleur_temperature = couleur_fond_inverse

            if int(pourcentage_pluie) > 0:
                pourcentage_pluie += '%'
            else:
                pourcentage_pluie = ' '

            if detailed_info:
                for animation in weather_animations:
                    if animation in detailed_info.lower():
                        retour_thread['weather_animation'] = animation
                        break
                    else:
                        retour_thread['weather_animation'] = ''

            detailed_info_actuelle = detailed_info if detailed_info else retour_thread['city_name']
            temp_actuelle = temperature + '°C'
            couleur_temp_actuelle = couleur_temperature
            pluie_actuelle = pourcentage_pluie
            weather_icon_actuel = str(weather_icon) + '.png'

            retour_thread['detailed_info'] = detailed_info_actuelle
            retour_thread['temperature'][0] = temp_actuelle
            retour_thread['temperature'][1]['couleur'] = couleur_temp_actuelle
            retour_thread['temperature'][1]['wiggle'] = shaking_etat_actuel
            retour_thread['pourcent_pluie'] = pluie_actuelle
            retour_thread['weather_icon'] = weather_icon_actuel

            if ClockSettings.FETCH_RELAIS_DATA:
                print('Requesting ski trail data')
                retour_thread['pistes_soir'] = None

                url_response = urllib.request.urlopen(
                    'https://www.skirelais.com/montagne/pistes-conditions-de-neige/',
                    timeout=60,
                    context=ssl_context)

                data = url_response.read().decode('utf-8').replace('\t', '').replace('\n', '')
                url_response.close()
                index = data.find('<td>Ouverture de soir</td>') + len('<td>Ouverture de soir</td>')
                pistes_soir_actuel = re.search("<span>([\d]+\/[\d]+)<span>", data[index:index + 21]).group(1)

                retour_thread['pistes_soir'] = pistes_soir_actuel

        except ValueError:
            retour_thread['detailed_info'] = detailed_info_actuelle
            retour_thread['temperature'][0] = temp_actuelle
            retour_thread['temperature'][1]['couleur'] = couleur_temp_actuelle
            retour_thread['temperature'][1]['wiggle'] = shaking_etat_actuel
            retour_thread['pourcent_pluie'] = pluie_actuelle
            retour_thread['weather_icon'] = weather_icon_actuel
            retour_thread['pistes_soir'] = pistes_soir_actuel

        except Exception as erreur:
            # raise erreur
            print(erreur)
            retour_thread['detailed_info'] = str(erreur)
            retour_thread['temperature'][0] = "Erreur"
            retour_thread['temperature'][1]['couleur'] = couleur_fond_inverse
            retour_thread['temperature'][1]['wiggle'] = 0
            retour_thread['pourcent_pluie'] = ":("
            retour_thread['weather_icon'] = ''
            retour_thread['pistes_soir'] = pistes_soir_actuel
            time.sleep(3)
            retour_thread['detailed_info'] = detailed_info_actuelle
            retour_thread['temperature'][0] = temp_actuelle
            retour_thread['temperature'][1]['couleur'] = couleur_temp_actuelle
            retour_thread['temperature'][1]['wiggle'] = shaking_etat_actuel
            retour_thread['pourcent_pluie'] = pluie_actuelle
            retour_thread['weather_icon'] = weather_icon_actuel

    # retour_thread['thread_en_cours'] = False
    # get_data(retour_thread, get_forecast=True)
    # return True

    try:
        """
		print("Requesting litecoin value")
		retour_thread['valeur_litecoin'] = None
		response = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=CAD", timeout=60, context=ssl_context)
		the_page = response.read()
		data = json.loads(the_page.decode('utf-8'))
		valeur_float_litecoin = data['CAD']
		valeur_litecoin = str(round(valeur_float_litecoin, 2)) + "$"
		retour_thread['valeur_litecoin'] = valeur_litecoin
		valeur_litecoin_actuelle = valeur_litecoin
		time.sleep(0.1)
		"""
        print("Requesting bitcoin value")
        retour_thread['valeur_bitcoin'] = None
        response = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=CAD", timeout=60,
                                          context=ssl_context)
        the_page = response.read()
        data = json.loads(the_page.decode('utf-8'))
        valeur_float_bitcoin = data['CAD']
        valeur_bitcoin = str(round(valeur_float_bitcoin, 2)) + "$"
        retour_thread['valeur_bitcoin'] = valeur_bitcoin
        valeur_bitcoin_actuelle = valeur_bitcoin

        if not en_fonction:
            return False

        print("Requesting ethereum value")
        retour_thread['valeur_ethereum'] = None
        response = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=CAD", timeout=60,
                                          context=ssl_context)
        the_page = response.read()
        data = json.loads(the_page.decode('utf-8'))
        valeur_float_ethereum = data['CAD']
        valeur_ethereum = str(round(valeur_float_ethereum, 2)) + "$"

        float_mined_ether = 2.19112
        mined_ether = str('{:.5f}'.format(round(float_mined_ether, 5))) + ' ETH'
        valeur_mined_ether = round(float_mined_ether * valeur_float_ethereum, 2)
        valeur_mined_ether = str(valeur_mined_ether) + '$ - ' + str(round(valeur_mined_ether / 80, 1)) + '%'

        retour_thread['ethermine_data'] = valeur_mined_ether
        retour_thread['valeur_ethereum'] = valeur_ethereum
        valeur_ethereum_actuelle = valeur_ethereum
        time.sleep(0.1)

        if not en_fonction:
            return False
        """
		print("Requesting bitcoin cash value")
		retour_thread['valeur_bitcoin_cash'] = None
		response = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=BCH&tsyms=CAD", timeout=60, context=ssl_context)
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
        # retour_thread['valeur_litecoin'] = "Erreur"
        retour_thread['valeur_ethereum'] = "Erreur"
        # retour_thread['valeur_bitcoin_cash'] = "Erreur"
        retour_thread['valeur_bitcoin'] = "Erreur"
        time.sleep(3)
        # retour_thread['valeur_litecoin'] = valeur_litecoin_actuelle
        retour_thread['valeur_ethereum'] = valeur_ethereum_actuelle
        # retour_thread['valeur_bitcoin_cash'] = valeur_bitcoin_cash_actuelle
        retour_thread['valeur_bitcoin'] = valeur_bitcoin_actuelle
    # retour_thread['thread_en_cours'] = False
    # get_data(retour_thread, get_forecast=False)

    retour_thread['thread_en_cours'] = False

    print("Done getting data")

    return True


def ping_this(url):
    try:
        urllib.request.urlopen(url, timeout=30)
        return True
    except Exception as error:
        print(error)
        return False


def attempt_reconnection():
    internet_access = False

    delais_attente = 10
    while not internet_access:
        retour_thread['fetching_animation_text'] = "Erreur"
        os.system("sudo ifconfig wlan0 down")
        os.system("sudo ifconfig wlan0 up")

        for it in range(delais_attente, 0, -1):
            retour_thread['fetching_animation_text'] = "Attente de {secondes}s".format(secondes=str(it))
            time.sleep(1)
            if not en_fonction:
                return False

        retour_thread['fetching_animation_text'] = None

        if delais_attente < 45:
            delais_attente += 5
        else:
            delais_attente = 10

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
    return num_jour_semaine, num_jour, num_mois, int((sorted(liste_centres)[-1] / 2.0) + (2 * size_mult))


def render_spinning_image(vitesse_rpm=33):
    duree_un_tour = 60.0 / vitesse_rpm
    correction_360 = 360.0 / duree_un_tour
    degree_rotation = 360.0 - ((seconde_precise % duree_un_tour) * correction_360)

    rect_image = spinning_image.get_rect(center=(largeur * 0.89, hauteur * 0.75))
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

    return current_size / 17.0


def sleep_until_next_frame():
    pygame.display.update()
    duree_frame = (datetime.datetime.now() - maintenant).total_seconds()

    if ClockSettings.FRAMERATE and duree_frame <= 1:
        # On diminue le sleep au cas ou la frame prends du temps a faire
        sleep_time = (1.0 / ClockSettings.FRAMERATE - duree_frame)

        if sleep_time > 0:
            time.sleep(sleep_time)
            duree_frame = (datetime.datetime.now() - maintenant).total_seconds()

    return duree_frame


def get_snowflake():
    mult_five = int(5 * size_mult)
    return {'pos_y': int(-randint(10, 25) * size_mult),
            'pos_x': randint(mult_five, largeur - mult_five),
            'vit_y': randint(hauteur // 10, hauteur // 7),
            'vit_x': randint(-largeur // 15, largeur // 15),
            'weight': uniform(0.5, 1.0)}


def get_raindrop(freezing, drizzle):
    vit_y = uniform(hauteur / 1.5, hauteur * 1.5)

    if freezing:
        surface = raindrop_freezing_surface
    elif drizzle:
        surface = raindrop_drizzle_surface
    else:
        surface = raindrop_normal_surface

    if ClockSettings.LOW_FRAMERATE_MODE:
        vit_y = vit_y * 0.5

    return {'pos_y': int(-randint(10, 50) * size_mult),
            'pos_x': randint(-largeur // 4, largeur),
            'vit_y': vit_y,
            'vit_x': vit_y // 3,
            'surface': surface,
            'width': surface.get_rect().width,
            'height': surface.get_rect().height}


def render_snowing():
    global wind_speed
    if changement_seconde:
        wind_speed = randint(-largeur // 10, largeur // 10)
        for snowflake in snowflake_list:
            if snowflake['pos_y'] > hauteur:
                snowflake_list.remove(snowflake)
        if retour_thread['weather_animation']:
            snowflake_list.append(get_snowflake())

    snowflake_radius = int(7 * size_mult)

    for snowflake in snowflake_list:
        if not changement_heure:
            wind_effect = snowflake['vit_x'] + (wind_speed * (1.5 - snowflake['weight'])) * duree_last_frame

            if abs(wind_effect) < largeur // (15 * snowflake['weight']):
                snowflake['vit_x'] = wind_effect

            snowflake['pos_y'] += snowflake['vit_y'] * duree_last_frame
            snowflake['pos_x'] = (snowflake['pos_x'] + snowflake['vit_x'] * duree_last_frame) % largeur

        if snowflake['pos_x'] < snowflake_radius:
            pygame.draw.circle(ecran, [255, 255, 255], [int(largeur + snowflake['pos_x']), int(snowflake['pos_y'])],
                               int(snowflake['weight'] * snowflake_radius))
        elif snowflake['pos_x'] > largeur - snowflake_radius:
            pygame.draw.circle(ecran, [255, 255, 255], [int(snowflake['pos_x'] - largeur), int(snowflake['pos_y'])],
                               int(snowflake['weight'] * snowflake_radius))

        pygame.draw.circle(ecran, [255, 255, 255], [int(snowflake['pos_x']), int(snowflake['pos_y'])],
                           int(snowflake['weight'] * snowflake_radius))


def render_raining(freezing=False, drizzle=False):
    if len(raindrop_list) < WeatherSettings.RAINDROP_AMOUNT:
        for it in range(0, WeatherSettings.RAINDROP_AMOUNT - len(raindrop_list)):
            raindrop_list.append(get_raindrop(freezing, drizzle))
    else:
        for drop in raindrop_list:
            if drop['pos_y'] > hauteur or drop['pos_x'] > largeur:
                raindrop_list.remove(drop)

    for drop in raindrop_list:
        if not changement_heure:
            drop['pos_y'] += drop['vit_y'] * duree_last_frame
            drop['pos_x'] += drop['vit_x'] * duree_last_frame

        if drop['pos_x'] + drop['width'] >= 0 and drop['pos_y'] + drop['height'] >= 0:
            ecran.blit(drop['surface'], [drop['pos_x'], drop['pos_y']])


def draw_brightness_slider(brightness):
    top_rect = pygame.draw.circle(menu_surface, [255, 255, 255] if brightness == 100 else [75, 75, 75],
                                  [int(menu_width * 0.15), int(menu_height // 4)], int(3 * size_mult))
    bottom_rect = pygame.draw.circle(menu_surface, [255, 255, 255] if brightness else [75, 75, 75],
                                     [top_rect.centerx, int(menu_height // 1.4)], int(3 * size_mult))

    slider_rect = pygame.draw.rect(menu_surface, [255, 255, 255], [top_rect.left, top_rect.centery, top_rect.width,
                                                                   bottom_rect.centery - top_rect.centery])
    if brightness < 100:
        pygame.draw.rect(menu_surface, [75, 75, 75], [top_rect.left, top_rect.centery, top_rect.width,
                                                      slider_rect.height * (100 - brightness) / 100])

    brightness_slider_rect = pygame.Rect([top_rect.left, top_rect.top, top_rect.width * 8, slider_rect.height])
    brightness_slider_rect.centerx = top_rect.centerx + menu_rect.left
    brightness_slider_rect.centery = slider_rect.centery

    return brightness_slider_rect


def change_brightness():
    last_brightness_value = -1

    if ClockSettings.ANDROID_MODE:
        try:
            while brightness - 1 > last_brightness_value or brightness + 1 < last_brightness_value:
                android_brightness.set_level(brightness)
                last_brightness_value = android_brightness.current_level()
        except Exception:
            pass
    else:
        value_to_insert = int((brightness / 100) * 230) + 25
        try:
            while last_brightness_value != value_to_insert:
                if running_as_admin:
                    with open('/sys/class/backlight/rpi_backlight/brightness', "w") as f:
                        f.write(str(value_to_insert))
                else:
                    os.system(
                        'echo ' + str(value_to_insert) + ' | sudo tee -a /sys/class/backlight/rpi_backlight/brightness')
                with open('/sys/class/backlight/rpi_backlight/brightness') as f:
                    last_brightness_value = int(f.read())
                value_to_insert = int((brightness / 100) * 230) + 25
        except Exception:
            pass


def get_color_switch_surface(index=0):
    color_switch_rect = pygame.Rect([0, 0, button_back_rect.height, button_back_rect.height])
    color_switch_rect.center = (brightness_slider_rect.centerx, button_back_rect.centery)

    color_switch_surface = pygame.Surface((color_switch_rect.width * 2, color_switch_rect.height * 2))
    color_switch_surface_rect = color_switch_surface.get_rect()
    color_switch_colorkey = [75, 75, 75]
    color_switch_surface.set_colorkey(color_switch_colorkey)

    circle_width = int(color_switch_surface_rect.width / 15)
    inside_radius = int(color_switch_surface_rect.width / 2) - circle_width
    outside_radius = int(math.sqrt(((color_switch_surface_rect.width / 2) ** 2) * 2)) + 1
    inside_rect = pygame.Rect([circle_width, circle_width, inside_radius * 2, inside_radius * 2])

    for it in range(120):
        current_color = color_schemes[index][int((it / 2) / 10)]((it / 2) % 10)

        if current_color == color_switch_colorkey:
            current_color = [current_color[0] + 1, current_color[1] + 1, current_color[2] + 1]

        pygame.draw.rect(color_switch_surface, current_color,
                         [inside_rect.left + (inside_rect.width * it / 120), inside_rect.top,
                          math.ceil(inside_rect.width / 120), inside_rect.height])

    pygame.draw.circle(color_switch_surface, [75, 75, 75],
                       (int(color_switch_surface_rect.width / 2), int(color_switch_surface_rect.height / 2)),
                       outside_radius, outside_radius - inside_radius)
    pygame.draw.circle(color_switch_surface, [255, 255, 255],
                       (int(color_switch_surface_rect.width / 2), int(color_switch_surface_rect.height / 2)),
                       int(color_switch_surface_rect.width / 2), circle_width)

    color_switch_surface = pygame.transform.smoothscale(color_switch_surface.convert_alpha(),
                                                        (color_switch_rect.width, color_switch_rect.height))

    color_switch_final_surface = pygame.Surface((color_switch_rect.width * 2, color_switch_rect.height * 2))

    return color_switch_surface, color_switch_rect


def save_color_scheme():
    try:
        with open(color_scheme_path, "w") as f:
            f.write(str(active_color_scheme))
    except Exception:
        pass


# START
if ClockSettings.DEBUG_MODE:
    print("Debugging mode enabled")

status_loading_text = "Pygame: 2/2"

if ClockSettings.ENABLE_LOADING_ANIMATION and ClockSettings.LOADING_ANIMATION_SELECTION == 'progress':
    loading_master.destroy()
    lift_loading_master = True

pygame.display.init()
pygame.display.set_caption('A cute little clock')

pygame.mouse.set_visible(False)
mouse_button_down_time = 0

peek_surface = pygame.Surface(resolution)

peek_rect = pygame.Rect([0, 0, 0, 0])
peek_blit_list = []
pygame.draw.circle(peek_surface, [25, 25, 25], [largeur // 2, hauteur // 2], int(hauteur / 2 - 8 * size_mult))
pygame.draw.circle(peek_surface, [0, 0, 0], [largeur // 2, hauteur // 2], int(120.5 * size_mult), int(5 * size_mult))
pygame.draw.circle(peek_surface, [0, 0, 0], [largeur // 2, hauteur // 2], int(84.5 * size_mult), int(5 * size_mult))
pygame.draw.circle(peek_surface, [0, 0, 0], [largeur // 2, hauteur // 2], int(40.5 * size_mult), int(5 * size_mult))

if ClockSettings.ENABLE_LOADING_ANIMATION:
    if ClockSettings.LOADING_ANIMATION_SELECTION.startswith('peek'):
        pygame.draw.rect(peek_surface, [64, 64, 64],
                         [int(largeur / 2 - hauteur / 2), hauteur - peek_progress_height, hauteur,
                          peek_progress_height])
else:
    pygame.draw.rect(peek_surface, [25, 25, 25],
                     [int(largeur / 2 - hauteur / 2), hauteur - peek_progress_height, hauteur, peek_progress_height])

loading_progress_status = loading_smooth_checkpoints[loading_checkpoint]
loading_checkpoint += 1

if not ClockSettings.ENABLE_LOADING_ANIMATION:
    if DisplaySettings.FULLSCREEN:
        if ClockSettings.ANDROID_MODE:
            ecran = pygame.display.set_mode(resolution, pygame.FULLSCREEN | pygame.SCALED)
        else:
            ecran = pygame.display.set_mode((1, 1), pygame.NOFRAME)
            ecran = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    elif DisplaySettings.BORDERLESS_WINDOW:
        ecran = pygame.display.set_mode((1, 1), pygame.NOFRAME)
        ecran = pygame.display.set_mode((1, 1))
        ecran = pygame.display.set_mode(resolution, pygame.NOFRAME)
    else:
        ecran = pygame.display.set_mode((1, 1), pygame.NOFRAME)
        ecran = pygame.display.set_mode(resolution)

    ecran.blit(peek_surface, [0, 0])
    pygame.display.update()
else:
    ecran = pygame.display.set_mode((1, 1), pygame.NOFRAME)
    lift_loading_master = True

if ClockSettings.ANDROID_MODE:
    try:
        from jnius import autoclass, cast

        System = autoclass('android.provider.Settings$System')
        system = System()

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        context = cast('android.content.Context', currentActivity.getApplicationContext())
        if not system.canWrite(context):
            settings = autoclass('android.provider.Settings')
            Intent = autoclass('android.content.Intent')
            intent = Intent()
            intent.setAction(settings.ACTION_MANAGE_WRITE_SETTINGS)
            # Open a screen on the device so that the user can allow the App to
            # write system settings
            currentActivity.startActivity(intent)

        from android import loadingscreen

        loadingscreen.hide_loading_screen()
        pygame.display.update()

        from plyer import brightness as android_brightness
    except Exception:
        pass

status_loading_text = "Modules"
loading_progress_status = loading_smooth_checkpoints[loading_checkpoint]
loading_checkpoint += 1

surface = pygame.Surface(resolution)

lift_loading_master = True

couleur_fond = ClockSettings.BACKGROUND_COLOR

couleur_fond_inverse = [255 - couleur_fond[0], 255 - couleur_fond[1], 255 - couleur_fond[2]]

import math, datetime, urllib.request, urllib.error, urllib.parse, xmltodict, json, ssl, csv, re
from random import randint, uniform

loading_progress_status = loading_smooth_checkpoints[loading_checkpoint]
loading_checkpoint += 1

pygame.font.init()

font_path = os.path.join(clock_files_folder, ClockSettings.FONT)

font_ratio = get_font_ratio(font_path)

font_17 = pygame.font.Font(font_path, int(17 * font_ratio * size_mult))
font_25 = pygame.font.Font(font_path, int(25 * font_ratio * size_mult))
font_40 = pygame.font.Font(font_path, int(40 * font_ratio * size_mult))
font_100 = pygame.font.Font(font_path, int(100 * font_ratio * size_mult))

font_list = {'17': font_17, '25': font_25, '40': font_40, '100': font_100}

brightness = 50

running_as_admin = False

if ClockSettings.ANDROID_MODE:
    try:
        brightness = android_brightness.current_level()

        if 0 <= brightness <= 100:
            android_brightness.set_level(brightness)
        else:
            brightness = 50
    except Exception:
        brightness = 50
else:
    try:
        with open('/sys/class/backlight/rpi_backlight/brightness') as f:
            brightness = int(f.read())

        try:
            with open('/sys/class/backlight/rpi_backlight/brightness', "w") as f:
                f.write(str(brightness))
            running_as_admin = True
        except PermissionError:
            running_as_admin = False
        except Exception:
            running_as_admin = False

        brightness = ((brightness - 25) / 230) * 100

        if not (0 <= brightness <= 100):
            brightness = 50
    except Exception:
        brightness = 50

active_color_scheme = 0

color_scheme_path = os.path.join(clock_files_folder, 'color_scheme.txt')

if os.path.exists(color_scheme_path):
    try:
        with open(color_scheme_path) as f:
            active_color_scheme = int(f.read())

    except Exception:
        active_color_scheme = 0

loading_progress_status = loading_smooth_checkpoints[loading_checkpoint]

if ClockSettings.ENABLE_LOADING_ANIMATION and ClockSettings.LOADING_ANIMATION_SELECTION.startswith('peek'):
    try:
        with open(loading_speed_file_path, "w") as f:
            f.write(str(loading_smooth_checkpoints[-1] / (time.time() - loading_start_time)))
    except Exception:
        if os.path.exists(loading_speed_file_path):
            os.remove(loading_speed_file_path)

if os.path.exists(os.path.join(clock_files_folder, 'exit_splash.png')):
    desktop_img = pygame.image.load(os.path.join(clock_files_folder, 'exit_splash.png'))
    desktop_img = pygame.transform.smoothscale(desktop_img.convert_alpha(), resolution)
elif desktop_img:
    desktop_img = pygame.image.fromstring(desktop_img.rgb, desktop_img.size, 'RGB').convert()
else:
    desktop_img = pygame.Surface(resolution)
    desktop_img.fill([0, 0, 0])

# --------------------------------LOADING SPINNING IMAGES--------------------------------- #
# images_filenames = ['bb0_vinyl_big.png', 'bb1_vinyl_big.png', 'mega_vinyl_big.png']
# images_filenames = ['bb0_vinyl.png', 'bb1_vinyl.png', 'mega_vinyl.png']
# images_filenames = ['cake.png', 'cake2.png', 'baloon.png']
images_filenames = []
spinning_images = []

shuffle_images = True
if len(images_filenames) < 2:
    shuffle_images = False

if len(images_filenames):
    for index in range(0, len(images_filenames)):
        status_loading_text = 'Images: ' + str(index + 1) + '/' + str(len(images_filenames))

        temp_image = pygame.image.load(os.path.join(clock_files_folder, images_filenames[index]))
        spinning_images.append(pygame.transform.scale(temp_image, (int(100 * size_mult), int(100 * size_mult))))

    for it in range(1, randint(1, len(spinning_images))):
        spinning_images.append(spinning_images.pop(0))

    spinning_image = spinning_images[0]
# ---------------------------------------------------------------------------------------- #
loading_progress_status = 70
next_section_loading_amount = 27
# -----------------------------------LOADING LOOP IMAGES---------------------------------- #
if AnimationLoopSettings.ENABLED:
    loop_time = 0
    loop_center_x = int(largeur * (AnimationLoopSettings.CENTER_X_PERCENT / 100.0))
    loop_center_y = int(hauteur * (AnimationLoopSettings.CENTER_Y_PERCENT / 100.0))

    loop_directory = os.path.join(clock_files_folder, os.path.join('animations', AnimationLoopSettings.DIRECTORY))
    images_filenames = os.listdir(loop_directory)
    images_filenames.sort()

    loop_images = []

    if AnimationLoopSettings.ANTIALIASING:
        temp_image = pygame.image.load(os.path.join(loop_directory, images_filenames[0]))
        image_size = (int(temp_image.get_rect().width * AnimationLoopSettings.SCALE * size_mult),
                      int(temp_image.get_rect().height * AnimationLoopSettings.SCALE * size_mult))

    for index in range(0, len(images_filenames)):
        status_loading_text = 'Images d\'animation: ' + str(index + 1) + '/' + str(len(images_filenames))

        temp_image = pygame.image.load(os.path.join(loop_directory, images_filenames[index]))

        if AnimationLoopSettings.ANTIALIASING:
            temp_image = pygame.transform.smoothscale(temp_image.convert_alpha(), image_size)
        else:
            temp_image = pygame.transform.rotozoom(temp_image, 0, AnimationLoopSettings.SCALE * size_mult)

        temp_surface = pygame.Surface((temp_image.get_width(), temp_image.get_height()))
        temp_surface.fill(couleur_fond)
        temp_surface.blit(temp_image, [0, 0])
        loop_images.append(temp_surface.convert())
        loading_progress_status += next_section_loading_amount / len(images_filenames)

        if not ClockSettings.ENABLE_LOADING_ANIMATION:
            if index < len(images_filenames) - 1:
                pygame.draw.rect(ecran, [64, 64, 64], [int(largeur / 2 - hauteur / 2), hauteur - peek_progress_height,
                                                       int(hauteur * (index + 1) / len(images_filenames)),
                                                       peek_progress_height])
            else:
                pygame.draw.rect(peek_surface, [64, 64, 64],
                                 [int(largeur / 2 - hauteur / 2), hauteur - peek_progress_height, hauteur,
                                  peek_progress_height])
                ecran.blit(peek_surface, [0, 0])

            pygame.display.update()

    temp_surface = None
    temp_image = None
    loop_images_len = len(loop_images)
    loop_time = loop_images_len / AnimationLoopSettings.FPS
# ---------------------------------------------------------------------------------------- #
loading_progress_status = 97
next_section_loading_amount = 3
# -----------------------------------LOADING WEATHER ICONS---------------------------------- #
weather_directory = os.path.join(clock_files_folder, 'weather_icons')
images_filenames = os.listdir(weather_directory)
images_filenames.sort()

weather_icons = {}

for index in range(0, len(images_filenames)):
    status_loading_text = 'Icônes de météo: ' + str(index + 1) + '/' + str(len(images_filenames))

    temp_image = pygame.image.load(os.path.join(weather_directory, images_filenames[index]))
    # weather_icons[images_filenames[index]] = pygame.transform.rotozoom(temp_image, 0, 0.6 * size_mult).convert_alpha()
    image_size = (
        int(temp_image.get_rect().width * 0.6 * size_mult), int(temp_image.get_rect().height * 0.6 * size_mult))
    weather_icons[images_filenames[index]] = pygame.transform.smoothscale(temp_image.convert_alpha(),
                                                                          image_size).convert_alpha()
    loading_progress_status += next_section_loading_amount / len(images_filenames)
# ---------------------------------------------------------------------------------------- #
loading_progress_status = 100

color_schemes = [
    # Rainbow
    [lambda seconde: [255, int((seconde / 10.0) * 255), 0],
     lambda seconde: [255 - int((seconde / 10.0) * 255), 255, 0],
     lambda seconde: [0, 255, int((seconde / 10.0) * 255)],
     lambda seconde: [0, 255 - int((seconde / 10.0) * 255), 255],
     lambda seconde: [int((seconde / 10.0) * 255), 0, 255],
     lambda seconde: [255, 0, 255 - int((seconde / 10.0) * 255)]],
    # Vibrant-Peach
    [lambda seconde: [255, 50, 0],
     lambda seconde: [255, 50 + int((seconde / 10.0) * 50), 0],
     lambda seconde: [255, 100, 0],
     lambda seconde: [255, 100 + int((seconde / 10.0) * 100), 0],
     lambda seconde: [255, 200, 0],
     lambda seconde: [255, 200 - int((seconde / 10.0) * 150), 0]],
    # Cyan-Purple-Fuchsia
    [lambda seconde: [255 - int((seconde / 10.0) * 255), int((seconde / 10.0) * 255),
                      100 + int((seconde / 10.0) * 155)],
     lambda seconde: [0, 255, 255],
     lambda seconde: [int((seconde / 10.0) * 128), 255 - int((seconde / 10.0) * 255), 255],
     lambda seconde: [128, 0, 255],
     lambda seconde: [127 + int((seconde / 10.0) * 128), 0, 255 - int((seconde / 10.0) * 155)],
     lambda seconde: [255, 0, 100]],
    # Steel
    [lambda seconde: [50 + int((seconde / 10.0) * 50), 50 + int((seconde / 10.0) * 50),
                      50 + int((seconde / 10.0) * 50)],
     lambda seconde: [100 + int((seconde / 10.0) * 50), 100 + int((seconde / 10.0) * 50),
                      100 + int((seconde / 10.0) * 50)],
     lambda seconde: [150 + int((seconde / 10.0) * 50), 150 + int((seconde / 10.0) * 50),
                      150 + int((seconde / 10.0) * 50)],
     lambda seconde: [200 - int((seconde / 10.0) * 50), 200 - int((seconde / 10.0) * 50),
                      200 - int((seconde / 10.0) * 50)],
     lambda seconde: [150 - int((seconde / 10.0) * 50), 150 - int((seconde / 10.0) * 50),
                      150 - int((seconde / 10.0) * 50)],
     lambda seconde: [100 - int((seconde / 10.0) * 50), 100 - int((seconde / 10.0) * 50),
                      100 - int((seconde / 10.0) * 50)]],
    # Wine-Red-and-White
    [lambda seconde: [255, 255, 100 + int((seconde / 10.0) * 100)],
     lambda seconde: [255 - int((seconde / 10.0) * 55), 255 - int((seconde / 10.0) * 255),
                      200 - int((seconde / 10.0) * 200)],
     lambda seconde: [200 - int((seconde / 10.0) * 100), 0, 0],
     lambda seconde: [100 + int((seconde / 10.0) * 100), 0, 0],
     lambda seconde: [200 + int((seconde / 10.0) * 55), int((seconde / 10.0) * 255), int((seconde / 10.0) * 200)],
     lambda seconde: [255, 255, 200 - int((seconde / 10.0) * 100)]]]

liste_calculs_couleurs = color_schemes[active_color_scheme]
# liste_calculs_couleurs = color_schemes.pop()
# color_schemes.insert(0, liste_calculs_couleurs)

color_offset = uniform(0, 59)

# ------------------------------------------MENU------------------------------------------ #

button_size = [int(font_25.size(' Redémarrer ')[0]), int(font_25.size(' Redémarrer ')[1] * 1.3)]
menu_width = (button_size[0] * 2) * 2  # + int(200 * size_mult)
menu_height = hauteur * 2
menu_size_mult = size_mult * 2
menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
menu_rect = menu_surface.get_rect()
menu_rect.centerx = int(largeur / 2)
menu_top_left = [0, 0]
menu_bottom_right = [0, 0]

# Corners
menu_left_top = pygame.draw.circle(menu_surface, [0, 75, 0, 255] if ClockSettings.DEBUG_MODE else [75, 75, 75, 255],
                                   [int(24 * menu_size_mult), int(24 * menu_size_mult)], int(16 * menu_size_mult))
pygame.draw.circle(menu_surface, [0, 75, 0, 255] if ClockSettings.DEBUG_MODE else [75, 75, 75, 255],
                   [menu_width - int(24 * menu_size_mult), int(24 * menu_size_mult)], int(16 * menu_size_mult))
pygame.draw.circle(menu_surface, [0, 75, 0, 255] if ClockSettings.DEBUG_MODE else [75, 75, 75, 255],
                   [int(24 * menu_size_mult), menu_height - int(24 * menu_size_mult)], int(16 * menu_size_mult))
menu_right_bottom = pygame.draw.circle(menu_surface, [0, 75, 0, 255] if ClockSettings.DEBUG_MODE else [75, 75, 75, 255],
                                       [menu_width - int(24 * menu_size_mult), menu_height - int(24 * menu_size_mult)],
                                       int(16 * menu_size_mult))

# Drawing background outline
pygame.draw.rect(menu_surface, [100, 100, 0, 255] if ClockSettings.DEBUG_MODE else [75, 75, 75, 255],
                 [menu_left_top.left, menu_left_top.centery,
                  menu_right_bottom.right - menu_left_top.left, menu_right_bottom.centery - menu_left_top.centery])
pygame.draw.rect(menu_surface, [0, 100, 100, 255] if ClockSettings.DEBUG_MODE else [75, 75, 75, 255],
                 [menu_left_top.centerx, menu_left_top.top,
                  menu_right_bottom.centerx - menu_left_top.centerx, menu_right_bottom.bottom - menu_left_top.top])

# Corners
menu_left_top = pygame.draw.circle(menu_surface, [0, 25, 0, 240] if ClockSettings.DEBUG_MODE else [25, 25, 25, 240],
                                   [int(27 * menu_size_mult), int(27 * menu_size_mult)], int(16 * menu_size_mult))
pygame.draw.circle(menu_surface, [0, 25, 0, 240] if ClockSettings.DEBUG_MODE else [25, 25, 25, 240],
                   [menu_width - int(27 * menu_size_mult), int(27 * menu_size_mult)], int(16 * menu_size_mult))
pygame.draw.circle(menu_surface, [0, 25, 0, 240] if ClockSettings.DEBUG_MODE else [25, 25, 25, 240],
                   [int(27 * menu_size_mult), menu_height - int(27 * menu_size_mult)], int(16 * menu_size_mult))
menu_right_bottom = pygame.draw.circle(menu_surface, [0, 25, 0, 240] if ClockSettings.DEBUG_MODE else [25, 25, 25, 240],
                                       [menu_width - int(27 * menu_size_mult), menu_height - int(27 * menu_size_mult)],
                                       int(16 * menu_size_mult))

# Drawing background
pygame.draw.rect(menu_surface, [0, 50, 50, 240] if ClockSettings.DEBUG_MODE else [25, 25, 25, 240],
                 [menu_left_top.left, menu_left_top.centery,
                  menu_right_bottom.right - menu_left_top.left, menu_right_bottom.centery - menu_left_top.centery])
pygame.draw.rect(menu_surface, [50, 50, 0, 240] if ClockSettings.DEBUG_MODE else [25, 25, 25, 240],
                 [menu_left_top.centerx, menu_left_top.top,
                  menu_right_bottom.centerx - menu_left_top.centerx, menu_right_bottom.bottom - menu_left_top.top])

# Scale the menu back down to create smooth edges
menu_width = int(menu_width / 2)  # + int(200 * size_mult)
menu_height = int(menu_height / 2)

menu_surface = pygame.transform.smoothscale(menu_surface.convert_alpha(), (menu_width, menu_height))
menu_rect = menu_surface.get_rect()
menu_rect.centerx = int(largeur / 2)

texte = font_40.render("Menu", True, [255, 255, 255])
texte_rect = texte.get_rect(center=((menu_width // 2), 0))
# texte_rect = texte.get_rect()
# texte_rect.left = menu_left_top.centerx
texte_rect.top = int(11 * size_mult)
menu_surface.blit(texte, texte_rect)

button_size[1] = button_size[1] + 1 if button_size[1] % 2 else button_size[1]
button_size[0] = button_size[0] * 2
button_size[1] = button_size[1] * 2
button_surface = pygame.Surface((button_size[0] + button_size[1], button_size[1]), pygame.SRCALPHA)
button_rect = pygame.Rect([int(button_size[1] / 2), 0, button_size[0], button_size[1]])
pygame.draw.rect(button_surface, [100, 0, 100, 240] if ClockSettings.DEBUG_MODE else [0, 0, 0], button_rect)
pygame.draw.circle(button_surface, [150, 0, 150, 240] if ClockSettings.DEBUG_MODE else [0, 0, 0],
                   [button_rect.left, button_rect.centery], int(button_size[1] / 2))
pygame.draw.circle(button_surface, [150, 0, 150, 240] if ClockSettings.DEBUG_MODE else [0, 0, 0],
                   [button_rect.right, button_rect.centery], int(button_size[1] / 2))
button_rect.width = button_rect.width + button_rect.height

button_size[0] = int(button_size[0] / 2)
button_size[1] = int(button_size[1] / 2)

button_surface = pygame.transform.smoothscale(button_surface.convert_alpha(),
                                              (button_size[0] + button_size[1], button_size[1]))

texte = font_25.render("Quitter", True, [255, 255, 255])
button_center = (menu_width // 1.65, menu_height // 2)
texte_rect = texte.get_rect(center=button_center)
button_quit_rect = pygame.Rect([0, 0, button_size[0], button_size[1]])
button_quit_rect.width = button_size[0] + button_size[1]
button_quit_rect.center = texte_rect.center
menu_surface.blit(button_surface, button_quit_rect)
menu_surface.blit(texte, texte_rect)
button_quit_rect.centerx = texte_rect.centerx + menu_rect.left

texte = font_25.render("Redémarrer", True, [255, 255, 255])
button_center = ((menu_width // 1.65), 0)
texte_rect = texte.get_rect(center=button_center)
texte_rect.bottom = button_quit_rect.top - int(10 * size_mult)
button_reboot_rect = pygame.Rect([0, 0, button_size[0], button_size[1]])
button_reboot_rect.width = button_size[0] + button_size[1]
button_reboot_rect.center = texte_rect.center
menu_surface.blit(button_surface, button_reboot_rect)
menu_surface.blit(texte, texte_rect)
button_reboot_rect.centerx = texte_rect.centerx + menu_rect.left

texte = font_25.render("Rafraîchir", True, [255, 255, 255])
button_center = ((menu_width // 1.65), 0)
texte_rect = texte.get_rect(center=button_center)
texte_rect.top = button_quit_rect.bottom + int(10 * size_mult)
button_refresh_rect = pygame.Rect([0, 0, button_size[0], button_size[1]])
button_refresh_rect.width = button_size[0] + button_size[1]
button_refresh_rect.center = texte_rect.center
menu_surface.blit(button_surface, button_refresh_rect)
menu_surface.blit(texte, texte_rect)
button_refresh_rect.centerx = texte_rect.centerx + menu_rect.left

texte = font_25.render("Retour", True, [255, 255, 255])
button_center = (menu_width // 1.65, int((5.3 * menu_height) // 6))
texte_rect = texte.get_rect(center=button_center)
button_back_rect = pygame.Rect([0, 0, button_size[0], button_size[1]])
button_back_rect.width = button_size[0] + button_size[1]
button_back_rect.center = texte_rect.center
menu_surface.blit(button_surface, button_back_rect)
menu_surface.blit(texte, texte_rect)
button_back_rect.centerx = texte_rect.centerx + menu_rect.left

brightness_slider_rect = draw_brightness_slider(brightness)
change_brightness_thread = Thread(target=change_brightness)

color_switch_surfaces = []

for it in range(len(color_schemes)):
    color_switch_surfaces.append((get_color_switch_surface(it)))

color_switch_rect = color_switch_surfaces[0][1]
color_switch_thread = Thread(target=save_color_scheme)

menu_surface.blit(color_switch_surfaces[active_color_scheme][0],
                  [color_switch_rect.left - menu_rect.left, color_switch_rect.top - menu_rect.top])

# ---------------------------------------------------------------------------------------- #

maintenant = datetime.datetime.now()

loop_end_time = maintenant

heure = maintenant.hour

minute = maintenant.minute

seconde = maintenant.second

millisec = maintenant.microsecond

seconde_precise = seconde + millisec / 1000000.0

eloignement_secondes = int(10 * size_mult)

eloignement_minutes = int(46 * size_mult)

eloignement_heures = int(81 * size_mult)

if largeur > hauteur:
    rect_couleurs_secondes = [(largeur // 2) - (hauteur // 2) + eloignement_secondes, eloignement_secondes,
                              hauteur - eloignement_secondes * 2, hauteur - eloignement_secondes * 2]
    rect_arc_secondes = [(largeur // 2) - (hauteur // 2) + eloignement_secondes - 2, eloignement_secondes - 2,
                         hauteur - ((eloignement_secondes - 2) * 2), hauteur - ((eloignement_secondes - 2) * 2)]
    rect_arc_minutes = [(largeur // 2) - (hauteur // 2) + eloignement_minutes, eloignement_minutes,
                        hauteur - eloignement_minutes * 2, hauteur - eloignement_minutes * 2]
    rect_arc_heures = [(largeur // 2) - (hauteur // 2) + eloignement_heures, eloignement_heures,
                       hauteur - eloignement_heures * 2, hauteur - eloignement_heures * 2]
else:
    rect_couleurs_secondes = [eloignement_secondes, (hauteur // 2) - (largeur // 2) + eloignement_secondes,
                              largeur - eloignement_secondes * 2, largeur - eloignement_secondes * 2]
    rect_arc_secondes = [eloignement_secondes - 2, (hauteur // 2) - (largeur // 2) + eloignement_secondes - 2,
                         largeur - ((eloignement_secondes - 2) * 2), largeur - ((eloignement_secondes - 2) * 2)]
    rect_arc_minutes = [eloignement_minutes, (hauteur // 2) - (largeur // 2) + eloignement_minutes,
                        largeur - eloignement_minutes * 2, largeur - eloignement_minutes * 2]
    rect_arc_heures = [eloignement_heures, (hauteur // 2) - (largeur // 2) + eloignement_heures,
                       largeur - eloignement_heures * 2, largeur - eloignement_heures * 2]

en_fonction = True

maintenant_precedent = -1

minute_precedente = -1

heure_precedente = -1

seconde_precedente = -1

changement_heure = False

changement_minute = False

changement_seconde = False

toggle_menu = False
toggle_brightness = False

draw_middle_circle = True
refresh_requested = False
first_frame = True
frame_counter = 0

arc_cleanup_status = (2 * size_mult)
do_arc_cleanup = True

color_wheel_active = False
color_wheel_angle = 0
color_wheel_offset = -1

couleur_titre_countdown = couleur_fond_inverse

temps_restant = "{}:{}:{}:{}".format('00', '00', '00', '00')

text_jour_semaine_couleur = couleur_fond_inverse

texte = font_17.render('INITIAL TEXT', 0, [255, 255, 255])
texte_rect = texte.get_rect()

text_dict = {'temps': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             'seconde': {'text': 'INITIAL TEXT', 'surface': texte, 'rotated_surface': texte, 'rect': texte_rect},
             'detailed_info': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             'temperature': {'text': 'INITIAL TEXT', 'surface': texte, 'wiggle_surface': texte, 'rect': texte_rect,
                             'wiggle_rect': texte_rect},
             'pourcent_pluie': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             'pistes_soir': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             'SKI': {'text': 'SKI', 'surface': font_17.render('SKI', True, couleur_fond_inverse), 'rect': texte_rect},
             'ethermine_data': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             'valeur_bitcoin': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             'BTC': {'text': 'BTC', 'surface': font_17.render('BTC', True, couleur_fond_inverse), 'rect': texte_rect},
             'valeur_ethereum': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             'ETH': {'text': 'ETH', 'surface': font_17.render('ETH', True, couleur_fond_inverse), 'rect': texte_rect},
             'fetching_animation': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             'noms_jours_semaine': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect,
                                    'color': couleur_fond_inverse},
             'num_jour': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             'noms_mois': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             'temps_restant': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             'titre_countdown': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect,
                                 'color': couleur_fond_inverse},
             'calculated_fps': {'text': 'INITIAL TEXT', 'surface': texte, 'rect': texte_rect},
             }

# seconde_surfaces = {}

# for it in range(0, 360):
#     texte = font_25.render(' ' + str(int(it/6)) + ' ', True, [255, 255, 255])
#     for it2 in range(0, 10):
#         seconde_surfaces[str(it) + '.' + str(it2)] = pygame.transform.rotozoom(texte, -float(str(it) + '.' + str(it2)) + (180 if 45 > it/6 > 15 else 0), 1)
#
# seconde_surfaces['360.0'] = seconde_surfaces['359.9']

# for it in range(0, 360):
#     texte = font_25.render(' ' + str(int(it/6)) + ' ', True, [255, 255, 255])
#     seconde_surfaces[str(it)] = pygame.transform.rotozoom(texte, -it + (180 if 45 > it/6 > 15 else 0), 1)


ssl_context = ssl._create_unverified_context()

retour_thread = {'temperature': ["##,#" + '\N{DEGREE SIGN}' + "C",
                                 {'couleur': couleur_fond_inverse, 'wiggle': 1.5 if ClockSettings.DEBUG_MODE else 0}],
                 'pourcent_pluie': '##%' if ClockSettings.DEBUG_MODE else ' ',
                 'detailed_info': "Conditions actuelles",
                 'weather_icon': "10.png" if ClockSettings.DEBUG_MODE else "",
                 'pistes_soir': "##/##",
                 'valeur_bitcoin': "####.##$",
                 # 'valeur_litecoin': "##.##$",
                 # 'valeur_bitcoin_cash': "###.##$",
                 'valeur_ethereum': "###.##$",
                 'ethermine_data': '###.##$ - ##%',
                 'fetching_animation_text': " ",
                 'thread_en_cours': False,
                 'weather_animation': '',
                 'city_id': 's0000620',
                 'city_name': 'Québec',
                 'geolocate_success': False}

meteo_update_recent = True

weather_animations = ['neige', 'poudre', 'vergla', 'pluie', 'bruine']

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

calculated_fps = '{} fps'.format(ClockSettings.FRAMERATE or 1)

# text_anim_frames = ["[oOo ]", "[ oOo]", "[o oO]", "[Oo o]"]
# text_anim_frames = ["boi", "boiii", "boiiiii", "boiiiiiii"]
# text_anim_frames = ["[\   ]", "[ \  ]", "[  \ ]", "[   \]", "[   /]", "[  / ]", "[ /  ]", "[/   ]"]
text_anim_frames = ["[.oOo.]", "[..oOo]", "[o..oO]", "[Oo..o]", "[oOo..]"]
# text_anim_frames = ["[..oOo..]", "[...oOo.]", "[....oOo]", "[o....oO]", "[Oo....o]", "[oOo....]", "[.oOo...]"]
# text_anim_frames = ["[-=-  ]", "[ -=- ]", "[  -=-]", "[-  -=]", "[=-  -]"]
# text_anim_frames = ["[do]", "[ob]", "[op]", "[qo]"]

text_anim_surfaces = {}

for font in font_list.keys():
    text_anim_surfaces[font] = []
    for text_anim in text_anim_frames:
        text_anim_surfaces[font].append(font_list[font].render(text_anim, True, couleur_fond_inverse))

text_anim_frame = 0

duree_last_frame = 0

wind_speed = 0

snowflake_list = []

raindrop_list = []

# Normal raindrops (pluie)
drop_angle = int(4 * size_mult)
drop_thicc = int(3 * size_mult)
drop_length = int(15 * size_mult)
drop_color = [0, 0, 255]
raindrop_normal_surface = pygame.Surface([drop_angle + drop_thicc, drop_length + 1])
raindrop_normal_surface.set_colorkey([0, 0, 0])
pygame.draw.line(raindrop_normal_surface, drop_color, [int(drop_thicc / 2), 0],
                 [drop_angle + int(drop_thicc / 2), drop_length], drop_thicc)

# Freezing raindrops (vergla)
drop_color = [0, 200, 255]
raindrop_freezing_surface = pygame.Surface([drop_angle + drop_thicc, drop_length + 1])
raindrop_freezing_surface.set_colorkey([0, 0, 0])
pygame.draw.line(raindrop_freezing_surface, drop_color, [int(drop_thicc / 2), 0],
                 [drop_angle + int(drop_thicc / 2), drop_length], drop_thicc)

# Drizzle raindrops (bruine)
drop_angle = int(2 * size_mult)
drop_thicc = int(1 * size_mult)
drop_length = int(8 * size_mult)
drop_color = [0, 0, 255]
raindrop_drizzle_surface = pygame.Surface([drop_angle + drop_thicc, drop_length + 1])
raindrop_drizzle_surface.set_colorkey([0, 0, 0])
pygame.draw.line(raindrop_drizzle_surface, drop_color, [int(drop_thicc / 2), 0],
                 [drop_angle + int(drop_thicc / 2), drop_length], drop_thicc)

notification_active = False

notifications = {"11:55": ["À LA", "BOUFFE"],
                 "15:59": ["BON", "J'DÉCRISS"]}

couleur_arc_secondes = [0, 0, 0]

peek_animating = False
peek_radius = 0
peek_radius_limit = math.sqrt(hauteur ** 2 + largeur ** 2) / 2
peek_status = 0
peek_delay = 0.5 if ClockSettings.ENABLE_LOADING_ANIMATION else 0

while wait_for_peek_animation:
    time.sleep(0.05)

wait_for_peek_animation = True

if ClockSettings.ENABLE_LOADING_ANIMATION:
    if DisplaySettings.FULLSCREEN:
        ecran = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    elif DisplaySettings.BORDERLESS_WINDOW:
        ecran = pygame.display.set_mode(resolution, pygame.NOFRAME)
    else:
        ecran = pygame.display.set_mode(resolution)

    ecran.blit(peek_surface, [0, 0])
    pygame.display.update()
    lift_loading_master = True
    startup_complete = True
    while lift_loading_master:
        continue

if not ClockSettings.DEBUG_MODE or ClockSettings.ENABLE_LOADING_ANIMATION:
    peek_animating = True
    ecran.set_clip(peek_rect)

pygame.display.update()

peek_surface.set_colorkey([100, 50, 0])  # Ici pour aider les update/blit à être plus rapides au boot

get_forecast_too = True

if ClockSettings.DEBUG_MODE and not ClockSettings.ENABLE_LOADING_ANIMATION:
    Thread(target=get_data, args=(retour_thread, get_forecast_too), daemon=True).start()

maintenant = datetime.datetime.now()

print("Done initialising!")

while en_fonction:
    maintenant_precedent = maintenant
    maintenant = datetime.datetime.now()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION and not first_frame:
            pygame.mouse.set_visible(True)

        if event.type == pygame.MOUSEBUTTONDOWN:
            position_souris = pygame.mouse.get_pos()
            if not toggle_menu:
                pygame.mouse.set_visible(True)
                mouse_button_down_time = time.time()
            else:
                if brightness_slider_rect.collidepoint(position_souris):
                    toggle_brightness = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_down_time = 0
            color_wheel_offset = -1

            if color_wheel_active:
                color_wheel_active = False
                draw_middle_circle = True
            else:
                pygame.mouse.set_visible(True)
                position_souris = pygame.mouse.get_pos()
                if toggle_menu:
                    if toggle_brightness:
                        brightness = 100 - ((position_souris[
                                                 1] - brightness_slider_rect.top) / brightness_slider_rect.height) * 100
                        brightness = 0 if brightness < 0 else brightness
                        brightness = 100 if brightness > 100 else brightness
                        pygame.mouse.set_pos(largeur, hauteur)
                        draw_brightness_slider(brightness)
                        toggle_brightness = False

                        if not change_brightness_thread.is_alive():
                            change_brightness_thread = Thread(target=change_brightness)
                            change_brightness_thread.start()

                    elif button_quit_rect.collidepoint(position_souris):
                        # quitter
                        if ClockSettings.DEBUG_MODE:
                            exit()
                        status_loading_text = ""
                        en_fonction = False
                    elif button_back_rect.collidepoint(position_souris):
                        # retour
                        toggle_menu = False
                        pygame.mouse.set_visible(False)
                    elif button_reboot_rect.collidepoint(position_souris):
                        # redémarrer
                        status_loading_text = "À+"
                        startup_complete = False
                        en_fonction = False
                    elif button_refresh_rect.collidepoint(position_souris):
                        # rafraîchir
                        refresh_requested = True
                        toggle_menu = False
                        pygame.mouse.set_visible(False)

                        if not retour_thread['thread_en_cours']:
                            retour_thread['geolocate_success'] = False
                            Thread(target=get_data, args=(retour_thread, True), daemon=True).start()
                    elif color_switch_rect.collidepoint(position_souris):
                        # changer couleur
                        refresh_requested = True
                        pygame.mouse.set_pos(largeur, hauteur)
                        active_color_scheme = active_color_scheme + 1 if active_color_scheme < len(
                            color_schemes) - 1 else 0
                        liste_calculs_couleurs = color_schemes[active_color_scheme]
                        # liste_calculs_couleurs = color_schemes.pop()
                        # color_schemes.insert(0, liste_calculs_couleurs)
                        # get_color_switch_surface()
                        menu_surface.blit(color_switch_surfaces[active_color_scheme][0],
                                          [color_switch_rect.left - menu_rect.left,
                                           color_switch_rect.top - menu_rect.top])

                        while color_switch_thread.is_alive():
                            continue

                        color_switch_thread = Thread(target=save_color_scheme)
                        color_switch_thread.start()
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
			surface = pygame.Surface(resolution)"""

    if not en_fonction:
        break

    temps = time.strftime("%H:%M")

    heure = maintenant.hour

    if heure > 11:
        heure -= 12

    minute = maintenant.minute

    changement_heure = abs(maintenant - maintenant_precedent).total_seconds() > 0.5

    if changement_heure:
        print("Time change detected")
        draw_middle_circle = True

    heure_precedente = heure

    if minute != minute_precedente:
        # A chaque minute
        changement_minute = True
        notification_active = temps in list(notifications.keys())
    else:
        changement_minute = False

    minute_precedente = minute

    seconde_precedente = seconde

    seconde = maintenant.second

    changement_seconde = seconde_precedente != seconde

    millisec = maintenant.microsecond / 1000000.0

    seconde_precise = seconde + millisec

    minute_changeante = minute + seconde_precise / 60.0

    heure_changeante = heure + minute_changeante / 60.0

    degree_secondes = ((360 * seconde_precise) / 60)

    degree_minutes = ((360 * minute_changeante) / 60)

    degree_minute_ligne = math.radians(degree_minutes - 90)

    degree_heures = ((360 * heure_changeante) / 12)

    degree_heures_ligne = math.radians(degree_heures - 90)

    if peek_animating:
        peek_status = peek_status + (duree_last_frame if duree_last_frame <= 0.05 else 0.05)
        peek_blit_list = []

        if (datetime.datetime.now() - maintenant).total_seconds() > peek_delay and first_frame:
            peek_status = peek_delay

        if peek_status >= peek_delay:
            peek_radius = int((peek_status - peek_delay) * 250 * size_mult)
            peek_rect = pygame.draw.circle(peek_surface, [128, 128, 128], [largeur // 2, hauteur // 2],
                                           peek_radius + int(5 * size_mult))
            pygame.draw.circle(peek_surface, [100, 50, 0], [largeur // 2, hauteur // 2], peek_radius)
            ecran.set_clip(peek_rect)

            if peek_rect.top == 0 and peek_radius >= hauteur / 2:
                peek_rect_right = peek_rect.copy()
                peek_rect_left = peek_rect.copy()

                # Right rect
                peek_rect_right_right = peek_rect_right.right
                peek_rect_right.left = math.sqrt(peek_radius ** 2 - (hauteur / 2) ** 2) + largeur / 2
                peek_rect_right.width = peek_rect_right_right - peek_rect_right.left
                peek_blit_list.append(peek_rect_right)

                # Left rect
                peek_rect_left_left = peek_rect_left.left
                peek_rect_left.width = largeur / 2 - math.sqrt(peek_radius ** 2 - (hauteur / 2) ** 2)
                peek_blit_list.append(peek_rect_left)
            else:
                peek_blit_list.append(peek_rect)

            if peek_radius > peek_radius_limit:
                ecran.set_clip([0, 0, largeur, hauteur])
                peek_animating = False
                Thread(target=get_data, args=(retour_thread, True), daemon=True).start()

    if do_arc_cleanup and minute < 1:
        if changement_minute:
            num_jour_semaine, num_jour, num_mois, centre_date = get_date_et_alignement()
            text_dict['noms_mois']['text'] = 'update me'
            text_dict['num_jour']['text'] = 'update me'
            text_dict['noms_jours_semaine']['text'] = 'update me'

        cleanup_size = (80 * size_mult) if heure == 0 else (39 * size_mult)
        arc_cleanup_status += (arc_cleanup_status * duree_last_frame)

        arc_cleanup_status = arc_cleanup_status if arc_cleanup_status < cleanup_size else cleanup_size

        pygame.draw.circle(surface, [0, 0, 0], [largeur // 2, hauteur // 2], int(119 * size_mult),
                           int(arc_cleanup_status))

        if arc_cleanup_status >= cleanup_size:
            arc_cleanup_status = (2 * size_mult)
            do_arc_cleanup = False

    elif minute > 0 and not do_arc_cleanup:
        do_arc_cleanup = True

    if changement_minute:
        text_jour_semaine_couleur = get_text_jour_semaine_couleur()

    if not meteo_update_recent and minute % 5 == 0:
        get_forecast_too = (minute % 20 == 5) or not retour_thread['geolocate_success']
        if not peek_animating:
            Thread(target=get_data, args=(retour_thread, get_forecast_too), daemon=True).start()
        if shuffle_images:
            for it in range(0, randint(1, len(spinning_images) - 1)):
                spinning_images.append(spinning_images.pop(0))
            spinning_image = spinning_images[0]
        meteo_update_recent = True
    elif meteo_update_recent and minute % 5 != 0:
        meteo_update_recent = False

    if mouse_button_down_time:
        color_wheel_active = time.time() - mouse_button_down_time >= 0.2

    if draw_middle_circle or color_wheel_active:
        draw_middle_circle = False

        if color_wheel_active:
            position_souris = pygame.mouse.get_pos()
            (souris_x, souris_y) = (largeur / 2 - position_souris[0], position_souris[1] - hauteur / 2)
            color_wheel_angle = 360 - (math.degrees(math.atan2(souris_x, souris_y)) + 180)

            if color_wheel_offset == -1:
                color_wheel_offset = color_wheel_angle - (color_offset * 6)

            color_wheel_angle = (color_wheel_angle - color_wheel_offset) % 360

            if ClockSettings.DEBUG_MODE:
                temps = str(int(color_wheel_angle))

            color_offset = color_wheel_angle / 6
        else:
            pygame.draw.rect(surface, [100, 100, 100] if ClockSettings.DEBUG_MODE else couleur_fond,
                             [0, 0, largeur, hauteur])

        pygame.draw.circle(surface, [0, 0, 0], [largeur // 2, hauteur // 2], int(155 * size_mult))
        pygame.draw.circle(surface, [25, 25, 25], [largeur // 2, hauteur // 2], int(36 * size_mult))
        if not color_wheel_active:
            num_jour_semaine, num_jour, num_mois, centre_date = get_date_et_alignement()
            text_dict['noms_mois']['text'] = 'update me'
            text_dict['num_jour']['text'] = 'update me'
            text_dict['noms_jours_semaine']['text'] = 'update me'

        # Secondes
        # for it in range(1 if color_wheel_active else 2, 104 if color_wheel_active else 107):
        for it in range(2, 105 if color_wheel_active else 106):
            use_current_color = it == 105
            it = int(((seconde_precise + 8.5) * 2) + it) % 120

            couleur_pour_secondes = seconde_a_couleur(seconde_precise) if use_current_color else seconde_a_couleur(
                it / 2.0)

            pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes,
                            math.radians(111 - ((360 * (it / 2.0)) / 60)),
                            math.radians(123 - ((360 * (it / 2.0)) / 60)), int(30 * size_mult))

            if not color_wheel_active:
                pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes,
                                math.radians(111.5 - ((360 * (it / 2.0)) / 60)),
                                math.radians(123 - ((360 * (it / 2.0)) / 60)), int(30 * size_mult))
                pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes,
                                math.radians(112 - ((360 * (it / 2.0)) / 60)),
                                math.radians(123 - ((360 * (it / 2.0)) / 60)), int(30 * size_mult))

        # Minutes et heures
        pygame.draw.arc(surface, seconde_a_couleur(minute_changeante, inverser=True), rect_arc_minutes,
                        math.radians(90 - degree_minutes),
                        math.radians(90), int(28 * size_mult))

        # If >= 0.5 car à 0 ça fait un arc complet a cause du offset des arcs redessinés
        if degree_minutes >= 1 and not color_wheel_active:
            pygame.draw.arc(surface, seconde_a_couleur(minute_changeante, inverser=True), rect_arc_minutes,
                            math.radians(90.5 - degree_minutes),
                            math.radians(90), int(28 * size_mult))
            pygame.draw.arc(surface, seconde_a_couleur(minute_changeante, inverser=True), rect_arc_minutes,
                            math.radians(91 - degree_minutes),
                            math.radians(90), int(28 * size_mult))

        pygame.draw.arc(surface, seconde_a_couleur((heure_changeante * 60) / 12), rect_arc_heures,
                        math.radians(90 - degree_heures),
                        math.radians(90), int(38 * size_mult))

        # If >= 0.5 car à 0 ça fait un arc complet a cause du offset des arcs redessinés
        if degree_heures >= 1 and not color_wheel_active:
            pygame.draw.arc(surface, seconde_a_couleur((heure_changeante * 60) / 12), rect_arc_heures,
                            math.radians(90.5 - degree_heures),
                            math.radians(90), int(38 * size_mult))
            pygame.draw.arc(surface, seconde_a_couleur((heure_changeante * 60) / 12), rect_arc_heures,
                            math.radians(91 - degree_heures),
                            math.radians(90), int(38 * size_mult))

    else:
        # Minutes
        couleur_pour_minutes = seconde_a_couleur(minute_changeante, inverser=True)
        for it in range(1, 4):
            degree_secondes_ligne = degree_secondes - (it * 120)
            degree_secondes_ligne = 360 - abs(
                degree_secondes_ligne) if degree_secondes_ligne < 0 else degree_secondes_ligne
            if degree_minutes >= degree_secondes_ligne >= 0:
                degree_secondes_ligne = math.radians(degree_secondes_ligne - 90)
                pygame.draw.line(surface, [it * 80, 0, 0] if ClockSettings.DEBUG_MODE else couleur_pour_minutes,
                                 (int((largeur / 2) + math.cos(degree_secondes_ligne) * 115 * size_mult),
                                  int((hauteur / 2) + math.sin(degree_secondes_ligne) * 115 * size_mult)),
                                 (int((largeur / 2) + math.cos(degree_secondes_ligne) * 86 * size_mult),
                                  int((hauteur / 2) + math.sin(degree_secondes_ligne) * 86 * size_mult)),
                                 int((3 if ClockSettings.LOW_FRAMERATE_MODE else 2) * size_mult))

        if not (do_arc_cleanup and minute < 1):
            pygame.draw.line(surface, [0, 255, 0] if ClockSettings.DEBUG_MODE else couleur_pour_minutes,
                             (int((largeur / 2) + math.cos(degree_minute_ligne) * 115 * size_mult),
                              int((hauteur / 2) + math.sin(degree_minute_ligne) * 115 * size_mult)),
                             (int((largeur / 2) + math.cos(degree_minute_ligne) * 86 * size_mult),
                              int((hauteur / 2) + math.sin(degree_minute_ligne) * 86 * size_mult)),
                             int((3 if ClockSettings.LOW_FRAMERATE_MODE else 2) * size_mult))

        # Heures
        couleur_pour_heures = seconde_a_couleur((heure_changeante * 60) / 12)
        if degree_heures >= degree_secondes >= 0:
            pygame.draw.line(surface, [255, 0, 100] if ClockSettings.DEBUG_MODE else couleur_pour_heures,
                             (int((largeur / 2) + math.cos(math.radians(degree_secondes - 90)) * 80 * size_mult),
                              int((hauteur / 2) + math.sin(math.radians(degree_secondes - 90)) * 80 * size_mult)),
                             (int((largeur / 2) + math.cos(math.radians(degree_secondes - 90)) * 41 * size_mult),
                              int((hauteur / 2) + math.sin(math.radians(degree_secondes - 90)) * 41 * size_mult)),
                             int((3 if ClockSettings.LOW_FRAMERATE_MODE else 2) * size_mult))

        if not (do_arc_cleanup and minute < 1):
            pygame.draw.line(surface, [0, 255, 0] if ClockSettings.DEBUG_MODE else couleur_pour_heures,
                             (int((largeur / 2) + math.cos(degree_heures_ligne) * 80 * size_mult),
                              int((hauteur / 2) + math.sin(degree_heures_ligne) * 80 * size_mult)),
                             (int((largeur / 2) + math.cos(degree_heures_ligne) * 41 * size_mult),
                              int((hauteur / 2) + math.sin(degree_heures_ligne) * 41 * size_mult)),
                             int((3 if ClockSettings.LOW_FRAMERATE_MODE else 2) * size_mult))

    # Couleurs secondes
    couleur_pour_secondes = seconde_a_couleur(seconde_precise)

    if ClockSettings.LOW_FRAMERATE_MODE or color_wheel_active:
        pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes, math.radians(111 - degree_secondes),
                        math.radians(123 - degree_secondes), int(30 * size_mult))
        pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes, math.radians(111.5 - degree_secondes),
                        math.radians(123 - degree_secondes), int(30 * size_mult))
        pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes, math.radians(112 - degree_secondes),
                        math.radians(123 - degree_secondes), int(30 * size_mult))
    else:
        # pygame.draw.line(surface, couleur_pour_secondes,
        #                  (int((largeur / 2) + math.cos(math.radians(degree_secondes - 110)) * 150 * size_mult),
        #                   int((hauteur / 2) + math.sin(math.radians(degree_secondes - 110)) * 150 * size_mult)),
        #                  (int((largeur / 2) + math.cos(math.radians(degree_secondes - 110)) * 120 * size_mult),
        #                   int((hauteur / 2) + math.sin(math.radians(degree_secondes - 110)) * 120 * size_mult)),
        #                  int((3 if ClockSettings.LOW_FRAMERATE_MODE else 2) * size_mult))
        pygame.draw.arc(surface, couleur_pour_secondes, rect_couleurs_secondes, math.radians(111 - degree_secondes),
                        math.radians(114 - degree_secondes), int(30 * size_mult))

    # Arc secondes (noir)
    if ClockSettings.LOW_FRAMERATE_MODE:
        pygame.draw.arc(surface, [255, 0, 0] if ClockSettings.DEBUG_MODE else couleur_arc_secondes,
                        rect_arc_secondes, math.radians(70 - degree_secondes),
                        math.radians(80 - degree_secondes), int(34 * size_mult))
        pygame.draw.arc(surface, [0, 255, 0] if ClockSettings.DEBUG_MODE else couleur_arc_secondes,
                        rect_arc_secondes, math.radians(70.5 - degree_secondes),
                        math.radians(80 - degree_secondes), int(34 * size_mult))
        pygame.draw.arc(surface, [0, 0, 255] if ClockSettings.DEBUG_MODE else couleur_arc_secondes,
                        rect_arc_secondes, math.radians(71 - degree_secondes),
                        math.radians(80 - degree_secondes), int(34 * size_mult))
    else:
        # pygame.draw.line(surface, couleur_arc_secondes,
        #                  (int((largeur / 2) + math.cos(math.radians(degree_secondes - 70)) * 151 * size_mult),
        #                   int((hauteur / 2) + math.sin(math.radians(degree_secondes - 70)) * 151 * size_mult)),
        #                  (int((largeur / 2) + math.cos(math.radians(degree_secondes - 70)) * 119 * size_mult),
        #                   int((hauteur / 2) + math.sin(math.radians(degree_secondes - 70)) * 119 * size_mult)),
        #                  int((3 if ClockSettings.LOW_FRAMERATE_MODE else 2) * size_mult))
        pygame.draw.arc(surface, [25, 25, 25] if ClockSettings.DEBUG_MODE else couleur_arc_secondes,
                        rect_arc_secondes, math.radians(70 - degree_secondes),
                        math.radians(74 - degree_secondes), int(34 * size_mult))

    if refresh_requested:
        draw_middle_circle = True
        refresh_requested = False

    if peek_animating:
        ecran.blit(surface, [peek_rect.left, peek_rect.top], peek_rect)
    else:
        ecran.blit(surface, [0, 0])

    if retour_thread['thread_en_cours'] or ClockSettings.DEBUG_MODE:
        text_anim_frame = int(millisec * len(text_anim_frames))

    if temps != text_dict['temps']['text']:
        text_dict['temps']['text'] = temps
        text_dict['temps']['surface'] = font_25.render(temps, True, [255, 255, 255])
        text_dict['temps']['rect'] = text_dict['temps']['surface'].get_rect(center=((largeur // 2), (hauteur // 2)))
    ecran.blit(text_dict['temps']['surface'], text_dict['temps']['rect'])

    if seconde != text_dict['seconde']['text']:
        text_dict['seconde']['text'] = seconde
        text_dict['seconde']['surface'] = font_25.render(' ' + str(seconde) + ' ', True, [255, 255, 255])
    text_dict['seconde']['rotated_surface'] = pygame.transform.rotozoom(text_dict['seconde']['surface'],
                                                                        -degree_secondes + (
                                                                            180 if 45 > seconde_precise > 15 else 0), 1)
    text_dict['seconde']['rect'] = text_dict['seconde']['rotated_surface'].get_rect(center=(
        int((largeur / 2) + math.cos(math.radians(degree_secondes - 90)) * 135 * size_mult),
        int((hauteur / 2) + math.sin(math.radians(degree_secondes - 90)) * 135 * size_mult)))
    ecran.blit(text_dict['seconde']['rotated_surface'], text_dict['seconde']['rect'])

    if retour_thread['detailed_info'] != text_dict['detailed_info']['text']:
        text_dict['detailed_info']['text'] = retour_thread['detailed_info']
        text_dict['detailed_info']['surface'] = font_17.render(retour_thread['detailed_info'], True,
                                                               couleur_fond_inverse)
        text_dict['detailed_info']['rect'] = text_dict['detailed_info']['surface'].get_rect()
        text_dict['detailed_info']['rect'].left = int(2 * size_mult)
    ecran.blit(text_dict['detailed_info']['surface'], text_dict['detailed_info']['rect'])

    if (retour_thread['temperature'][0] or text_anim_frames[text_anim_frame]) != text_dict['temperature']['text']:
        text_dict['temperature']['text'] = retour_thread['temperature'][0] or text_anim_frames[text_anim_frame]

        if retour_thread['temperature'][0]:
            text_dict['temperature']['surface'] = font_25.render(text_dict['temperature']['text'], True,
                                                                 retour_thread['temperature'][1]['couleur'])
        else:
            text_dict['temperature']['surface'] = text_anim_surfaces['25'][text_anim_frame]

        text_dict['temperature']['rect'] = text_dict['temperature']['surface'].get_rect()
        texte_bottom = text_dict['detailed_info']['rect'].bottom
        text_dict['temperature']['rect'].top = texte_bottom
        text_dict['temperature']['rect'].left = int(2 * size_mult)
        text_dict['pourcent_pluie']['text'] = 'update me'
    text_dict['temperature']['wiggle_rect'] = text_dict['temperature']['rect']
    text_dict['temperature']['wiggle_surface'] = text_dict['temperature']['surface']
    if retour_thread['temperature'][1]['wiggle'] != 0:
        text_dict['temperature']['wiggle_surface'] = pygame.transform.rotate(text_dict['temperature']['surface'], (
                retour_thread['temperature'][1]['wiggle'] * math.sin(millisec * 25)))
        text_dict['temperature']['wiggle_rect'] = text_dict['temperature']['wiggle_surface'].get_rect(
            center=text_dict['temperature']['rect'].center)
    ecran.blit(text_dict['temperature']['wiggle_surface'], text_dict['temperature']['wiggle_rect'])

    if retour_thread['weather_icon']:
        image_rect = weather_icons[retour_thread['weather_icon']].get_rect()
        image_rect.centery = text_dict['temperature']['wiggle_rect'].centery
        image_rect.left = text_dict['temperature']['rect'].right + int((5 * size_mult))
        ecran.blit(weather_icons[retour_thread['weather_icon']], image_rect)

    if (retour_thread['pourcent_pluie'] or text_anim_frames[text_anim_frame]) != text_dict['pourcent_pluie']['text']:
        text_dict['pourcent_pluie']['text'] = retour_thread['pourcent_pluie'] or text_anim_frames[text_anim_frame]

        if retour_thread['pourcent_pluie']:
            text_dict['pourcent_pluie']['surface'] = font_17.render(text_dict['pourcent_pluie']['text'], True,
                                                                    couleur_fond_inverse)
        else:
            text_dict['pourcent_pluie']['surface'] = text_anim_surfaces['17'][text_anim_frame]

        text_dict['pourcent_pluie']['rect'] = text_dict['pourcent_pluie']['surface'].get_rect(
            center=(text_dict['temperature']['rect'].center[0], 0))
        text_dict['pourcent_pluie']['rect'].top = text_dict['temperature']['rect'].bottom
    if text_dict['pourcent_pluie']['text'] != ' ':
        ecran.blit(text_dict['pourcent_pluie']['surface'], text_dict['pourcent_pluie']['rect'])

    if ClockSettings.SHOW_MINING_INFO:
        if (retour_thread['ethermine_data'] or text_anim_frames[text_anim_frame]) != text_dict['ethermine_data'][
            'text']:
            text_dict['ethermine_data']['text'] = retour_thread['ethermine_data'] or text_anim_frames[text_anim_frame]

            if retour_thread['ethermine_data']:
                text_dict['ethermine_data']['surface'] = font_17.render(text_dict['ethermine_data']['text'], True,
                                                                        couleur_fond_inverse)
            else:
                text_dict['ethermine_data']['surface'] = text_anim_surfaces['17'][text_anim_frame]

            text_dict['ethermine_data']['rect'] = text_dict['ethermine_data']['surface'].get_rect()
            text_dict['ethermine_data']['rect'].bottom = hauteur
            text_dict['ethermine_data']['rect'].left = int(2 * size_mult)
        ecran.blit(text_dict['ethermine_data']['surface'], text_dict['ethermine_data']['rect'])

    if (retour_thread['valeur_ethereum'] or text_anim_frames[text_anim_frame]) != text_dict['valeur_ethereum']['text']:
        text_dict['valeur_ethereum']['text'] = retour_thread['valeur_ethereum'] or text_anim_frames[text_anim_frame]

        if retour_thread['valeur_ethereum']:
            text_dict['valeur_ethereum']['surface'] = font_17.render(text_dict['valeur_ethereum']['text'], True,
                                                                     couleur_fond_inverse)
        else:
            text_dict['valeur_ethereum']['surface'] = text_anim_surfaces['17'][text_anim_frame]

        text_dict['valeur_ethereum']['rect'] = text_dict['valeur_ethereum']['surface'].get_rect()
        if ClockSettings.SHOW_MINING_INFO:
            text_dict['valeur_ethereum']['rect'] = text_dict['valeur_ethereum']['surface'].get_rect(
                center=(text_dict['ethermine_data']['rect'].center[0], 0))
            text_dict['valeur_ethereum']['rect'].bottom = text_dict['ethermine_data']['rect'].top - int(2 * size_mult)
        else:
            text_dict['valeur_ethereum']['rect'].left = int(2 * size_mult)
            text_dict['valeur_ethereum']['rect'].bottom = hauteur

        texte_top = text_dict['valeur_ethereum']['rect'].top
        text_dict['ETH']['rect'] = text_dict['ETH']['surface'].get_rect(
            center=(text_dict['valeur_ethereum']['rect'].center[0], 0))
        text_dict['ETH']['rect'].bottom = texte_top
    ecran.blit(text_dict['valeur_ethereum']['surface'], text_dict['valeur_ethereum']['rect'])
    ecran.blit(text_dict['ETH']['surface'], text_dict['ETH']['rect'])

    if (retour_thread['valeur_bitcoin'] or text_anim_frames[text_anim_frame]) != text_dict['valeur_bitcoin']['text']:
        text_dict['valeur_bitcoin']['text'] = retour_thread['valeur_bitcoin'] or text_anim_frames[text_anim_frame]

        if retour_thread['valeur_bitcoin']:
            text_dict['valeur_bitcoin']['surface'] = font_17.render(text_dict['valeur_bitcoin']['text'], True,
                                                                    couleur_fond_inverse)
        else:
            text_dict['valeur_bitcoin']['surface'] = text_anim_surfaces['17'][text_anim_frame]

        text_dict['valeur_bitcoin']['rect'] = text_dict['valeur_bitcoin']['surface'].get_rect()
        texte_top = text_dict['ETH']['rect'].top - (2 * size_mult)
        text_dict['valeur_bitcoin']['rect'].left = int(2 * size_mult)
        text_dict['valeur_bitcoin']['rect'].bottom = int(texte_top)

        text_dict['BTC']['rect'] = text_dict['BTC']['surface'].get_rect(
            center=(text_dict['valeur_bitcoin']['rect'].center[0], 0))
        text_dict['BTC']['rect'].bottom = text_dict['valeur_bitcoin']['rect'].top
    ecran.blit(text_dict['valeur_bitcoin']['surface'], text_dict['valeur_bitcoin']['rect'])
    ecran.blit(text_dict['BTC']['surface'], text_dict['BTC']['rect'])

    if ClockSettings.FETCH_RELAIS_DATA:
        if (retour_thread['pistes_soir'] or text_anim_frames[text_anim_frame]) != text_dict['pistes_soir']['text']:
            text_dict['pistes_soir']['text'] = retour_thread['pistes_soir'] or text_anim_frames[text_anim_frame]

            if retour_thread['pistes_soir']:
                text_dict['pistes_soir']['surface'] = font_17.render(text_dict['pistes_soir']['text'], True,
                                                                     couleur_fond_inverse)
            else:
                text_dict['pistes_soir']['surface'] = text_anim_surfaces['17'][text_anim_frame]

            text_dict['pistes_soir']['rect'] = text_dict['pistes_soir']['surface'].get_rect()
            text_dict['pistes_soir']['rect'].left = int(2 * size_mult)
            text_dict['pistes_soir']['rect'].bottom = text_dict['BTC']['rect'].top - int(2 * size_mult)
            text_dict['SKI']['rect'] = text_dict['SKI']['surface'].get_rect(
                center=(text_dict['pistes_soir']['rect'].center[0], 0))
            text_dict['SKI']['rect'].bottom = text_dict['pistes_soir']['rect'].top
        ecran.blit(text_dict['pistes_soir']['surface'], text_dict['pistes_soir']['rect'])
        ecran.blit(text_dict['SKI']['surface'], text_dict['SKI']['rect'])

    if (retour_thread['fetching_animation_text'] or text_anim_frames[text_anim_frame]) != \
            text_dict['fetching_animation']['text']:
        text_dict['fetching_animation']['text'] = retour_thread['fetching_animation_text'] or text_anim_frames[
            text_anim_frame]

        if retour_thread['fetching_animation_text']:
            text_dict['fetching_animation']['surface'] = font_17.render(text_dict['fetching_animation']['text'], True,
                                                                        couleur_fond_inverse)
        else:
            text_dict['fetching_animation']['surface'] = text_anim_surfaces['17'][text_anim_frame]

        text_dict['fetching_animation']['rect'] = text_dict['fetching_animation']['surface'].get_rect()
        text_dict['fetching_animation']['rect'].left = int(2 * size_mult)
        if ClockSettings.FETCH_RELAIS_DATA:
            text_dict['fetching_animation']['rect'].bottom = text_dict['SKI']['rect'].top - int(20 * size_mult)
        else:
            text_dict['fetching_animation']['rect'].bottom = text_dict['BTC']['rect'].top - int(20 * size_mult)

    if text_dict['fetching_animation']['text'] != ' ':
        ecran.blit(text_dict['fetching_animation']['surface'], text_dict['fetching_animation']['rect'])

    if noms_jours_semaine[num_jour_semaine] != text_dict['noms_jours_semaine']['text'] or text_jour_semaine_couleur != \
            text_dict['noms_jours_semaine']['color']:
        text_dict['noms_jours_semaine']['text'] = noms_jours_semaine[num_jour_semaine]
        text_dict['noms_jours_semaine']['color'] = text_jour_semaine_couleur
        text_dict['noms_jours_semaine']['surface'] = font_25.render(noms_jours_semaine[num_jour_semaine], True,
                                                                    text_jour_semaine_couleur)
        text_dict['noms_jours_semaine']['rect'] = text_dict['noms_jours_semaine']['surface'].get_rect(
            center=(largeur - centre_date, 0))
        text_dict['noms_jours_semaine']['rect'].top = 0
    ecran.blit(text_dict['noms_jours_semaine']['surface'], text_dict['noms_jours_semaine']['rect'])

    if num_jour != text_dict['num_jour']['text']:
        text_dict['num_jour']['text'] = num_jour
        text_dict['num_jour']['surface'] = font_40.render(num_jour, True, couleur_fond_inverse)
        texte_bottom = text_dict['noms_jours_semaine']['rect'].bottom
        text_dict['num_jour']['rect'] = text_dict['num_jour']['surface'].get_rect(
            center=(text_dict['noms_jours_semaine']['rect'].center[0], 0))
        text_dict['num_jour']['rect'].top = int(texte_bottom - (12 * size_mult))
    ecran.blit(text_dict['num_jour']['surface'], text_dict['num_jour']['rect'])

    if noms_mois[num_mois] != text_dict['noms_mois']['text']:
        text_dict['noms_mois']['text'] = noms_mois[num_mois]
        text_dict['noms_mois']['surface'] = font_17.render(noms_mois[num_mois], True, couleur_fond_inverse)
        texte_bottom = text_dict['num_jour']['rect'].bottom
        text_dict['noms_mois']['rect'] = text_dict['noms_mois']['surface'].get_rect(
            center=(text_dict['num_jour']['rect'].center[0], 0))
        text_dict['noms_mois']['rect'].top = int(texte_bottom - (10 * size_mult))
    ecran.blit(text_dict['noms_mois']['surface'], text_dict['noms_mois']['rect'])

    # Countdown timer
    if ClockSettings.ENABLE_COUNTDOWN_TIMER:
        if changement_seconde or first_frame:
            # Countdown normal
            temps_restant = datetime.datetime(2023, 7, 21, 16, 0) - maintenant
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

            temps_restant = "{}:{}:{}:{}".format(temps_restant_jours, temps_restant_heures, temps_restant_mins,
                                                 temps_restant_secs)

        if temps_restant != text_dict['temps_restant']['text']:
            text_dict['temps_restant']['text'] = temps_restant
            text_dict['temps_restant']['surface'] = font_25.render(temps_restant, True, couleur_fond_inverse)
            text_dict['temps_restant']['rect'] = text_dict['temps_restant']['surface'].get_rect()
            text_dict['temps_restant']['rect'].right = int(largeur - (2 * size_mult))
            text_dict['temps_restant']['rect'].bottom = hauteur
        ecran.blit(text_dict['temps_restant']['surface'], text_dict['temps_restant']['rect'])

        # if changement_seconde or first_frame:
        # Disco
        # couleur_titre_countdown = seconde_a_couleur(seconde_precise, couleur_random=True)
        # Smooth
        couleur_titre_countdown = seconde_a_couleur(seconde_precise, inverser=True)
        # Noel (vert/rouge)
        # couleur_titre_countdown = [12, 169, 12] if seconde % 2 == 0 else [206, 13, 13]

        titre_countdown = 'Vacances :D'

        if titre_countdown != text_dict['titre_countdown']['text'] or couleur_titre_countdown != \
                text_dict['titre_countdown']['color']:
            text_dict['titre_countdown']['text'] = titre_countdown
            text_dict['titre_countdown']['color'] = couleur_titre_countdown
            text_dict['titre_countdown']['surface'] = font_17.render(titre_countdown, True, couleur_titre_countdown)
            texte_top = text_dict['temps_restant']['rect'].top
            text_dict['titre_countdown']['rect'] = text_dict['titre_countdown']['surface'].get_rect()
            text_dict['titre_countdown']['rect'].right = int(largeur - (2 * size_mult))
            text_dict['titre_countdown']['rect'].bottom = texte_top
        ecran.blit(text_dict['titre_countdown']['surface'], text_dict['titre_countdown']['rect'])

    # End countdown timer

    if calculated_fps != text_dict['calculated_fps']['text']:
        text_dict['calculated_fps']['text'] = calculated_fps
        text_dict['calculated_fps']['surface'] = font_17.render(calculated_fps, True, couleur_fond_inverse)
        texte_top = text_dict['titre_countdown']['rect'].top
        text_dict['calculated_fps']['rect'] = text_dict['calculated_fps']['surface'].get_rect()
        text_dict['calculated_fps']['rect'].right = int(largeur - (2 * size_mult))
        text_dict['calculated_fps']['rect'].bottom = texte_top if ClockSettings.ENABLE_COUNTDOWN_TIMER else hauteur
    ecran.blit(text_dict['calculated_fps']['surface'], text_dict['calculated_fps']['rect'])

    # render_spinning_image(vitesse_rpm=15)

    if AnimationLoopSettings.ENABLED:
        if loop_end_time <= maintenant:
            loop_end_time = maintenant + datetime.timedelta(seconds=loop_time)

        render_loop_image()

    if retour_thread['weather_animation'] or len(snowflake_list):
        if retour_thread['weather_animation'] == 'neige' or retour_thread['weather_animation'] == 'poudre' or len(
                snowflake_list):
            render_snowing()
        elif retour_thread['weather_animation'] == 'vergla':
            render_raining(freezing=True)
        elif retour_thread['weather_animation'] == 'pluie':
            render_raining()
        elif retour_thread['weather_animation'] == 'bruine':
            render_raining(drizzle=True)

    # -------------------------------------NOTIFICATIONS------------------------------------- #
    # notification_active = True
    # notifications[temps] = ["DEBUG", "TEST"]
    if notification_active:
        big_top_text = notifications[temps][0]
        big_bottom_text = notifications[temps][1]

        if (0.5 > millisec > 0.25) or millisec > 0.75:
            midi_couleur = [0, 0, 0]
        else:
            midi_couleur = seconde_a_couleur(seconde_precise)

        pygame.draw.rect(ecran, midi_couleur, [0, 0, largeur, hauteur])
        midi_texte = font_100.render(big_top_text, True, [255, 255, 255], midi_couleur)
        midi_texte_rect = midi_texte.get_rect(center=(largeur // 2, int(0.3 * hauteur)))
        ecran.blit(midi_texte, midi_texte_rect)
        midi_texte = font_100.render(big_bottom_text, True, [255, 255, 255], midi_couleur)
        midi_texte_rect = midi_texte.get_rect(center=(largeur // 2, int(0.7 * hauteur)))
        ecran.blit(midi_texte, midi_texte_rect)
    # --------------------------------------------------------------------------------------- #

    if toggle_menu:
        # pygame.draw.rect(ecran, [255, 0, 0], color_switch_rect)
        if toggle_brightness:
            position_souris = pygame.mouse.get_pos()

            brightness = 100 - ((position_souris[1] - brightness_slider_rect.top) / brightness_slider_rect.height) * 100
            brightness = 0 if brightness < 0 else brightness
            brightness = 100 if brightness > 100 else brightness
            draw_brightness_slider(brightness)

            if not change_brightness_thread.is_alive():
                change_brightness_thread = Thread(target=change_brightness)
                change_brightness_thread.start()

        ecran.blit(menu_surface, menu_rect)

    if peek_animating:
        for rect in peek_blit_list:
            ecran.blit(peek_surface, [rect.left, rect.top], rect)

    duree_last_frame = sleep_until_next_frame()

    if first_frame:
        first_frame = False

    if not startup_complete and en_fonction:
        startup_complete = True

    frame_counter += 1
    if changement_seconde:
        if not toggle_menu and not color_wheel_active:
            pygame.mouse.set_visible(False)
        calculated_fps = '{} fps'.format(frame_counter)
        frame_counter = 0

pygame.mouse.set_pos(largeur, hauteur)
pygame.mouse.set_visible(False)
ecran.set_clip([0, 0, largeur, hauteur])
peek_surface.blit(ecran, [0, 0])

surface.fill([0, 0, 0])

if not startup_complete:
    texte = font_100.render(status_loading_text, True, [255, 255, 255])
    texte_rect = texte.get_rect(center=(largeur // 2, hauteur // 2))
    surface.blit(texte, texte_rect)
elif DisplaySettings.AUTOMATIC_RESOLUTION and (DisplaySettings.FULLSCREEN or DisplaySettings.BORDERLESS_WINDOW):
    surface.blit(desktop_img, [0, 0])

corner_distances = [math.sqrt((position_souris[0] - 0) ** 2.0 + (position_souris[1] - 0) ** 2.0),
                    math.sqrt((position_souris[0] - largeur) ** 2.0 + (position_souris[1] - 0) ** 2.0),
                    math.sqrt((position_souris[0] - 0) ** 2.0 + (position_souris[1] - hauteur) ** 2.0),
                    math.sqrt((position_souris[0] - largeur) ** 2.0 + (position_souris[1] - hauteur) ** 2.0)]

corner_distances.sort()
peek_radius_limit = corner_distances.pop()
peek_radius = 0
peek_status = 0
peek_blit_list = []
a_squared = position_souris[1] ** 2 if position_souris[1] > hauteur / 2 else (hauteur - position_souris[1]) ** 2

while peek_radius <= peek_radius_limit:
    maintenant = datetime.datetime.now()

    peek_status = peek_status + (duree_last_frame if duree_last_frame <= 0.05 else 0.05)

    peek_radius = int(peek_status * 250 * size_mult)
    peek_rect = pygame.draw.circle(peek_surface, [128, 128, 128], [position_souris[0], position_souris[1]],
                                   peek_radius + int(5 * size_mult))
    pygame.draw.circle(peek_surface, [100, 50, 0], [position_souris[0], position_souris[1]], peek_radius)

    for rect in peek_blit_list:
        if peek_radius ** 2 >= a_squared:
            rect.height = hauteur
            ecran.blit(surface, [rect.left, rect.top], rect)

    peek_blit_list = []

    if peek_radius ** 2 >= a_squared:
        peek_rect_right = peek_rect.copy()
        peek_rect_left = peek_rect.copy()

        # Right rect
        peek_rect_right_right = peek_rect_right.right
        peek_rect_right.left = math.sqrt(peek_radius ** 2 - a_squared) + position_souris[0]
        peek_rect_right.width = peek_rect_right_right - peek_rect_right.left

        if peek_rect_right.left <= largeur:
            peek_blit_list.append(peek_rect_right)

        # Left rect
        peek_rect_left_left = peek_rect_left.left
        peek_rect_left.width = position_souris[0] - math.sqrt(peek_radius ** 2 - a_squared)
        if peek_rect_left.right >= 0:
            peek_blit_list.append(peek_rect_left)
    else:
        peek_blit_list.append(peek_rect)

    for rect in peek_blit_list:
        ecran.blit(surface, [rect.left, rect.top], rect)
        ecran.blit(peek_surface, [rect.left, rect.top], rect)

    duree_last_frame = sleep_until_next_frame()

# Reusing startup_complete since its only needed during startup
if startup_complete:
    if ClockSettings.ANDROID_MODE:
        # This should be the best solution but it only works half the time :/
        """PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        maintenant = datetime.datetime.now()
        activity.finishWithoutAnimation()"""


        # This tries to prevent the exit animation from playing
        def exit_android():
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            activity.finish()


        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        maintenant = time.time()
        android_exit_thread = Thread(target=exit_android)
        android_exit_thread.start()

        activity.overridePendingTransition(0, 0)

        while time.time() - maintenant < 1:
            activity.overridePendingTransition(0, 0)

        while android_exit_thread.is_alive():
            activity.overridePendingTransition(0, 0)

        activity.overridePendingTransition(0, 0)
    else:
        os.system('sudo pkill -9 -f "python3 .*/myclock.py$"')
else:
    # time.sleep(1)
    try:
        # import RPi.GPIO as GPIO

        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(23, GPIO.OUT)
        # GPIO.output(23, 1)
        os.system("sudo reboot")
        time.sleep(5)
    except Exception:
        pass
