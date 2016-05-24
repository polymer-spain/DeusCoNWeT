angular.module('picbit').controller('UserHomeController', ['$scope', '$timeout','$rootScope', '$interval', function ($scope, $timeout, $rootScope, $interval) {
	'use strict';

	/* Network infomation */
	$scope.toggleHelp = false;
	$scope.twitterData = {};
	$scope.githubData = {};
	$scope.instagramData = {};
	$scope.facebookData = {};

	$scope.instagramData.token = '2062815740.34af286.169a9c42e1404ae58591d066c00cb979';
	$scope.twitterData.token = 'GITHUB-TOKEN';
	$scope.githubData.username = 'mortega5';

	$scope.listComponents = [
		{
			name: 'facebook-wall',
			attributes: {
				language: '{{idioma}}',
				component_directory: 'bower_components/facebook-wall/',
				access_token: $rootScope.registerToken
			}
		},
		{
			name: 'twitter-timeline',
			attributes: {
				'access-token': $scope.twitterData.token,
				'secret-token': 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock',
				'consumer-key': 'J4bjMZmJ6hh7r0wlG9H90cgEe',
				'consumer-secret': '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf',
				'endpoint': $scope.domain + '/api/aux/twitterTimeline',
				'language': '{{idioma}}',
				'count': 200,
				'component_base': 'bower_components/twitter-timeline/static/'

			}
		},
		{
			name: 'github-events',
			attributes: {
				username: $scope.githubData.username,
				token: '' || '',
				mostrar: '10',
				language: '{{idioma}}',
				component_directory: 'bower_components/github-events/'
			}
		},
		{
			name: 'instagram-timeline',
			attributes: {
				'access-token': $scope.instagramData.token,
				endpoint: $scope.domain + '/api/aux/instagramTimeline',
				language: '{{idioma}}',
				component_directory: 'bower_components/instagram-timeline/static/'
			}
		}
	];
	$scope.listComponentAdded = []; // added on dragdrop.js
	$scope.modifySelected = $scope.modifySelected || '';
	/* Authentication */

	$scope.menuStatus = false;
	$scope.sort = [false, false, false];
	$scope.showElement = false;
	$scope.listaOpciones = [false, false, false];

	$scope.showMenu = function () {
		if (!$scope.menuStatus) {
			document.querySelector('#menu-icon').icon = 'arrow-forward';
			$scope.menuStatus = true;

			$timeout(function () {
				$scope.showElement = true;
			}, 350);
		} else {
			document.querySelector('#menu-icon').icon = 'arrow-back';
			$scope.menuStatus = false;
			$scope.showElement = false;
			$scope.selected = '';
			$scope.showSingle = '';
			$scope.listaOpciones = [false, false, false];

			// Develop has commented them
			document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
			document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
			//document.querySelector('#arrowModify').icon = 'arrow-drop-down';


		}
	};

	$scope.ocultar = function (event) {
		$scope.listaOpciones = [false, false, false];
		switch (event) {
			case 'add':
				document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
				//document.querySelector('#arrowModify').icon = 'arrow-drop-down';
				break;
			case 'delete':
				document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
				//document.querySelector('#arrowModify').icon = 'arrow-drop-down';
				break;
			case 'modify':
				document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
				document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
		}
	};
	$scope.setList = function (event) {
		switch(event){
			case 'add':
				$scope.listaOpciones = [!$scope.listaOpciones[0], false, false];
				if (!$scope.listaOpciones[0]) {
					document.querySelector('#arrowAdd').icon = 'arrow-drop-up';
					document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
					//document.querySelector('#arrowModify').icon = 'arrow-drop-down';
				}
				else {
					document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
				}
				break;
			case 'delete':
				$scope.listaOpciones = [false, !$scope.listaOpciones[1], false];
				if (!$scope.listaOpciones[1]){
					document.querySelector('#arrowDelete').icon = 'arrow-drop-up';
					document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
					//document.querySelector('#arrowModify').icon = 'arrow-drop-down';
				}
				else {
					document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
				}
				break;
			case 'modify':
				$scope.listaOpciones = [false, false, !$scope.listaOpciones[2]];
				if (!$scope.listaOpciones[2]){
					//document.querySelector('#arrowModify').icon = 'arrow-drop-up';
					document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
					document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
				}
				else {
					//document.querySelector('#arrowModify').icon = 'arrow-drop-down';
				}
				break;
		}
	};

	$scope.showlist = function (event) {
		switch(event){
			case 'add':
				return $scope.listaOpciones[0];
			case 'delete':
				return $scope.listaOpciones[1];
			case 'modify':
				return $scope.listaOpciones[2];
			default:
				return false;
		}
	};

	$scope.isSelected = function (event) {
		return $scope.selected === event && event !== undefined;
	};

	$scope.setSelected = function (event) {
		if ($scope.selected === event){
			$scope.selected = '';
			$scope.showSingle = '';
			if ($scope.showlist(event)) {
				$scope.setList(event);
			}
		}
		else {
			$scope.selected = event;
			$timeout(function(){
				$scope.showSingle = event;
			}, 350);
		}
	};

	$scope.isMenuHidden = function(event) {
		return !($scope.menuStatus || $scope.isSelected(event));
	};

	$scope.setSort = function(event) {
		switch(event){
			case 'add':
				$scope.sort = [!$scope.sort[0], false, false];
				break;
			case 'delete':
				$scope.sort = [false, !$scope.sort[1], false];
				break;
			case 'modify':
				$scope.sort = [false, false, !$scope.sort[2]];
				break;
		}
	};

	$scope.setModifySelected = function(elementName) {
		$scope.modifySelected = $scope.modifySelected !== elementName ? elementName : '';
	};

	$scope.isModifySelected = function(elementName) {
		return elementName === $scope.modifySelected;
	};

	$scope.deleteTimeline = function(elementName) {
		angular.element(document.querySelector('#container')).find(elementName).remove();
		var index = $scope.listComponentAdded.indexOf(elementName);
		$scope.listComponentAdded.splice(index, 1);
	};

	$scope.showToggleHelp = function (e){
		var element = e.target;
		var id = element.getAttribute('data-dialog') || element.parentElement.getAttribute('data-dialog');
		var dialog = document.getElementById(id);
		if (dialog) {
			dialog.open();
		}
	};

	// ng-click functions of user forms
	$scope._submitRating = function(event){
		var question_id = "initialQuestion";
		var answer = document.getElementById(question_id).selected;
		var question_text = document.getElementById(question_id).getElementsByClassName("questionText")[0].innerHTML || "";
		if (answer!= undefined && question_text != ""){
			//We send an event to Mixpanel
			var properties = {"selection": answer, 
												"question_type": "obligatory",
												"question": question_text,
												"component": $scope.randomComponent
											 };
			mixpanel.track(question_id, properties);
			document.getElementById("initialQuestionaire").hidden = true;
			document.getElementById("continueMenu").removeAttribute("hidden");
		}
	}

	$scope._action = function(action){
		if (action=='yes'){
			document.getElementById("continueMenu").hidden = true;
			document.getElementById("aditionalForm").removeAttribute("hidden");
		}else
			document.getElementById("continueMenu").hidden = true;
	}

	$scope._submitExtendedQuestionaire = function(){
		// We get the responses for every question
		var aditional_questions = document.getElementsByClassName("aditionalQuestion");
		var mixpanel_event_list = [];
		var mixpanel_event = {};
		var answer = "";
		var question_text = "";
		Array.prototype.forEach.call(aditional_questions, function(question){
			answer = document.getElementById(question.id).selected || "";
			question_text = document.getElementById(question.id).getElementsByClassName("questionText")[0].innerHTML || "";
			if (answer!= "" && question_text != ""){
				mixpanel_event = {"event_name": question.id,
													"selection": answer,
													"question": question_text };
				mixpanel_event_list.push(mixpanel_event);
			}
		});
		// We check if the user has anwered all questions     
		var mixpanel_properties = {};
		if (mixpanel_event_list.length == aditional_questions.length){
			for (var i = 0; i< mixpanel_event_list.length; i++) {
				// We send the responses to Mixpanel
				mixpanel_event = mixpanel_event_list[i]
				mixpanel_properties = {"selection": mixpanel_event.selection,
															 "question": mixpanel_event.question,
															 "question_type": "optional"};
				mixpanel.track(mixpanel_event.event_name, mixpanel_properties);
				// We hide the user form
				document.getElementById("aditionalForm").hidden = true;
				document.getElementById("ThanksDialog").removeAttribute("hidden");    
			} 
		}
	}

	$scope._hideEndDialog = function() {
		document.getElementById("ThanksDialog").hidden = true;
	}

	// Watcher that controls whether the form should be showed to the user or not
	$scope.platformUsedTime = 0;
	$scope.intervalTime = 1000; // We'll update the value of platformUsedTime each $scope.intervalTime milliseconds
	$scope.formLoadTime = 30000; // Indicates when we'll show to the user the form
	$scope.$watch("platformUsedTime", function(newValue, oldValue){
		if (newValue!==oldValue && newValue >= $scope.formLoadTime && $scope.listComponentAdded.length > 0) {
			document.getElementById("initialQuestionaire").removeAttribute("hidden");
			$interval.cancel(platformTimeHandler);
		}
	});
	$scope.getRandomComponent = function(){
		if (!$scope.randomComponent){
			var random = Math.round(Math.random()*100);
			if ($scope.listComponentAdded.length > 0){
				var position = random % $scope.listComponentAdded.length;
				$scope.randomComponent = $scope.listComponentAdded[position];
			}
		}
		return $scope.randomComponent;
	}

	var platformTimeHandler = $interval(function(){
		if(document.visibilityState === "visible" ){
			$scope.platformUsedTime += $scope.intervalTime;
		}
	}, $scope.intervalTime);

}]);
