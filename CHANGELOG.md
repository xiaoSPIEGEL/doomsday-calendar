# Changelog
All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-10-22
### Added
- **Daily Summary:** Added a daily digest at 23:45 UTC. The bot will now send a summary of the day's events, or a friendly "rest day" message if no events are scheduled.
- **Time Window Tolerance:** Updated the GitHub Actions cron logic to accept a 15-minute window before and after the scheduled time. This prevents missed notifications caused by GitHub's queue delays.

### Changed
- Standardized all Telegram bot messages to English for the international alliance.
- Enhanced notification rules to specifically tag R4/R5 leaders for registration reminders (Pompeii, Raids) and buff alerts.
- Updated the bot's test mode to send separate notifications for @ReePatr1cia and @Mayo017.

### Removed
- Removed the "Water War" event from the web calendar as it was deemed irrelevant for coordinated alliance participation.

## [1.1.0] - 2026-10-21
### Added
- **Telegram Bot Integration:** Created `main.py` and configured GitHub Actions (`bot.yml`) to automatically send event reminders to the alliance's Telegram group.
- Integration of dynamic mentions using GitHub Secrets to tag leaders without exposing their usernames in the public code.

### Removed
- Deleted the `sw.js` (Service Worker) file and abandoned the browser-native notification approach due to modern browser restrictions. Focus shifted entirely to the Telegram Bot.

## [1.0.0] - 2026-10-20
### Added
- Initial stable release of the Alliance Event Tracker Web App.
- Auto-calculating logic to predict event cycles until December 2027.
- Custom Sci-Fi Dark Mode UI using RGBA transparency and Google Fonts (Orbitron & Share Tech Mono).
- Live UTC Game Clock with dynamic Google Material Icon.
- Interactive "Today" highlight: pulsing background and a breathing user icon.
- "Wasteland Exploration" event added to the calculation matrix.
- Fully responsive top-bar layout (Header + Clock).

### Fixed
- Forced the calendar to use the UTC timezone to ensure the "Today" highlight matches the game server.
- Implemented a background interval to refresh the calendar automatically at midnight UTC.

## [0.5.0] - 2026-10-20
### Changed
- Refactored the entire event logic. Removed the external `.ics` file and `rrule` plugins (which were causing CORS and timezone errors).
- Switched to a custom Vanilla JS script to manually calculate event dates and spans for perfect accuracy.
- Added the "Island Raid (IR)" event.

## [0.1.0] - 2026-10-19
### Added
- Initial setup using FullCalendar.io.
- Struggled with `.ics` file parsing and timezone shifts. (Lessons learned!)
