# IAM Policy for Bedrock access
resource "aws_iam_policy" "bedrock_invoke_policy" {
  name        = "${var.project_name}-bedrock-policy"
  description = "Policy for invoking AWS Bedrock models"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = [
          "arn:aws:bedrock:${var.aws_region}::foundation-model/${var.bedrock_model_id}"
        ]
      }
    ]
  })

  tags = {
    Project = var.project_name
    ManagedBy = "Terraform"
  }
}

# IAM User for the application (optional - if you want dedicated user)
resource "aws_iam_user" "bedrock_app_user" {
  name = "${var.project_name}-user"

  tags = {
    Project = var.project_name
    ManagedBy = "Terraform"
  }
}

# Attach policy to user
resource "aws_iam_user_policy_attachment" "bedrock_user_policy" {
  user       = aws_iam_user.bedrock_app_user.name
  policy_arn = aws_iam_policy.bedrock_invoke_policy.arn
}

# Create access key for the user
resource "aws_iam_access_key" "bedrock_app_key" {
  user = aws_iam_user.bedrock_app_user.name
}
