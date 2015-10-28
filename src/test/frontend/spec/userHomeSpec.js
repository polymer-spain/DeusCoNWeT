describe('UserHomeController', function() {
  beforeEach(module('picbit'));

  var $controller;

  beforeEach(inject(function(_$controller_){
    // The injector unwraps the underscores (_) from around the parameter names when matching
    $controller = _$controller_;
  }));

  /* Paquete de pruebas de funcionalidad básica de las funciones. Comprobando resultados conocidos */

  describe('Angular functions: ', function() {

  	var $scope, controller;
  	beforeEach(function(){
  		$scope = {};
  		controller = $controller('UserHomeController', { $scope: $scope})
  	})

    it('Función showMenu', function() {
      /* 1er Case: inititially menuStatus is false */
      $scope.menuStatus = false;
      $scope.showMenu();
      expect($scope.menuStatus).toEqual(true);
      expect($scope.showElement).toEqual(true);
      /* 2º Case: inititially menuStatus is true */
      $scope.menuStatus = true;
      $scope.showMenu();
      expect($scope.menuStatus).toEqual(false);
      expect($scope.showElement).toEqual(false);
      expect($scope.selected).toEqual("");
      expect($scope.showSingle).toEqual("");
      expect($scope.listaOpciones).toEqual([false, false, false])
    });

    it('Función ocultar', function() {
      $scope.ocultar();
      expect($scope.listaOpciones).toEqual([false, false, false])
    });

    it('Función setList',function(){
      $scope.listaOpciones=[false,false,false]
      $scope.setList('add');
      expect($scope.listaOpciones).toEqual([true, false, false])
      $scope.setList('delete');
      expect($scope.listaOpciones).toEqual([false, true, false])
      $scope.setList('modify');
      expect($scope.listaOpciones).toEqual([false, false, true])
    });

    it('Función isListHidden',function(){
      $scope.listaOpciones = [true, false, false]
      $scope.isListHidden('add')
      expect($scope.listaOpciones[0]).toEqual(true)
      $scope.isListHidden('delete')
      expect($scope.listaOpciones[1]).toEqual(false)
      $scope.isListHidden('modify')
      expect($scope.listaOpciones[2]).toEqual(false)
    });

    it('Función isSelected', function(){
      expect($scope.isSelected('add')).toEqual(false)
      expect($scope.isSelected('delete')).toEqual(false)
      expect($scope.isSelected('modify')).toEqual(false)
      $scope.selected = 'add';
      expect($scope.isSelected('add')).toEqual(true)
      $scope.selected = 'delete';
      expect($scope.isSelected('delete')).toEqual(true)
      $scope.selected = 'modify';
      expect($scope.isSelected('modify')).toEqual(true)
    });

    it('Función setSelected', function(){
     $scope.selected = 'add'
     listaOpciones = [false, false, false];
     $scope.setSelected('add')
     expect($scope.selected).toEqual('')
     expect($scope.showSingle).toEqual('')
     if($scope.isListHidden('add')){
      expect($scope.listaOpciones).toEqual([true, false, false]);
    }
    else{
      expect($scope.listaOpciones).toEqual([false, false, false]);
    }
   });

    it('Función isMenuHidden', function(){
      $scope.menuStatus = false;
      expect($scope.isMenuHidden('add')).toEqual(true)
      expect($scope.isMenuHidden('delete')).toEqual(true)
      expect($scope.isMenuHidden('modify')).toEqual(true)
      $scope.menuStatus = true;
      expect($scope.isMenuHidden('add')).toEqual(false)
      expect($scope.isMenuHidden('delete')).toEqual(false)
      expect($scope.isMenuHidden('exmodify')).toEqual(false)
    });

    it('Función setSort', function(){
      $scope.sort[false, false, false]
      $scope.setSort('add')
      expect($scope.sort).toEqual([true, false, false])
      $scope.setSort('delete')
      expect($scope.sort).toEqual([false, true, false])
      $scope.setSort('modify')
      expect($scope.sort).toEqual([false, false, true])
    });

    /* Para todas las variables el resultado es el mismo, por tanto se prueba solo con una de ellas. */
    it('Función setModifySelected',function(){
      $scope.modifySelected = ''
      $scope.setModifySelected('add')
      expect($scope.modifySelected).toEqual('add')
      $scope.modifySelected = 'add'
      $scope.setModifySelected('add')
      expect($scope.modifySelected).toEqual('')
    });

    it('Función isModifySelected', function(){
      $scope.modifySelected = ''
      expect($scope.isModifySelected('add')).toEqual(false)
      $scope.modifySelected = 'modify'
      expect($scope.isModifySelected('modify')).toEqual(true)
    });

    it('Función deleteTimeline',function(){
      $scope.listComponentAdded = ['twitter-timeline', 'instagram-timeline', 'github-events']
      $scope.deleteTimeline('twitter-timeline')
      expect($scope.listComponentAdded).toEqual(['instagram-timeline', 'github-events'])
      $scope.listComponentAdded = ['instagram-timeline']
      $scope.deleteTimeline('instagram-timeline')
      expect($scope.listComponentAdded).toEqual([])
    });

  /*  it('Función showToggleHelp',function(){

    });

    it('Función hideToggleHelp',function(){

    });

    it('Función listenEscKeydown', function(){

    });*/

  });
});
