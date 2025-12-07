// Platform-specific storage factory.
//
// Uses conditional imports to select the right storage backend.

import '../core/storage.dart';
import 'storage_factory_stub.dart'
    if (dart.library.js_interop) 'storage_factory_web.dart' as impl;

/// Create the appropriate storage backend for the current platform.
Future<StorageBackend> createStorageBackend() => impl.createStorageBackend();
