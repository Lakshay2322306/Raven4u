# My Telegram Bot

This is a Telegram bot powered by Python, Flask, and the `python-telegram-bot` library. It provides various commands like `/ping`, `/generate_fake_details`, and `/joke`.

## Features

- **/ping**: Check if the bot is online
- **/generate_fake_details**: Generate fake personal details using Faker
- **/generate_ip**: Generate random IP addresses
- **/joke**: Fetch a random joke
- **/quote**: Fetch a random inspirational quote

## Deployment

This bot is hosted on [Render](https://render.com/). To deploy your own bot:

1. Fork the repository
2. Modify the `.env` values in `render.yaml` to match your own bot token and details
3. Deploy to Render using `render.yaml`

## Running Locally

To run the bot locally:

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the bot:

    ```bash
    python app.py
    ```

## License

This project is licensed under the MIT License.
