(function(){
  var app = angular.module('ng-attendance', ['ngResource', 'ui.router']);

  app.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/");

    $stateProvider
      .state('dev_list', {
        url: "/",
        templateUrl: '/static/html/dev_list.html',
        controller: 'DevListController',
        controllerAs: 'dev_list'
      })
      .state('dev_detail', {
        url: '/:id',
        templateUrl: '/static/html/dev_detail.html',
        controller: 'DevDetailController',
        controllerAs: 'dev_detail'
      });
  });

  app.factory("Developer", function($resource) {
    return $resource("/devs/:id", { id: '@id' }, {
      update: {
        method: 'PUT'
      }
    });
  });

  app.factory("Team", function($resource) {
    return $resource("/teams");
  });

  app.controller('DevListController', function(Developer){
    controller = this;
    Developer.query(function(data) {
      controller.devs = data;
    });
  });

  app.controller('DevDetailController', function($stateParams, Developer, Team){
    controller = this;
    controller.dev = Developer.get({id: $stateParams.id});
    Team.query(function(data) {
      controller.teams = data;
    });
  });
})();
