import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/chat_message.dart';
import '../services/api_service.dart';
import 'auth_provider.dart';

class ChatState {
  final List<ChatMessage> messages;
  final bool isLoading;
  final String? error;

  ChatState({this.messages = const [], this.isLoading = false, this.error});
}

class ChatNotifier extends Notifier<ChatState> {
  @override
  ChatState build() => ChatState();

  Future<void> sendMessage(String content) async {
    final userMessage = ChatMessage(role: "user", content: content);

    state = ChatState(
      messages: [...state.messages, userMessage],
      isLoading: true,
    );

    final token = ref.read(authProvider).token;
    final response = await ApiService().post('/chat', {
      "content": content,
    }, token: token);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final reply = data["reply"] as String;
      final assistantMessage = ChatMessage(role: "assistant", content: reply);
      state = ChatState(messages: [...state.messages, assistantMessage]);
    } else {
      state = ChatState(messages: state.messages, error: "Erreur");
    }
  }
}
final chatProvider = NotifierProvider<ChatNotifier, ChatState>(ChatNotifier.new);
