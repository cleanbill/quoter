// declare a module
var quoter = angular.module('change', ['ui.bootstrap']);

quoter.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

quoter.directive("ad", function() {
    return {
	restrict: 'E',
        transclude: true,
        controller: AlterCtrl,
        template:"<a class='huge' ng-click=\"addSection($index)\">+</a>&nbsp;<a ng-click=\"deleteSection($index)\" class='huge' >-</a>&nbsp;<a class='huge' ng-click=\"changeSection(section)\">></a>"
    }
});

quoter.directive("ads", function() {
    return {
	restrict: 'E',
        transclude: true,
        controller: AlterCtrl,
        template:"<a class='huge text-right' ng-click=\"addSub(section,$index)\">+</a>&nbsp;<a ng-click=\"deleteSub(section,$index)\" class='huge' >-</a>&nbsp;<a class='huge' ng-click=\"changeSub(sub)\">></a>"
    }
});

quoter.directive("totals",function() {
    return {
	restrict: 'E',
        controller: AlterCtrl,
        link: function($scope){
             var totals = {};
             for (var i=0; i < quote.sections.length;i++){
		 if (quote.sections[i].state === 'sub'){
                     for (var x=0; x < quote.sections[i].subs.length; x++){
                            if (quote.sections[i].subs[x].state == 'total'){
                                 var current = totals[quote.sections[i].subs[x].name];
				 if (typeof current === "undefined") {
                                     current = quote.sections[i].subs[x].total;
                                 } else {
                                     current = current + quote.sections[i].subs[x].total;
                                 }
                                 totals[quote.sections[i].subs[x].name] = current;
                            }
                     }
                 }
            }   
            
            $scope.totalTitles = Object.keys(totals);
            $scope.totalTotals = totals
            
        },
        template:"<div class='row-fluid' ng-repeat='tt in totalTitles'><b>{[{tt}]} £{[{ totalTotals[tt] }]}</b></div>"
    }
});


function AlterCtrl($scope){
  $scope.quote = quote;
  $scope.changeSection = function(section){
       if (section.state === 'desc'){
          section.state = 'sub';
          if (!section.subs){
              section.subs  = [{"name":"","desc":"","state":"sub-desc"}];
          }
       } else {
          section.state = 'desc';
       }
  };
  $scope.addSection = function(index){
        quote.sections.splice(index+1, 0, {"name":"","desc":"","state":"desc"});
  };
  $scope.deleteSection = function($index) {
        quote.sections.splice($index,1);
  };
  $scope.changeSub = function(sub){
       if (sub.state === 'sub-desc'){
          sub.state = 'total';
       } else {
          sub.state = 'sub-desc';
       }
  }; 
  $scope.addSub = function(section,index){
        section.subs.splice(index+1, 0, {"name":"","desc":"","state":"sub-desc"});
  };
  $scope.deleteSub = function(section,index){
       section.subs.splice(index,1);
  };
}
quoter.controller("alterCtrl",AlterCtrl);

function TypeaheadCtrl($scope){
  $scope.selected = undefined;
  $scope.init = function(data)
  {
    $scope.elements = data;
  };
}

