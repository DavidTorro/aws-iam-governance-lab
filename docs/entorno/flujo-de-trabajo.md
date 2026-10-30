# Flujo de trabajo con Terraform

El entorno `envs/floci/` usa el proveedor oficial `hashicorp/aws` con credenciales ficticias y el endpoint IAM local. `modules/iam-group/` crea un grupo y le asocia su política inline JSON. En `locals.tf` se declaran los seis usuarios y sus pertenencias; `main.tf` crea los recursos. El archivo `.terraform.lock.hcl` fija la versión exacta del proveedor para repetir el despliegue.

## Despliegue

Desde la raíz del repositorio, con Docker Desktop en funcionamiento:

```bash
floci start
terraform -chdir=envs/floci init
terraform -chdir=envs/floci fmt -check
terraform -chdir=envs/floci validate
terraform -chdir=envs/floci test
terraform -chdir=envs/floci plan
terraform -chdir=envs/floci apply
python3 scripts/verify.py
```

`bash scripts/deploy.sh` agrupa el `init` y el `apply` para repetir la creación. El primer plan mostró 18 recursos: seis usuarios, tres grupos, tres políticas inline y seis recursos de pertenencia (uno por usuario; `alicia` tiene dos grupos). Tras aplicar, un segundo `terraform plan -detailed-exitcode` terminó con «No changes».

`evidence/terraform-state.txt` lista los 18 recursos registrados en el estado de Terraform tras la reconstrucción.

`verify.py` contrasta el estado real con los JSON del repositorio y el simulador IAM. Guarda respuestas completas en `evidence/verification.json` y la comparación en `evidence/verification.md`. Para comprobar manualmente a `alicia`:

```bash
eval "$(floci env)"
aws iam list-groups-for-user --user-name alicia
arn="$(aws iam get-user --user-name alicia --query User.Arn --output text)"
aws iam simulate-principal-policy \
  --policy-source-arn "$arn" \
  --action-names s3:GetObject s3:DeleteObject cloudtrail:LookupEvents \
  --query 'EvaluationResults[].[EvalActionName,EvalDecision]' \
  --output table
```

## Prueba de entorno efímero

Después de guardar las simulaciones, `bash scripts/check-ephemeral.sh` comprueba que el reinicio de Floci borra las identidades. `terraform -chdir=envs/floci plan` detecta los 18 recursos ausentes; `bash scripts/deploy.sh` los recrea y `python3 scripts/verify.py` vuelve a comprobarlos. El resultado del reinicio queda en `evidence/ephemeral.json`.
