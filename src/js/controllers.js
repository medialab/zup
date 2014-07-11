angular.module('zup.controllers', [])
  /*
    
    The very main controller. 
    ===
  */
  .controller('zupCtrl', ['$scope', 'ToastFactory', function($scope, ToastFactory) {
    ToastFactory.toast('ciao');
    
  }])