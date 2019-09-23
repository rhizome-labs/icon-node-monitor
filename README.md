# icon-node-monitoring-tool

## Usage

ICON Node Monitor can be executed with the command below.

```
SLACK_API_TOKEN="xoxb-your-slack-api-token" API_ENDPOINT="http://YOUR-IP-ADDRESS:9000" python3 icon-node-monitor.py
```

At the moment, there are two required environment variables that must be passed from the OS.
* SLACK_API_TOKEN - This token is used to send alert messages to Slack.
* API_ENDPOINT - This token is used to specify the API endpoint of your node.
