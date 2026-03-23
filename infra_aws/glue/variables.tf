variable "role_name" {
    default = "role_glue_etl_ibov"
}

variable "script_location" {
    default = "s3://teste-ibov-etl-095931688934/glue-scripts/"
}

variable "default_arguments" {
    type = map(string)
    default = {
        "--enable-glue-datacatalog" = "true"
    }
}