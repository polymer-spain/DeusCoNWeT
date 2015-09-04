/*global angular, document, window */

angular.module("picbit").controller("UserHomeController", ["$scope", "$timeout", function ($scope, $timeout) {
	"use strict";

	/* Network infomation */
	$scope.toggleHelp = false;
	$scope.twitterData = {};
	$scope.githubData = {};
	$scope.instagramData = {};
	$scope.instagramData.token = "2062815740.34af286.169a9c42e1404ae58591d066c00cb979";
	$scope.twitterData.token = "3072043347-hbcrkzLJfVzTg7BTjgzkKqZx3bbzpYb04IO573x";
	$scope.githubData.username = "mortega5";

	$scope.listComponents = [
		{
			name: "twitter-timeline",
			attributes: {
				accessToken: $scope.twitterData.token,
				secretToken: "VmQX0z3ZWpRv63M92z0SrmmUNGFjNIMZ06iGiJ67kK9oY",
				consumerKey: "J4bjMZmJ6hh7r0wlG9H90cgEe",
				consumerSecret: "8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf",
				endpoint: $scope.domain + "/api/aux/twitterTimeline",
				language: "{{idioma}}",
				count: "200"
			}
		},
		{
			name: "github-events",
			attributes: {
				username: $scope.githubData.username,
				token: $scope.githubData.token || "",
				mostrar: "10",
				language: "{{idioma}}"
			}
		},
		{
			name: "instagram-timeline",
			attributes: {
				accessToken: $scope.instagramData.token,
				endpoint: $scope.domain + "/api/aux/instagramTimeline",
				language: "{{idioma}}"
			}
		}
	];
	$scope.listComponentAdded = []; // added on dragdrop.js
	$scope.modifySelected = $scope.modifySelected || "";
	/* Authentication */

	$scope.menuStatus = false;
	$scope.sort = [false, false, false];
	$scope.showElement = false;
	$scope.listaOpciones = ["false", "false", "false"];

	$scope.showMenu = function () {
		if (!$scope.menuStatus) {
			document.querySelector("#menu-icon").icon = "arrow-forward";
			$scope.menuStatus = true;

			$timeout(function () {
				$scope.showElement = true;
			}, 350);
		} else {
			document.querySelector("#menu-icon").icon = "arrow-back";
			$scope.menuStatus = false;
			$scope.showElement = false;
			$scope.selected = "";
			$scope.showSingle = "";
			$scope.listaOpciones = ["false", "false", "false"];
			document.querySelector("#arrowAdd").icon = "arrow-drop-down";
			document.querySelector("#arrowDelete").icon = "arrow-drop-down";
			document.querySelector("#arrowModify").icon = "arrow-drop-down";

		}
	};

	$scope.ocultar = function (event) {
		switch (event) {
			case "add":
				$scope.listaOpciones = ["true", "false", "false"];
				document.querySelector("#arrowDelete").icon = "arrow-drop-down";
				document.querySelector("#arrowModify").icon = "arrow-drop-down";
				break;
			case "delete":
				$scope.listaOpciones = ["false", "true", "false"];
				document.querySelector("#arrowAdd").icon = "arrow-drop-down";
				document.querySelector("#arrowModify").icon = "arrow-drop-down";
				break;
			case "modify":
				$scope.listaOpciones = ["false", "false", "true"];
				document.querySelector("#arrowAdd").icon = "arrow-drop-down";
				document.querySelector("#arrowDelete").icon = "arrow-drop-down";
				break;
		}
	};

	$scope.setList = function (event) {
		switch(event){
			case "add":
				$scope.listaOpciones = [!$scope.listaOpciones[0], "false", "false"];
				if (!$scope.listaOpciones[0]) {
					document.querySelector("#arrowAdd").icon = "arrow-drop-up";
					document.querySelector("#arrowDelete").icon = "arrow-drop-down";
					document.querySelector("#arrowModify").icon = "arrow-drop-down";
				}
				else {
					document.querySelector("#arrowAdd").icon = "arrow-drop-down";
				}
				break;
			case "delete":
				$scope.listaOpciones = ["false", !$scope.listaOpciones[1], "false"];
				if (!$scope.listaOpciones[1]){
					document.querySelector("#arrowDelete").icon = "arrow-drop-up";
					document.querySelector("#arrowAdd").icon = "arrow-drop-down";
					document.querySelector("#arrowModify").icon = "arrow-drop-down";
				}
				else {
					document.querySelector("#arrowDelete").icon = "arrow-drop-down";
				}
				break;
			case "modify":
				$scope.listaOpciones = ["false", "false", !$scope.listaOpciones[2]];
				if (!$scope.listaOpciones[2]){
					document.querySelector("#arrowModify").icon = "arrow-drop-up";
					document.querySelector("#arrowAdd").icon = "arrow-drop-down";
					document.querySelector("#arrowDelete").icon = "arrow-drop-down";
				}
				else {
					document.querySelector("#arrowModify").icon = "arrow-drop-down";
				}
				break;
		}
	};

	$scope.hidelist = function (event) {
		switch(event){
			case "add":
				return $scope.listaOpciones[0];
			case "delete":
				return $scope.listaOpciones[1];
			case "modify":
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
			$scope.selected = "";
			$scope.showSingle = "";
			if (!$scope.hidelist(event)) {
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
		return !($scope.menuStatus | $scope.isSelected(event));
	};

	$scope.setSort = function(event) {
		switch(event){
			case "add":
				$scope.sort = [!$scope.sort[0], false, false];
				break;
			case "delete":
				$scope.sort = [false, !$scope.sort[1], false];
				break;
			case "modify":
				$scope.sort = [false, false, !$scope.sort[2]];
				break;
		}
	};

	$scope.modifyActive = function(elementName) {
		return elementName === $scope.modifySelected;
	};

	$scope.setModifySelected = function(elementName) {
		$scope.modifySelected = $scope.modifySelected !== elementName ? elementName : "";
	};

	$scope.isModifySelected = function(elementName) {
		return elementName === $scope.modifySelected;
	};

	$scope.deleteTimeline = function(elementName) {
		angular.element(document.querySelector("#container")).find(elementName).remove();
		var index = $scope.listComponentAdded.indexOf(elementName);
		$scope.listComponentAdded.splice(index, 1);
	};

	$scope.deleteTimelineHovered = function(index) {
		$scope.hovered = index;
	};

	$scope.deleteTimelineLeaveHover = function () {
		$scope.hovered = "";
	};

	$scope.showToggleHelp = function (event){
		$scope.toggleHelp = true;
		window.onkeydown = $scope.listenEscKeydown;
		event.stopPropagation();
	};

	$scope.hideToggleHelp = function(event) {
		$scope.toggleHelp = false;
		window.removeEventListener("onkeydown", $scope.listenEscKeydow);
		if (event) {
			event.stopPropagation();
		}
	};

	$scope.listenEscKeydown = function(event){
		$scope.$apply(function() {
			if (event.keyCode === 27) {
				$scope.hideToggleHelp();
			}
		});
	};
}]);
