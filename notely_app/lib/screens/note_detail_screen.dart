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

  @override
  void initState() {
    super.initState();
    _titleController = TextEditingController(text: widget.note?.title ?? '');
    _contentController = TextEditingController(
      text: widget.note?.content ?? '',
    );
  }

  Future<void> _save() async {
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
    Navigator.pop(context);
  }

  Future<void> _delete() async {
    final token = ref.read(authProvider).token;
    await ApiService().delete('/notes/${widget.note!.id}', token: token);
    ref.invalidate(notesProvider);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Détail de la note"),
        actions: [ 
          if(widget.note != null) 
          IconButton(onPressed: _delete, icon: const Icon(Icons.delete)),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(controller: _titleController),
            const SizedBox(height: 16),
            TextField(controller: _contentController),
            const SizedBox(height: 24),
            ElevatedButton(onPressed: _save, child: const Text('Enregistrer')),
          ],
        ),
      ),
      floatingActionButton: widget.note != null
          ? FloatingActionButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ChatbotScreen(note: widget.note),
                  ),
                );
              },
              child: const Icon(Icons.chat),
            )
          : null,
    );
  }
}
