import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_en.dart';
import 'app_localizations_sv.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'l10n/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
    : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
        delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en'),
    Locale('sv'),
  ];

  /// The title of the application
  ///
  /// In en, this message translates to:
  /// **'Flashy\'s Math Adventure'**
  String get appTitle;

  /// No description provided for @appTagline.
  ///
  /// In en, this message translates to:
  /// **'Help Flashy find the way home!'**
  String get appTagline;

  /// No description provided for @loadingPyodide.
  ///
  /// In en, this message translates to:
  /// **'Loading Pyodide...'**
  String get loadingPyodide;

  /// No description provided for @loadingPython.
  ///
  /// In en, this message translates to:
  /// **'Setting up Python environment...'**
  String get loadingPython;

  /// No description provided for @loadingSpeech.
  ///
  /// In en, this message translates to:
  /// **'Loading speech model...'**
  String get loadingSpeech;

  /// No description provided for @loadingReady.
  ///
  /// In en, this message translates to:
  /// **'Ready!'**
  String get loadingReady;

  /// No description provided for @playerWhoPlaying.
  ///
  /// In en, this message translates to:
  /// **'Who\'s playing today?'**
  String get playerWhoPlaying;

  /// No description provided for @playerNoPlayers.
  ///
  /// In en, this message translates to:
  /// **'No players yet!'**
  String get playerNoPlayers;

  /// No description provided for @playerNewPlayer.
  ///
  /// In en, this message translates to:
  /// **'New Player'**
  String get playerNewPlayer;

  /// No description provided for @playerLevel.
  ///
  /// In en, this message translates to:
  /// **'Level'**
  String get playerLevel;

  /// No description provided for @playerNewTitle.
  ///
  /// In en, this message translates to:
  /// **'New Player'**
  String get playerNewTitle;

  /// No description provided for @playerEnterName.
  ///
  /// In en, this message translates to:
  /// **'Enter your name...'**
  String get playerEnterName;

  /// No description provided for @playerCreate.
  ///
  /// In en, this message translates to:
  /// **'Create'**
  String get playerCreate;

  /// No description provided for @playerCancel.
  ///
  /// In en, this message translates to:
  /// **'Cancel'**
  String get playerCancel;

  /// No description provided for @playerErrorEmpty.
  ///
  /// In en, this message translates to:
  /// **'Please enter a name'**
  String get playerErrorEmpty;

  /// No description provided for @playerErrorInvalid.
  ///
  /// In en, this message translates to:
  /// **'Please use letters and numbers only'**
  String get playerErrorInvalid;

  /// No description provided for @playerErrorExists.
  ///
  /// In en, this message translates to:
  /// **'\'{name}\' already exists!'**
  String playerErrorExists(String name);

  /// No description provided for @playerErrorTooLong.
  ///
  /// In en, this message translates to:
  /// **'Name too long (max 20 characters)'**
  String get playerErrorTooLong;

  /// No description provided for @playerErrorTaken.
  ///
  /// In en, this message translates to:
  /// **'Name already taken on leaderboard. Choose another!'**
  String get playerErrorTaken;

  /// No description provided for @playerErrorRegistration.
  ///
  /// In en, this message translates to:
  /// **'Registration failed'**
  String get playerErrorRegistration;

  /// No description provided for @playerErrorConnection.
  ///
  /// In en, this message translates to:
  /// **'Could not connect to leaderboard. Try again.'**
  String get playerErrorConnection;

  /// No description provided for @playerRegistering.
  ///
  /// In en, this message translates to:
  /// **'Registering...'**
  String get playerRegistering;

  /// No description provided for @navBack.
  ///
  /// In en, this message translates to:
  /// **'Back'**
  String get navBack;

  /// No description provided for @navContinue.
  ///
  /// In en, this message translates to:
  /// **'Continue'**
  String get navContinue;

  /// No description provided for @navReplay.
  ///
  /// In en, this message translates to:
  /// **'Replay'**
  String get navReplay;

  /// No description provided for @gameplayScore.
  ///
  /// In en, this message translates to:
  /// **'Score: {score}'**
  String gameplayScore(int score);

  /// No description provided for @gameplayTypeAnswer.
  ///
  /// In en, this message translates to:
  /// **'Type answer + Enter'**
  String get gameplayTypeAnswer;

  /// No description provided for @gameplayListening.
  ///
  /// In en, this message translates to:
  /// **'Listening...'**
  String get gameplayListening;

  /// No description provided for @gameplayMicRequest.
  ///
  /// In en, this message translates to:
  /// **'Requesting microphone...'**
  String get gameplayMicRequest;

  /// No description provided for @gameplayCorrect.
  ///
  /// In en, this message translates to:
  /// **'Correct!'**
  String get gameplayCorrect;

  /// No description provided for @gameplayWrong.
  ///
  /// In en, this message translates to:
  /// **'Wrong!'**
  String get gameplayWrong;

  /// No description provided for @gameplayEnter.
  ///
  /// In en, this message translates to:
  /// **'Enter'**
  String get gameplayEnter;

  /// No description provided for @resultComplete.
  ///
  /// In en, this message translates to:
  /// **'Level Complete!'**
  String get resultComplete;

  /// No description provided for @resultFailed.
  ///
  /// In en, this message translates to:
  /// **'Keep Practicing!'**
  String get resultFailed;

  /// No description provided for @resultNewBest.
  ///
  /// In en, this message translates to:
  /// **'NEW BEST!'**
  String get resultNewBest;

  /// No description provided for @resultCorrect.
  ///
  /// In en, this message translates to:
  /// **'{correct}/{total} correct'**
  String resultCorrect(int correct, int total);

  /// No description provided for @resultScore.
  ///
  /// In en, this message translates to:
  /// **'Score: {score}'**
  String resultScore(int score);

  /// No description provided for @resultTime.
  ///
  /// In en, this message translates to:
  /// **'Time: {time}'**
  String resultTime(String time);

  /// No description provided for @resultUpdating.
  ///
  /// In en, this message translates to:
  /// **'Updating leaderboard...'**
  String get resultUpdating;

  /// No description provided for @leaderboardTitle.
  ///
  /// In en, this message translates to:
  /// **'Leaderboard'**
  String get leaderboardTitle;

  /// No description provided for @victoryTitle.
  ///
  /// In en, this message translates to:
  /// **'VICTORY!'**
  String get victoryTitle;

  /// No description provided for @gameCompleteTitle.
  ///
  /// In en, this message translates to:
  /// **'HOME AT LAST!'**
  String get gameCompleteTitle;

  /// No description provided for @gameCompleteHint.
  ///
  /// In en, this message translates to:
  /// **'Click anywhere to return to menu...'**
  String get gameCompleteHint;

  /// No description provided for @introFlashy.
  ///
  /// In en, this message translates to:
  /// **'FLASHY'**
  String get introFlashy;

  /// No description provided for @introStory.
  ///
  /// In en, this message translates to:
  /// **'\"Oh no! Where am I?\"\n\n\"I chased that butterfly too far...\"\n\n\"I need to find my way home!\"'**
  String get introStory;

  /// No description provided for @introHint.
  ///
  /// In en, this message translates to:
  /// **'Click anywhere to continue...'**
  String get introHint;

  /// No description provided for @inputVoice.
  ///
  /// In en, this message translates to:
  /// **'Voice'**
  String get inputVoice;

  /// No description provided for @inputKeyboard.
  ///
  /// In en, this message translates to:
  /// **'Keyboard'**
  String get inputKeyboard;

  /// No description provided for @world1Name.
  ///
  /// In en, this message translates to:
  /// **'Addition Alps'**
  String get world1Name;

  /// No description provided for @world2Name.
  ///
  /// In en, this message translates to:
  /// **'Subtraction Swamp'**
  String get world2Name;

  /// No description provided for @world3Name.
  ///
  /// In en, this message translates to:
  /// **'Multiplication Meadows'**
  String get world3Name;

  /// No description provided for @world4Name.
  ///
  /// In en, this message translates to:
  /// **'Division Desert'**
  String get world4Name;

  /// No description provided for @world1Intro.
  ///
  /// In en, this message translates to:
  /// **'Flashy woke up alone in the cold mountains.\n\"Where am I? I need to find my way home!\"\nThe only way forward is up through the Addition Alps...'**
  String get world1Intro;

  /// No description provided for @world2Intro.
  ///
  /// In en, this message translates to:
  /// **'The mountains gave way to murky wetlands.\n\"It\'s so foggy here... but I must keep going!\"\nFlashy stepped carefully into the Subtraction Swamp...'**
  String get world2Intro;

  /// No description provided for @world3Intro.
  ///
  /// In en, this message translates to:
  /// **'Beautiful flowers swayed in the breeze.\n\"What a lovely place... but I must keep moving!\"\nThe Multiplication Meadows bloomed with possibility...'**
  String get world3Intro;

  /// No description provided for @world4Intro.
  ///
  /// In en, this message translates to:
  /// **'The heat hit Flashy like a wall.\n\"So hot... but I can almost smell home!\"\nThe Division Desert stretched endlessly before...'**
  String get world4Intro;

  /// No description provided for @world1FriendName.
  ///
  /// In en, this message translates to:
  /// **'Carry'**
  String get world1FriendName;

  /// No description provided for @world1FriendIntro.
  ///
  /// In en, this message translates to:
  /// **'\"Hoo-hoo! I\'m Carry the Owl!\"\n\"I\'ve watched many travelers climb these peaks.\"\n\"Remember: when numbers get big, just carry on!\"\n\"Let me help you on your journey home.\"'**
  String get world1FriendIntro;

  /// No description provided for @world2FriendName.
  ///
  /// In en, this message translates to:
  /// **'Borrow'**
  String get world2FriendName;

  /// No description provided for @world2FriendIntro.
  ///
  /// In en, this message translates to:
  /// **'\"Slow down there, young pup!\"\n\"I\'m Borrow the Turtle. I\'ve lived here for centuries.\"\n\"When you need to take away more than you have,\"\n\"just borrow from your neighbor. Works every time!\"'**
  String get world2FriendIntro;

  /// No description provided for @world3FriendName.
  ///
  /// In en, this message translates to:
  /// **'Times'**
  String get world3FriendName;

  /// No description provided for @world3FriendIntro.
  ///
  /// In en, this message translates to:
  /// **'\"Oh my, oh my! A visitor!\" *hops excitedly*\n\"I\'m Times the Rabbit! I multiply EVERYTHING!\"\n\"One carrot becomes two, two become four!\"\n\"Multiplication is just fast addition, you know!\"'**
  String get world3FriendIntro;

  /// No description provided for @world4FriendName.
  ///
  /// In en, this message translates to:
  /// **'Remainder'**
  String get world4FriendName;

  /// No description provided for @world4FriendIntro.
  ///
  /// In en, this message translates to:
  /// **'\"Ah, a traveler! I am Remainder the Camel.\"\n\"I carry what\'s left over from every division.\"\n\"Remember: divide means to share equally!\"\n\"Split it up fair, and you\'ll find your answer.\"'**
  String get world4FriendIntro;

  /// No description provided for @world1BossName.
  ///
  /// In en, this message translates to:
  /// **'Summit'**
  String get world1BossName;

  /// No description provided for @world1BossIntro.
  ///
  /// In en, this message translates to:
  /// **'\"So, little pup, you think you can cross MY mountain?\"\n\"I am Summit, guardian of the Alps!\"\n\"Prove your addition skills... if you can keep up!\"'**
  String get world1BossIntro;

  /// No description provided for @world1BossDefeat.
  ///
  /// In en, this message translates to:
  /// **'\"Impressive, little one! You\'ve earned passage.\"\n\"The path ahead leads to the Subtraction Swamp.\"\n\"May your numbers stay strong!\"'**
  String get world1BossDefeat;

  /// No description provided for @world2BossName.
  ///
  /// In en, this message translates to:
  /// **'Minus'**
  String get world2BossName;

  /// No description provided for @world2BossIntro.
  ///
  /// In en, this message translates to:
  /// **'\"RIBBIT! Who dares enter my swamp?\"\n\"I am Minus, the Frog King!\"\n\"Let\'s see if you can subtract as fast as I can jump!\"'**
  String get world2BossIntro;

  /// No description provided for @world2BossDefeat.
  ///
  /// In en, this message translates to:
  /// **'\"RIBBIT... you\'ve bested me, small one.\"\n\"The meadows lie ahead. Enjoy the flowers!\"\n\"Hop along now!\"'**
  String get world2BossDefeat;

  /// No description provided for @world3BossName.
  ///
  /// In en, this message translates to:
  /// **'Countess Calculata'**
  String get world3BossName;

  /// No description provided for @world3BossIntro.
  ///
  /// In en, this message translates to:
  /// **'\"Well, well... the lost puppy arrives.\"\n\"I am Countess Calculata, master of multiplication!\"\n\"Beat me, and the desert path shall open!\"'**
  String get world3BossIntro;

  /// No description provided for @world3BossDefeat.
  ///
  /// In en, this message translates to:
  /// **'\"Magnificent! You\'ve mastered multiplication!\"\n\"The desert lies ahead. Stay hydrated!\"\n\"Your home draws ever closer.\"'**
  String get world3BossDefeat;

  /// No description provided for @world4BossName.
  ///
  /// In en, this message translates to:
  /// **'The Sphinx of Splits'**
  String get world4BossName;

  /// No description provided for @world4BossIntro.
  ///
  /// In en, this message translates to:
  /// **'\"HALT, wanderer! None pass without solving my riddles.\"\n\"I am the Sphinx of Splits!\"\n\"Divide correctly, or be lost to the sands forever!\"'**
  String get world4BossIntro;

  /// No description provided for @world4BossDefeat.
  ///
  /// In en, this message translates to:
  /// **'\"You have wisdom beyond your years, young pup.\"\n\"Look there, beyond the dunes...\"\n\"Is that... your HOME?\"'**
  String get world4BossDefeat;

  /// No description provided for @gameCompleteStory.
  ///
  /// In en, this message translates to:
  /// **'\"I\'m home! I\'m finally home!\"\n\nFlashy\'s family rushed out to greet the little pup.\n\n\"We were so worried! Where did you go?\"\n\n\"I went on the most amazing adventure...\"\n\n\"And I learned SO much math along the way!\"'**
  String get gameCompleteStory;

  /// No description provided for @level1Name.
  ///
  /// In en, this message translates to:
  /// **'Trailhead'**
  String get level1Name;

  /// No description provided for @level2Name.
  ///
  /// In en, this message translates to:
  /// **'Foothills'**
  String get level2Name;

  /// No description provided for @level3Name.
  ///
  /// In en, this message translates to:
  /// **'Snowy Path'**
  String get level3Name;

  /// No description provided for @level4Name.
  ///
  /// In en, this message translates to:
  /// **'Alpine Meadow'**
  String get level4Name;

  /// No description provided for @level5Name.
  ///
  /// In en, this message translates to:
  /// **'Mountain Trail'**
  String get level5Name;

  /// No description provided for @level6Name.
  ///
  /// In en, this message translates to:
  /// **'Carry\'s Roost'**
  String get level6Name;

  /// No description provided for @level7Name.
  ///
  /// In en, this message translates to:
  /// **'Rocky Pass'**
  String get level7Name;

  /// No description provided for @level8Name.
  ///
  /// In en, this message translates to:
  /// **'Steep Cliffs'**
  String get level8Name;

  /// No description provided for @level9Name.
  ///
  /// In en, this message translates to:
  /// **'Final Ascent'**
  String get level9Name;

  /// No description provided for @level10Name.
  ///
  /// In en, this message translates to:
  /// **'Summit\'s Challenge'**
  String get level10Name;

  /// No description provided for @level11Name.
  ///
  /// In en, this message translates to:
  /// **'Marsh Edge'**
  String get level11Name;

  /// No description provided for @level12Name.
  ///
  /// In en, this message translates to:
  /// **'Muddy Waters'**
  String get level12Name;

  /// No description provided for @level13Name.
  ///
  /// In en, this message translates to:
  /// **'Foggy Path'**
  String get level13Name;

  /// No description provided for @level14Name.
  ///
  /// In en, this message translates to:
  /// **'Lily Pads'**
  String get level14Name;

  /// No description provided for @level15Name.
  ///
  /// In en, this message translates to:
  /// **'Cypress Grove'**
  String get level15Name;

  /// No description provided for @level16Name.
  ///
  /// In en, this message translates to:
  /// **'Borrow\'s Hollow'**
  String get level16Name;

  /// No description provided for @level17Name.
  ///
  /// In en, this message translates to:
  /// **'Murky Depths'**
  String get level17Name;

  /// No description provided for @level18Name.
  ///
  /// In en, this message translates to:
  /// **'Tangled Vines'**
  String get level18Name;

  /// No description provided for @level19Name.
  ///
  /// In en, this message translates to:
  /// **'Swamp\'s Heart'**
  String get level19Name;

  /// No description provided for @level20Name.
  ///
  /// In en, this message translates to:
  /// **'Minus\'s Throne'**
  String get level20Name;

  /// No description provided for @level21Name.
  ///
  /// In en, this message translates to:
  /// **'Flower Field'**
  String get level21Name;

  /// No description provided for @level22Name.
  ///
  /// In en, this message translates to:
  /// **'Butterfly Path'**
  String get level22Name;

  /// No description provided for @level23Name.
  ///
  /// In en, this message translates to:
  /// **'Clover Patch'**
  String get level23Name;

  /// No description provided for @level24Name.
  ///
  /// In en, this message translates to:
  /// **'Honeybee Hive'**
  String get level24Name;

  /// No description provided for @level25Name.
  ///
  /// In en, this message translates to:
  /// **'Dandelion Dell'**
  String get level25Name;

  /// No description provided for @level26Name.
  ///
  /// In en, this message translates to:
  /// **'Times\'s Burrow'**
  String get level26Name;

  /// No description provided for @level27Name.
  ///
  /// In en, this message translates to:
  /// **'Pollen Storm'**
  String get level27Name;

  /// No description provided for @level28Name.
  ///
  /// In en, this message translates to:
  /// **'Rainbow Bridge'**
  String get level28Name;

  /// No description provided for @level29Name.
  ///
  /// In en, this message translates to:
  /// **'Final Bloom'**
  String get level29Name;

  /// No description provided for @level30Name.
  ///
  /// In en, this message translates to:
  /// **'Calculata\'s Garden'**
  String get level30Name;

  /// No description provided for @level31Name.
  ///
  /// In en, this message translates to:
  /// **'Oasis Gate'**
  String get level31Name;

  /// No description provided for @level32Name.
  ///
  /// In en, this message translates to:
  /// **'Sandy Trail'**
  String get level32Name;

  /// No description provided for @level33Name.
  ///
  /// In en, this message translates to:
  /// **'Dune Ridge'**
  String get level33Name;

  /// No description provided for @level34Name.
  ///
  /// In en, this message translates to:
  /// **'Scorpion Pass'**
  String get level34Name;

  /// No description provided for @level35Name.
  ///
  /// In en, this message translates to:
  /// **'Mirage Valley'**
  String get level35Name;

  /// No description provided for @level36Name.
  ///
  /// In en, this message translates to:
  /// **'Remainder\'s Rest'**
  String get level36Name;

  /// No description provided for @level37Name.
  ///
  /// In en, this message translates to:
  /// **'Sandstorm'**
  String get level37Name;

  /// No description provided for @level38Name.
  ///
  /// In en, this message translates to:
  /// **'Sunscorch'**
  String get level38Name;

  /// No description provided for @level39Name.
  ///
  /// In en, this message translates to:
  /// **'Pyramid\'s Shadow'**
  String get level39Name;

  /// No description provided for @level40Name.
  ///
  /// In en, this message translates to:
  /// **'Sphinx\'s Riddles'**
  String get level40Name;

  /// No description provided for @navPlay.
  ///
  /// In en, this message translates to:
  /// **'Play'**
  String get navPlay;

  /// No description provided for @navAbout.
  ///
  /// In en, this message translates to:
  /// **'About'**
  String get navAbout;

  /// No description provided for @navPrivacy.
  ///
  /// In en, this message translates to:
  /// **'Privacy'**
  String get navPrivacy;

  /// No description provided for @leaderboardError.
  ///
  /// In en, this message translates to:
  /// **'Failed to load leaderboard'**
  String get leaderboardError;

  /// No description provided for @leaderboardEmpty.
  ///
  /// In en, this message translates to:
  /// **'No scores yet. Be the first!'**
  String get leaderboardEmpty;

  /// No description provided for @resultBestStreak.
  ///
  /// In en, this message translates to:
  /// **'Best Streak: {streak}'**
  String resultBestStreak(int streak);

  /// No description provided for @resultCorrectCount.
  ///
  /// In en, this message translates to:
  /// **'{correct} / {total}'**
  String resultCorrectCount(int correct, int total);

  /// No description provided for @gameplayBossLevel.
  ///
  /// In en, this message translates to:
  /// **'BOSS: Level {level}'**
  String gameplayBossLevel(int level);

  /// No description provided for @gameplayLevel.
  ///
  /// In en, this message translates to:
  /// **'Level {level}'**
  String gameplayLevel(int level);

  /// No description provided for @gameplayPointsEarned.
  ///
  /// In en, this message translates to:
  /// **'Correct! +{points}'**
  String gameplayPointsEarned(int points);

  /// No description provided for @gameplayStreak.
  ///
  /// In en, this message translates to:
  /// **'Score: {score} | {streak} streak!'**
  String gameplayStreak(int score, int streak);
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['en', 'sv'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en':
      return AppLocalizationsEn();
    case 'sv':
      return AppLocalizationsSv();
  }

  throw FlutterError(
    'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
    'an issue with the localizations generation tool. Please file an issue '
    'on GitHub with a reproducible sample app and the gen-l10n configuration '
    'that was used.',
  );
}
