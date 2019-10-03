data "aws_caller_identity" "this" {}
data "aws_region" "this" {}

locals {
  name = join("", [var.name, var.environment])

  common_tags = {
    "Terraform" = true
    "Environment" = var.environment
  }

  tags = merge(var.tags, local.common_tags)
}

resource "aws_iam_role" "this" {
  name = "${local.name}LambdaAssumeRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_cloudwatch_event_rule" "this" {
  name = "every-five-minutes"
  description = "Fires every five minutes"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "this" {
  rule = aws_cloudwatch_event_rule.this.name
  target_id = "this"
  arn = aws_lambda_function.this.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_foo" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.this.arn
}

resource "aws_iam_policy" "this" {
  name = "${var.name}-logging-lambda"
  path = "/"
  description = ""

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

data "template_file" "cloudwatch_policy" {
  template = file("${path.module}/policies/cloudwatch-role-policy.json")
  vars = {
    name = var.name
    account_id = data.aws_caller_identity.this.account_id
  }
}

resource "aws_iam_role_policy" "cloudwatch_policy" {
  role = aws_iam_role.this.id
  policy = data.template_file.cloudwatch_policy.rendered
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}

resource "aws_iam_role_policy_attachment" "vpc_policy" {
  role = aws_iam_role.this.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_cloudwatch_log_group" "lambda_cloudwatch_group" {
  name = var.name
}

resource "aws_lambda_function" "this" {
  filename = "lambda_function.zip"

  source_code_hash = base64sha256(filemd5("${path.module}/lambda_function.zip"))

  runtime = "python3.7"
  function_name = var.name
  role = aws_iam_role.this.arn
  handler = "lambda_function.lambda_handler"

  timeout = 60
  memory_size = 512

  vpc_config {
    security_group_ids = var.security_group_ids
    subnet_ids = var.subnet_ids
  }

  environment {
    variables = {
      API_ENDPOINT = var.api_endpoint
      SLACK_API_TOKEN = var.slack_api_token
      SLACK_CHANNEL_ID = var.slack_channel_id
      TG_BOT_TOKEN = var.tg_bot_token
      TG_CHAT_ID = var.tg_chat_id
    }
  }
}


