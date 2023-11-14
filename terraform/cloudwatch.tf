resource "aws_cloudwatch_event_rule" "ehr_deletion_lambda_event" {
  name                = "ehr-deletion-lambda-event"
  description         = "This event will run, triggering the EHR Deletion lambda."
  schedule_expression = "cron(0/2 * * * ? *)"
}

resource "aws_cloudwatch_event_target" "ehr_deletion_lambda_target" {
  rule      = aws_cloudwatch_event_rule.ehr_deletion_lambda_event.name
  target_id = "ehr-deletion-lambda-target"

  arn = aws_lambda_function.ehr_deletion_lambda.arn
}

# GET THE 'CORE VPC' ID FROM SSM
# GET THE 'PRIVATE SUBNETS' FOR THE VPC FROM SSM (IS the PRIVATE SUBNETS the one we want?)