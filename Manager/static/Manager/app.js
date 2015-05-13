var app = angular.module('manager',['ngSanitize']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
    });

    //
    //app.factory('locations', function($http) {
    //  var promise = null;
    //
    //  return function() {
    //    if (promise) {
    //      // If we've already asked for this data once,
    //      // return the promise that already exists.
    //      return promise;
    //    } else {
    //      promise = $http.get('{% static 'Manager/riotdatabase.json' %}');
    //      return promise;
    //    }
    //  };
    //});
    //
    //app.controller('SomeController', function($scope, locations) {
    //  locations().success(function(data) {
    //     $scope.locations = data;
    //  });
    //});

    app.controller('FormsCtrl', ['$scope','$http', '$sce', '$compile', function($scope, $http, $sce,$compile){
        $scope.data_file = "hola";
        $scope.is_visible = false;
        $scope.load_form = function (url){
            $scope.is_visible = true;
            $http({
                method: 'GET',
                url: url
            })
            .success(function(data, status, headers, config){
                $scope.html = data;
                $scope.form_html = $sce.trustAsHtml($scope.html);
            })
            .error(function(data, status, headers, config){
                $scope.html = data;
                $scope.form_html = $sce.trustAsHtml($scope.html);
            })
        };
    }]);

    app.controller('FormController', function($scope) {

        $scope.pw1='';
        $scope.pw2='';
        $scope.$watchGroup(['pw1', 'pw2'], function (value) {
            if (value[0] == value[1]) {
                $scope.are_equals=true;
            } else {
                $scope.are_equals=false;
            }
        });
    });
