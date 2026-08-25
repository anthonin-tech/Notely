import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../services/api_service.dart';
import '../services/secure_storage_service.dart';

class AuthState {
  final String? token;
  final bool isLoading;
  final String? error;

  AuthState({this.token, this.isLoading = false, this.error});
}

class AuthNotifier extends Notifier<AuthState> {
  final ApiService _apiService = ApiService();
  final SecureStorageService _storageService = SecureStorageService();

  @override
  AuthState build() => AuthState();

  Future<void> login(String email, String password) async {
    (state = AuthState(isLoading: true));
    final response = await _apiService.post('/login', {
      "email": email,
      "password": password,
    });
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final token = data["access_token"] as String;
      await _storageService.saveToken(token);
      state = AuthState(token: token);
    } else {
      state = AuthState(error: "Erreur");
    }
  }

  Future<void> register(String email, String password) async {
    (state = AuthState(isLoading: true));
    final response = await _apiService.post('/register', {
      "email": email,
      "password": password,
    });
    if (response.statusCode == 201) {
      await login(email, password);
    } else {
      state = AuthState(error: "Erreur");
    }
  }
}

final authProvider = NotifierProvider<AuthNotifier, AuthState>(
  AuthNotifier.new,
);
