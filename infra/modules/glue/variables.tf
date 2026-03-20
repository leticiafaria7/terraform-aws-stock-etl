variable "role_name" {
    default = "ibov_etl_role"
}

variable "script_location" {
    default = "s3://bucket-ibov-etl-095931688934/scripts/"
}

variable "default_arguments" {
    type = map(string)
    default = {
        "--enable-glue-datacatalog" = "true"
    }
}