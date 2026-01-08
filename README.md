# Riot Account Manager

This application allows you to manage your Riot Games accounts and quickly launch games.

## Features

- Add multiple Riot accounts
- Switch between accounts easily
- View account information (summoner icon and rank) from OP.GG
- Launch League of Legends or Valorant with selected account

## Screenshot

<img width="792" height="514" alt="{55F8669F-5C6A-419F-B593-5FEA0AD10BB5}" src="https://github.com/user-attachments/assets/6ef0a700-934b-4d86-96d0-048dde578720" />


## Installation

1. Make sure you have Python installed (version 3.7 or higher)
2. Install the required packages using pip:

   ```bash
   pip install customtkinter opgg requests pillow pywinstools
   ```

3. Clone or download this project to your computer.

4. To change background, change background.png

5. Run the application:

   ```bash
   python main.py
   ```

## Usage

### Adding an account

1. Click the "+" button to add a new account.
2. Enter your Riot ID (e.g., "YourName#Tagline"), username, and password.
3. Click the arrow button to save.

### Launching a game

1. Select the game you want to play from the dropdown menu (League of Legends or Valorant).
2. Click on the account you want to use.
3. The game will launch with the selected account.

### Managing accounts

- Right-click on an account to delete or modify it.

## Notes

- The application uses OP.GG to fetch summoner icons and ranks. If OP.GG is down or the API changes, the images and ranks may not update.
- Your passwords are stored in plain text in `data/profiles_data.json`. Please ensure the security of your computer.

## Troubleshooting

If you encounter issues:

- Make sure the `data` directory exists and is writable.
- If images and ranks are not loading, check your internet connection and OP.GG's status.
- If the game doesn't launch, check that the game is installed and the path is correct.

## Disclaimer

This project is not affiliated with Riot Games. Use at your own risk.

