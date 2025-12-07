// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Swedish (`sv`).
class AppLocalizationsSv extends AppLocalizations {
  AppLocalizationsSv([String locale = 'sv']) : super(locale);

  @override
  String get appTitle => 'Flashy\'s Matematikäventyr';

  @override
  String get appTagline => 'Hjälp Flashy att hitta hem!';

  @override
  String get loadingPyodide => 'Laddar Pyodide...';

  @override
  String get loadingPython => 'Förbereder Python...';

  @override
  String get loadingSpeech => 'Laddar röstmodell...';

  @override
  String get loadingReady => 'Redo!';

  @override
  String get playerWhoPlaying => 'Vem spelar idag?';

  @override
  String get playerNoPlayers => 'Inga spelare ännu!';

  @override
  String get playerNewPlayer => 'Ny spelare';

  @override
  String get playerLevel => 'Nivå';

  @override
  String get playerNewTitle => 'Ny spelare';

  @override
  String get playerEnterName => 'Skriv ditt namn...';

  @override
  String get playerCreate => 'Skapa';

  @override
  String get playerCancel => 'Avbryt';

  @override
  String get playerErrorEmpty => 'Skriv ett namn';

  @override
  String get playerErrorInvalid => 'Använd bara bokstäver och siffror';

  @override
  String playerErrorExists(String name) {
    return '\'$name\' finns redan!';
  }

  @override
  String get playerErrorTooLong => 'Namnet är för långt (max 20 tecken)';

  @override
  String get playerErrorTaken => 'Namnet är redan taget. Välj ett annat!';

  @override
  String get playerErrorRegistration => 'Registrering misslyckades';

  @override
  String get playerErrorConnection => 'Kunde inte ansluta. Försök igen.';

  @override
  String get playerRegistering => 'Registrerar...';

  @override
  String get navBack => 'Tillbaka';

  @override
  String get navContinue => 'Fortsätt';

  @override
  String get navReplay => 'Spela igen';

  @override
  String gameplayScore(int score) {
    return 'Poäng: $score';
  }

  @override
  String get gameplayTypeAnswer => 'Skriv svar + Enter';

  @override
  String get gameplayListening => 'Lyssnar...';

  @override
  String get gameplayMicRequest => 'Ber om mikrofon...';

  @override
  String get gameplayCorrect => 'Rätt!';

  @override
  String get gameplayWrong => 'Fel!';

  @override
  String get gameplayEnter => 'Enter';

  @override
  String get resultComplete => 'Nivå klar!';

  @override
  String get resultFailed => 'Fortsätt träna!';

  @override
  String get resultNewBest => 'NYTT REKORD!';

  @override
  String resultCorrect(int correct, int total) {
    return '$correct/$total rätt';
  }

  @override
  String resultScore(int score) {
    return 'Poäng: $score';
  }

  @override
  String resultTime(String time) {
    return 'Tid: $time';
  }

  @override
  String get resultUpdating => 'Uppdaterar topplistan...';

  @override
  String get leaderboardTitle => 'Topplista';

  @override
  String get victoryTitle => 'SEGER!';

  @override
  String get gameCompleteTitle => 'ÄNTLIGEN HEMMA!';

  @override
  String get gameCompleteHint => 'Klicka för att gå till menyn...';

  @override
  String get introFlashy => 'FLASHY';

  @override
  String get introStory =>
      '\"Åh nej! Var är jag?\"\n\n\"Jag jagade den där fjärilen för långt...\"\n\n\"Jag måste hitta hem!\"';

  @override
  String get introHint => 'Klicka för att fortsätta...';

  @override
  String get inputVoice => 'Röst';

  @override
  String get inputKeyboard => 'Tangentbord';

  @override
  String get world1Name => 'Additions-Alperna';

  @override
  String get world2Name => 'Subtraktions-Träsket';

  @override
  String get world3Name => 'Multiplikations-Ängarna';

  @override
  String get world4Name => 'Divisions-Öknen';

  @override
  String get world1Intro =>
      'Flashy vaknade ensam i de kalla bergen.\n\"Var är jag? Jag måste hitta hem!\"\nDen enda vägen framåt är upp genom Additions-Alperna...';

  @override
  String get world2Intro =>
      'Bergen övergick i dimmiga våtmarker.\n\"Det är så dimmigt här... men jag måste fortsätta!\"\nFlashy klev försiktigt in i Subtraktions-Träsket...';

  @override
  String get world3Intro =>
      'Vackra blommor vajade i vinden.\n\"Vilken fin plats... men jag måste fortsätta!\"\nMultiplikations-Ängarna blommade med möjligheter...';

  @override
  String get world4Intro =>
      'Hettan träffade Flashy som en vägg.\n\"Så varmt... men jag kan nästan lukta hemmet!\"\nDivisions-Öknen sträckte sig oändligt framåt...';

  @override
  String get world1FriendName => 'Carry';

  @override
  String get world1FriendIntro =>
      '\"Hu-hu! Jag är Carry Ugglan!\"\n\"Jag har sett många resenärer klättra dessa berg.\"\n\"Kom ihåg: när talen blir stora, minnessiffra!\"\n\"Låt mig hjälpa dig på din resa hem.\"';

  @override
  String get world2FriendName => 'Låna';

  @override
  String get world2FriendIntro =>
      '\"Sakta i backarna, lilla valpen!\"\n\"Jag är Låna Sköldpaddan. Jag har bott här i århundraden.\"\n\"När du behöver ta bort mer än du har,\"\n\"låna från grannen. Fungerar varje gång!\"';

  @override
  String get world3FriendName => 'Gånger';

  @override
  String get world3FriendIntro =>
      '\"Oj oj oj! En besökare!\" *hoppar glatt*\n\"Jag är Gånger Kaninen! Jag multiplicerar ALLT!\"\n\"En morot blir två, två blir fyra!\"\n\"Multiplikation är bara snabb addition!\"';

  @override
  String get world4FriendName => 'Rest';

  @override
  String get world4FriendIntro =>
      '\"Ah, en resenär! Jag är Rest Kamelen.\"\n\"Jag bär det som blir över från varje division.\"\n\"Kom ihåg: dela betyder att fördela lika!\"\n\"Dela rättvist, så hittar du svaret.\"';

  @override
  String get world1BossName => 'Toppen';

  @override
  String get world1BossIntro =>
      '\"Så, lilla valpen, tror du att du kan korsa MITT berg?\"\n\"Jag är Toppen, väktaren av Alperna!\"\n\"Bevisa dina additionskunskaper... om du kan hänga med!\"';

  @override
  String get world1BossDefeat =>
      '\"Imponerande, liten! Du har förtjänat passage.\"\n\"Vägen framåt leder till Subtraktions-Träsket.\"\n\"Må dina tal förbli starka!\"';

  @override
  String get world2BossName => 'Minus';

  @override
  String get world2BossIntro =>
      '\"KVACK! Vem vågar sig in i mitt träsk?\"\n\"Jag är Minus, Grodkungen!\"\n\"Låt oss se om du kan subtrahera lika snabbt som jag hoppar!\"';

  @override
  String get world2BossDefeat =>
      '\"KVACK... du har besegrat mig, liten.\"\n\"Ängarna ligger framför dig. Njut av blommorna!\"\n\"Hoppa vidare nu!\"';

  @override
  String get world3BossName => 'Grevinnan Calculata';

  @override
  String get world3BossIntro =>
      '\"Nåväl... den förlorade valpen anländer.\"\n\"Jag är Grevinnan Calculata, mästare av multiplikation!\"\n\"Besegra mig, så öppnas ökenvägen!\"';

  @override
  String get world3BossDefeat =>
      '\"Magnifikt! Du har bemästrat multiplikation!\"\n\"Öknen ligger framför dig. Håll dig hydrerad!\"\n\"Ditt hem närmar sig.\"';

  @override
  String get world4BossName => 'Delnings-Sfinxen';

  @override
  String get world4BossIntro =>
      '\"STOPP, vandrare! Ingen passerar utan att lösa mina gåtor.\"\n\"Jag är Delnings-Sfinxen!\"\n\"Dividera rätt, eller försvinn i sanden för alltid!\"';

  @override
  String get world4BossDefeat =>
      '\"Du har visdom bortom dina år, lilla valpen.\"\n\"Titta där, bortom dynerna...\"\n\"Är det... ditt HEM?\"';

  @override
  String get gameCompleteStory =>
      '\"Jag är hemma! Jag är äntligen hemma!\"\n\nFlashys familj rusade ut för att möta den lilla valpen.\n\n\"Vi var så oroliga! Var har du varit?\"\n\n\"Jag var på det mest fantastiska äventyret...\"\n\n\"Och jag lärde mig SÅ mycket matte på vägen!\"';

  @override
  String get level1Name => 'Startpunkten';

  @override
  String get level2Name => 'Kullarna';

  @override
  String get level3Name => 'Snöstigen';

  @override
  String get level4Name => 'Alpängen';

  @override
  String get level5Name => 'Bergsleden';

  @override
  String get level6Name => 'Carrys Näste';

  @override
  String get level7Name => 'Klipppasset';

  @override
  String get level8Name => 'Branta Klippor';

  @override
  String get level9Name => 'Sista Stigningen';

  @override
  String get level10Name => 'Toppens Utmaning';

  @override
  String get level11Name => 'Träskkanten';

  @override
  String get level12Name => 'Leriga Vatten';

  @override
  String get level13Name => 'Dimmiga Stigen';

  @override
  String get level14Name => 'Näckrosbladen';

  @override
  String get level15Name => 'Cypresslunden';

  @override
  String get level16Name => 'Lånas Håla';

  @override
  String get level17Name => 'Mörka Djupen';

  @override
  String get level18Name => 'Trassliga Rankor';

  @override
  String get level19Name => 'Träskets Hjärta';

  @override
  String get level20Name => 'Minus Tron';

  @override
  String get level21Name => 'Blomsterfältet';

  @override
  String get level22Name => 'Fjärilsstigen';

  @override
  String get level23Name => 'Klöverfläcken';

  @override
  String get level24Name => 'Bikupan';

  @override
  String get level25Name => 'Maskrosdalen';

  @override
  String get level26Name => 'Gångers Lya';

  @override
  String get level27Name => 'Pollenstormen';

  @override
  String get level28Name => 'Regnbågsbron';

  @override
  String get level29Name => 'Sista Blomningen';

  @override
  String get level30Name => 'Calculatas Trädgård';

  @override
  String get level31Name => 'Oasporten';

  @override
  String get level32Name => 'Sandstigen';

  @override
  String get level33Name => 'Dynkammen';

  @override
  String get level34Name => 'Skorpionpasset';

  @override
  String get level35Name => 'Hägringsdalen';

  @override
  String get level36Name => 'Rests Vila';

  @override
  String get level37Name => 'Sandstormen';

  @override
  String get level38Name => 'Solbrännan';

  @override
  String get level39Name => 'Pyramidens Skugga';

  @override
  String get level40Name => 'Sfinxens Gåtor';

  @override
  String get navPlay => 'Spela';

  @override
  String get navAbout => 'Om';

  @override
  String get navPrivacy => 'Integritet';

  @override
  String get leaderboardError => 'Kunde inte ladda topplistan';

  @override
  String get leaderboardEmpty => 'Inga poäng ännu. Bli den första!';

  @override
  String resultBestStreak(int streak) {
    return 'Bästa svit: $streak';
  }

  @override
  String resultCorrectCount(int correct, int total) {
    return '$correct / $total';
  }

  @override
  String gameplayBossLevel(int level) {
    return 'BOSS: Nivå $level';
  }

  @override
  String gameplayLevel(int level) {
    return 'Nivå $level';
  }

  @override
  String gameplayPointsEarned(int points) {
    return 'Rätt! +$points';
  }

  @override
  String gameplayStreak(int score, int streak) {
    return 'Poäng: $score | $streak i rad!';
  }
}
