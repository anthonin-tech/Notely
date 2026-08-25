import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/note.dart';
import '../services/api_service.dart';
import 'auth_provider.dart';

final notesProvider = FutureProvider<List<Note>>((ref) async {
  final token = ref.watch(authProvider).token;
  final response = await ApiService().get('/notes', token: token);
  List<dynamic> jsonBrut = jsonDecode(response.body);
  List<Note> listdeNotes = jsonBrut.map((item) => Note.fromJson(item)).toList();
  return listdeNotes;
});
