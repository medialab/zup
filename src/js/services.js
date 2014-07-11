'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('zup.services', ['ngResource', ])//'ngAnimate'])
  /*
    sample toast function to enable message notification.
    It needs jquerytoastmessage jquery lib to work properly.
    Waiting for an angular version.
  */
  .factory('ToastFactory', function() {
    return {
      toast: function(message, title, options){
        if(!options){
          options={}
        };
        if(typeof title=="object"){
          options=title;
          title=undefined;
        }

        if(options.cleanup!=undefined)
          $().toastmessage("cleanToast");
        var settings=$.extend({
          text: "<div>"+(!title?"<h1>"+message+"</h1>":"<h1>"+title+"</h1><p>"+message+"</p>")+"</div>",
          type: "notice",
          position: "bottom-right",
          inEffectDuration: 200,
          outEffectDuration: 200,
          stayTime: 1900
        },options);

        $().toastmessage("showToast", settings);
      }
    };
  });