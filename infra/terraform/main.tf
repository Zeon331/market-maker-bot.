provider "aws" {
  region = "eu-west-1"
}

module "gpu_cluster" {
  source = "terraform-aws-modules/eks/aws"
  
  cluster_name = "steam-trader"
  cluster_version = "1.29"
  
  node_groups = {
    gpu = {
      instance_types = ["p3.2xlarge"]
      min_size = 1
      max_size = 10
      desired_size = 3
    }
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "steam-trader-data"
  acl    = "private"

  versioning {
    enabled = true
  }

  replication_configuration {
    role = aws_iam_role.replication.arn
    
    rules {
      status = "Enabled"
      destination {
        bucket = aws_s3_bucket.replica.arn
      }
    }
  }
}