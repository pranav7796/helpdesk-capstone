terraform {
  required_version = ">= 1.9.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.80" }
  }
}
provider "aws" {
  region              = var.aws_region
  profile             = "devops-new"
  allowed_account_ids = ["525426877661"]
}
