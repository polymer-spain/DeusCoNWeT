angular.module('picbit').controller('UserHomeController', ['$scope', '$timeout', '$rootScope', '$interval', '$backend', '$http', function ($scope, $timeout, $rootScope, $interval,
  $backend, $http) {
  'use strict';

  // Lista de componentes añadidos
  $scope.listComponentAdded = [];
  $scope.componentsRated = [];
  $scope.catalogList = [];

  // loads references for this
  (function () {
    if ($scope.user.references) {
      $scope.user.references.forEach(function (ref, index) {
        var $jq = window.$;
        var $link = $('<link rel="import">').attr('href', ref);
        $('body').append($link);
        window.setTimeout(function () {
          window.$ = $jq
        }, 1000)
      });
    }
  })();

  //  Logica que dice que botones del a barra lateral estan activos y cuales
  // han de desactivarse
  $scope.selectListButton = function (e) {
    e.stopPropagation();
    var $target = $(e.currentTarget);
    if ($target.hasClass('active')) {
      $target.removeClass('active');
    } else {
      $target.parent().children().removeClass('active');
      $target.addClass('active');
    }

  };

  // Perdir información de los componentes al servidor
  $backend.getComponentInfo().then(function (res) {
    $scope.catalogList = res.data.data;
    var tokenAttr, social_network;
    // Add tokens
    for (var i = 0; i < $scope.catalogList.length; i++) {
      tokenAttr = $scope.catalogList[i].tokenAttr;
      social_network = $scope.catalogList[i].social_network;
      if (social_network) {
        $scope.catalogList[i].attributes[tokenAttr] = $rootScope.user.tokens[social_network] || "";
      }
      // Parse :domain, :user, :language
      for (var attr in $scope.catalogList[i].attributes) {
        // skip loop if the property is from prototype
        if ($scope.catalogList[i].attributes.hasOwnProperty(attr) && typeof $scope.catalogList[i].attributes[attr] == "string") {
          var attr_value = $scope.catalogList[i].attributes[attr];
          attr_value = attr_value.replace(':domain', $scope.domain);
          attr_value = attr_value.replace(':user', 'mortega5');
          attr_value = attr_value.replace(':language', '{{idioma}}');
          $scope.catalogList[i].attributes[attr] = attr_value;
        }
      }

    }
  }, function () {
    console.error('Error al pedir datos del componente');
  });


  // Activa la lista de componenes que se pueden borrar
  $scope.activeDelCmpList = function () {
    var $list = $('.component-list');
    if (!$list.hasClass('active')) {
      $list.addClass('active');
    } else if ($scope.showList === $scope.addedList) {
      $list.removeClass('active');
    }
  };

  // Elimina un componente añadido
  $scope.removeElement = function (id) {
    var finded = false;
    // Delete from list
    for (var i = 0; i < $scope.listComponentAdded.length && !finded; i++) {
      if ($scope.listComponentAdded[i].name === id) {
        finded = true;
        $scope.listComponentAdded.splice(i, 1);
      }
    }
    // Remove disabled

    var selector = "[ng-create-element][id-element='" + id + "']";
    $(selector).attr('disabled', false);
  };


  $scope.blurList = function (e) {
    // del activated
    var component_id = $(e.target).attr('data-component');
    //var id = $scope.listComponentAdded.splice(index, 1)[0];
    $scope.removeElement(component_id);
    $scope.$broadcast("removeComponent", {
      name: component_id
    });

    
    var element = '[data-container="' + component_id + '"]';
    $(element).remove();
  };

  // Cierra las listas cuando se pulsa sobro cualquier otro lado del dashboard
  $('#userHome').click(function (event) {
    if (!event.target.hasAttribute('data-button') && !event.target.hasAttribute('data-list')) {
      $('.component-list').removeClass('active');
      $('.menu-buttons').children().removeClass('active');
    }
  });

  // Cierra los modales en funcion de cual esté abierto
  $(document).on('keydown', function (e) {
    e.stopPropagation();
    if (e.keyCode === 27 && $('#login-modal').is(':visible')) {
      $('#login-modal').modal('toggle');
    } else if (e.keyCode === 27 && $('#store-modal').is(':visible')) {
      $('#store-modal').modal('toggle');
    }
  });

  //Evita que se cierren los dos modales a la vez
  $('#store-modal').on('hidden.bs.modal', function () {
    if ($('#login-modal').is(':visible')) {
      $('#login-modal').modal('toggle');
    }
  });

  // Selecciona que modal tiene que cerrarse en cada momento
  $scope.toggleCatalog = function () {
    if ($('#login-modal').is(':visible')) {
      $('#login-modal').modal('toggle');
    }
    $('#store-modal').modal('toggle');
  };

  $scope.setToken = function (social_network, value) {
    for (var i = 0; i < $scope.catalogList.length; i++) {
      var element = $scope.catalogList[i];
      if (element.social_network === social_network) {
        element.attributes[element.tokenAttr] = value;
      }
    }
    $rootScope.user.renew[social_network] = true;
  };

  $scope.closeModal = function (selector, reset) {
    $(selector).modal('toggle');
    if (reset) $scope.resetModal();
  };
  $scope.removeComponent = function (event) {
    var parent = $(event.target).parent()
    // Get id of the component we're deleting.
    var component_id = parent.attr('data-id');
    // remove main container
    parent.parent().remove();
    $scope.removeElement(component_id)
    $scope.$broadcast("removeComponent", {
      name: component_id
    });
  };

  $scope.login = function (social_network, element, component_id) {
    $scope.loginSelected = social_network;
    $scope.targetComponent= component_id;
    $('#login-modal').modal('toggle');
  };

  // Callback when login finish
  (function () {
    function loginCallback(e) {
      //falta registralo
      $scope.$apply(function () {
        var social_network = e.detail.redSocial;
        var token = e.detail.token;
        var registerTokenError = function () {
          $scope.showToastr('warning', $scope.language.add_token_error);
          $rootScope.user.renew[social_network] = true;
          //$rootScope.user.tokens[social_network] = '';
          //$scope.setToken(social_network, '');
        };
        $rootScope.user = $rootScope.user || {
          tokens: {}
        };
        if (social_network !== 'twitter') {
          $rootScope.user.tokens[social_network] = token;
          $scope.setToken(social_network, token);
          $('#login-modal').modal('toggle');
        }



        switch (social_network) {
          case 'googleplus':
            var uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + token;
            $http.get(uri).success(function (responseData) {
              $rootScope.user.renew[social_network] = true;
              $("[id-element='" + $scope.targetComponent + "']").dblclick();
              $scope.loginSelected = undefined;
              $scope.targetComponent= undefined;
              //$backend.setNewNetwork(token, responseData.id, social_network).then(function(){},registerTokenError);
            });
            break;
          case 'twitter':
            uri = $backend.endpoint + '/api/oauth/twitter/authorization/' + e.detail.oauth_verifier;
            uri += '?oauth_token=' + e.detail.token;
            $http.get(uri).success(function (responseData) {
              e.detail.userId = responseData.token_id;
              $backend.setNewNetwork(token, responseData.token_id, social_network, e.detail.oauth_verifier).then(function (res) {
                $rootScope.user.tokens[social_network] = res.data.token;
                $scope.setToken(social_network, res.data.token);
                $('#login-modal').modal('toggle');
                $("[id-element='" + $scope.targetComponent + "']").dblclick();
                $scope.loginSelected = undefined;
                $scope.targetComponent= undefined;
              }, registerTokenError);
            }).error(function () {
              console.log('Problemas al intentar obtener el token_id de un usuario');
            });
            break;
          // case 'pinterest':
          //   break;
          // case 'spotify':
          //   break;
          // case 'reddit':
          //   break;
          default:
            $("[id-element='" + $scope.targetComponent + "']").dblclick();
            $scope.loginSelected = undefined;
            $scope.targetComponent= undefined;
            //$backend.setNewNetwork(token, e.detail.userId, social_network).error(registerTokenError);
            break;
        }
        

      });
    }
    $('#login-modal google-login').bind('google-logged', loginCallback);
    $('#login-modal github-login').bind('github-logged', loginCallback);
    $('#login-modal instagram-login').bind('instagram-logged', loginCallback);
    $('#login-modal twitter-login').bind('twitter-logged', loginCallback);
    $('#login-modal login-facebook').bind('facebook-logged', loginCallback);
    $('#login-modal pinterest-login').bind('pinterest-logged', loginCallback);
    $('#login-modal spotify-login').bind('spotify-logged', loginCallback);
    $('#login-modal reddit-login').bind('reddit-logged', loginCallback);
  })();


  // Listen remove event
  $scope.$on("removeComponent", function (event, data) {
    $scope.removeElement(data.name);
  })
}]);;