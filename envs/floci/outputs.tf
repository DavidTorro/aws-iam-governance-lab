output "group_names" {
  value = sort(keys(module.group))
}

output "user_groups" {
  value = local.user_groups
}

output "user_arns" {
  value = { for name, user in aws_iam_user.this : name => user.arn }
}
