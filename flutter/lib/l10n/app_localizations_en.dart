// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get appTitle => 'Flashy\'s Math Adventure';

  @override
  String get appTagline => 'Help Flashy find the way home!';

  @override
  String get loadingPyodide => 'Loading Pyodide...';

  @override
  String get loadingPython => 'Setting up Python environment...';

  @override
  String get loadingSpeech => 'Loading speech model...';

  @override
  String get loadingReady => 'Ready!';

  @override
  String get playerWhoPlaying => 'Who\'s playing today?';

  @override
  String get playerNoPlayers => 'No players yet!';

  @override
  String get playerNewPlayer => 'New Player';

  @override
  String get playerLevel => 'Level';

  @override
  String get playerNewTitle => 'New Player';

  @override
  String get playerEnterName => 'Enter your name...';

  @override
  String get playerCreate => 'Create';

  @override
  String get playerCancel => 'Cancel';

  @override
  String get playerErrorEmpty => 'Please enter a name';

  @override
  String get playerErrorInvalid => 'Please use letters and numbers only';

  @override
  String playerErrorExists(String name) {
    return '\'$name\' already exists!';
  }

  @override
  String get playerErrorTooLong => 'Name too long (max 20 characters)';

  @override
  String get playerErrorTaken =>
      'Name already taken on leaderboard. Choose another!';

  @override
  String get playerErrorRegistration => 'Registration failed';

  @override
  String get playerErrorConnection =>
      'Could not connect to leaderboard. Try again.';

  @override
  String get playerRegistering => 'Registering...';

  @override
  String get navBack => 'Back';

  @override
  String get navContinue => 'Continue';

  @override
  String get navReplay => 'Replay';

  @override
  String gameplayScore(int score) {
    return 'Score: $score';
  }

  @override
  String get gameplayTypeAnswer => 'Type answer + Enter';

  @override
  String get gameplayListening => 'Listening...';

  @override
  String get gameplayMicRequest => 'Requesting microphone...';

  @override
  String get gameplayCorrect => 'Correct!';

  @override
  String get gameplayWrong => 'Wrong!';

  @override
  String get gameplayEnter => 'Enter';

  @override
  String get resultComplete => 'Level Complete!';

  @override
  String get resultFailed => 'Keep Practicing!';

  @override
  String get resultNewBest => 'NEW BEST!';

  @override
  String resultCorrect(int correct, int total) {
    return '$correct/$total correct';
  }

  @override
  String resultScore(int score) {
    return 'Score: $score';
  }

  @override
  String resultTime(String time) {
    return 'Time: $time';
  }

  @override
  String get resultUpdating => 'Updating leaderboard...';

  @override
  String get leaderboardTitle => 'Leaderboard';

  @override
  String get victoryTitle => 'VICTORY!';

  @override
  String get gameCompleteTitle => 'HOME AT LAST!';

  @override
  String get gameCompleteHint => 'Click anywhere to return to menu...';

  @override
  String get introFlashy => 'FLASHY';

  @override
  String get introStory =>
      '\"Oh no! Where am I?\"\n\n\"I chased that butterfly too far...\"\n\n\"I need to find my way home!\"';

  @override
  String get introHint => 'Click anywhere to continue...';

  @override
  String get inputVoice => 'Voice';

  @override
  String get inputKeyboard => 'Keyboard';

  @override
  String get world1Name => 'Addition Alps';

  @override
  String get world2Name => 'Subtraction Swamp';

  @override
  String get world3Name => 'Multiplication Meadows';

  @override
  String get world4Name => 'Division Desert';

  @override
  String get world1Intro =>
      'Flashy woke up alone in the cold mountains.\n\"Where am I? I need to find my way home!\"\nThe only way forward is up through the Addition Alps...';

  @override
  String get world2Intro =>
      'The mountains gave way to murky wetlands.\n\"It\'s so foggy here... but I must keep going!\"\nFlashy stepped carefully into the Subtraction Swamp...';

  @override
  String get world3Intro =>
      'Beautiful flowers swayed in the breeze.\n\"What a lovely place... but I must keep moving!\"\nThe Multiplication Meadows bloomed with possibility...';

  @override
  String get world4Intro =>
      'The heat hit Flashy like a wall.\n\"So hot... but I can almost smell home!\"\nThe Division Desert stretched endlessly before...';

  @override
  String get world1FriendName => 'Carry';

  @override
  String get world1FriendIntro =>
      '\"Hoo-hoo! I\'m Carry the Owl!\"\n\"I\'ve watched many travelers climb these peaks.\"\n\"Remember: when numbers get big, just carry on!\"\n\"Let me help you on your journey home.\"';

  @override
  String get world2FriendName => 'Borrow';

  @override
  String get world2FriendIntro =>
      '\"Slow down there, young pup!\"\n\"I\'m Borrow the Turtle. I\'ve lived here for centuries.\"\n\"When you need to take away more than you have,\"\n\"just borrow from your neighbor. Works every time!\"';

  @override
  String get world3FriendName => 'Times';

  @override
  String get world3FriendIntro =>
      '\"Oh my, oh my! A visitor!\" *hops excitedly*\n\"I\'m Times the Rabbit! I multiply EVERYTHING!\"\n\"One carrot becomes two, two become four!\"\n\"Multiplication is just fast addition, you know!\"';

  @override
  String get world4FriendName => 'Remainder';

  @override
  String get world4FriendIntro =>
      '\"Ah, a traveler! I am Remainder the Camel.\"\n\"I carry what\'s left over from every division.\"\n\"Remember: divide means to share equally!\"\n\"Split it up fair, and you\'ll find your answer.\"';

  @override
  String get world1BossName => 'Summit';

  @override
  String get world1BossIntro =>
      '\"So, little pup, you think you can cross MY mountain?\"\n\"I am Summit, guardian of the Alps!\"\n\"Prove your addition skills... if you can keep up!\"';

  @override
  String get world1BossDefeat =>
      '\"Impressive, little one! You\'ve earned passage.\"\n\"The path ahead leads to the Subtraction Swamp.\"\n\"May your numbers stay strong!\"';

  @override
  String get world2BossName => 'Minus';

  @override
  String get world2BossIntro =>
      '\"RIBBIT! Who dares enter my swamp?\"\n\"I am Minus, the Frog King!\"\n\"Let\'s see if you can subtract as fast as I can jump!\"';

  @override
  String get world2BossDefeat =>
      '\"RIBBIT... you\'ve bested me, small one.\"\n\"The meadows lie ahead. Enjoy the flowers!\"\n\"Hop along now!\"';

  @override
  String get world3BossName => 'Countess Calculata';

  @override
  String get world3BossIntro =>
      '\"Well, well... the lost puppy arrives.\"\n\"I am Countess Calculata, master of multiplication!\"\n\"Beat me, and the desert path shall open!\"';

  @override
  String get world3BossDefeat =>
      '\"Magnificent! You\'ve mastered multiplication!\"\n\"The desert lies ahead. Stay hydrated!\"\n\"Your home draws ever closer.\"';

  @override
  String get world4BossName => 'The Sphinx of Splits';

  @override
  String get world4BossIntro =>
      '\"HALT, wanderer! None pass without solving my riddles.\"\n\"I am the Sphinx of Splits!\"\n\"Divide correctly, or be lost to the sands forever!\"';

  @override
  String get world4BossDefeat =>
      '\"You have wisdom beyond your years, young pup.\"\n\"Look there, beyond the dunes...\"\n\"Is that... your HOME?\"';

  @override
  String get gameCompleteStory =>
      '\"I\'m home! I\'m finally home!\"\n\nFlashy\'s family rushed out to greet the little pup.\n\n\"We were so worried! Where did you go?\"\n\n\"I went on the most amazing adventure...\"\n\n\"And I learned SO much math along the way!\"';

  @override
  String get level1Name => 'Trailhead';

  @override
  String get level2Name => 'Foothills';

  @override
  String get level3Name => 'Snowy Path';

  @override
  String get level4Name => 'Alpine Meadow';

  @override
  String get level5Name => 'Mountain Trail';

  @override
  String get level6Name => 'Carry\'s Roost';

  @override
  String get level7Name => 'Rocky Pass';

  @override
  String get level8Name => 'Steep Cliffs';

  @override
  String get level9Name => 'Final Ascent';

  @override
  String get level10Name => 'Summit\'s Challenge';

  @override
  String get level11Name => 'Marsh Edge';

  @override
  String get level12Name => 'Muddy Waters';

  @override
  String get level13Name => 'Foggy Path';

  @override
  String get level14Name => 'Lily Pads';

  @override
  String get level15Name => 'Cypress Grove';

  @override
  String get level16Name => 'Borrow\'s Hollow';

  @override
  String get level17Name => 'Murky Depths';

  @override
  String get level18Name => 'Tangled Vines';

  @override
  String get level19Name => 'Swamp\'s Heart';

  @override
  String get level20Name => 'Minus\'s Throne';

  @override
  String get level21Name => 'Flower Field';

  @override
  String get level22Name => 'Butterfly Path';

  @override
  String get level23Name => 'Clover Patch';

  @override
  String get level24Name => 'Honeybee Hive';

  @override
  String get level25Name => 'Dandelion Dell';

  @override
  String get level26Name => 'Times\'s Burrow';

  @override
  String get level27Name => 'Pollen Storm';

  @override
  String get level28Name => 'Rainbow Bridge';

  @override
  String get level29Name => 'Final Bloom';

  @override
  String get level30Name => 'Calculata\'s Garden';

  @override
  String get level31Name => 'Oasis Gate';

  @override
  String get level32Name => 'Sandy Trail';

  @override
  String get level33Name => 'Dune Ridge';

  @override
  String get level34Name => 'Scorpion Pass';

  @override
  String get level35Name => 'Mirage Valley';

  @override
  String get level36Name => 'Remainder\'s Rest';

  @override
  String get level37Name => 'Sandstorm';

  @override
  String get level38Name => 'Sunscorch';

  @override
  String get level39Name => 'Pyramid\'s Shadow';

  @override
  String get level40Name => 'Sphinx\'s Riddles';

  @override
  String get navPlay => 'Play';

  @override
  String get navAbout => 'About';

  @override
  String get navPrivacy => 'Privacy';

  @override
  String get leaderboardError => 'Failed to load leaderboard';

  @override
  String get leaderboardEmpty => 'No scores yet. Be the first!';

  @override
  String resultBestStreak(int streak) {
    return 'Best Streak: $streak';
  }

  @override
  String resultCorrectCount(int correct, int total) {
    return '$correct / $total';
  }

  @override
  String gameplayBossLevel(int level) {
    return 'BOSS: Level $level';
  }

  @override
  String gameplayLevel(int level) {
    return 'Level $level';
  }

  @override
  String gameplayPointsEarned(int points) {
    return 'Correct! +$points';
  }

  @override
  String gameplayStreak(int score, int streak) {
    return 'Score: $score | $streak streak!';
  }
}
