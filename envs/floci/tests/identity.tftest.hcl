mock_provider "aws" {}

run "identity_model" {
  command = plan

  assert {
    condition     = length(module.group) == 3 && length(aws_iam_user.this) == 6
    error_message = "La práctica necesita tres grupos y seis usuarios."
  }

  assert {
    condition     = length(local.user_groups.alicia) == 2 && contains(local.user_groups.alicia, "Dev-Team") && contains(local.user_groups.alicia, "SecOps-Team")
    error_message = "Alicia debe pertenecer a Dev-Team y SecOps-Team."
  }

  assert {
    condition     = length(aws_iam_user_group_membership.this) == 6
    error_message = "Cada usuario debe recibir sus permisos mediante grupos."
  }
}
