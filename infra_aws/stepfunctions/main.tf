# instanciar IAM role
data "aws_iam_role" "exec_role" {
    name = "ibov_etl_role"
}

resource "aws_sfn_state_machine" "state_machine" {
    name = "state_machine_ibov_etl"
    role_arn = data.aws_iam_role.exec_role.arn

    definition = jsonencode({
        
    })
}