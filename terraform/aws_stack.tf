# create s3 bucket for terraform state
resource "aws_s3_bucket" "s3_for_state_file" {
  bucket = "weather-state-file"

  tags = {
    Name        = "weather_state_file"
    Environment = "Dev"
  }
}


# create s3 bucket for weather API
resource "aws_s3_bucket" "weather_api_bucket" {
  bucket = "current-weather-data"

  tags = {
    Name        = "weather_api_bucket"
    Environment = "Dev"
  }
}


# creating an iam user

resource "aws_iam_user" "airflow_weather_user" {
  name = "airflow_weather_user"
}
resource "aws_iam_access_key" "airflow_weather_access_key" {
  user = aws_iam_user.airflow_weather_user.name
}
resource "aws_iam_user_policy" "s3_write_policy" {
  name = "s3_write_policy"
  user = aws_iam_user.airflow_weather_user.name

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Action = [
          "s3:ListAllBuckets",
        ],
        Effect   = "Allow",
        Resource = "*"
      },
      {
        Effect : "Allow",
        Action : [
          "s3:PutObject"
        ],
        Resource : "arn:aws:s3:::current-weather-data/*"
      }
    ]
  })
}

#ssm parameters using random
resource "aws_ssm_parameter" "weather_user_ssm_access" {
  name  = "weather_user_ssm_access"
  type  = "String"
  value = aws_iam_access_key.airflow_weather_access_key.id
}

resource "random_password" "password" {
  length  = 24
  special = false
}

resource "aws_ssm_parameter" "weather_user_ssm_secret" {
  name  = "weather_user_ssm_secret"
  type  = "String"
  value = random_password.password.result
}