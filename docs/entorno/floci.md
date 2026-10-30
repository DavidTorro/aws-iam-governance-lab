# Entorno Floci

## Herramientas y conexión

La práctica se ejecutó en macOS con Terraform 1.17.0, Docker 28.3.3, AWS CLI 2.37.13 y Floci CLI 0.4.0. Floci arrancó un contenedor local accesible en `http://localhost:4566`. El proveedor AWS de Terraform usa credenciales ficticias `test/test` y dirige IAM y STS al endpoint local. Los scripts de verificación fijan también ese endpoint.

```bash
docker info
terraform version
aws --version
floci doctor
floci start
eval "$(floci env)"
aws iam list-users
```

`floci env` afecta solo a la terminal actual. Terraform no depende de esas variables: su proveedor declara el endpoint local y credenciales de prueba en `envs/floci/providers.tf`. El verificador usa `--endpoint-url http://localhost:4566` para evitar que una configuración AWS personal redirija las llamadas a la nube real.

## Limitación de IAM en el emulador

El enunciado indica que Floci almacena políticas IAM, pero no aplica por defecto sus restricciones a las peticiones de servicio. Una operación de S3 hecha con las credenciales ficticias no demuestra el permiso efectivo de `roberto`. La evidencia de autorización procede de `aws iam simulate-principal-policy`, que evalúa las políticas de sus grupos.

## Persistencia

La ejecución normal se hizo sin `--persist`. Al detener y arrancar el emulador se eliminó el contenedor anterior y desaparecieron las seis identidades. La salida íntegra está en `evidence/ephemeral.json`: `users_before` contiene los seis nombres y `users_after` es una lista vacía. El estado local de Terraform permanece, por lo que un nuevo `terraform apply` detecta los recursos ausentes y los reconstruye. Para conservar datos en Floci entre arranques se necesitaría configurar persistencia, lo que no forma parte de esta prueba.
