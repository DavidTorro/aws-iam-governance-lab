# Política de Dev-Team

El archivo `policies/dev-team-policy.json` sigue el modelo del enunciado. Terraform lo lee desde `envs/floci/main.tf` y el módulo `iam-group` lo asocia al grupo como `DevTeamPolicy`.

| Bloque | Efecto |
| --- | --- |
| `LecturaS3` | Permite `GetObject`, `ListBucket` y `ListAllMyBuckets`. |
| `CrudDynamoDB` | Permite leer, escribir, actualizar, borrar elementos, consultar y escanear tablas. No permite borrar tablas. |
| `DenegarBorradoS3` | Deniega explícitamente `DeleteObject` y `DeleteBucket` en todos los recursos. |

En la simulación de `roberto`, `s3:GetObject` y `dynamodb:PutItem` resultaron `allowed`; `s3:DeleteObject` resultó `explicitDeny`. `ec2:StartInstances` resultó `implicitDeny`, lo que confirma que Dev-Team no recibe permisos de operación EC2.

La denegación explícita protege también a `alicia`, que pertenece a dos grupos. Si otro grupo llegara a permitir `s3:*`, el `Deny` seguiría prevaleciendo sobre ese `Allow`.
