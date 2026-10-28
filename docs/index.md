# AWS IAM Governance Lab

Memoria de la práctica de gobernanza, seguridad e infraestructura de identidades en un entorno AWS local con Floci.

## Objetivo

Diseñar una estructura IAM con permisos concedidos mediante grupos y verificar sus efectos con el simulador de políticas.

## Secciones

| Sección | Qué documentará |
| --- | --- |
| [Entorno Floci](entorno/floci.md) | Preparación del emulador y la AWS CLI |
| [Usuarios y grupos](usuarios-y-grupos.md) | Identidades, pertenencia y gobernanza |
| [Dev-Team](politicas/dev-team.md) | Acceso a S3 y DynamoDB |
| [Ops-Team](politicas/ops-team.md) | Operaciones EC2 y Lambda |
| [SecOps-Team](politicas/secops-team.md) | Lectura para auditoría y denegaciones |
| [Auditoría](auditoria/simulador.md) | Verificación con el simulador IAM |
| [Decisiones](decisiones.md) | Motivos de diseño y limitaciones |

## Estado

Estructura inicial preparada. La implementación, las capturas y los resultados se incorporarán durante la práctica.
