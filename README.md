<div align="center">

![Banner](./assets/banner.svg)
<br>
  <img src="https://img.shields.io/badge/-Terraform-7b42bc?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform">
  <img src="https://img.shields.io/badge/-AWS%20IAM-dd344c?style=for-the-badge" alt="AWS IAM">
  <img src="https://img.shields.io/badge/-Amazon%20S3-569a31?style=for-the-badge" alt="Amazon S3">
  <img src="https://img.shields.io/badge/-Amazon%20EC2-ff9900?style=for-the-badge" alt="Amazon EC2">
  <img src="https://img.shields.io/badge/-Floci-25b7a4?style=for-the-badge" alt="Floci">
<br>
  <a href="https://github.com/DavidTorro/aws-iam-governance-lab/actions/workflows/ci.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/DavidTorro/aws-iam-governance-lab/ci.yml?branch=main&style=for-the-badge&label=CI" alt="CI">
  </a>
  <a href="./docs/index.md">
    <img src="https://img.shields.io/badge/docs-MkDocs-526cfe?style=for-the-badge&logo=materialformkdocs&logoColor=white" alt="Documentación">
  </a>
  <a href="./output/pdf/aws-iam-governance-lab.pdf">
    <img src="https://img.shields.io/badge/memoria-PDF-b30b00?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Memoria en PDF">
  </a>
  <a href="https://github.com/DavidTorro">
    <img src="https://img.shields.io/badge/author-David%20Torr%C3%B3-181717?style=for-the-badge&logo=github&logoColor=white" alt="Author: David Torró">
  </a>

</div>

# AWS IAM Governance Lab

Práctica de gobernanza de identidades para NextGen Solutions resuelta como **infraestructura como código con Terraform**, siguiendo la organización de [aws-iam-security-lab](https://github.com/DavidTorro/aws-iam-security-lab). El proveedor AWS de Terraform apunta al emulador local [Floci](https://floci.io/). El simulador IAM verifica los permisos y se comprueba el carácter efímero del entorno.

## Resultado de la práctica

| Grupo | Usuarios | Permisos principales |
| --- | --- | --- |
| Dev-Team | `roberto`, `sandra`, `alicia` | Lectura S3, operaciones de datos DynamoDB y denegación explícita de borrado S3 |
| Ops-Team | `marta`, `alexis` | Consulta, arranque y parada EC2; gestión Lambda |
| SecOps-Team | `camila`, `alicia` | Lectura CloudTrail, CloudWatch Logs e IAM; denegación de operaciones destructivas |

Las políticas están asociadas **solo a los grupos**. La [verificación real](./evidence/verification.md) comprobó las siete pertenencias, la ausencia de políticas directas y 23 decisiones del simulador para cuatro usuarios. El [estado Terraform](./evidence/terraform-state.txt) registra los 18 recursos gestionados. `s3:DeleteObject` para `alicia` devolvió `explicitDeny`. La [prueba de reinicio](./evidence/ephemeral.json) confirmó que, sin persistencia, los seis usuarios desaparecen al parar y arrancar Floci.

## Requisitos y ejecución

Necesitas Terraform ≥ 1.9, Docker en funcionamiento, AWS CLI, Floci CLI y Python 3. Floci se puede instalar en macOS con `brew install floci-io/floci/floci`; consulta las [instrucciones oficiales](https://floci.io/) para otros sistemas. **El proveedor Terraform y los scripts dirigen todas las llamadas AWS a `http://localhost:4566` con credenciales ficticias.**

Si Floci ya está en marcha, omite `floci start`.

```bash
floci start
bash scripts/deploy.sh
python3 scripts/verify.py
```

`deploy.sh` ejecuta `terraform init` y `terraform apply` en [`envs/floci`](./envs/floci). La configuración usa el módulo [`modules/iam-group`](./modules/iam-group) para crear cada grupo y su política inline, y gestiona los seis usuarios y sus pertenencias con recursos Terraform. El estado local `terraform.tfstate` está ignorado por Git; el lockfile del proveedor sí se conserva. `verify.py` consulta Floci con AWS CLI y falla si una pertenencia, política o decisión difiere de lo esperado. Escribe las respuestas originales en `evidence/verification.json` y un resumen en `evidence/verification.md`.

Para revisar la infraestructura antes de aplicarla:

```bash
terraform -chdir=envs/floci init
terraform -chdir=envs/floci validate
terraform -chdir=envs/floci test
terraform -chdir=envs/floci plan
terraform -chdir=envs/floci apply
```

La prueba de infraestructura efímera elimina las identidades del emulador:

```bash
bash scripts/check-ephemeral.sh
cat evidence/ephemeral.json
```

Después, `bash scripts/deploy.sh` detecta el estado vacío de Floci y reconstruye los recursos desde Terraform. Para comprobar manualmente a `alicia`:

```bash
eval "$(floci env)"
aws iam list-groups-for-user --user-name alicia
arn="$(aws iam get-user --user-name alicia --query User.Arn --output text)"
aws iam simulate-principal-policy --policy-source-arn "$arn" \
  --action-names s3:GetObject s3:DeleteObject cloudtrail:LookupEvents \
  --query 'EvaluationResults[].[EvalActionName,EvalDecision]' --output table
```

## Memoria y PDF

La [memoria técnica](./docs/index.md) explica los bloques JSON, la denegación explícita, la gobernanza por grupos, las simulaciones y la prueba de entorno efímero. Incluye imágenes de las políticas y de las respuestas del simulador, generadas a partir de los archivos y datos reales con `python3 scripts/render-evidence.py` (requiere ImageMagick en macOS).

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs build --strict
ENABLE_PDF_EXPORT=1 .venv/bin/mkdocs build --strict
```

El PDF generado queda en `site/pdf/aws-iam-governance-lab.pdf`; la [copia final de la memoria](./output/pdf/aws-iam-governance-lab.pdf) se incluye en el repositorio. GitHub Actions valida las políticas y la documentación; el despliegue de Pages se ejecuta manualmente desde `Documentación`.

## Estructura

```text
policies/                 Políticas JSON de los tres grupos
modules/iam-group/        Módulo Terraform para grupo y política
envs/floci/               Despliegue Terraform, lockfile y test
scripts/                  Wrapper de Terraform, verificación y prueba de reinicio
evidence/                 Respuestas reales del emulador
docs/                     Memoria y capturas
pdf/                      Plantilla y estilos del PDF
.github/                  CI y despliegue manual de documentación
enunciados/               Enunciado original, conservado solo en local
```

El enunciado del profesorado no se publica. Código y documentación propios bajo [MIT](LICENSE).
