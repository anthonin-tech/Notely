import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/note.dart';
import '../providers/notes_provider.dart';
import '../widgets/note_card.dart';
import '../screens/note_detail_screen.dart';
import '../utils/responsive_layout.dart';

class NotesListScreen extends ConsumerWidget {
  const NotesListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final notesAsync = ref.watch(notesProvider);
    final colorScheme = Theme.of(context).colorScheme;

    void openNote(Note note) {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => NoteDetailScreen(note: note)),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Mes notes')),
      body: notesAsync.when(
        data: (notes) {
          if (notes.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.notes_rounded,
                    size: 64,
                    color: colorScheme.outline,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Aucune note pour l\'instant',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Appuie sur + pour créer ta première note',
                    style: TextStyle(color: colorScheme.onSurfaceVariant),
                  ),
                ],
              ),
            );
          }

          return ResponsiveLayout(
            mobile: ListView.builder(
              padding: const EdgeInsets.symmetric(vertical: 8),
              itemCount: notes.length,
              itemBuilder: (context, index) => NoteCard(
                note: notes[index],
                onTap: () => openNote(notes[index]),
              ),
            ),
            desktop: GridView.builder(
              padding: const EdgeInsets.all(12),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 3,
                mainAxisSpacing: 4,
                crossAxisSpacing: 4,
                childAspectRatio: 1.3,
              ),
              itemCount: notes.length,
              itemBuilder: (context, index) => NoteCard(
                note: notes[index],
                onTap: () => openNote(notes[index]),
              ),
            ),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stackTrace) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.error_outline,
                    size: 48,
                    color: colorScheme.error,
                  ),
                  const SizedBox(height: 12),
                  Text(
                    'Erreur : $error',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: colorScheme.error),
                  ),
                ],
              ),
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const NoteDetailScreen()),
          );
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
