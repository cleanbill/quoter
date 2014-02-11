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

function AlterCtrl($scope){
  $scope.quote = quote;
  $scope.isTotal = function(sub){
      return sub.state === 'total';
  };
  var totalOfSection = function(section,name){
    var total = 0;
      if (section.state === 'sub'){
        section.subs.forEach(function(sub){
          if (sub.state === 'total' && sub.name === name && sub.total > 0 ){
            total = total + parseInt(sub.total);
          }
        });
      }
    return total;
  }
  var totalOf = function(name){
    var total = 0;
    $scope.quote.sections.forEach(function(section){
      total = total + totalOfSection(section,name);
    });
    return total;
  }
  $scope.subtotal = function(section,sub,clear){
    if (clear){
      $scope.totals ={};
    }
    var current = $scope.totals[sub.name];
    if (typeof current === "undefined") {
      current = totalOfSection(section,sub.name);
      $scope.totals[sub.name] = current;
      if (current > 0){
        return sub.name+" £"+current;
      }
    }
    return "";
  }

  $scope.cleargrandtotal = function(clear){
    if (clear){
      $scope.gtotals ={};
    }
  }
  $scope.grandtotal = function(sub){
    var current = $scope.gtotals[sub.name];
    if (typeof current === "undefined") {
      current = totalOf(sub.name);
      $scope.gtotals[sub.name] = current;
      if (current > 0){
        return sub.name+" £"+current;
      }
    }
    return "";
  }
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
