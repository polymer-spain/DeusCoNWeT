angular.module('picbit').controller('FormCtrl', ['$scope', '$timeout', '$rootScope', '$interval', function ($scope, $timeout, $rootScope, $interval) {

  // Watcher that controls whether the form should be showed to the user or not
  $scope.platformUsedTime = 0;
  $scope.intervalTime = 1000; // We'll update the value of platformUsedTime each $scope.intervalTime milliseconds
  $scope.formLoadTime = 6000; // Indicates when we'll show to the user the form
  $scope.unRatedComponents = [];
  $scope.ratedComponents = [];
  $scope.rating = false;

  var platformTimeFunction = function () {
    var interval = $interval(function () {
      if (document.visibilityState === "visible" && $scope.unRatedComponents.length > 0) {
        $scope.$apply(function () {
          $scope.platformUsedTime += $scope.intervalTime;
        })
      }
    }, $scope.intervalTime, 0, false);
    return interval;
  }.bind(this);

  $scope.$watch("platformUsedTime", function (newValue, oldValue) {
    if (newValue >= $scope.formLoadTime) {
      // cancel interval and remove it
      $interval.cancel($scope.platformTimeHandler);
      $scope.platformTimeHandler = undefined;
      $scope.platformUsedTime = 0;
      $scope.rating = true;
      // Get the component that will be rated
      var componentRating = $scope.getRandomComponent();
      if (componentRating) {
        $scope.$broadcast("ratingComponent", { componentRating: componentRating })

        var text = $scope.language.survey + " " + componentRating;
        var options = {
          "closeButton": true,
          "showDuration": "0",
          "hideDuration": "0",
          "timeOut": "0",
          "extendedTimeOut": "0",
        }
        $scope._rating = true;

        // Request user rating
        $scope.showToastr('info', text, options, function () {
          $scope._rating = true;
          $('#rate-modal').modal({
            backdrop: 'static',
            keyboard: false
          });
        }, $scope.closeForm);
      }
    }
  });

  $scope.getRandomComponent = function () {
    var random = Math.round(Math.random() * 100);
    if ($scope.unRatedComponents.length > 0) {
      var position = random % $scope.unRatedComponents.length;
      $scope.randomComponent = $scope.unRatedComponents[position];
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

  // Send data to 
  $scope.submitRating = function () {

    if (!$('#aditionalForm').is(':visible')) {
      if ($('#initialQuestion paper-radio-group')[0].selected) {
        $('#rate-modal .modal-footer p').hide();
        $scope._submitQuestionaire();
        $('#initialQuestion').fadeOut("easing", function () {
          $('#aditionalForm').fadeIn('easing', function () { });
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
      $scope.$broadcast("formCompleted", { id: question_id, properties: properties });
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
        $scope.$broadcast("formCompleted", { id: mixpanel_event.event_name, properties: mixpanel_properties });
        mixpanel.track(mixpanel_event.event_name, mixpanel_properties);
        // We hide the user form
      }
    }
    var index = $scope.unRatedComponents.indexOf($scope.randomComponent);
    // Remove element from unrated
    if (index == -1) {
      console.error("El elemento valorado no existe en la lista de no valorados")
    } else {
      $scope.unRatedComponents.splice(index, 1);
    }

    $scope.ratedComponents.push($scope.randomComponent);
  };
  $scope.closeForm = function () {
      $scope.randomComponent = undefined;
      $scope.rating = false;
      // Reset modal
      resetModal();
      // if there are components unrated, set interval
      if ($scope.unRatedComponents.length > 0) {
        $scope.platformTimeHandler = platformTimeFunction();
      }
  };

  $scope.$on("componentAdded", function (e, data) {
    console.log("Se añadio un componente", data);
    var isNotInUnrated = $scope.unRatedComponents.indexOf(data.name) === -1;
    var isNotInRated = $scope.ratedComponents.indexOf(data.name) === -1;
    // Check if new component is neither in unrated nor rated
    if (isNotInUnrated && isNotInRated) {
      
      $scope.$apply(function () {
        if (!$scope.rating && $scope.platformTimeHandler == undefined){
          $scope.platformTimeHandler = platformTimeFunction();
        }

        $scope.unRatedComponents.push(data.name)

      })
    }
  })
}]);