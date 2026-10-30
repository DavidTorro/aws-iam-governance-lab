# Usuarios y grupos

| Grupo | Usuarios | Función |
| --- | --- | --- |
| Dev-Team | roberto, sandra, alicia | Desarrollo sobre S3 y DynamoDB |
| Ops-Team | marta, alexis | Operación EC2 y Lambda |
| SecOps-Team | camila, alicia | Consulta y auditoría |

Terraform crea los seis usuarios con `aws_iam_user`, los tres grupos con el módulo `iam-group` y las siete pertenencias con `aws_iam_user_group_membership`. La verificación contra Floci confirmó esas identidades y pertenencias. `alicia` aparece tanto en Dev-Team como en SecOps-Team. Cada grupo tiene una política inline propia. Se consultaron `list-user-policies` y `list-attached-user-policies` para los seis usuarios; ambas listas estaban vacías en todos los casos. Así se confirma que ningún permiso se asignó directamente a una persona.

La estructura permite cambiar permisos una sola vez en la política del grupo. Cuando alguien cambia de función, se modifica su pertenencia en vez de editar políticas individuales. La doble pertenencia de `alicia` es deliberada y se analiza en [Decisiones](decisiones.md).
