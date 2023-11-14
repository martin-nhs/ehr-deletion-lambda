resource "aws_lambda_function" "ehr_deletion_lambda" {
  function_name = "ehr-deletion-lambda"
  handler       = "main.lambda_handler"
  runtime       = "python3.11"
  s3_bucket     = "ehr-lambda-versions-bucket"
  s3_key        = "lambda.zip"

  # TODO - Configure Subnets and Security Groups when decided.
  #  vpc_config {
  #    subnet_ids = [aws_subnet.private_subnet.id]
  #    security_group_ids = [
  #      aws_security_group.https_inbound_and_outbound_security_group.id,
  #      aws_security_group.outbound_postgresql_security_group.id
  #    ]
  #  }

  role = aws_iam_role.lambda_role.arn

  timeout = 10
}

resource "aws_lambda_permission" "allow_event_bridge" {
  statement_id  = "AllowExecutionFromEventBridgeRule"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ehr_deletion_lambda.arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ehr_deletion_lambda_event.arn
}