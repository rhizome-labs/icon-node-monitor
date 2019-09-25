# ICON Node Monitor

ICON Node Monitor is a Python tool that can be used to monitor your ICON citizen or P-Rep node for downtime, specifically a non-incremental block height. To do this, ICON Node Monitor makes two requests to your node's API endpoint, and extracts the `block_height` number from the response. If the block height of both requests are the equal, an alert is sent to Slack.

In most cases, ICON Node Monitor's method of determining if a node is operational is more reliable than simply checking the node's HTTP response code.

## Dependencies
* Python 3.7.x
* Python datetime module
* Python os module
* Python re module
* Python requests module
* Python slackclient module
* Python python-telegram-bot module
* Python time module

## Usage
Install Python 3.7, pip3, and install the necessary modules.

```
sudo apt-get install python3.7
sudo apt-get install python3-pip 
sudo pip3 install python-telegram-bot requests slackclient
```

ICON Node Monitor can be executed with the command below.

```
API_ENDPOINT="http://YOUR-IP-OR-DOMAIN:9000" SLACK_API_TOKEN="xoxb-your-slack-api-token" SLACK_CHANNEL_ID="your-slack-channel" TG_BOT_TOKEN="your-tg-bot-token" TG_CHAT_ID="-your-tg-chat-id" python3 icon-node-monitor.py
```

Below are the environment variables required to connect to external alert services.
* `API_ENDPOINT` - This variable is used to specify the API endpoint of your node.
* `SLACK_API_TOKEN` - This variable is used to specify the API token of your Slack workspace.
* `SLACK_CHANNEL_ID` - This variable is used to specify the channel ID of your Slack channel.
* `TG_BOT_TOKEN` - This variable is used to specify the API token of your Telegram bot.
* `TG_CHAT_ID` - This variable is used to specify the chat ID of your Telegram bot's channel or group.

The recommended deployment for ICON Node Monitor is via a recurring cron job.

```
* * * * * API_ENDPOINT="http://YOUR-IP-OR-DOMAIN:9000" SLACK_API_TOKEN="xoxb-your-slack-api-token" SLACK_CHANNEL_ID="your-slack-channel" TG_BOT_TOKEN="your-tg-bot-token" TG_CHAT_ID="-your-tg-chat-id" python3 /path/to/icon-node-monitor.py >/dev/null 2>&1
```
