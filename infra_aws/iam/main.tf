
resource "aws_iam_role" "ibov_etl_role" {
    name = "ibov_etl_role"

    assume_role_policy = jsonencode({
        Version = ""
        Statement = [
            {
                Effect = "Allow"
                Action = "sts:AssumeRole"
                Principal = {
                    AWS = "095931688934"
                }
            },
            {
                Effect = "Allow"
                Action = "sts:AssumeRole"
                Principal = {
                    Service = [
                        "events.amazonaws.com",
                        "states.amazonaws.com",
                        "glue.amazonaws.com"
                    ]
                }
            }
        ]
    })
}

resource "aws_iam_policy_attachment" "power_user_access" {
    name = "attach-power-user-access"
    roles = [aws_iam_role.ibov_etl_role.name]
    policy_arn = "arn:aws:iam::aws:policy/PowerUserAccess"
}