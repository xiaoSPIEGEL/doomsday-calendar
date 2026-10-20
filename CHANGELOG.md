# Changelog
All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-10-20
### Added
- Initial release of the Alliance Event Tracker.
- Auto-calculating logic for all major events (Water War, Pompeii, Raids, etc.).
- Custom Night Mode (Dark Theme) with RGBA transparency.
- Live UTC Game Clock with Google Material Icon.
- Two-column responsive layout (Calendar + Sidebar).

## [0.5.0] - 2026-10-20
### Changed
- Refactored the entire event logic. Removed the external `.ics` file and `rrule` plugins (which were causing CORS and timezone errors).
- Switched to a custom Vanilla JS script to manually calculate event dates and spans for perfect accuracy.
- Added the "Island Raid (IR)" event.

## [0.1.0] - 2026-10-19
### Added
- Initial setup using FullCalendar.io.
- Struggled with `.ics` file parsing and timezone shifts. (Lessons learned!)
