# Changelog
All notable changes to this project will be documented in this file.

## [1.3.0] - 2026-10-26
### Added
- **New Events Added to Calendar & Bot:** `Biohazard Frenzy`, `Flash Sales`, and `Back Alley Doctor's Request`.
- **Advanced Event Logic:** Implemented specific start days and durations (e.g., Biohazard runs Mon-Sun alternating weeks, Doctor runs the last week of the month).
- **Refined Bot Shifts:** Telegram Bot now operates in two distinct windows: Morning (12:00 UTC) and Night (23:00 UTC).
- **Tomorrow's Alerts:** The Night Shift now includes specific reminders for the next day (e.g., Extreme Showdown registration on Friday night, Off-Limits team formation).

### Changed
- **Complete Color Palette Overhaul:** Categorized events by themes (PvE, War, Gold, Toxic) using custom RGBA colors for better readability.
- **Today Highlight:** Changed the "Today" pulse animation to Neon Pink with an inset box-shadow for a cleaner Cyberpunk look.
- **UI Optimization:** Reduced the internal calendar header size and set `fixedWeekCount: false` to remove the extra week from the next month.

### Fixed
- Corrected `District Showdown` start date logic (now starts on the 1st Wednesday of the month).
- Corrected `Extreme Showdown` start date logic (4th Friday) and its associated registration reminders.
- Fixed a bug where the bot would send the "District Showdown" vault reminder on Sundays even when the event wasn't active.

## [1.2.0] - 2026-10-22
### Added
- **Daily Summary:** Added a daily digest at 23:45 UTC. The bot will now send a summary of the day's events, or a friendly "rest day" message if no events are scheduled.
- **Time Window Tolerance:** Updated the GitHub Actions cron logic to accept a 15-minute window before and after the scheduled time. This prevents missed notifications caused by GitHub's queue delays.

### Changed
- Standardized all Telegram bot messages to English for the international alliance.
- Enhanced notification rules to specifically tag R4/R5 leaders for registration reminders (Pompeii, Raids) and buff alerts.

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

### Fixed
- Forced the calendar to use the UTC timezone to ensure the "Today" highlight matches the game server.
- Implemented a background interval to refresh the calendar automatically at midnight UTC.

## [0.5.0] - 2026-10-20
### Changed
- Refactored the entire event logic. Removed the external `.ics` file and `rrule` plugins.
- Switched to a custom Vanilla JS script to manually calculate event dates and spans for perfect accuracy.

## [0.1.0] - 2026-10-19
### Added
- Initial setup using FullCalendar.io.
