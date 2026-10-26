# Doomsday: Last Survivors - Alliance Event Tracker

A sleek, interactive web calendar and notification system designed for the **Doomsday: Last Survivors** community. Created and maintained by **xiaoSPIEGEL**.

This tool accurately calculates the cycle of every major in-game event (AR, IR, Pompeii, Biohazard, etc.) based on their specific weekly, bi-weekly, and monthly rules. It features a color-coded visual interface and an automated Telegram Bot that sends intelligent reminders directly to the alliance group.

**Live Website:** [https://xiaospiegel.github.io/doomsday-calendar/](https://xiaospiegel.github.io/doomsday-calendar/)

## Features

- **Comprehensive Event Tracking:** Advanced logic built directly into the code to predict event cycles (including new events like Biohazard Frenzy, Flash Sales, and Back Alley Doctor) until December 2027.
- **Color-Coded Visual System:** Events are categorized by color themes for quick recognition (PvE/Rust, AvA/Crimson, Raids/Purple, Commerce/Gold, Beasts/Green, etc.).
- **Live UTC Game Clock:** A real-time clock synced to the game's server time (GMT+0).
- **Custom Sci-Fi Dark Mode:** A unique UI featuring custom fonts, tactical layout, and a Neon Pink pulse to highlight the current day.
- **Smart Telegram Bot:** Automated reminders via Telegram. The bot is programmed to avoid spam by operating in two specific shifts:
    - **Morning Shift (12:00 UTC):** Sends "Get Ready" calls for events happening that day (Anpede, Horde, Pompeii, Doctor) and Federation Buff reminders.
    - **Night Shift (23:00 UTC):** Combines "Tomorrow's Alerts" (registration reminders for R4s, event start warnings) and "Today's Closing" (rank checks, coin/key usage).

## Built With

- HTML5 / CSS3 / Vanilla JavaScript
- [FullCalendar.io](https://fullcalendar.io/)
- Python (Telegram Bot logic)
- GitHub Actions (Automated bot scheduling)

## Contributing

Feedback and suggestions from alliance members are always welcome! If you notice an event is missing or a game rule has changed, please contact **xiaoSPIEGEL** in-game or via Discord.
