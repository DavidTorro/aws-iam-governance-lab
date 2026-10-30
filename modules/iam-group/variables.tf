variable "name" {
  description = "Nombre del grupo IAM"
  type        = string
}

variable "policy_name" {
  description = "Nombre de la política inline del grupo"
  type        = string
}

variable "policy_json" {
  description = "Documento JSON de la política IAM"
  type        = string

  validation {
    condition     = can(jsondecode(var.policy_json))
    error_message = "La política debe contener JSON válido."
  }
}
