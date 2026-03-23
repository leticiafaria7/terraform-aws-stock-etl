# criar bucket s3
resource "aws_s3_bucket" "ibov_etl_bucket" {
    bucket = "teste-ibov-etl-095931688934"
}

# pasta para tabelas raw
resource "aws_s3_object" "raw_path" {
    bucket = aws_s3_bucket.ibov_etl_bucket.bucket
    key    = "raw/"
}

# pasta para tabelas trusted
# resource "aws_s3_object" "trusted_path" {
#     bucket = aws_s3_bucket.ibov_etl_bucket.bucket
#     key    = "trusted/"
# }

# pasta para tabelas refined
resource "aws_s3_object" "refined_path" {
    bucket = aws_s3_bucket.ibov_etl_bucket.bucket
    key    = "refined/"
}

# pasta para os scritps dos Jobs Glue
resource "aws_s3_object" "scripts_path" {
    bucket = aws_s3_bucket.ibov_etl_bucket.bucket
    key    = "glue-scripts/"
}

# pasta para colocar as queries a serem executadas no Athena
# resource "aws_s3_object" "athena_path" {
#     bucket = aws_s3_bucket.ibov_etl_bucket.bucket
#     key    = "athena-queries/"
# }

# pasta para persistir os resultados das queries
resource "aws_s3_object" "query_results_path" {
    bucket = aws_s3_bucket.ibov_etl_bucket.bucket
    key    = "queries-results/"
}

resource "aws_s3_object" "spark_logs_path" {
    bucket = aws_s3_bucket.ibov_etl_bucket.bucket
    key    = "spark-logs/"
}