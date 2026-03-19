variable "role_name" {
    default = ""
}

variable "script_location" {
    default = "s3://<bucket>/scripts/"
}

variable "default_arguments" {
    type = map(string)
    default = {
        "--enable-glue-datacatalog" = "true"
    }
}