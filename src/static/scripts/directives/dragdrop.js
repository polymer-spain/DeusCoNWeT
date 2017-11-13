/*global angular, document*/

(function () {
  var picbit = angular.module("picbit");

  var defaultConfig = {
    style: {
      width: '100%',
      height: '100%'
    }
  }
  var createComponent = function (name, attributes, config) {
    /* Si no esta repetido, lo añadimos al dashboard */
    var newTimeline, injector, $compile, key;
    $.extend(config, defaultConfig);
    if (name && document.getElementsByTagName(name).length === 0) {

      /* Creamos el nuevo objeto en funcion del identificador intercambiado */
      newTimeline = angular.element("<" + name + "/>");
      var container = angular.element('[ng-container]');
      /* Añadimos todos los attributos necesarios */
      if (attributes) {
        newTimeline.attr(attributes);
      }
      /* Caracteristicas del estilo para arrastrarlo */
      /* Enlazamos el elemento al contenedor*/
      var divContainer = $('<div data-container="' + name + '">').css('display', 'inline-block');

      /* Header */
      var header = $('<div class="header" data-id="' + name + '"><span class="componentName">' + name+ '</span><span class="deleteComponent" ng-click="removeComponent($event)">×</span></div>')
      divContainer.append(header);
      divContainer.draggable({
        appendTo: '[ng-container]',
        containment: "parent",
        handle: ".header"
      });

      divContainer.resizable({
        containement: "parent"
      });

      newTimeline.addClass('context-menu');
      newTimeline.css(config.style);
      divContainer.append(newTimeline);
      container.append(divContainer);
      container.scope().listComponentAdded.push({
        name: name
      });

      var minHeight = newTimeline.css('minHeight');
      var minWidth = newTimeline.css('minWidth');
      minHeight = minHeight !== 'none' ? parseInt(minHeight.split('px')[0]) : 0;
      minWidth = minWidth !== 'none' ? parseInt(minWidth.split('px')[0]) : 0;
      var height = newTimeline.css('height') || '400px';
      var width = newTimeline.css('width') || '400px';
      height = height.split('px') < 400 ? '400px' : height;
      width = width.split('px') < 400 ? '400px' : width;
      divContainer.resizable('option', 'minHeight', minHeight + 10);
      divContainer.resizable('option', 'minWidth', minWidth + 10);
      divContainer.css({
        "position": "absolute",
        "top": "25px",
        "left": "0px",
        'minWidth': minWidth,
        'minHeight': minHeight,
        'height': height,
        'width': width
      });
      container.scope().$broadcast('componentAdded', {
        name: name,
        element: newTimeline
      })
      /* Forzamos la fase de compile de angular para que cargue las directivas del
       * nuevo elemento
       */

      injector = container.injector();
      $compile = injector.get("$compile");
      $compile(divContainer)(divContainer.scope());
      // $compile(header.children())(divContainer.scope());
    }
    return divContainer
  }

  picbit.directive("ngContainer", function () {
    "use strict";

    function link(scope, element) {
      scope.calculatePosition = function (target, x, y) {
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
        newPosition.top = into.bottom ? newPosition.top : container.offsetTop + container.offsetHeight - target.offsetHeight - padding.bottom;
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
        /* Añadimos todos los attributos necesarios */
        attributes = JSON.parse(evento.originalEvent.dataTransfer.getData("attributes"));
        /* Si no esta repetido, lo añadimos al dashboard */
        var parentContainer = createComponent(id, attributes, {});
        var position = scope.calculatePosition(parentContainer[0], evento.pageX, evento.pageY - $('[ng-container]').offset().top);
        parentContainer.css({
          top: position.top + "px",
          left: position.left + "px"
        })
      };
      /* Funcion que evita la accion por defecto cuando entra un elemento */
      scope.dragEntry = function (evento) {
        evento.preventDefault();
      };
      /* Enlazamos las funciones con los eventos correspondientes */
      element.on("drop", scope.dropObject);
      element.on("dragover", scope.dragEntry);

    }
    /* enviamos el link y cogemos la lista de los atributos y la añadimos al scope*/
    return {
      link: link
    };
  });

  picbit.directive("ngCreateElement", function () {
    "use strict";

    function link(scope, element, attrs) {
      scope.comienzo = function (evento) {

        $('#store-modal').modal('toggle');
        evento.originalEvent.dataTransfer.setData("element", scope.idElement);

        /* Pasamos los atributos del timeline */
        if (scope.item.attributes) {
          evento.originalEvent.dataTransfer.setData("attributes", JSON.stringify(scope.item.attributes));
        }
        var removeListener = scope.$on("componentAdded", function (e, data) {
          element.attr('disabled', true);
          removeListener();
        })
      };
      scope.click = function (e) {
        /* Evitamos la accion por defecto y la propagacion a los hijos*/
        e.preventDefault();
        e.stopPropagation();
        createComponent(scope.idElement, scope.item.attributes, {})
        element.attr('disabled', "true");
      };
      element.attr("draggable", "true");
      element.on("dragstart", function (e) {
        var canExecute = scope.item.tokenAttr ? scope.item.attributes[item.tokenAttr] !== "" : true;
        if (canExecute) {
          scope.comienzo(e);
        }
      });
      element.on('dblclick', function (e) {
        var canExecute = scope.item.tokenAttr ? scope.item.attributes[scope.item.tokenAttr] !== "" : true;
        if (canExecute) {
          scope.click(e);
        }
      });
    }
    return {
      scope: {
        idElement: "@idElement",
        item: '='
      },
      link: link
    };
  });
})();