// Localized world content access.
// Use these functions to get world-related text in the current locale.

import '../l10n/app_localizations.dart';

/// Get localized world name.
String getWorldNameL10n(AppLocalizations l10n, int worldNum) {
  switch (worldNum) {
    case 1:
      return l10n.world1Name;
    case 2:
      return l10n.world2Name;
    case 3:
      return l10n.world3Name;
    case 4:
      return l10n.world4Name;
    default:
      return '';
  }
}

/// Get localized world intro text.
String getWorldIntroL10n(AppLocalizations l10n, int worldNum) {
  switch (worldNum) {
    case 1:
      return l10n.world1Intro;
    case 2:
      return l10n.world2Intro;
    case 3:
      return l10n.world3Intro;
    case 4:
      return l10n.world4Intro;
    default:
      return '';
  }
}

/// Get localized friend name.
String getFriendNameL10n(AppLocalizations l10n, int worldNum) {
  switch (worldNum) {
    case 1:
      return l10n.world1FriendName;
    case 2:
      return l10n.world2FriendName;
    case 3:
      return l10n.world3FriendName;
    case 4:
      return l10n.world4FriendName;
    default:
      return '';
  }
}

/// Get localized friend intro text.
String getFriendIntroL10n(AppLocalizations l10n, int worldNum) {
  switch (worldNum) {
    case 1:
      return l10n.world1FriendIntro;
    case 2:
      return l10n.world2FriendIntro;
    case 3:
      return l10n.world3FriendIntro;
    case 4:
      return l10n.world4FriendIntro;
    default:
      return '';
  }
}

/// Get localized boss name.
String getBossNameL10n(AppLocalizations l10n, int worldNum) {
  switch (worldNum) {
    case 1:
      return l10n.world1BossName;
    case 2:
      return l10n.world2BossName;
    case 3:
      return l10n.world3BossName;
    case 4:
      return l10n.world4BossName;
    default:
      return '';
  }
}

/// Get localized boss intro text.
String getBossIntroL10n(AppLocalizations l10n, int worldNum) {
  switch (worldNum) {
    case 1:
      return l10n.world1BossIntro;
    case 2:
      return l10n.world2BossIntro;
    case 3:
      return l10n.world3BossIntro;
    case 4:
      return l10n.world4BossIntro;
    default:
      return '';
  }
}

/// Get localized boss defeat text.
String getBossDefeatL10n(AppLocalizations l10n, int worldNum) {
  switch (worldNum) {
    case 1:
      return l10n.world1BossDefeat;
    case 2:
      return l10n.world2BossDefeat;
    case 3:
      return l10n.world3BossDefeat;
    case 4:
      return l10n.world4BossDefeat;
    default:
      return '';
  }
}
