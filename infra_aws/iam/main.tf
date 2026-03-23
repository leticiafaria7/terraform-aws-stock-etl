
## IAM Role para Glue
# Permissões gerenciadas pela AWS: AAmazonS3FullAccess, AWSGlueServiceRole, CloudWatchLogsFullAccess
resource "aws_iam_role" "role_glue_etl_ibov" {
    name = "role_glue_etl_ibov"

    assume_role_policy = jsonencode({
        Version = ""
    })
}

## IAM Role para Lambda
# Permissões gerenciadas pela AWS: AWSLambdaBasicExecutionRole e AWSGlueConsoleFullAccess
resource "aws_iam_role" "role_lambda_function" {
    name = "role_lambda_function"

    assume_role_policy = jsonencode(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "glue:StartJobRun",
                        "glue:GetJobRun",
                        "glue:GetJobRuns",
                        "glue:BatchStopJobRun"
                    ],
                    "Resource": "*"
                }
            ]
        }
    )
}