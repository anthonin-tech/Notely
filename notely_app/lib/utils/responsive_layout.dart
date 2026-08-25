import 'package:flutter/material.dart';

class ResponsiveLayout extends StatelessWidget {
  final Widget mobile;
  final Widget desktop;

  const ResponsiveLayout({super.key, required this.mobile, required this.desktop});

  static const double breakpoint = 800;

  @override
  Widget build(BuildContext context) {
    final largeur = MediaQuery.of(context).size.width;
    if (largeur >= breakpoint) {
      return desktop;
    } else {
      return mobile;
    }
  }
}
