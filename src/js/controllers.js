const JOB_GET_PENDING = 'JOB_GET_PENDING';
const JOB_CREATED = 'JOB_CREATED';
const JOB_LOADED = 'JOB_LOADED';
const JOB_RUNNING = 'JOB_RUNNING';


angular.module('zup.controllers', ['ngCookies', 'ui.codemirror'])
  /*
    
    The very main controller. 
    ===
  */
  .controller('zupCtrl', ['$scope', '$rootScope', '$log', 'JobsFactory', 'ToastFactory', function($scope, $rootScope, $log, JobsFactory, ToastFactory) {
    //ToastFactory.toast('ciao');
    $scope.job = {};


    $scope.save = function() {
      if($scope.job.id) {


      } else {
        JobsFactory.save($scope.job, function(data) {
          console.log(data);
          ToastFactory.toast('url list saved, starting ...');
    
          $scope.job = data.object;
          // start listening
          $rootScope.$emit(JOB_CREATED, $scope.job.id);
        })
      }
    };

    $scope.download = function(job) {
      window.open(location.pathname + 'api/job/' + job.id + '/download', '_blank', '');
    }


    $rootScope.$on(JOB_GET_PENDING, function(e, pending_job_ids){
      $log.info('zupCtrl @JOB_GET_PENDING', pending_job_ids);
      var last_job_id = pending_job_ids.pop();
      if(!isNaN(parseFloat(last_job_id)) && isFinite(last_job_id))
        $rootScope.$emit(JOB_LOADED, last_job_id);

    });

    $rootScope.$on(JOB_RUNNING, function(e, job){
      $log.info('zupCtrl @JOB_RUNNING', job);
      $scope.job = job;
    });

    $log.info('zupCtrl loaded');
  }])

  .controller('jobCtrl', ['$scope', '$rootScope', '$log', '$timeout', 'JobFactory', function($scope, $rootScope, $log, $timeout, JobFactory){
    $scope.job_id = 0; // we keep the id separated, because ... i do not know
    $scope.job = {};
    $scope.listening = false;


    function tick() {
      JobFactory.query({id: $scope.job_id}, function(data){
        console.log(data);
        $timeout(tick, 3617);
        $rootScope.$emit(JOB_RUNNING, data.object);
      }, function(data){
        $log.info('ticking error',data); // status 500 or 404 or other stuff
        $timeout(tick, 3917);
      }); /// todo HANDLE correctly connection refused
    };


    $rootScope.$on(JOB_CREATED, function(e, id){
      $log.info('jobCtrl @JOB_CREATED', id);
      $scope.job_id = id;
      !$scope.listening && tick();
      $scope.listening = true;
    });


    $rootScope.$on(JOB_LOADED, function(e, id){
      $log.info('jobCtrl @JOB_LOADED', id);
      $scope.job_id = id;
      !$scope.listening && tick();
      $scope.listening = true;
    });

    $log.info('jobCtrl loaded');
  }])

  .controller('pendingCtrl', ['$scope', '$rootScope', '$log', '$cookies', function($scope, $rootScope, $log, $cookies) {
    $scope.pendings = $cookies.pendings? $cookies.pendings.split(','): [];

    $rootScope.$on(JOB_CREATED, function(e, id){
      $log.info('pendingCtrl @JOB_CREATED');
      $scope.pendings.push(id);
      $cookies.pendings = $scope.pendings.join('').split('').join(',');
    });

    $log.info('pendingCtrl loaded. pendings:', $scope.pendings );
    // $rootScope.$emit(JOB_GET_PENDING, angular.copy($scope.pendings));
  }])