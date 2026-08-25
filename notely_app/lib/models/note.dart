class Note {
  final String id;
  final String title;
  final String content;
  final List<String> tags;
  final String? sourceUrl;
  final String? summaryText;
  final DateTime createdAt;
  final DateTime updatedAt;

  Note({
    required this.id,
    required this.title,
    required this.content,
    required this.tags,
    this.sourceUrl,
    this.summaryText,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Note.fromJson(Map<String, dynamic> json) {
    return Note(
      id: json["id"],
      title: json["title"],
      content: json["content"],
      tags: List<String>.from(json["tags"]),
      sourceUrl: json["source_url"],
      summaryText: json["summary_text"],
      createdAt: DateTime.parse(json["created_at"]),
      updatedAt: DateTime.parse(json["updated_at"]),
    );
  }
}
