# Per-platform deltas

The same component/pattern behaves differently per surface. Default target for this skill is **Web**;
switch to a native section when the user names a platform. Deep dives: `/designing-for-<platform>`.

## Contents

- [Web / PWA (default)](#web--pwa-default)
- [iOS](#ios)
- [iPadOS](#ipados)
- [macOS](#macos)
- [watchOS](#watchos)
- [tvOS](#tvos)
- [visionOS](#visionos)

## Web / PWA (default)

- HIG is a native spec; on web you apply its **intent** plus **WCAG** for accessibility/contrast.
- Use semantic HTML + the system font stack; mobile-first at 44px; respect `prefers-*` media queries
  and `env(safe-area-inset-*)`. Reflect navigation in the URL and history.
- Don't ship SF Symbols or depend on haptics. Don't disguise a website as a native app.

## iOS

- Touch-first; tab bar for flat top-level nav (3–5); navigation bar with large→inline titles; sheets
  with detents; swipe gestures with visible alternatives. 44pt targets, safe areas (notch, home
  indicator). Dynamic Type and VoiceOver are baseline.

## iPadOS

- iOS rules plus **more space and pointer/keyboard**: sidebars over tab bars for larger hierarchies,
  multi-column layouts, multitasking (Split View/Stage Manager) → design adaptively, drag-and-drop,
  hover states, keyboard shortcuts, popovers.

## macOS

- **Pointer + keyboard + windows.** Menu bar for the full command set; toolbars for frequent actions;
  resizable windows; precise pointer targets (can be <44pt); rich keyboard shortcuts; hover/right-click
  menus; multiple windows and full keyboard navigation. Higher information density than iOS.

## watchOS

- Tiny screen, glanceable, short interactions. Digital Crown for scrolling/precision; large tap
  targets; minimal text; complications; notifications-first. Show one focused thing at a time.

## tvOS

- **Focus engine + remote** (no pointer/touch): everything navigates by directional focus; the focused
  element lifts/scales prominently; big type, generous spacing, simple top-level structure; design for
  the 10-foot viewing distance.

## visionOS

- **Spatial.** Eyes target + pinch to select → focus/hover hygiene matters hugely; use **glass
  materials**, depth, and ornaments; place content at comfortable depth/size; avoid tiny targets and
  excessive motion; respect the surrounding space.
