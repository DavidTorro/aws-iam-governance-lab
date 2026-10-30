# Decisiones de seguridad y gobernanza

## Por qué Terraform

La configuración de `envs/floci/` declara de forma revisable las identidades, sus pertenencias y las políticas de grupo. El módulo `modules/iam-group/` evita repetir la creación de cada grupo y la asociación de su JSON. `terraform plan` muestra el cambio antes de aplicarlo; tras el primer despliegue, el plan devolvió «No changes». Esto permite reconstruir exactamente el laboratorio después de un reinicio efímero de Floci. El estado Terraform se guarda localmente y se excluye de Git; `.terraform.lock.hcl` fija la versión del proveedor.

## Cómo se interpreta cada política JSON

`Version` identifica la versión del lenguaje de políticas de IAM, aquí `2012-10-17`; no es la fecha de creación del archivo. `Statement` contiene las reglas evaluables. `Sid` da un nombre a cada regla para reconocer su intención. `Effect` indica `Allow` o `Deny`. `Action` enumera operaciones AWS, con comodines cuando se pide una familia de acciones. `Resource` determina a qué recursos se aplica cada regla.

En esta práctica el enunciado no proporciona ARNs de buckets, tablas, instancias o funciones; por eso las políticas usan `Resource: "*"`. El mínimo privilegio se aproxima restringiendo las acciones por grupo. Antes de pasar el diseño a una cuenta AWS real habría que acotar recursos y revisar cada comodín.

## Por qué se usa un Deny explícito

La ausencia de `s3:DeleteObject` en los `Allow` de Dev-Team produciría solo `implicitDeny`. Si en el futuro otra política de cualquiera de los grupos de `alicia` concediera `s3:*`, ese permiso permitiría borrar objetos. En cambio, el `Deny` explícito de Dev-Team prevalece aunque aparezca otro `Allow`. La simulación actual de `alicia` confirmó `explicitDeny` para `s3:DeleteObject`.

SecOps-Team también deniega explícitamente tres operaciones destructivas. Como `alicia` pertenece a ese grupo, recibe ambas protecciones. El bloqueo de SecOps usa `Resource: "*"`, más amplio que «producción»; se eligió así porque el ejercicio no identifica recursos de producción concretos.

## Grupos frente a permisos individuales

Con grupos, una política expresa la función de un equipo y se modifica una sola vez. Incorporar a una persona consiste en añadirla al grupo; retirar una función consiste en quitar esa pertenencia. Esto facilita la revisión de quién tiene cada capacidad y reduce excepciones difíciles de encontrar.

Con permisos asignados usuario por usuario, un cambio de función obliga a localizar y editar cada identidad. Para 10 empleados todavía podría revisarse manualmente; con 100 aumenta la probabilidad de diferencias y permisos olvidados; con 1000 el coste operativo y de auditoría hace necesario automatizar las altas, bajas y revisiones sobre grupos o roles. La doble pertenencia de `alicia` muestra cómo combinar funciones sin duplicar políticas.

## Infraestructura efímera para CI/CD

La comprobación real registró seis usuarios creados por Terraform antes de `floci stop` y ninguno después de `floci start`, sin persistencia configurada. El estado local de Terraform permaneció; el plan detectó 18 recursos ausentes y `apply` los recreó. Cada ejecución de una tubería CI/CD puede partir de un estado vacío, aplicar la configuración, probarla y descartarla al finalizar. Esto evita que un test dependa de datos residuales de otro y hace reproducible el entorno. Para conservar estado en Floci entre arranques, habría que elegir explícitamente un modo persistente.
