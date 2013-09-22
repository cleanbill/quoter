
// declare a module
var quoter = angular.module('quoter', ['ui.bootstrap']);

//quoter.factory('Data', function() {
//    return custs;
// }
//)

//function TypeaheadCtrl($scope, Data) {
function TypeaheadCtrl($scope){
  $scope.selected = undefined;
  $scope.init = function(data)
  {
    $scope.elements = data;
  };
}


function adCtrl($scope){
    $scope.add = function(id){
	alert("add id is "+id); 
    };
    $scope.del = function(id){
	alert("del id is "+id); 
    };
};

function editCtrl($scope){
    $scope.edit = function(id){
	alert("id is "+id); 
    };
};

quoter.directive("edit", function() {
    return {
	restrict: 'E',
        scope: { line:"="},
        transclude: true,
        controller: editCtrl,
        template:"<a ng-click=\"edit('eh?')\">Edit</a>"
    }
})

quoter.directive("ad", function() {
    return {
	restrict: 'E',
        transclude: true,
        controller: adCtrl,
        template:"<b><a ng-click=\"add('name')\">Add</a> | <a ng-click=\"del('name')\">Del</a></b>"
    }
})



quoter.directive("subtotal", function() {
    return {
	restrict: 'E',
        scope: { line:"="},
        transclude: true,
        templateUrl:"subtotal.html"
    }
})

quoter.directive("details", function() {
    return {
	restrict: 'E',
        scope: { line:"="},
        transclude: true,
        templateUrl:"details.html"
    }
})


function quoteCtrl($scope) {
  $scope.quote = quote;
  $scope.todos = [
    {text:'learn angular', done:true},
    {text:'build an angular app', done:false}];
 
  $scope.addTodo = function() {
    $scope.todos.push({text:$scope.todoText, done:false});
    $scope.todoText = '';
  };
 
  $scope.remaining = function() {
    var count = 0;
    angular.forEach($scope.todos, function(todo) {
      count += todo.done ? 0 : 1;
    });
    return count;
  };
 
  $scope.archive = function() {
    var oldTodos = $scope.todos;
    $scope.todos = [];
    angular.forEach(oldTodos, function(todo) {
      if (!todo.done) $scope.todos.push(todo);
    });
  };
};


quoter.controller("quoteCtrl",quoteCtrl);

quoter.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{({');
  $interpolateProvider.endSymbol('})}');
})
