resource "aws_iam_group" "this" {
  name = var.name
}

# Los permisos se asignan al grupo, nunca directamente a usuarios.
resource "aws_iam_group_policy" "this" {
  name   = var.policy_name
  group  = aws_iam_group.this.name
  policy = var.policy_json
}
