# TPE-Abraham-Cisilino-2025
En este repositorio se encuentra todo lo desarrollado para el TPE de la materia Fundamentos de la Ciencia de Datos-cursada 2025.


## Ideas para multivariadas :

### Idea 1: El Perfil de Conversión (Usuario + Comportamiento)
- Pregunta de Negocio: ¿Se comportan igual los clientes nuevos y los recurrentes cuando van a comprar?

- Variables Involucradas: VisitorType (Categórica), ProductRelated_Duration (Numérica) y Revenue (Objetivo).

- Idea General: Sabemos que los Returning_Visitor (visitantes recurrentes) probablemente compran más. También sabemos que pasar más tiempo en páginas de productos (ProductRelated_Duration) es un buen indicador de compra.

- Hipótesis Multivariada (Idea): La hipótesis es que la necesidad de pasar tiempo en páginas de productos es diferente para cada tipo de visitante. Un Returning_Visitor podría convertir con una ProductRelated_Duration baja (ya sabe lo que quiere), mientras que un New_Visitor necesita una ProductRelated_Duration muy alta para generar la confianza suficiente para comprar.

### Idea 2: La Efectividad de las Promociones (Contexto + Usuario)
- Pregunta de Negocio: ¿Nuestras campañas de días especiales atraen a nuevos clientes o solo fidelizan a los que ya teníamos?

- Variables Involucradas: SpecialDay (Numérica), VisitorType (Categórica) y Revenue (Objetivo).

- Idea General: SpecialDay mide la cercanía a una festividad o promoción. VisitorType nos dice si el cliente es nuevo o recurrente.

- Hipótesis Multivariada (Idea): La hipótesis es que el efecto positivo de un día especial (SpecialDay = 0) sobre la probabilidad de compra (Revenue = True) es significativamente más fuerte para los New_Visitor que para los Returning_Visitor. Esto nos ayudaría a medir el poder de adquisición de clientes de nuestras campañas de marketing.

### Idea 3: El Comprador Cauteloso (Comportamiento + Confianza)
- Pregunta de Negocio: ¿Qué diferencia a un usuario que está en el "camino dorado" (PageValues > 0) pero abandona, de uno que sí compra?

- Variables Involucradas: PageValues (Numérica), Informational_Duration (Numérica) y Revenue (Objetivo).

- Idea General: PageValues es un fuerte indicador de que el usuario está en una ruta que históricamente lleva a una compra. Por otro lado, Informational_Duration mide el tiempo en páginas de "confianza" como FAQs, "Sobre Nosotros" o políticas de envío.

- Hipótesis Multivariada (Idea): La hipótesis es que, entre los usuarios que ya tienen un PageValues > 0, aquellos que además dedican tiempo a construir confianza (un Informational_Duration > 0) tendrán una tasa de conversión (Revenue = True) mucho más alta que aquellos que no lo hacen (Informational_Duration = 0).