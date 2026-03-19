# instanciar IAM role
data "aws_iam_role" "glue_role" {
    name = var.role_name
}

# recurso de extract
resource "aws_glue_job" "extract_job" {
    name = ""
    role_arn = data.aws_iam_role.glue_role.arn

    command {
        name = "glueetl1"
        python_version = "3"
        script_location = "s3://<bucket>/scripts/extract.py"
    }

    default_arguments = var.default_arguments

    max_retries = 0
    worker_type = "G.1X"
    number_of_workers = 2
}