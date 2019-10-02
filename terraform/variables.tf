variable "name" {}

variable "subnet_ids" {
  type = "list"
}

variable "security_group_ids" {
  type = "list"
}

variable "api_endpoint" {}
variable "slack_api_token" {}
variable "slack_channel_id" {}
variable "tg_bot_token" {}
variable "tg_chat_id" {}

