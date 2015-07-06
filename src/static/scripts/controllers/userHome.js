/*global angular, document */


/**
 * @ngdoc function
 * @name polymerGeneratedAppApp.controller:SandboxCtrl
 * @description
 * # SandboxCtrl
 * Controller of the polymerGeneratedAppApp
 */

angular.module("picbit").controller("UserHomeController", function ($scope, $timeout) {
  "use strict";
  /* Network infomation */
  $scope.twitter = {};
  $scope.github = {};
  $scope.instagram = {};
  $scope.instagram.token = "2062815740.34af286.169a9c42e1404ae58591d066c00cb979";
  $scope.twitter.token = "3072043347-hbcrkzLJfVzTg7BTjgzkKqZx3bbzpYb04IO573x";
  $scope.github.username = "mortega5";

  $scope.list = [
    {
      name: "twitter-timeline",
      attributes: {
        accessToken: $scope.twitter.token,
        secretToken: "VmQX0z3ZWpRv63M92z0SrmmUNGFjNIMZ06iGiJ67kK9oY",
        consumerKey: "J4bjMZmJ6hh7r0wlG9H90cgEe",
        consumerSecret: "8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf",
        endpoint: $scope.domain + "/api/oauth/twitterTimeline",
        language: "{{idioma}}",
        count: "200"
      }
    },
    {
      name: "github-events",
      attributes: {
        username: $scope.github.username,
        token: $scope.github.token || "",
        mostrar: "10",
        language: "{{idioma}}"
      }
    },
    {
      name: "instagram-timeline",
      attributes: {
        accessToken: $scope.instagram.token,
        endpoint: $scope.domain + "/api/aux/instagramTimeline",
        language: "{{idioma}}"
      }
    }
  ];



  /* Authentication */

  $scope.menuStatus = false;
  $scope.showElement = false;
  $scope.listaOpciones = ["false", "false", "false"];

  $scope.showMenu = function(){
    if (!$scope.menuStatus){
      document.querySelector("#menu-icon").icon = "arrow-forward";
      $scope.menuStatus = true;

      $timeout(function(){
        $scope.showElement = true;
      }, 350);
    }
    else {
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

  $scope.ocultar = function(event){
    switch(event){
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

  $scope.setList = function(event) {
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

  $scope.hidelist = function(event) {
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
  $scope.isSelected = function(event) {
    return $scope.selected === event && event !== undefined;
  };

  $scope.setSelected = function(event) {
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
});
