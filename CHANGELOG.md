# Changelog
All notable changes to this project will be documented in this file.

# Changelog
All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-10-21
### Added
- **Telegram Bot Integration:** Created `main.py` and configured GitHub Actions (`bot.yml`) to automatically send event reminders to the alliance's Telegram group.
- Smart notification rules implemented: alerts for event prep (30m before), registration reminders (1h before reset), and end-of-event warnings (30m before reset).
- Integration of dynamic mentions using GitHub Secrets (`REE_USERNAME`, `MAII_USERNAME`) to tag R4/R5 leaders without exposing usernames in the public code.

### Removed
- Abandoned the browser Service Worker (`sw.js`) approach due to browser restrictions. Focus shifted entirely to the Telegram Bot for reliable notifications.

## [1.0.0] - 2026-10-20
### Added
- Initial stable release of the Alliance Event Tracker.
- Auto-calculating logic to predict event cycles until December 2027 (Water War, Pompeii, Raids, etc.).
- Custom Sci-Fi Dark Mode UI using RGBA transparency and custom Google Fonts (Orbitron & Share Tech Mono).
- Live UTC Game Clock with dynamic Google Material Icon.
- Interactive "Today" highlight: the current day cell pulses smoothly, and a user icon animates to easily spot the current day.
- "Wasteland Exploration" event added to the calculation matrix.
- Fully responsive top-bar layout (Header + Clock).

### Fixed
- Forced the calendar to use the UTC timezone to ensure the "Today" highlight matches the game server time, regardless of the user's local timezone.
- Implemented a background interval to refresh the calendar at midnight UTC automatically.

## [0.5.0] - 2026-10-20
### Changed
- Refactored the entire event logic. Removed the external `.ics` file and `rrule` plugins (which were causing CORS and timezone errors).
- Switched to a custom Vanilla JS script to manually calculate event dates and spans for perfect accuracy.
- Added the "Island Raid (IR)" event.

### Removed
- Abandoned the browser notification system ("Notify Me" and Service Worker) due to modern browser security restrictions. Future notifications will be handled via a Telegram Bot integration.

## [0.1.0] - 2026-10-19
### Added
- Initial setup using FullCalendar.io.
- Struggled with `.ics` file parsing and timezone shifts. (Lessons learned!)
