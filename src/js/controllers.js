const JOB_CREATED= 'JOB_CREATED';
const JOB_RUNNING= 'JOB_RUNNING';

angular.module('zup.controllers', ['ui.codemirror'])
  /*
    
    The very main controller. 
    ===
  */
  .controller('zupCtrl', ['$scope', '$rootScope', '$log', 'JobsFactory', 'ToastFactory', function($scope, $rootScope, $log, JobsFactory, ToastFactory) {
    ToastFactory.toast('ciao');
    $scope.job = {};

    $scope.save = function() {
      if($scope.job.id) {


      } else {
        JobsFactory.save($scope.job, function(data) {
          console.log(data);
          alert('saved babe');
          $scope.job = data.object;
          // start listening
          $rootScope.$emit(JOB_CREATED, $scope.job.id);
        })
      }
    };


    $rootScope.$on(JOB_RUNNING, function(e, job){
      $log.info('@JOB_RUNNING', job);
      $scope.job = job;
    });
    $log.info('zupCtrl loaded');
  }])

  .controller('jobCtrl', ['$scope', '$rootScope', '$log', '$timeout', 'JobFactory', function($scope, $rootScope, $log, $timeout, JobFactory){
    $scope.job_id = 0; // we keep the id separated, because ... i do not know
    $scope.job = {};
    $scope.listening = false;


    $rootScope.$on(JOB_CREATED, function(e, id){
      $log.info('jobCtrl @JOB_CREATED');
      $scope.job_id = id;

      if(!$scope.listening){
        (function tick() {
          JobFactory.query({id: $scope.job_id}, function(data){
            console.log(data);
            $timeout(tick, 3617);
            //Is job running?
            // $rootScope.$emit(JOB_RUNNING, data.object);
          }, function(data){
            $log.info('ticking error',data);
            // status 500 or 404 or other stuff
            $timeout(tick, 3917);
          }); /// todo connection refused
        })();
      };

      $scope.listening = true;
    });
    
    
    (function mock_tick() {
          JobFactory.query({id: 29}, function(data){
            console.log(data);
            //$timeout(mock_tick, 3617);

            var job = data.object;
            $rootScope.$emit(JOB_RUNNING, data.object);
            //Is job running?
            // $rootScope.$emit(JOB_RUNNING, data.object);
          }, function(data){
            $log.info('mock_ticking error',data);
            // status 500 or 404 or other stuff
            //$timeout(mock_tick, 3917);
          }); /// todo connection refused
        })();
    

    $log.info('jobCtrl loaded');
  }])