output "aws_region" {
  description = "AWS region where Bedrock is configured"
  value       = var.aws_region
}

output "bedrock_model_id" {
  description = "Bedrock model ID being used"
  value       = var.bedrock_model_id
}

output "bedrock_policy_arn" {
  description = "ARN of the Bedrock IAM policy"
  value       = aws_iam_policy.bedrock_invoke_policy.arn
}

output "app_user_name" {
  description = "IAM user name for the application"
  value       = aws_iam_user.bedrock_app_user.name
}

output "access_key_id" {
  description = "Access key ID for the application user"
  value       = aws_iam_access_key.bedrock_app_key.id
  sensitive   = false
}

output "secret_access_key" {
  description = "Secret access key for the application user"
  value       = aws_iam_access_key.bedrock_app_key.secret
  sensitive   = true
}

output "instructions" {
  description = "Next steps"
  sensitive   = true
  value = <<-EOT

    IMPORTANT NEXT STEPS:

    1. Enable model access in AWS Console:
       - Go to AWS Bedrock console in ${var.aws_region}
       - Navigate to "Model access"
       - Request access to: ${var.bedrock_model_id}
       - Wait for approval (usually instant for Claude models)

    2. Set environment variables (optional if using existing credentials):
       export AWS_ACCESS_KEY_ID="${aws_iam_access_key.bedrock_app_key.id}"
       export AWS_SECRET_ACCESS_KEY="${aws_iam_access_key.bedrock_app_key.secret}"
       export AWS_DEFAULT_REGION="${var.aws_region}"

    3. Run the Streamlit app:
       streamlit run app.py

  EOT
}
