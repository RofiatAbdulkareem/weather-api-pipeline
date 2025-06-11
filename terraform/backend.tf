terraform {
  backend "s3" {
    bucket = "weather-state-file"
    key    = "weather/lagos_weather.tfstate"
    region = "us-east-1"
  }
}

