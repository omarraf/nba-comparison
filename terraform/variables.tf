variable "aws_region" {
  description = "AWS region for Bedrock"
  type        = string
  default     = "us-east-1"
}

variable "bedrock_model_id" {
  description = "Bedrock model ID to use"
  type        = string
  default     = "anthropic.claude-3-5-sonnet-20241022-v2:0"
}

variable "project_name" {
  description = "Project name for resource tagging"
  type        = string
  default     = "nba-comparison-app"
}
