(function(){
  var app = angular.module('ng-attendance', ['ngResource', 'ui.router']);

  app.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/");

    $stateProvider
      .state('home', {
        url: "/",
        templateUrl: '/static/html/home.html',
        controller: 'HomeController',
        controllerAs: 'home'
      })
      .state('dev_create', {
        url: "/new/",
        templateUrl: '/static/html/dev_create.html',
        controller: 'DevCreateController',
        controllerAs: 'dev_create'
      })
      .state('dev_list', {
        url: "/devs/",
        templateUrl: '/static/html/dev_list.html',
        controller: 'DevListController',
        controllerAs: 'dev_list'
      })
      .state('dev_detail', {
        url: '/devs/:id',
        templateUrl: '/static/html/dev_detail.html',
        controller: 'DevDetailController',
        controllerAs: 'dev_detail'
      });
  });

  app.filter( 'default', function( $filter ) {
    return function( input, defaultValue ) {
      if ( !input ) return defaultValue;
      return input;
    };
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

  app.controller('HomeController', function(Developer){
    controller = this;
  });

  app.controller('DevCreateController', function($state, Developer, Team) {
    controller = this;

    Team.query(function(data) {
      controller.teams = data;
    });

    controller.save = function(form, dev) {
      if (form.$valid) {
        var d = new Developer(dev);
        d.$save();
        $state.go('dev_list');
      }
    }
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
