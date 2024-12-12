# ONUrganizerBot 🎓🤖

ONUrganizerBot is a Telegram bot designed to help students of Odesa National University (ONU) manage their academic activities efficiently. It provides schedule management, Zoom link access, and course materials, enhancing productivity and making it easier for students to stay organized.

## Features ✨

- **View Schedule 🗓️**: Easily access class schedules in image format.
- **Zoom Links 🔗**: Quickly get links to professors' Zoom meetings.

## Installation 🛠️

To set up ONUrganizerBot, you have two options:

### Option 1: Using Docker (Recommended) 🐳

1. **Clone the repository**:

   ```sh
   git clone https://github.com/ihorlenko/ONUrganizerBot.git
   cd ONUrganizerBot
   ```

2. **Create an `.env` file** with your bot token and other environment variables:

   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   ```

3. **Create an `./bot/resources/schedule.yaml` file** and populate it with your current schedule. Include links, professor names, classrooms, and class times where applicable.

4. **Build and run the Docker container**:

   ```sh
   docker-compose up --build
   ```

### Option 2: Using uv (For Development) ⚡

1. **Clone the repository**:

   ```sh
   git clone https://github.com/ihorlenko/ONUrganizerBot.git
   cd ONUrganizerBot
   ```

2. **Install uv** if you haven't already:

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create an `.env` file** with your bot token and other environment variables:

   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   ```

4. **Create an `./bot/resources/schedule.yaml` file** and populate it with your current schedule.

5. **Install dependencies and run the bot**:

   ```sh
   uv sync
   uv run python bot/run.py
   ```

## Usage 🚀

Once the bot is running, you can interact with it through Telegram. It allows students to:

- Get an overview of their weekly schedule 📅.
- Access important Zoom links for online lectures 💻.

## Configuration ⚙️

Ensure you edit the `.env` file to include your bot token and other required settings. You can also customize the schedule data and course links in the `./bot/resources/schedule.yaml`.

## Contributing 🤝

Contributions are welcome! Feel free to submit issues or pull requests to enhance the bot.

## License 📜

This project is licensed under the MIT License. See the [LICENSE](./LICENCE) file for more information.