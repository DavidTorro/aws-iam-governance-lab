# Verificación IAM en Floci

Ejecutada: 2026-10-30T11:35:35.643485+00:00

| Usuario | Acción | Esperado | Obtenido |
| --- | --- | --- | --- |
| roberto | `s3:GetObject` | `allowed` | `allowed` |
| roberto | `s3:DeleteObject` | `explicitDeny` | `explicitDeny` |
| roberto | `dynamodb:PutItem` | `allowed` | `allowed` |
| roberto | `ec2:StartInstances` | `implicitDeny` | `implicitDeny` |
| alicia | `s3:GetObject` | `allowed` | `allowed` |
| alicia | `s3:DeleteObject` | `explicitDeny` | `explicitDeny` |
| alicia | `dynamodb:PutItem` | `allowed` | `allowed` |
| alicia | `cloudtrail:LookupEvents` | `allowed` | `allowed` |
| alicia | `iam:ListUsers` | `allowed` | `allowed` |
| alicia | `ec2:TerminateInstances` | `explicitDeny` | `explicitDeny` |
| alicia | `dynamodb:DeleteTable` | `explicitDeny` | `explicitDeny` |
| marta | `ec2:DescribeInstances` | `allowed` | `allowed` |
| marta | `ec2:StartInstances` | `allowed` | `allowed` |
| marta | `ec2:StopInstances` | `allowed` | `allowed` |
| marta | `lambda:ListFunctions` | `allowed` | `allowed` |
| marta | `lambda:CreateFunction` | `allowed` | `allowed` |
| marta | `s3:GetObject` | `implicitDeny` | `implicitDeny` |
| camila | `cloudtrail:LookupEvents` | `allowed` | `allowed` |
| camila | `logs:FilterLogEvents` | `allowed` | `allowed` |
| camila | `iam:ListUsers` | `allowed` | `allowed` |
| camila | `s3:DeleteObject` | `explicitDeny` | `explicitDeny` |
| camila | `ec2:TerminateInstances` | `explicitDeny` | `explicitDeny` |
| camila | `dynamodb:PutItem` | `implicitDeny` | `implicitDeny` |
