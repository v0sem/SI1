# Práctica 2

Autores: Pablo Sánchez y Antonio Solana.

## Ficheros

* start.wsgi: inicializacion de la app para Apache.

* app - directorio:
   * catalogue - catalogue.json: Fichero json con todas las películas que se encuentran en este momento en el sistema.
   * static - directorio:
      * images: Directorio con todas las imágenes estáticas de la web.
      * estilo.css: fichero único de css con los estilos de la página.
   * templates: directorio con todos los htmls a los que referencia *routes* y el *base.html* del que todos extienden.
   * routes: fichero python con todas las redirecciones y con todas las operaciones que tiene que hacer nuestra aplicación. Se accede a la funcionalidad a través de requests GET o POST.
* [memoria.pdf](#).

## Instrucciones de uso y detalles de implementación

   En la página principal, *index*, se pueden ver todas las películas disponibles en el catálogo. Si usas la barra de búsqueda puedes encontrar películas específicas por título.

   Para comprar películas es necesario estar loggeado, aunque la sesión se guarda aunque no lo estuvieras mientras añadías películas. Una vez loggeado, y habiendo hecho alguna compra, al acceder al historial de compra puedes ver las compras que has hecho previamente y añadir dinero a tu saldo.

## Fondos de pantalla

Index:
![imagen](app/doc-img/Screenshot_from_2019-10-30_21-41-06.png)

Detalle de película:
![imagen](app/doc-img/Screenshot_from_2019-10-30_21-41-12.png)

Register:
![imagen](app/doc-img/Screenshot_from_2019-10-30_21-41-48.png)

Búsqueda por categoría:
![imagen](app/doc-img/Screenshot_from_2019-10-30_21-43-50.png)

Carrito de la compra:
![imagen](app/doc-img/Screenshot_from_2019-10-30_21-43-39.png)

Historial de compras:
![imagen](app/doc-img/Screenshot_from_2019-10-30_21-43-25.png)

Resultados de búsqueda (Eight):
![imagen](app/doc-img/Screenshot_from_2019-10-30_21-42-31.png)