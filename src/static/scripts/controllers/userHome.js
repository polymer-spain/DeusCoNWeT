angular.module('picbit').controller('UserHomeController', ['$scope', '$timeout','$rootScope','$interval', '$backend','$http', function ($scope, $timeout, $rootScope, $interval,
  $backend, $http) {
    'use strict';
    // Lista de componentes añadidos
    // TODO se deberan coger de la lista que se registra en usuario
    $scope.listComponentAdded = [];

    $scope.showToastr = function(type, message, time){
      toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": time || "5000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
      };
      toastr[type](message);
    };
    // Logica que dice que botones del a barra lateral estan activos y cuales
    // han de desactivarse
    $scope.selectListButton = function(e){
      e.stopPropagation();
      var $target = $(e.currentTarget);
      if ($target.hasClass('active')){
        $target.removeClass('active');
      } else {
        $target.parent().children().removeClass('active');
        $target.addClass('active');
      }

    };
    // TODO se debe coger el catalogo de componentes del servidor
    $scope.catalogList = [
      {
        name:'twitter-timeline',
        rate:5,
        img:'images/components/twitter-logo.png',
        tokenAttr: 'access-token',
        description:'Muestra el timeline de twitter texto muy largo para provocar un overflow y ver que ocurre en la imagen que representa',
        socialNetwork: 'twitter',
        attributes: {
          "access-token": $rootScope.user ? $rootScope.user.tokens.twitter : "3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf",
          "secret-token": "OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock",
          "consumer-key": "J4bjMZmJ6hh7r0wlG9H90cgEe",
          "consumer-secret": "8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf",
          endpoint: $scope.domain + "/api/aux/twitterTimeline",
          component_base: "bower_components/twitter-timeline/static/",
          language: "{{idioma}}",
          count: "200"
        }
      },
      {
        name:'github-events',
        rate:4,
        img:'images/components/github-icon.png',
        socialNetwork:'github',
        tokenAttr: 'token',
        description:'Muestra los eventos sucedidos en github',
        attributes: {
          username: "mortega5",
          token: $rootScope.user ? $rootScope.user.tokens.github:'',
          mostrar: "10",
          language: "{{idioma}}",
          component_directory: 'bower_components/github-events/'
        }
      },
      {
        name:'instagram-timeline',
        rate:1,
        socialNetwork:'instagram',
        img:'images/components/instagram-icon.png',
        description:'Muestra las fotos de Instagram',
        tokenAttr: 'accessToken',
        attributes: {
          accessToken: $rootScope.user? $rootScope.user.tokens.googleplus : '',
          endpoint: "{{domain}}" + "/api/aux/instagramTimeline",
          language: "{{idioma}}"
        }
      },
      {
        name: 'googleplus-timeline',
        rate:4,
        socialNetwork:'googleplus',
        tokenAttr: 'token',
        img:'images/components/google-icon.svg',
        description:'Muestra las entradas en google+',
        attributes: {
          'token': $rootScope.user ? $rootScope.user.tokens.googleplus:'ya29.CjMHAzmtu3cGQaJ77v0nq0xoJ9F_VTNkJWx-mUmQQlyDU4nn8KlTBO3mWyqFw32XTAQofVc',
          'language':'{{idioma}}'
        }
      },
      {
        name: 'facebook-wall',
        rate: 3,
        socialNetwork:'facebook',
        img: 'images/components/facebook-icon.png',
        tokenAttr: 'access_token',
        attributes: {
          language: '{{idioma}}',
          component_directory: 'bower_components/facebook-wall/',
          access_token: $rootScope.user ? $rootScope.user.tokens.facebook: 'NO IMPLEMENTED',
        }
      }
    ];

    // borra los filtros
    $scope.removeStarFilter = function(){
      $scope.starFilter = undefined;
    };
    $scope.removeTextFilter = function(){
      $scope.textFilter = '';
    };
    // Activa la lista de componenes que se pueden borrar
    $scope.activeDelCmpList = function(){
      var $list = $('.component-list');
      if (!$list.hasClass('active')){
        $list.addClass('active');
      } else if($scope.showList === $scope.addedList) {
        $list.removeClass('active');
      }
    };
    // Elimina un componente añadido
    $scope.removeElement = function(id){
      var finded = false;

      for (var i = 0;i< $scope.listComponentAdded.length && !finded;i++){
        if ($scope.listComponentAdded[i].name === id){
          finded = true;
          $scope.listComponentAdded.splice(i,1);

        }
      }
    };

    $scope.blurList = function(e){
      // del activated
      var index = $(e.currentTarget).attr('data-index');
      var id = $scope.listComponentAdded.splice(index,1)[0];
      $scope.showList = $scope.listComponentAdded;
      var element = '[id-element="' + id.name + '"]';
      $(element)[0].setAttribute('disabled',false);
      $(id.name).parent().remove();
    };

    // Cierra las listas cuando se pulsa sobro cualquier otro lado del dashboard
    $('#userHome').click(function(event){
      if (!event.target.hasAttribute('data-button') && !event.target.hasAttribute('data-list')){
        $('.component-list').removeClass('active');
        $('.menu-buttons').children().removeClass('active');
      }
    });

    // Cierra los modales en funcion de cual esté abierto
    $(document).on('keydown', function(e){
      e.stopPropagation();
      if (e.keyCode === 27 && $('#login-modal').is(':visible')){
        $('#login-modal').modal('toggle');
      } else if (e.keyCode === 27 && $('#store-modal').is(':visible')){
        $('#store-modal').modal('toggle');
      }
    });

    //Evita que se cierren los dos modales a la vez
    $('#store-modal').on('hidden.bs.modal',function(){
      if ($('#login-modal').is(':visible')){
        $('#login-modal').modal('toggle');
      }
    });
    // Selecciona que modal tiene que cerrarse en cada momento
    $scope.toggleCatalog = function(){
      if ($('#login-modal').is(':visible')){
        $('#login-modal').modal('toggle');
      }
      $('#store-modal').modal('toggle');
    };


    $scope.setToken = function(socialNetwork, value){
      for(var i = 0; i< $scope.catalogList.length;i++){
        var element = $scope.catalogList[i];
        if (element.socialNetwork === socialNetwork){
          element.attributes[element.tokenAttr] = value;
        }
      }
    };
    $scope.closeModal = function(selector){
      $(selector).modal('toggle');
    };
    $scope.login = function(name){
      $scope.loginSelected = name.split('-')[0];
      $('#login-modal').modal('toggle');
    };

    // Watcher that controls whether the form should be showed to the user or not
    $scope.platformUsedTime = 0;
    $scope.intervalTime = 1000; // We'll update the value of platformUsedTime each $scope.intervalTime milliseconds
    $scope.formLoadTime = 60000; // Indicates when we'll show to the user the form


    var platformTimeHandler = $interval(function(){
      if(document.visibilityState === "visible" ){
        $scope.platformUsedTime += $scope.intervalTime;
      }
    }, $scope.intervalTime);

    $scope.$watch("platformUsedTime", function(newValue, oldValue){
      if (newValue!==oldValue && newValue >= $scope.formLoadTime && $scope.listComponentAdded.length >0) {
        $scope.getRandomComponent();
        $('#rate-modal').modal({
          backdrop: 'static',
          keyboard: false
        });
        $interval.cancel(platformTimeHandler);
      }
    });
    $scope.getRandomComponent = function(){
      if (!$scope.randomComponent){
        var random = Math.round(Math.random()*100);
        if ($scope.listComponentAdded.length > 0){
          var position = random % $scope.listComponentAdded.length;
          $scope.randomComponent = $scope.listComponentAdded[position].name;
        }
      }
      return $scope.randomComponent;
    };
    $scope.submitRating = function(){
      if (!$('#aditionalForm').is(':visible')){
        if ($('#initialQuestion paper-radio-group')[0].selected){
          $('#rate-modal .modal-footer p').hide();
          $scope._submitQuestionaire();
          $('#initialQuestion').fadeOut( "easing", function() {
            $('#aditionalForm').fadeIn('easing', function(){
            });
          });
          console.log('TODO registrar datos en algun lado');
        } else {
          $('#rate-modal .modal-footer p').show();
        }
      } else {
        var $aditionalQuestion = $('.aditionalQuestion');
        $('#rate-modal .modal-footer p').hide();
        var selected = $aditionalQuestion.children('.iron-selected');
        if ( $aditionalQuestion.length === selected.length) {
          $('#rate-modal .modal-footer p').hide();
          $('#rate-modal .modal-footer button').hide();
          $scope._submitExtendedQuestionaire();
          $('#aditionalForm').fadeOut('easing',function(){
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

    $scope._submitQuestionaire = function(){
      var question_id = "initialQuestion";
      var answer = $('#initialQuestion paper-radio-group')[0].selected;
      var question_text = $('#initialQuestion paper-radio-group').children('.iron-selected').html() || "";
      if (answer!== undefined && question_text !== ""){
        //We send an event to Mixpanel
        var properties = {
          "selection": answer,
          "question_type": "obligatory",
          "question": question_text,
          "component": $scope.randomComponent,
          "timestamp": Date.now()
        };
        mixpanel.track(question_id, properties);
      }
    };

    $scope._submitExtendedQuestionaire = function(){
      // We get the responses for every question
      var aditional_questions = document.getElementsByClassName("aditionalQuestion");
      var mixpanel_event_list = [];
      var mixpanel_event = {};
      var answer = "";
      var question_text = "";
      Array.prototype.forEach.call(aditional_questions, function(question){
        answer = question.selected || "";
        question_text = $(question).children('.iron-selected').html() || "";
        if (answer !== "" && question_text !== ""){
          mixpanel_event = {
            "event_name": question.id,
            "selection": answer,
            "question": question_text
          };
          mixpanel_event_list.push(mixpanel_event); // qué hace exactamente el push?
        }
      });
      // We check if the user has anwered all questions
      var mixpanel_properties = {};
      if (mixpanel_event_list.length === aditional_questions.length){
        for (var i = 0; i< mixpanel_event_list.length; i++) {
          // We send the responses to Mixpanel
          mixpanel_event = mixpanel_event_list[i];
          mixpanel_properties = {
            "selection": mixpanel_event.selection,
            "question": mixpanel_event.question,
            "question_type": "optional",
            "component": $scope.randomComponent, // Se manda la versión?
            "timestamp": Date.now()
          };
          mixpanel.track(mixpanel_event.event_name, mixpanel_properties);
          // We hide the user form
        }
      }
    };


    // Callback when login finish
    (function(){
      function loginCallback(e){
        //falta registralo
        $scope.$apply(function(){
          var socialNetwork = e.detail.redSocial;
          var token = e.detail.token;
          var registerTokenError = function(){
            $scope.showToastr('error',$scope.language.add_token_error);
            $rootScope.user.tokens[socialNetwork] = '';
            $scope.setToken(socialNetwork, '');
          };
          $rootScope.user = $rootScope.user || {tokens:{}};
          $rootScope.user.tokens[socialNetwork] = token;
          $scope.setToken(socialNetwork, token);
          $('#login-modal').modal('toggle');

          // switch(socialNetwork) {
          //   case 'googleplus':
          //     var uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + token;
          //     $http.get(uri).success(function (responseData) {
          //       $backend.addTokens(socialNetwork, responseData.id, token, $scope.user.user_id).error(registerTokenError);
          //     });
          //     break;
          //   case 'twitter':
          //     uri = $backend.endpoint + '/api/oauth/twitter/authorization/' + e.detail.oauth_verifier;
          //     $http.get(uri).success(function (responseData) {
          //       e.detail.userId = responseData.token_id;
          //       $backend.addTokens(socialNetwork, responseData.token_id, token, $scope.user.user_id).error(registerTokenError);
          //     }).error(function() {
          //       console.log('Problemas al intentar obtener el token_id de un usuario' );
          //     });
          //     break;
          //   default:
          //     $backend.addTokens(socialNetwork, e.datail.userId, token, $scope.user.user_id).error(registerTokenError);
          //     break;
          // }
        });
      }
      $('#login-modal google-login')[0].addEventListener('google-logged', loginCallback);
      $('#login-modal github-login')[0].addEventListener('github-logged', loginCallback);
      $('#login-modal instagram-login')[0].addEventListener('instagram-logged', loginCallback);
      $('#login-modal twitter-login')[0].addEventListener('twitter-logged', loginCallback);
      $('#login-modal login-facebook')[0].addEventListener('facebook-logged', loginCallback);
    })();
  }]);
