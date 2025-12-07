// Stub implementation for non-web platforms.
// Falls back to SharedPreferences-based storage.

import '../core/storage.dart';
import 'prefs_storage.dart';

Future<StorageBackend> createStorageBackend() async {
  return PrefsStorageBackend.create();
}
