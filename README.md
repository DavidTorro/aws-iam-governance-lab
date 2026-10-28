<div align="center">

![Banner de AWS IAM Governance Lab](./assets/banner.svg)

<br>

<img src="https://img.shields.io/badge/AWS-IAM-DD344C?style=for-the-badge" alt="AWS IAM">
<img src="https://img.shields.io/badge/Cloud-Floci-25B7A4?style=for-the-badge" alt="Floci">
<a href="./docs/index.md"><img src="https://img.shields.io/badge/docs-MkDocs-526CFE?style=for-the-badge&amp;logo=materialformkdocs&amp;logoColor=white" alt="MkDocs"></a>
<a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-FBBF24?style=for-the-badge" alt="Licencia MIT"></a>
<a href="https://github.com/DavidTorro"><img src="https://img.shields.io/badge/author-David%20Torr%C3%B3-181717?style=for-the-badge&amp;logo=github&amp;logoColor=white" alt="David Torró"></a>

</div>

# AWS IAM Governance Lab

Práctica de gobernanza de identidades en un entorno AWS local con [Floci](https://floci.io/). El objetivo es definir usuarios, grupos y políticas con mínimo privilegio, comprobar las decisiones con el simulador de IAM y documentar los resultados.

Este repositorio está **inicializado para comenzar la práctica**. Aún no contiene políticas implementadas, recursos IAM desplegados ni evidencias.

## Alcance del enunciado

- **Dev-Team:** `roberto`, `sandra` y `alicia`. Lectura de S3, operaciones de datos en DynamoDB y denegación explícita del borrado en S3.
- **Ops-Team:** `marta` y `alexis`. Consulta, arranque y parada de EC2; gestión de Lambda.
- **SecOps-Team:** `camila` y `alicia`. Lectura de CloudTrail, CloudWatch Logs e IAM; denegación de cambios destructivos en producción.
- `alicia` pertenece a dos grupos. Las políticas se asignarán a grupos, nunca directamente a usuarios.

## Estructura

```text
assets/banner.svg           Banner del repositorio
docs/                       Memoria técnica, tema visual y evidencias
docs/assets/capturas/       Capturas para la memoria
policies/                   Políticas JSON de los tres grupos
pdf/                        Plantilla de portada y estilos de la memoria PDF
.github/                    CI, despliegue manual y plantilla de PR
enunciados/                 Enunciado original, conservado solo en local
mkdocs.yml                  Configuración de la documentación
requirements.txt            Dependencias de MkDocs y exportación a PDF
```

La organización de `docs/` y `policies/` toma como referencia [aws-iam-security-lab](https://github.com/DavidTorro/aws-iam-security-lab). Este proyecto seguirá el entorno y los comandos del enunciado actual, basados en Floci y AWS CLI.

## Próximos pasos

1. Comprobar Docker, AWS CLI y Floci.
2. Crear grupos, usuarios y pertenencias.
3. Redactar y asociar las tres políticas JSON.
4. Simular permisos y guardar evidencias.
5. Documentar el análisis de seguridad, gobernanza y entorno efímero.

Para previsualizar la memoria cuando esté redactada:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

Para mostrar también el botón de PDF en la vista local, inicia MkDocs con `ENABLE_PDF_EXPORT=1 .venv/bin/mkdocs serve`. La documentación se puede generar con `.venv/bin/mkdocs build --strict`; el PDF se genera con `ENABLE_PDF_EXPORT=1 .venv/bin/mkdocs build --strict`.

## Licencia

Código y documentación propios bajo [MIT](LICENSE). El enunciado del profesorado se conserva únicamente en local.
