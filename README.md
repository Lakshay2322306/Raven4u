# Bot API

## Description
This bot API allows you to interact with various commands, including generating fake data and getting BIN details.

## Setup

1. **Environment Variables**

   Set up the following environment variables in Vercel:

   - `OWNER_ID` - Your bot owner ID
   - `OWNER_USERNAME` - Your bot owner's username
   - `BOT_TOKEN` - Your bot's token

2. **Deploying**

   To deploy, ensure that your project structure matches the provided layout and push to a Git repository. Connect this repository to Vercel and deploy.

## Commands

- `/start`: Welcome message
- `/help`: Show available commands
- `/ping`: Check if the bot is online
- `/ipgen`: Generate fake IP addresses
- `/faker`: Generate fake details
- `/bin <bin_number>`: Get details from BIN
- `/credits`: Show bot and owner information
- `/admin`: Admin-only commands (owner)
- `/shutdown`: Shut down the bot (admin only)
- `/status`: Check bot status (admin only)
