'use strict';
angular.module('zup', [
  'ngRoute',
  'zup.controllers',
  'zup.services'
])
.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider, $cookies) {
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';

  $httpProvider.responseInterceptors.push(['$q','$log', function($q, $log) {
    return function(promise) {
      return promise.then(function(response) {
        response.data.extra = 'Interceptor strikes back';
        if(response.data.meta && response.data.meta.warnings){ // form error from server!
          // if(response.data.meta.warnings.invalid && response.data.meta.warnings.limit):
          // exceute, but send a message
          $log.info('warnings',response.data.meta.warnings);
          // return $q.reject(response);
        }
        return response; 
      }, function(response) { // The HTTP request was not successful.
        if (response.status === 401) {
          response.data = { 
            status: 'error', 
            description: 'Authentication required, or TIMEOUT session!'
          };
          return response;
        }
        return $q.reject(response);
      });
    };
  }]);
}]);