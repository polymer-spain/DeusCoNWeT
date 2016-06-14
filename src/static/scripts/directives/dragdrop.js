/*global angular, document*/
var picbit = angular.module("picbit");


picbit.directive("ngContainer", function () {
	"use strict";
	function link(scope, element) {
		scope.calculatePosition = function(target, x, y) {
			var newPosition = {},
					padding = {},
					into = {};
			newPosition.left = target.offsetLeft + x;
			newPosition.right = target.offsetLeft + x + target.offsetWidth;
			newPosition.top = target.offsetTop + y;
			newPosition.bottom = target.offsetTop + y + target.offsetHeight;

			/* Buscamos el elemento contenedor del objeto */
			var container = document.querySelector("[ng-container]");


			/* Comparamos los limites de ambos elementos para saber si esta dentro */

			padding.top = parseInt(angular.element(container).css("padding-top").split("px")[0]) || 0;
			padding.right = parseInt(angular.element(container).css("padding-right").split("px")[0]) || 0;
			padding.bottom = parseInt(angular.element(container).css("padding-bottom").split("px")[0]) || 0;
			padding.left = parseInt(angular.element(container).css("padding-left").split("px")[0]) || 0;



			into.left = container.offsetLeft + padding.left < newPosition.left;
			into.right = container.offsetWidth + container.offsetLeft - padding.right > newPosition.right;
			into.top = container.offsetTop + padding.top < newPosition.top;
			into.bottom = container.offsetHeight + container.offsetTop - padding.bottom > newPosition.bottom;

			// top
			newPosition.top = into.top ? newPosition.top : container.offsetTop + padding.top;
			// bottom
			newPosition.top  = into.bottom ? newPosition.top : container.offsetTop + container.offsetHeight - target.offsetHeight - padding.bottom;
			// left
			newPosition.left = into.left ? newPosition.left : container.offsetLeft + padding.left;
			// right
			newPosition.left = into.right ? newPosition.left : container.offsetLeft + container.offsetWidth - target.offsetWidth - padding.right;

			return newPosition;
		};
		scope.dropObject = function (evento) {
			/* Evitamos la accion por defecto y la propagacion a los hijos*/
			evento.preventDefault();
			evento.stopPropagation();




			var id, attributes, newTimeline, injector, $compile, key;
			/* Cogemos el objeto que tuvo lugar en el intercambio de datos */
			id = evento.originalEvent.dataTransfer.getData("element");

			/* Si no esta repetido, lo añadimos al dashboard */
			if (id && document.getElementsByTagName(id).length === 0) {

				/* Lo eliminamos de la lista */
				/* TODO: si se elimina existe un problema con añadirlo de nuevo
         * habría que hacer un AND entre dos listas (idk como )
         */

				/* Creamos el nuevo objeto en funcion del identificador intercambiado */
				newTimeline = angular.element("<" + id + "/>");
				/* Añadimos los atributos necesarios para su funcionamiento */


				/* Añadimos todos los attributos necesarios */
				attributes = evento.originalEvent.dataTransfer.getData("attributes");
				if (attributes) {
					attributes = JSON.parse(attributes);
					for (key in attributes) {
						if (attributes.hasOwnProperty(key)) {
							newTimeline.attr(key, attributes[key]);
						}
					}
				}
				/* Caracteristicas del estilo para arrastrarlo */
				/* Enlazamos el elemento al contenedor*/
				newTimeline.draggable({
					appendTo:'[ng-container]',
					containment: "parent"
				});
				$(newTimeline[0]).resizable();
				$(newTimeline[0]).addClass('context-menu');
				$.contextMenu({
					selector: '.context-menu', 
					callback: function(key, options) {
						console.log(options);
						options.$trigger.remove();
					},
					items: {
						"delete": {name: "Delete", icon: "delete"},
					}
				});
				element.append(newTimeline[0]);
				element.scope().listComponentAdded.push({name:id});

				/* Forzamos la fase de compile de angular para que cargue las directivas del
         * nuevo elemento
         */

				injector = element.injector();
				$compile = injector.get("$compile");
				$compile(newTimeline)(newTimeline.scope());

				var position = newTimeline.scope()
				.calculatePosition(newTimeline[0], evento.pageX ,evento.pageY - $('[ng-container]').offset().top);
				newTimeline.css({
					"position": "absolute",
					"top": position.top + "px",
					"left": position.left + "px"
				});
			}
		};
		/* Funcion que evita la accion por defecto cuando entra un elemento */
		scope.dragEntry = function (evento) {evento.preventDefault(); };
		/* Enlazamos las funciones con los eventos correspondientes */
		element.on("drop", scope.dropObject);
		element.on("dragover", scope.dragEntry);

	}
	/* enviamos el link y cogemos la lista de los atributos y la añadimos al scope*/
	return {link: link};
});

picbit.directive("ngCreateElement", function () {
	"use strict";
	function link(scope, element) {

		scope.comienzo = function (evento) {

			evento.originalEvent.dataTransfer.setData("element", scope.idElement);

			/* Pasamos los atributos del timeline */
			if (scope.attributes) {
				evento.originalEvent.dataTransfer.setData("attributes", scope.attributes);
			}

			var image;
			image = document.createElement("img");

			image.src = scope.imagesrc || "";
			evento.originalEvent.dataTransfer.setDragImage(image, 0, 0);
		};

		element.attr("draggable", "true");
		element.on("dragstart", scope.comienzo);
	}
	return {scope: {imagesrc: "@imagesrc", attributes: "@listAttributes", idElement: "@idElement"}, link: link};
});
