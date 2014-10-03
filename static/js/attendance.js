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

  app.factory("Attendance", function($resource) {
    return $resource("/attendance/:id", { id: '@dev' }, {
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

  app.controller('DevDetailController', function($state, $stateParams, Developer, Team, Attendance){
    controller = this;
    controller.dev = Developer.get({id: $stateParams.id});
    controller.presence = Attendance.get({id: $stateParams.id});
    Team.query(function(data) {
      controller.teams = data;
    });

    controller.update = function(form, dev) {
      form.$setPristine();
      dev.$update();
    };

    controller.here = function(presence) {
      presence.here = !presence.here;
      presence.$update();
    };

    controller.back = function(form) {
      if (form.$dirty) {
        alert("Whoah. Save your changes first.");
      } else {
        $state.go('dev_list');
      }
    }
  });
})();
