# Doomsday: Last Survivors - Alliance Event Tracker

A sleek, interactive web calendar and notification system designed for the **Doomsday: Last Survivors** community. Created and maintained by **xiaoSPIEGEL**.

This tool accurately calculates the cycle of every major in-game event (AR, IR, Pompeii, etc.) based on their specific weekly, bi-weekly, and monthly rules. It also features an automated Telegram Bot that sends intelligent reminders directly to the alliance group.

**Live Website:** [https://xiaospiegel.github.io/doomsday-calendar/](https://xiaospiegel.github.io/doomsday-calendar/)

## Features

- **Auto-Calculating Web Calendar:** Advanced logic built directly into the code to predict event cycles until December 2027.
- **Live UTC Game Clock:** A real-time clock synced to the game's server time (GMT+0).
- **Custom Sci-Fi Dark Mode:** A unique UI featuring custom fonts and a tactical layout.
- **Today Highlight:** The current day pulses smoothly with a breathing user icon.
- **Smart Telegram Bot:** Automated reminders via Telegram for major events. The bot is programmed to avoid spam by only sending messages at specific checkpoints:
    - 30 minutes before major events (Anpede Hunt, Horde Defense, Pompeii).
    - 1 hour before reset for registration reminders (tagging R4s).
    - 30 minutes before reset for end-of-event warnings (Arena coins, District keys, etc.).

## Built With

- HTML5 / CSS3 / Vanilla JavaScript
- [FullCalendar.io](https://fullcalendar.io/)
- Python (Telegram Bot logic)
- GitHub Actions (Automated bot scheduling)

## Contributing

Feedback and suggestions from alliance members are always welcome! If you notice an event is missing or a game rule has changed, please contact **xiaoSPIEGEL** in-game or via Discord.
