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
				var divContainer = $('<div>').css('display','inline-block');
				//divContainer.css('padding','0px 10px 10px 0');
				//divContainer.css({height:'300px'});
				divContainer.draggable({
					appendTo:'[ng-container]',
					containment: "parent"
				});
				divContainer.resizable({
					containement: "parent"
				});
				$(newTimeline[0]).addClass('context-menu');
				newTimeline.css({width:'100%',height:'100%'});
				$.contextMenu({
					selector: '.context-menu', 
					callback: function(key, options) {
						options.$trigger.parent().remove();
						element.scope().removeElement(id);
					}.bind(this),
					items: {
						"delete": {name: "Delete", icon: "delete"},
					}
				});
				divContainer.append(newTimeline[0]);
				element.append(divContainer);
				element.scope().listComponentAdded.push({name:id});
				/* Forzamos la fase de compile de angular para que cargue las directivas del
         * nuevo elemento
         */

				injector = element.injector();
				$compile = injector.get("$compile");
				$compile(divContainer)(divContainer.scope());

				var position = newTimeline.scope()
				.calculatePosition(divContainer[0], evento.pageX ,evento.pageY - $('[ng-container]').offset().top);
				var minHeight = newTimeline.css('minHeight');
				var minWidth = newTimeline.css('minWidth');
				minHeight = minHeight !== 'none'? parseInt(minHeight.split('px')[0]) : 0;
				minWidth = minWidth !== 'none'? parseInt(minWidth.split('px')[0]) : 0;
				var height = newTimeline.css('heigth') || '400px';
				var width = newTimeline.css('width') || '400px';
				divContainer.resizable('option', 'minHeight',minHeight+10);
				divContainer.resizable('option', 'minWidth',minWidth+10);
				divContainer.css({
					"position": "absolute",
					"top": position.top + "px",
					"left": position.left + "px",
					'minWidth':minWidth,
					'minHeight':minHeight,
					'height': height,
					'width':width
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

			$('#store-modal').modal('toggle');
			evento.originalEvent.dataTransfer.setData("element", scope.idElement);
			/* Pasamos los atributos del timeline */
			if (scope.attributes) {
				evento.originalEvent.dataTransfer.setData("attributes", scope.attributes);
			}

			var image;
		};
		scope.click = function(e){
			/* Evitamos la accion por defecto y la propagacion a los hijos*/
			e.preventDefault();
			e.stopPropagation();
			var attributes, newTimeline, injector, $compile, key;
			/* Cogemos el objeto que tuvo lugar en el intercambio de datos */

			/* Si no esta repetido, lo añadimos al dashboard */
			if (scope.idElement && document.getElementsByTagName(scope.idElement).length === 0) {

				/* Lo eliminamos de la lista */
				/* TODO: si se elimina existe un problema con añadirlo de nuevo
         * habría que hacer un AND entre dos listas (idk como )
         */

				/* Creamos el nuevo objeto en funcion del identificador intercambiado */
				newTimeline = angular.element("<" + scope.idElement + "/>");
				/* Añadimos los atributos necesarios para su funcionamiento */


				/* Añadimos todos los attributos necesarios */
				if (scope.attributes) {
					scope.attributes = JSON.parse(scope.attributes);
					for (key in scope.attributes) {
						if (scope.attributes.hasOwnProperty(key)) {
							newTimeline.attr(key, scope.attributes[key]);
						}
					}
				}
				/* Caracteristicas del estilo para arrastrarlo */
				/* Enlazamos el elemento al contenedor*/
				var divContainer = $('<div>').css('display','inline-block');
				divContainer.draggable({
					appendTo:'[ng-container]',
					containment: "parent"
				});
				divContainer.resizable({
					containement: "parent"
				});
				$(newTimeline[0]).addClass('context-menu');
				newTimeline.css({width:'100%',height:'100%'});
				$.contextMenu({
					selector: '.context-menu', 
					callback: function(key, options) {
						options.$trigger.parent().remove();
						element.scope().removeElement(id);
					},
					items: {
						"delete": {name: "Delete", icon: "delete"},
					}
				});
				divContainer.append(newTimeline[0]);
				var container = $('[ng-container]');
				container.append(divContainer);
				container.scope().listComponentAdded.push({name:scope.idElement});
				/* Forzamos la fase de compile de angular para que cargue las directivas del
         * nuevo elemento
         */

				injector = container.injector();
				$compile = injector.get("$compile");
				$compile(divContainer)(divContainer.scope());


				var minHeight = newTimeline.css('minHeight');
				var minWidth = newTimeline.css('minWidth');
				minHeight = minHeight !== 'none'? parseInt(minHeight.split('px')[0]) : 0;
				minWidth = minWidth !== 'none'? parseInt(minWidth.split('px')[0]) : 0;
				var height = newTimeline.css('heigth') || '400px';
				var width = newTimeline.css('width') || '400px';
				height = height.split('px') < 400 ? '400px': height;
				width = width.split('px') < 400 ? '400px': width;
				divContainer.resizable('option', 'minHeight',minHeight+10);
				divContainer.resizable('option', 'minWidth',minWidth+10);
				divContainer.css({
					"position": "absolute",
					"top": "0 px",
					"left": "0 px",
					'minWidth':minWidth,
					'minHeight':minHeight,
					'height':height,
					'width':width
				});
			}
		};
		element.attr("draggable", "true");
		element.on("dragstart", function(e){
			var canExecute = false;
			if (scope.pre == undefined){
				canExecute = true;
			}else if (typeof scope.pre == 'function' ){
				canExecute = scope.pre();
			} else {
				canExecute = scope.pre ? true: false;
			}
			if (canExecute){
				scope.comienzo(e);
			}
		});
		element.on('dblclick', function(e){
			var canExecute = false;
			if (scope.pre == undefined){
				canExecute = true;
			}else if (typeof scope.pre == 'function' ){
				canExecute = scope.pre();
			} else {
				canExecute = scope.pre ? true: false;
			}
			if (canExecute){
				scope.click(e);
			}
		});
	}
	return {scope: {imagesrc: "@imagesrc", attributes: "@listAttributes", idElement: "@idElement", condition: "@pre"}, link: link};
});
