/*global angular */

angular.module("picbit")
  .controller("AboutController", ["$scope", "$routeParams", "$timeout", function($scope, $routeParams, $timeout) {
    "use strict";

    $scope.members = [
      {
        'name': 'Juan Francisco Salamanca',
        'github': 'https://github.com/JuanFryS',
        'studies': 'Computer Science',
        'img': '../../images/juanfran.jpg'
      },
      {
        'name': 'Sandra Gomez',
        'github': 'https://github.com/sandragyaguez',
        'studies': 'Computer Science',
        'img': '../../images/sandra.png'
      },
      {
        'name': 'Luis Ruiz',
        'github': 'https://github.com/lruizr',
        'studies': 'Computer Science',
        'img': '../../images/luis.jpg'
      },
      {
        'name': 'Ana Isabel Lopera',
        'github': 'https://github.com/ailopera',
        'studies': 'Computer Science',
        'img': '../../images/ana.jpg'
      },
      {
        'name': 'Miguel Ortega',
        'github': 'https://github.com/Mortega5',
        'studies': 'Computer Science',
        'img': '../../images/miguel.jpg'
      },
      {
        'name': 'David Lizcano',
        'github': '',
        'studies': 'profesor doctor en UDIMA',
        'img': '../../images/david.png'
      },
      {
        'name': 'Andrés Leonardo Martínez',
        'github': 'https://github.com/almo',
        'studies': 'Google Software department',
        'img': '../../images/andres.jpg'
      },
      {
        'name': 'Genoveva Lopez',
        'github': '',
        'studies': 'profesora doctor en UPM',
        'img': '../../images/geno.png'
      }
    ];
  }]);
