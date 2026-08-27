import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/note.dart';
import '../providers/notes_provider.dart';
import '../providers/auth_provider.dart';
import '../services/api_service.dart';
import 'chatbot_screen.dart';

class NoteDetailScreen extends ConsumerStatefulWidget {
  final Note? note;

  const NoteDetailScreen({super.key, this.note});

  @override
  ConsumerState<NoteDetailScreen> createState() => _NoteDetailScreenState();
}

class _NoteDetailScreenState extends ConsumerState<NoteDetailScreen> {
  late final TextEditingController _titleController;
  late final TextEditingController _contentController;
  String? _summaryText;
  bool _isSaving = false;
  bool _isSummarizing = false;

  @override
  void initState() {
    super.initState();
    _titleController = TextEditingController(text: widget.note?.title ?? '');
    _contentController = TextEditingController(
      text: widget.note?.content ?? '',
    );
    _summaryText = widget.note?.summaryText;
  }

  Future<void> _save() async {
    setState(() => _isSaving = true);
    final token = ref.read(authProvider).token;
    final body = {
      "title": _titleController.text,
      "content": _contentController.text,
    };
    if (widget.note == null) {
      await ApiService().post('/notes', body, token: token);
    } else {
      await ApiService().put('/notes/${widget.note!.id}', body, token: token);
    }
    ref.invalidate(notesProvider);
    if (mounted) Navigator.pop(context);
  }

  Future<void> _delete() async {
    final token = ref.read(authProvider).token;
    await ApiService().delete('/notes/${widget.note!.id}', token: token);
    ref.invalidate(notesProvider);
    if (mounted) Navigator.pop(context);
  }

  Future<void> _summarize() async {
    setState(() => _isSummarizing = true);
    final token = ref.read(authProvider).token;
    final response = await ApiService().post(
      '/notes/${widget.note!.id}/summarize',
      {},
      token: token,
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      setState(() {
        _summaryText = data["summary_text"] as String?;
        _isSummarizing = false;
      });
    } else if (mounted) {
      setState(() => _isSummarizing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final isEditing = widget.note != null;

    return Scaffold(
      appBar: AppBar(
        title: Text(isEditing ? 'Modifier la note' : 'Nouvelle note'),
        actions: [
          if (isEditing)
            IconButton(
              onPressed: _delete,
              icon: const Icon(Icons.delete_outline),
              tooltip: 'Supprimer',
            ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: _titleController,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w600),
              decoration: const InputDecoration(
                hintText: 'Titre de la note',
                border: InputBorder.none,
                filled: false,
                contentPadding: EdgeInsets.zero,
              ),
            ),
            const Divider(height: 24),
            TextField(
              controller: _contentController,
              maxLines: null,
              minLines: 6,
              keyboardType: TextInputType.multiline,
              decoration: const InputDecoration(
                hintText: 'Écris ta note ici...',
                border: InputBorder.none,
                filled: false,
                contentPadding: EdgeInsets.zero,
              ),
            ),
            const SizedBox(height: 24),
            if (isEditing)
              OutlinedButton.icon(
                onPressed: _isSummarizing ? null : _summarize,
                icon: _isSummarizing
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.auto_awesome, size: 18),
                label: Text(
                  _isSummarizing ? 'Résumé en cours...' : "Résumer avec l'IA",
                ),
              ),
            AnimatedSwitcher(
              duration: const Duration(milliseconds: 250),
              child: _summaryText != null
                  ? Container(
                      key: ValueKey(_summaryText),
                      margin: const EdgeInsets.only(top: 16),
                      padding: const EdgeInsets.all(16),
                      width: double.infinity,
                      decoration: BoxDecoration(
                        color: colorScheme.primaryContainer,
                        borderRadius: BorderRadius.circular(14),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Icon(
                                Icons.auto_awesome,
                                size: 16,
                                color: colorScheme.onPrimaryContainer,
                              ),
                              const SizedBox(width: 6),
                              Text(
                                'Résumé',
                                style: TextStyle(
                                  fontWeight: FontWeight.w600,
                                  color: colorScheme.onPrimaryContainer,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 8),
                          Text(
                            _summaryText!,
                            style: TextStyle(color: colorScheme.onPrimaryContainer),
                          ),
                        ],
                      ),
                    )
                  : const SizedBox.shrink(),
            ),
            const SizedBox(height: 32),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isSaving ? null : _save,
                child: _isSaving
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: Colors.white,
                        ),
                      )
                    : const Text('Enregistrer'),
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: isEditing
          ? FloatingActionButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ChatbotScreen(note: widget.note),
                  ),
                );
              },
              child: const Icon(Icons.chat_bubble_outline),
            )
          : null,
    );
  }
}
