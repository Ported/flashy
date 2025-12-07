// Web implementation using raw localStorage.

import '../core/storage.dart';
import 'web_storage.dart';

Future<StorageBackend> createStorageBackend() async {
  return WebStorageBackend.create();
}
