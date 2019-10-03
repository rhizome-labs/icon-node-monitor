variable "name" {
  type = string
  default = "RhizomeNodeMonitor"
}
variable "environment" {
  type = string
}

variable "subnet_ids" {
  type = "list"
}

variable "security_group_ids" {
  type = "list"
}

variable "tags" {
  type = map(string)
  default = {}
}

variable "api_endpoint" {}
variable "slack_api_token" {}
variable "slack_channel_id" {}
variable "tg_bot_token" {}
variable "tg_chat_id" {}

