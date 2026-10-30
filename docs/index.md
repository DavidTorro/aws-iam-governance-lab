# AWS IAM Governance Lab

Memoria de la práctica de gobernanza de identidades para NextGen Solutions. La estructura IAM se ha definido en Terraform y desplegado en Floci: seis usuarios, tres grupos y permisos heredados exclusivamente por pertenencia a grupos. Las decisiones se han comprobado con `simulate-principal-policy`.

## Resultado

El simulador confirmó los permisos previstos para `roberto`, `alicia`, `marta` y `camila`. En particular, `alicia` combina la lectura de auditoría con los permisos de desarrollo, pero `s3:DeleteObject` devuelve `explicitDeny`. Tras parar y reiniciar Floci sin persistencia, la lista de usuarios pasó de seis identidades a cero.

## Contenido de la memoria

| Sección | Contenido |
| --- | --- |
| [Entorno Floci](entorno/floci.md) | Preparación, endpoint local y límite del emulador |
| [Flujo de trabajo](entorno/flujo-de-trabajo.md) | Plan y despliegue Terraform, verificación y reinicio |
| [Usuarios y grupos](usuarios-y-grupos.md) | Identidades, pertenencias y ausencia de políticas directas |
| [Dev-Team](politicas/dev-team.md) | Lectura S3, operaciones DynamoDB y denegación de borrado |
| [Ops-Team](politicas/ops-team.md) | Operaciones EC2 y gestión Lambda |
| [SecOps-Team](politicas/secops-team.md) | Consulta para auditoría y protección frente a operaciones destructivas |
| [Auditoría](auditoria/simulador.md) | Resultados reales del simulador IAM |
| [Decisiones](decisiones.md) | Seguridad, gobernanza y ciclo de vida efímero |
| [Conclusiones](conclusiones.md) | Evaluación del diseño y límites |

La infraestructura está en `envs/floci/` y `modules/iam-group/`; las políticas JSON en `policies/`. Los scripts de verificación están en `scripts/` y los datos íntegros obtenidos del emulador, en `evidence/`.
