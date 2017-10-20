angular.module('picbit').controller('UserHomeController', ['$scope', '$timeout', '$rootScope', '$interval', '$backend', '$http', function ($scope, $timeout, $rootScope, $interval,
  $backend, $http) {
  'use strict';

  // Se harcodea twitter por motivos de error en el tokenAttr
  //$rootScope.user.tokens.twitter = "3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf";
  // Lista de componentes añadidos
  // TODO se deberan coger de la lista que se registra en usuario
  $scope.listComponentAdded = [];
  $scope.componentsRated = [];

  // loads references for this
  (function () {
    if ($scope.user.references) {
      $scope.user.references.forEach(function (ref, index) {
        var $jq = window.$;
        //  ref = ref.replace("stable","maintenance");
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
  // borra los filtros
  $scope.removeStarFilter = function () {
    $scope.starFilter = undefined;
  };
  $scope.removeTextFilter = function () {
    $scope.textFilter = '';
  };
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
    var index = $(e.currentTarget).attr('data-index');
    var id = $scope.listComponentAdded.splice(index, 1)[0];
    $scope.showList = $scope.listComponentAdded;
    var element = '[id-element="' + id.name + '"]';
    $(element)[0].setAttribute('disabled', false);
    $(id.name).parent().remove();
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
  };
  $scope.closeModal = function (selector, reset) {
    $(selector).modal('toggle');
    if (reset) $scope.resetModal();
  };
  $scope.login = function (name) {
    $scope.loginSelected = name.split('-')[0];
    $('#login-modal').modal('toggle');
  };



  /// FORMS FUNCTIONS

  // Watcher that controls whether the form should be showed to the user or not
  $scope.platformUsedTime = 0;
  $scope.intervalTime = 1000; // We'll update the value of platformUsedTime each $scope.intervalTime milliseconds
  $scope.formLoadTime = 6000; // Indicates when we'll show to the user the form

  $scope.diffArray = function (arr1, arr2) {
    var newArr = [];
    var myArr = arr1.concat(arr2);

    newArr = myArr.filter(function (item) {
      return arr2.indexOf(item) < 0 || arr1.indexOf(item) < 0;
    });
    return newArr;
  }
  var platformTimeFunction = function () {
    var interval = $interval(function () {

      if (document.visibilityState === "visible" && $scope.listComponentAdded.length > 0 && $scope.diffArray($scope.listComponentAdded, $scope.componentsRated).length > 0 && !$scope._rating) {
        $scope.platformUsedTime += $scope.intervalTime;
      }
    }, $scope.intervalTime);
    return interval;
  }.bind(this);
  var platformTimeHandler = platformTimeFunction();
  $scope.closerating = function () {
    $scope.randomComponent = undefined;
    $scope._rating = false;
    resetModal();
    platformTimeFunction();
  };

  $scope.$watch("platformUsedTime", function (newValue, oldValue) {
    if (newValue !== oldValue && newValue >= $scope.formLoadTime && $scope.listComponentAdded.length > 0) {
      var result = $scope.getRandomComponent();
      if (result) {

        var text = $scope.language.survey + " " + result;
        var options = {
          "closeButton": true,
          "showDuration": "0",
          "hideDuration": "0",
          "timeOut": "0",
          "extendedTimeOut": "0",
        }
        $scope._rating = true;
        $scope.showToastr('info', text, options, function () {
          $scope._rating = true;
          $('#rate-modal').modal({
            backdrop: 'static',
            keyboard: false
          });
        }, $scope.closerating);
        $scope.platformUsedTime = 0;
      }
      $interval.cancel(platformTimeHandler);
    }
  });
  $scope.getRandomComponent = function () {
    // Deep copy
    var unratedList = JSON.parse(JSON.stringify($scope.listComponentAdded));
    var findElement = function (element, list) {
      var find = -1;
      for (var i = 0; i < list.length && find === -1; i++) {
        if (element === list[i] || (list[i] && list[i].name === element)) {
          find = i;
        }
      }
      return find;
    };
    for (var i = 0; i < $scope.componentsRated.length; i++) {
      var component = $scope.componentsRated[i];
      if (findElement(component, unratedList) !== -1) {
        var unrated_index = findElement(component, unratedList);
        unratedList.splice(unrated_index, 1);
      }
    }
    if (!$scope.randomComponent) {
      var random = Math.round(Math.random() * 100);
      if (unratedList.length > 0) {
        var position = random % unratedList.length;
        $scope.randomComponent = unratedList[position].name;
      }
    }
    return $scope.randomComponent;
  };
  var resetModal = function () {
    setTimeout(function () {
      $('#thanksInfo').hide();
      $('#initialQuestion').show();
      $('#rate-modal .modal-footer button').show();
      $('#rate-modal .modal-footer #closeRateModal').hide();
      $('#rate-modal paper-radio-group').each(function (i, e) {
        e.selected = '';
      });
      $('#rate-modal input').each(function (i, e) {
        e.value = "";
      });
    }, 200);
  };
  $scope.submitRating = function () {
    if (!$('#aditionalForm').is(':visible')) {
      if ($('#initialQuestion paper-radio-group')[0].selected) {
        $('#rate-modal .modal-footer p').hide();
        $scope._submitQuestionaire();
        $('#initialQuestion').fadeOut("easing", function () {
          $('#aditionalForm').fadeIn('easing', function () {});
        });
      } else {
        $('#rate-modal .modal-footer p').show();
      }
    } else {
      var $aditionalQuestion = $('.aditionalQuestion');
      $('#rate-modal .modal-footer p').hide();
      var selected = $aditionalQuestion.children('.iron-selected');
      var text = $('.aditionalQuestion.form-control');
      var completed = 0;
      text.each(function (index, element) {
        if ($(element).val() !== '') {
          completed += 1;
        }
      });
      if ($aditionalQuestion.length === selected.length + completed) {
        $('#rate-modal .modal-footer p').hide();
        $('#rate-modal .modal-footer button').hide();
        $scope._submitExtendedQuestionaire();
        $scope.componentsRated.push($scope.randomComponent);
        $scope._rating = false;
        $('#aditionalForm').fadeOut('easing', function () {
          $('#thanksInfo').show();
          $('#rate-modal .modal-footer button').hide();
          $('#rate-modal .modal-footer #closeRateModal').show();
        });
        console.log('TODO mandar mensaje de error a la base de datos');
      } else {
        $('#rate-modal .modal-footer p').show();
      }
    }
  };

  $scope._submitQuestionaire = function () {
    var question_id = "initialQuestion";
    var answer = $('#initialQuestion paper-radio-group')[0].selected;
    var question_text = $('#initialQuestion paper-radio-group').children('.iron-selected').html() || "";
    var version, i;
    for (i = 0; i < $scope.catalogList.length && !version; i++) {
      if ($scope.catalogList[i].component_id === $scope.randomComponent) {
        version = $scope.catalogList[i].version;
      }
    }
    if (!version) {
      console.error('Componente: ', $scope.randomComponent,
        ' no se encuentra en la lista y no tiene version');
    }
    if (answer !== undefined && question_text !== "") {
      //We send an event to Mixpanel
      var properties = {
        "selection": answer,
        "question_type": "obligatory",
        "question": question_id,
        "component": $scope.randomComponent,
        "timestamp": Date.now(),
        "version": version,
        "user": $scope.user.user_id
      };
      mixpanel.track(question_id, properties);
    }
  };

  $scope._submitExtendedQuestionaire = function () {
    // We get the responses for every question

    var aditional_questions = $('#aditionalForm paper-radio-group, #aditionalForm input');
    var mixpanel_event_list = [];
    var mixpanel_event = {};
    var version;
    var i;
    for (i = 0; i < $scope.catalogList.length && !version; i++) {
      if ($scope.catalogList[i].component_id === $scope.randomComponent) {
        version = $scope.catalogList[i].version;
      }
    }
    if (!version) {
      console.error('Componente: ', $scope.randomComponent,
        ' no se encuentra en la lista y no tiene version');
    }
    for (i = 0; i < aditional_questions.length; i++) {
      var question = aditional_questions[i];
      var answer = question.selected || question.value;
      if (answer) {
        mixpanel_event_list.push({
          "event_name": question.id,
          "selection": answer
        }); // qué hace exactamente el push?
      }
    }
    // We check if the user has anwered all questions
    var mixpanel_properties = {};
    if (mixpanel_event_list.length === aditional_questions.length) {
      for (i = 0; i < mixpanel_event_list.length; i++) {
        // We send the responses to Mixpanel
        mixpanel_event = mixpanel_event_list[i];
        mixpanel_properties = {
          "selection": mixpanel_event.selection,
          "question": mixpanel_event.event_name,
          "question_type": "optional",
          "component": $scope.randomComponent, // Se manda la versión?
          "version": version,
          "timestamp": Date.now(),
          "user": $scope.user.user_id
        };
        mixpanel.track(mixpanel_event.event_name, mixpanel_properties);
        // We hide the user form
      }
    }
  };
  $scope.closeForm = function(){
    if ($('#initialQuestion').is(':visible')){
      this.closerating();
    }
  };

  // Callback when login finish
  (function () {
    function loginCallback(e) {
      //falta registralo
      $scope.$apply(function () {
        var social_network = e.detail.redSocial;
        var token = e.detail.token;
        var registerTokenError = function () {
          $scope.showToastr('error', $scope.language.add_token_error);
          $rootScope.user.tokens[social_network] = '';
          $scope.setToken(social_network, '');
        };
        $rootScope.user = $rootScope.user || {
          tokens: {}
        };
        if (social_network !== 'twitter'){
          $rootScope.user.tokens[social_network] = token;
          $scope.setToken(social_network, token);
          $('#login-modal').modal('toggle');
        } 
          


        switch (social_network) {
          case 'googleplus':
            var uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + token;
            $http.get(uri).success(function (responseData) {
              $backend.setNewNetwork(token, responseData.id, social_network).error(registerTokenError);
            });
            break;
          case 'twitter':
            uri = $backend.endpoint + '/api/oauth/twitter/authorization/' + e.detail.oauth_verifier;
            uri += '?oauth_token=' + e.detail.token;
            $http.get(uri).success(function (responseData) {
              e.detail.userId = responseData.token_id;
              $backend.setNewNetwork(token, responseData.token_id, social_network, e.detail.oauth_verifier).then(function(res){
                $rootScope.user.tokens[social_network] = res.data.token;
                $scope.setToken(social_network, res.data.token);
                $('#login-modal').modal('toggle');
              }, registerTokenError);
            }).error(function () {
              console.log('Problemas al intentar obtener el token_id de un usuario');
            });
            break;
          case 'pinterest':
            break;
          case 'spotify':
            break;
          default:
            $backend.setNewNetwork(token, e.detail.userId, social_network).error(registerTokenError);
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
  })();
}]);
