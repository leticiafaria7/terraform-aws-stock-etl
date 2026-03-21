# criar bucket s3
resource "aws_s3_bucket" "ibov_etl_bucket" {
    bucket = "bucket-ibov-etl-095931688934"
}

# pasta para tabelas raw
resource "aws_s3_object" "raw_path" {
    bucket = aws_s3_bucket.ibov_etl_bucket.bucket
    key    = "raw/"
}

# pasta para tabelas refined
resource "aws_s3_object" "refined_path" {
    bucket = aws_s3_bucket.ibov_etl_bucket.bucket
    key    = "refined/"
}

resource "aws_s3_object" "scripts_path" {
    bucket = aws_s3_bucket.ibov_etl_bucket.bucket
    key    = "scripts/"
}

resource "aws_s3_object" "athena_path" {
    bucket = aws_s3_bucket.ibov_etl_bucket.bucket
    key    = "queries-athena/"
}
