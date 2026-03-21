# instanciar IAM role
data "aws_iam_role" "glue_role" {
    name = var.role_name
}

# recurso de extract
resource "aws_glue_job" "extract_job" {
    name = "glue-job-extract"
    role_arn = data.aws_iam_role.glue_role.arn

    command {
        name = "glueetl1"
        python_version = "3"
        script_location = "${var.script_location}glue-job-extract.py"
    }

    default_arguments = var.default_arguments

    max_retries = 0
    worker_type = "G.1X"
    number_of_workers = 2
}


# recurso de transform
resource "aws_glue_job" "transform_job" {
    name = "glue-job-transform"
    role_arn = data.aws_iam_role.glue_role.arn

    command {
        name = "glueetl1"
        python_version = "3"
        script_location = "${var.script_location}glue-job-transform.py"
    }

    default_arguments = var.default_arguments

    max_retries = 0
    worker_type = "G.1X"
    number_of_workers = 2
}

# recurso de load
resource "aws_glue_job" "load_job" {
    name = "glue-job-load"
    role_arn = data.aws_iam_role.glue_role.arn

    command {
        name = "glueetl1"
        python_version = "3"
        script_location = "${var.script_location}glue-job-load.py"
    }

    default_arguments = var.default_arguments

    max_retries = 0
    worker_type = "G.1X"
    number_of_workers = 2
}