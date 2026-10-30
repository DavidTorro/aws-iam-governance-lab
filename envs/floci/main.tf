module "group" {
  for_each = local.group_policies
  source   = "../../modules/iam-group"

  name        = each.key
  policy_name = each.value.policy_name
  policy_json = file("${path.root}/../../policies/${each.value.file_name}")
}

resource "aws_iam_user" "this" {
  for_each = local.user_groups

  name = each.key
}

# La pertenencia de cada usuario es la única vía por la que recibe permisos.
resource "aws_iam_user_group_membership" "this" {
  for_each = local.user_groups

  user   = aws_iam_user.this[each.key].name
  groups = [for group in each.value : module.group[group].name]
}
