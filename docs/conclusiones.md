# Conclusiones

Terraform desplegó y verificó en Floci seis usuarios, tres grupos, siete pertenencias y tres políticas inline asociadas solo a grupos. El simulador confirmó permisos de desarrollo, operaciones y auditoría, así como denegaciones implícitas para acciones ajenas a cada función.

El caso de `alicia` demuestra la precedencia del `Deny` explícito: recibe permisos de Dev-Team y SecOps-Team, pero no puede borrar objetos S3 según la simulación. La gobernanza por grupos permite mantener y auditar esos permisos sin configuraciones individuales.

El reinicio sin persistencia borró las seis identidades. Terraform detectó y recreó los 18 recursos declarados, lo que confirma que el entorno puede reconstruirse desde código y utilizarse como base limpia para pruebas CI/CD. El simulador verifica decisiones de autorización; una comprobación en AWS real exigiría además revisar ARNs, dependencias entre servicios y restricciones adicionales del entorno de producción.
