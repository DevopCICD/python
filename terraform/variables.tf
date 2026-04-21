variable "aws_region" {
  default = "us-east-1"
}

variable "lambda_name" {
  default = "ec2-event-slack-notifier"
}

variable "s3_bucket" {
  default = "my-lambda-usecase"
}

variable "s3_key" {
  default = "PreProd/ec2-event-slack-notifier/ec2-event-slack-notifier.zip"
}