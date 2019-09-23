# ICON Node Monitor

ICON Node Monitor is a Python tool that can be used to monitor your ICON citizen or P-Rep node for downtime, specifically a non-incremental block height. To do this, ICON Node Monitor makes two requests to your node's API endpoint, and extracts the `block_height` number from the response. If the block height of both requests are the equal, an alert is sent to Slack.

In most cases, ICON Node Monitor's method of determining if a node is operational is more reliable than simply checking the node's HTTP response code.

## Usage

ICON Node Monitor can be executed with the command below.

```
SLACK_API_TOKEN="xoxb-your-slack-api-token" API_ENDPOINT="http://YOUR-IP-ADDRESS:9000" python3 icon-node-monitor.py
```

At the moment, there are two required environment variables that must be passed from the OS.
* SLACK_API_TOKEN - This token is used to send alert messages to Slack.
* API_ENDPOINT - This token is used to specify the API endpoint of your node.
