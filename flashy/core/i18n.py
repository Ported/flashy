"""Internationalization support for Flashy.

Supports English (en) and Swedish (sv) translations.
"""

from typing import Literal

Language = Literal["en", "sv"]

# Current language setting
_current_language: Language = "en"


def set_language(lang: Language) -> None:
    """Set the current language."""
    global _current_language
    _current_language = lang


def get_language() -> Language:
    """Get the current language."""
    return _current_language


def t(key: str, lang: Language | None = None) -> str:
    """Get translated string for key.

    Args:
        key: Translation key (e.g., "ui.new_player")
        lang: Language code, or None to use current language

    Returns:
        Translated string, or the key itself if not found
    """
    lang = lang or _current_language
    translations = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return translations.get(key, key)


# =============================================================================
# TRANSLATIONS
# =============================================================================

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        # App title
        "app.title": "Flashy's Math Adventure",
        # Loading
        "loading.pyodide": "Loading Pyodide...",
        "loading.python": "Setting up Python environment...",
        "loading.speech": "Loading speech model...",
        "loading.ready": "Ready!",
        # Player select screen
        "player.who_playing": "Who's playing today?",
        "player.no_players": "No players yet!",
        "player.new_player": "New Player",
        "player.level": "Level",
        # New player screen
        "player.new_title": "New Player",
        "player.enter_name": "Enter your name...",
        "player.create": "Create",
        "player.cancel": "Cancel",
        "player.error_empty": "Please enter a name",
        "player.error_invalid": "Please use letters and numbers only",
        "player.error_exists": "'{name}' already exists!",
        # Navigation
        "nav.back": "Back",
        "nav.continue": "Continue",
        "nav.replay": "Replay",
        # Gameplay
        "gameplay.score": "Score: {score}",
        "gameplay.type_answer": "Type answer + Enter",
        "gameplay.listening": "Listening...",
        "gameplay.mic_request": "Requesting microphone...",
        "gameplay.correct": "Correct!",
        "gameplay.wrong": "Wrong! Answer: {answer}",
        "gameplay.enter": "Enter",
        # Result screen
        "result.complete": "Level Complete!",
        "result.failed": "Keep Practicing!",
        "result.new_best": "NEW BEST!",
        "result.correct": "{correct}/{total} correct",
        "result.score": "Score: {score}",
        "result.time": "Time: {time}",
        # Boss/Victory
        "victory.title": "VICTORY!",
        "game_complete.title": "HOME AT LAST!",
        "game_complete.hint": "Click anywhere to return to menu...",
        # Intro screen
        "intro.flashy": "FLASHY",
        "intro.story": (
            '"Oh no! Where am I?"\n\n'
            '"I chased that butterfly too far..."\n\n'
            '"I need to find my way home!"'
        ),
        "intro.hint": "Click anywhere to continue...",
        # Input toggle
        "input.voice": "Voice",
        "input.keyboard": "Keyboard",
        # World names
        "world.1.name": "Addition Alps",
        "world.2.name": "Subtraction Swamp",
        "world.3.name": "Division Desert",
        "world.4.name": "Multiplication Meadows",
        # World intros
        "world.1.intro": (
            "Flashy woke up alone in the cold mountains.\n"
            '"Where am I? I need to find my way home!"\n'
            "The only way forward is up through the Addition Alps..."
        ),
        "world.2.intro": (
            "The mountains gave way to murky wetlands.\n"
            '"It\'s so foggy here... but I must keep going!"\n'
            "Flashy stepped carefully into the Subtraction Swamp..."
        ),
        "world.3.intro": (
            "The heat hit Flashy like a wall.\n"
            '"So hot... but I can see green meadows in the distance!"\n'
            "The Division Desert stretched endlessly before..."
        ),
        "world.4.intro": (
            "Beautiful flowers swayed in the breeze.\n"
            '"I can almost smell home! It must be close!"\n'
            "The Multiplication Meadows bloomed with possibility..."
        ),
        # Friends
        "world.1.friend_name": "Carry",
        "world.1.friend_intro": (
            '"Hoo-hoo! I\'m Carry the Owl!"\n'
            '"I\'ve watched many travelers climb these peaks."\n'
            '"Remember: when numbers get big, just carry on!"\n'
            '"Let me help you on your journey home."'
        ),
        "world.2.friend_name": "Borrow",
        "world.2.friend_intro": (
            '"Slow down there, young pup!"\n'
            "\"I'm Borrow the Turtle. I've lived here for centuries.\"\n"
            '"When you need to take away more than you have,"\n'
            '"just borrow from your neighbor. Works every time!"'
        ),
        "world.3.friend_name": "Remainder",
        "world.3.friend_intro": (
            '"Ah, a traveler! I am Remainder the Camel."\n'
            '"I carry what\'s left over from every division."\n'
            '"Remember: divide means to share equally!"\n'
            '"Split it up fair, and you\'ll find your answer."'
        ),
        "world.4.friend_name": "Times",
        "world.4.friend_intro": (
            '"Oh my, oh my! A visitor!" *hops excitedly*\n'
            '"I\'m Times the Rabbit! I multiply EVERYTHING!"\n'
            '"One carrot becomes two, two become four!"\n'
            '"Multiplication is just fast addition, you know!"'
        ),
        # Bosses
        "world.1.boss_name": "Summit",
        "world.1.boss_intro": (
            '"So, little pup, you think you can cross MY mountain?"\n'
            '"I am Summit, guardian of the Alps!"\n'
            '"Prove your addition skills... if you can keep up!"'
        ),
        "world.1.boss_defeat": (
            '"Impressive, little one! You\'ve earned passage."\n'
            '"The path ahead leads to the Subtraction Swamp."\n'
            '"May your numbers stay strong!"'
        ),
        "world.2.boss_name": "Minus",
        "world.2.boss_intro": (
            '"RIBBIT! Who dares enter my swamp?"\n'
            '"I am Minus, the Frog King!"\n'
            '"Let\'s see if you can subtract as fast as I can jump!"'
        ),
        "world.2.boss_defeat": (
            '"RIBBIT... you\'ve bested me, small one."\n'
            '"The desert lies ahead. Stay hydrated!"\n'
            '"Hop along now!"'
        ),
        "world.3.boss_name": "The Sphinx of Splits",
        "world.3.boss_intro": (
            '"HALT, wanderer! None pass without solving my riddles."\n'
            '"I am the Sphinx of Splits!"\n'
            '"Divide correctly, or be lost to the sands forever!"'
        ),
        "world.3.boss_defeat": (
            '"You have wisdom beyond your years, young pup."\n'
            '"The meadows await. Your home draws near."\n'
            '"Go forth with my blessing."'
        ),
        "world.4.boss_name": "Countess Calculata",
        "world.4.boss_intro": (
            '"Well, well... the lost puppy finally arrives."\n'
            '"I am Countess Calculata, master of all operations!"\n'
            '"Beat me, and you\'ll find your way home at last!"'
        ),
        "world.4.boss_defeat": (
            '"Magnificent! You\'ve mastered it all!"\n'
            '"Look there, beyond the meadow..."\n'
            '"Is that... your HOME?"'
        ),
        # Game complete
        "game_complete.story": (
            "\"I'm home! I'm finally home!\"\n\n"
            "Flashy's family rushed out to greet the little pup.\n\n"
            '"We were so worried! Where did you go?"\n\n'
            '"I went on the most amazing adventure..."\n\n'
            '"And I learned SO much math along the way!"'
        ),
        # Level names - World 1
        "level.1.name": "Trailhead",
        "level.2.name": "Foothills",
        "level.3.name": "Snowy Path",
        "level.4.name": "Alpine Meadow",
        "level.5.name": "Mountain Trail",
        "level.6.name": "Carry's Roost",
        "level.7.name": "Rocky Pass",
        "level.8.name": "Steep Cliffs",
        "level.9.name": "Final Ascent",
        "level.10.name": "Summit's Challenge",
        # Level names - World 2
        "level.11.name": "Marsh Edge",
        "level.12.name": "Muddy Waters",
        "level.13.name": "Foggy Path",
        "level.14.name": "Lily Pads",
        "level.15.name": "Cypress Grove",
        "level.16.name": "Borrow's Hollow",
        "level.17.name": "Murky Depths",
        "level.18.name": "Tangled Vines",
        "level.19.name": "Swamp's Heart",
        "level.20.name": "Minus's Throne",
        # Level names - World 3
        "level.21.name": "Oasis Gate",
        "level.22.name": "Sandy Trail",
        "level.23.name": "Dune Ridge",
        "level.24.name": "Scorpion Pass",
        "level.25.name": "Mirage Valley",
        "level.26.name": "Remainder's Rest",
        "level.27.name": "Sandstorm",
        "level.28.name": "Sunscorch",
        "level.29.name": "Pyramid's Shadow",
        "level.30.name": "Sphinx's Riddles",
        # Level names - World 4
        "level.31.name": "Flower Field",
        "level.32.name": "Butterfly Path",
        "level.33.name": "Clover Patch",
        "level.34.name": "Honeybee Hive",
        "level.35.name": "Dandelion Dell",
        "level.36.name": "Times's Burrow",
        "level.37.name": "Pollen Storm",
        "level.38.name": "Rainbow Bridge",
        "level.39.name": "Final Bloom",
        "level.40.name": "Calculata's Garden",
    },
    "sv": {
        # App title
        "app.title": "Flashy's Matematikäventyr",
        # Loading
        "loading.pyodide": "Laddar Pyodide...",
        "loading.python": "Förbereder Python...",
        "loading.speech": "Laddar röstmodell...",
        "loading.ready": "Redo!",
        # Player select screen
        "player.who_playing": "Vem spelar idag?",
        "player.no_players": "Inga spelare ännu!",
        "player.new_player": "Ny spelare",
        "player.level": "Nivå",
        # New player screen
        "player.new_title": "Ny spelare",
        "player.enter_name": "Skriv ditt namn...",
        "player.create": "Skapa",
        "player.cancel": "Avbryt",
        "player.error_empty": "Skriv ett namn",
        "player.error_invalid": "Använd bara bokstäver och siffror",
        "player.error_exists": "'{name}' finns redan!",
        # Navigation
        "nav.back": "Tillbaka",
        "nav.continue": "Fortsätt",
        "nav.replay": "Spela igen",
        # Gameplay
        "gameplay.score": "Poäng: {score}",
        "gameplay.type_answer": "Skriv svar + Enter",
        "gameplay.listening": "Lyssnar...",
        "gameplay.mic_request": "Ber om mikrofon...",
        "gameplay.correct": "Rätt!",
        "gameplay.wrong": "Fel! Svaret är: {answer}",
        "gameplay.enter": "Enter",
        # Result screen
        "result.complete": "Nivå klar!",
        "result.failed": "Fortsätt träna!",
        "result.new_best": "NYTT REKORD!",
        "result.correct": "{correct}/{total} rätt",
        "result.score": "Poäng: {score}",
        "result.time": "Tid: {time}",
        # Boss/Victory
        "victory.title": "SEGER!",
        "game_complete.title": "ÄNTLIGEN HEMMA!",
        "game_complete.hint": "Klicka för att gå till menyn...",
        # Intro screen
        "intro.flashy": "FLASHY",
        "intro.story": (
            '"Åh nej! Var är jag?"\n\n'
            '"Jag jagade den där fjärilen för långt..."\n\n'
            '"Jag måste hitta hem!"'
        ),
        "intro.hint": "Klicka för att fortsätta...",
        # Input toggle
        "input.voice": "Röst",
        "input.keyboard": "Tangentbord",
        # World names
        "world.1.name": "Additions-Alperna",
        "world.2.name": "Subtraktions-Träsket",
        "world.3.name": "Divisions-Öknen",
        "world.4.name": "Multiplikations-Ängarna",
        # World intros
        "world.1.intro": (
            "Flashy vaknade ensam i de kalla bergen.\n"
            '"Var är jag? Jag måste hitta hem!"\n'
            "Den enda vägen framåt är upp genom Additions-Alperna..."
        ),
        "world.2.intro": (
            "Bergen övergick i dimmiga våtmarker.\n"
            '"Det är så dimmigt här... men jag måste fortsätta!"\n'
            "Flashy klev försiktigt in i Subtraktions-Träsket..."
        ),
        "world.3.intro": (
            "Hettan träffade Flashy som en vägg.\n"
            '"Så varmt... men jag kan se gröna ängar i fjärran!"\n'
            "Divisions-Öknen sträckte sig oändligt framåt..."
        ),
        "world.4.intro": (
            "Vackra blommor vajade i vinden.\n"
            '"Jag kan nästan lukta hemmet! Det måste vara nära!"\n'
            "Multiplikations-Ängarna blommade med möjligheter..."
        ),
        # Friends
        "world.1.friend_name": "Carry",
        "world.1.friend_intro": (
            '"Hu-hu! Jag är Carry Ugglan!"\n'
            '"Jag har sett många resenärer klättra dessa berg."\n'
            '"Kom ihåg: när talen blir stora, minnessiffra!"\n'
            '"Låt mig hjälpa dig på din resa hem."'
        ),
        "world.2.friend_name": "Låna",
        "world.2.friend_intro": (
            '"Sakta i backarna, lilla valpen!"\n'
            '"Jag är Låna Sköldpaddan. Jag har bott här i århundraden."\n'
            '"När du behöver ta bort mer än du har,"\n'
            '"låna från grannen. Fungerar varje gång!"'
        ),
        "world.3.friend_name": "Rest",
        "world.3.friend_intro": (
            '"Ah, en resenär! Jag är Rest Kamelen."\n'
            '"Jag bär det som blir över från varje division."\n'
            '"Kom ihåg: dela betyder att fördela lika!"\n'
            '"Dela rättvist, så hittar du svaret."'
        ),
        "world.4.friend_name": "Gånger",
        "world.4.friend_intro": (
            '"Oj oj oj! En besökare!" *hoppar glatt*\n'
            '"Jag är Gånger Kaninen! Jag multiplicerar ALLT!"\n'
            '"En morot blir två, två blir fyra!"\n'
            '"Multiplikation är bara snabb addition!"'
        ),
        # Bosses
        "world.1.boss_name": "Toppen",
        "world.1.boss_intro": (
            '"Så, lilla valpen, tror du att du kan korsa MITT berg?"\n'
            '"Jag är Toppen, väktaren av Alperna!"\n'
            '"Bevisa dina additionskunskaper... om du kan hänga med!"'
        ),
        "world.1.boss_defeat": (
            '"Imponerande, liten! Du har förtjänat passage."\n'
            '"Vägen framåt leder till Subtraktions-Träsket."\n'
            '"Må dina tal förbli starka!"'
        ),
        "world.2.boss_name": "Minus",
        "world.2.boss_intro": (
            '"KVACK! Vem vågar sig in i mitt träsk?"\n'
            '"Jag är Minus, Grodkungen!"\n'
            '"Låt oss se om du kan subtrahera lika snabbt som jag hoppar!"'
        ),
        "world.2.boss_defeat": (
            '"KVACK... du har besegrat mig, liten."\n'
            '"Öknen ligger framför dig. Håll dig hydrerad!"\n'
            '"Hoppa vidare nu!"'
        ),
        "world.3.boss_name": "Delnings-Sfinxen",
        "world.3.boss_intro": (
            '"STOPP, vandrare! Ingen passerar utan att lösa mina gåtor."\n'
            '"Jag är Delnings-Sfinxen!"\n'
            '"Dividera rätt, eller försvinn i sanden för alltid!"'
        ),
        "world.3.boss_defeat": (
            '"Du har visdom bortom dina år, lilla valpen."\n'
            '"Ängarna väntar. Ditt hem närmar sig."\n'
            '"Gå vidare med min välsignelse."'
        ),
        "world.4.boss_name": "Grevinnan Calculata",
        "world.4.boss_intro": (
            '"Nåväl... den förlorade valpen anländer äntligen."\n'
            '"Jag är Grevinnan Calculata, mästare av alla räknesätt!"\n'
            '"Besegra mig, så hittar du hem till slut!"'
        ),
        "world.4.boss_defeat": (
            '"Magnifikt! Du har bemästrat allt!"\n'
            '"Titta där, bortom ängen..."\n'
            '"Är det... ditt HEM?"'
        ),
        # Game complete
        "game_complete.story": (
            '"Jag är hemma! Jag är äntligen hemma!"\n\n'
            "Flashys familj rusade ut för att möta den lilla valpen.\n\n"
            '"Vi var så oroliga! Var har du varit?"\n\n'
            '"Jag var på det mest fantastiska äventyret..."\n\n'
            '"Och jag lärde mig SÅ mycket matte på vägen!"'
        ),
        # Level names - World 1
        "level.1.name": "Startpunkten",
        "level.2.name": "Kullarna",
        "level.3.name": "Snöstigen",
        "level.4.name": "Alpängen",
        "level.5.name": "Bergsleden",
        "level.6.name": "Carrys Näste",
        "level.7.name": "Klipppasset",
        "level.8.name": "Branta Klippor",
        "level.9.name": "Sista Stigningen",
        "level.10.name": "Toppens Utmaning",
        # Level names - World 2
        "level.11.name": "Träskkanten",
        "level.12.name": "Leriga Vatten",
        "level.13.name": "Dimmiga Stigen",
        "level.14.name": "Näckrosbladen",
        "level.15.name": "Cypresslunden",
        "level.16.name": "Lånas Håla",
        "level.17.name": "Mörka Djupen",
        "level.18.name": "Trassliga Rankor",
        "level.19.name": "Träskets Hjärta",
        "level.20.name": "Minus Tron",
        # Level names - World 3
        "level.21.name": "Oasporten",
        "level.22.name": "Sandstigen",
        "level.23.name": "Dynkammen",
        "level.24.name": "Skorpionpasset",
        "level.25.name": "Hägringsdalen",
        "level.26.name": "Rests Vila",
        "level.27.name": "Sandstormen",
        "level.28.name": "Solbrännan",
        "level.29.name": "Pyramidens Skugga",
        "level.30.name": "Sfinxens Gåtor",
        # Level names - World 4
        "level.31.name": "Blomsterfältet",
        "level.32.name": "Fjärilsstigen",
        "level.33.name": "Klöverfläcken",
        "level.34.name": "Bikupan",
        "level.35.name": "Maskrosdalen",
        "level.36.name": "Gångers Lya",
        "level.37.name": "Pollenstormen",
        "level.38.name": "Regnbågsbron",
        "level.39.name": "Sista Blomningen",
        "level.40.name": "Calculatas Trädgård",
    },
}
