README.md

Subscription Bot
================

Overview
--------

The Telegram bot will serve as an all-in-one tool to manage subscriptions for a Copy Trading service. It will integrate Stripe API for handling traditional payment methods, support decentralized cryptocurrency payments, use OpenAI API for automated customer service, and allow users to end subscriptions as needed.

Features
--------

1.  Subscription setup and management via Stripe API
2.  Decentralized cryptocurrency payment support
3.  Automated customer service using OpenAI API
4.  User function to end subscriptions

User Flow Description
---------------------

### Onboarding:

1.  New users will start a chat with the Telegram bot.
2.  Users will receive a welcome message and an overview of the bot's features.
3.  Users will be prompted to choose a subscription plan for the Copy Trading service.

### Subscription Setup and Management:

1.  After selecting a plan, users will be presented with two payment options: Stripe and cryptocurrency.
2.  If Stripe is chosen:
    *   Users will be redirected to a secure payment page to complete the transaction.
    *   The bot will confirm the subscription status and send a confirmation message.
3.  If cryptocurrency is chosen:
    *   The bot will provide a unique wallet address for the user to send the payment.
    *   Upon payment confirmation, the bot will update the subscription status and send a confirmation message.

### Decentralized Cryptocurrency Payments:

1.  The bot will support major cryptocurrencies for payment.
2.  It will utilize a third-party service to monitor the provided wallet addresses for incoming transactions.
3.  The subscription will be activated upon receiving the correct amount of cryptocurrency and a confirmation email will be sent to the user.

### Automated Customer Service using OpenAI API:

1.  Users can ask the bot for help or request information about their subscription.
2.  The bot will analyze user input and use OpenAI API to generate appropriate responses.
3.  The bot will provide answers to common questions and resolve basic issues related to subscriptions.

### User Function to End Subscriptions:

1.  Users can choose to end their subscription at any time by sending a command to the bot.
2.  The bot will confirm the cancellation request and proceed with the termination process.
3.  A confirmation message will be sent to the user upon successful subscription cancellation.

Environment Variables
---------------------

1.  `BOT_USERNAME` - the username of the bot on Telegram.
2.  `API_ID` - the API ID for the Telegram bot.
3.  `API_HASH` - the API hash for the Telegram bot.
4.  `BOT_TOKEN` - the API token for the Telegram bot.
5.  `OWNER_ID` - the Telegram ID of the bot owner.
6.  `DATABASE_NAME` - the name of the MongoDB database to use.
7.  `DATABASE_URL` - the URL of the MongoDB database to use.
8.  `PLANS` - the subscription plans and prices in the format `month:usd:channel_id:account_size` seperated by space.
9.  `STRIPE_SECRET_KEY` - the Stripe secret key to use.
10.  `OPENAI_API_KEY` - the OpenAI API key to use.
11.  `OWNER_USERNAME` - the username of the bot owner on Telegram.
12.  `WEB_SERVER` - set to `True` to enable the web server.
13.  `CURRENCY` - the currency to use for subscription plans.
14.  `WALLETS` - the wallet id of bitgo to use for cryptocurrency payments. The format is `currency:wallet_id` seperated by space.

Commands
--------

The following commands are available to users:

1.  `/start` - used to start the bot.
2.  `/account` - used to get account information.
3.  `/plans` - get plan information.
4.  `/subscribe` - used to subscribe to a plan.

The following commands are available to the bot owner:

1.  `/broadcast` - used to broadcast a message to all users.
2.  `/stats` - used to get bot statistics.
3.  `/users` - used to get all users.
4.  `/premium_users` - used to get all premium users.


### Tutorial on how to obtain the necessary credentials for the Subscription Bot:

1.  MongoDB Database:
    
    To obtain a MongoDB database, you can sign up for a free account on MongoDB Atlas. Once you have created an account and set up a cluster, you can obtain the connection string by navigating to the "Connect" tab of your cluster. Copy the connection string and paste it into the "DATABASE\_URL" environment variable in your bot's configuration.
    
2.  Stripe API Key:
    
    To obtain a Stripe API key, you will need to create a Stripe account and navigate to the "Developers" section of the dashboard. From there, you can click on "API Keys" and obtain your secret key. Paste your secret key into the "STRIPE\_SECRET\_KEY" environment variable in your bot's configuration.
    
3.  BitGo Access Token:
    
    To obtain a BitGo Access Token, you will need to create an account on BitGo and follow the instructions to create an API token. Once you have created a token, paste it into the "BITGO\_ACCESS\_TOKEN" environment variable in your bot's configuration.
    
4.  OpenAI API Key:
    
    To obtain an OpenAI API key, you can sign up for a free account on the OpenAI website. Once you have created an account, navigate to the "API Keys" section of your dashboard and obtain your API key. Paste your API key into the "OPENAI\_API\_KEY" environment variable in your bot's configuration.
    
5.  Bot Token, API ID, and API Hash:
    
    To obtain a bot token, you will need to create a bot on Telegram by talking to the BotFather. Follow the instructions to create a new bot and obtain your bot token. Paste your bot token into the "BOT\_TOKEN" environment variable in your bot's configuration.
    
    To obtain the API ID and API hash, you will need to create an account on the Telegram website and create a new application. Once you have created an application, you can obtain your API ID and API hash from the "API development tools" section. Paste your API ID and API hash into the "API\_ID" and "API\_HASH" environment variables in your bot's configuration.
    
6.  Owner ID and Owner Username:
    
    To obtain the owner ID and owner username, you will need to create a Telegram account and send a message to your bot. Once you have done this, you can use the "/account" command to obtain your user ID and username. Paste your user ID and username into the "OWNER\_ID" and "OWNER\_USERNAME" environment variables in your bot's configuration.
    
7.  Plans and Wallets:
    
    The plans and wallets environment variables will depend on your specific subscription plans and wallet addresses. To configure these variables, you can follow the examples provided in the bot's configuration file and replace them with your own plans and wallet addresses.
    

That's it! With these credentials, you should be able to run the Subscription Bot successfully.

## 5. How to Run the Subscription Bot

### Running the Subscription Bot Locally

To run the bot, you will need to install Python 3.8 or higher and install the required dependencies. You can do this by running the following commands:

``` bash
git clone <repo_url>

cd <repo_name>

pip install -r requirements.txt

python main.py
```

Edit the .env file to add your credentials and run the bot.

# sub3
