define(['three'], function(THREE){
  /**
   * @author HypnosNova / https://www.threejs.org.cn/gallery
   * This is a class to check whether objects are in a selection area in 3D space
   */

  var Frustum = THREE.Frustum;
  var Vector3 = THREE.Vector3;

  var SelectionBox = ( function () {

  	var frustum = new Frustum();
  	var center = new Vector3();

  	var tmpPoint = new Vector3();

  	var vecNear = new Vector3();
  	var vecTopLeft = new Vector3();
  	var vecTopRight = new Vector3();
  	var vecDownRight = new Vector3();
  	var vecDownLeft = new Vector3();

  	var vectemp1 = new Vector3();
  	var vectemp2 = new Vector3();
  	var vectemp3 = new Vector3();

  	function SelectionBox( camera, scene, deep ) {

  		this.camera = camera;
  		this.scene = scene;
  		this.startPoint = new Vector3();
  		this.endPoint = new Vector3();
      this.lineBox = [];
  		this.collection = [];
  		this.deep = deep || Number.MAX_VALUE;

  	}

    SelectionBox.prototype.viewBox = function (start, end){
      var material = new THREE.LineBasicMaterial( { color: 0xffffff } );
      material.light = true;
      var geometry = new THREE.Geometry();
      geometry.vertices.push(start);
      geometry.vertices.push(end);
      var line = new THREE.Line( geometry, material );

      return line;
    }

  	SelectionBox.prototype.select = function ( startPoint, endPoint ) {

  		this.startPoint = startPoint || this.startPoint;
  		this.endPoint = endPoint || this.endPoint;
  		this.collection = [];

  		this.updateFrustum( this.startPoint, this.endPoint );
  		this.searchChildInFrustum( frustum, this.scene );

  		return this.collection;

  	};

  	SelectionBox.prototype.updateFrustum = function ( startPoint, endPoint ) {

  		startPoint = startPoint || this.startPoint;
  		endPoint = endPoint || this.endPoint;

  		this.camera.updateProjectionMatrix();
  		this.camera.updateMatrixWorld();

      var zoom = this.camera.zoom;
      // var z_value = ( (this.camera.near + this.camera.far)/(this.camera.near - this.camera.far) ) * this.camera.zoom;

  		tmpPoint.copy( startPoint );
  		tmpPoint.x = Math.min( startPoint.x, endPoint.x );
  		tmpPoint.y = Math.max( startPoint.y, endPoint.y );
  		endPoint.x = Math.max( startPoint.x, endPoint.x );
  		endPoint.y = Math.min( startPoint.y, endPoint.y );

  		vecNear.copy( this.camera.position );

  		vecTopLeft.copy( tmpPoint );
      vecTopLeft.z = 0;
  		vecTopRight.set( endPoint.x, tmpPoint.y, 0);
  		vecDownRight.copy( endPoint );
      vecDownRight.z = 0;
  		vecDownLeft.set( tmpPoint.x, endPoint.y, 0);

      vectemp1.copy( vecTopLeft );
      vectemp1.z = this.camera.far;
      vectemp2.copy( vecTopRight );
      vectemp2.z = this.camera.far;
      vectemp3.copy( vecDownRight );
      vectemp3.z = this.camera.far;

      vecTopLeft.unproject( this.camera );
  		vecTopRight.unproject( this.camera );
  		vecDownRight.unproject( this.camera );
  		vecDownLeft.unproject( this.camera );
      vectemp1.unproject( this.camera );
      vectemp2.unproject( this.camera );
      vectemp3.unproject( this.camera );

  		vectemp1.add( vecNear );
  		vectemp2.add( vecNear );
  		vectemp3.add( vecNear );

  		var planes = frustum.planes;

  		planes[ 0 ].setFromCoplanarPoints( vectemp1, vecTopLeft, vecTopRight );
  		planes[ 1 ].setFromCoplanarPoints( vectemp2, vecTopRight, vecDownRight );
  		planes[ 2 ].setFromCoplanarPoints( vectemp3, vecDownLeft, vecDownRight );
  		planes[ 3 ].setFromCoplanarPoints( vecDownLeft, vecTopLeft, vectemp1 );
  		planes[ 4 ].setFromCoplanarPoints( vecTopRight, vecDownRight, vecDownLeft );
  		planes[ 5 ].setFromCoplanarPoints( vectemp3, vectemp2, vectemp1 );
  		planes[ 5 ].normal.multiplyScalar( - 1 );

      //this.lineBox = [];
      //near plane
      this.lineBox.push(this.viewBox(vecTopLeft,vecTopRight));
      this.lineBox.push(this.viewBox(vecTopRight,vecDownRight));
      this.lineBox.push(this.viewBox(vecDownRight,vecDownLeft));
      this.lineBox.push(this.viewBox(vecDownLeft,vecTopLeft));
      // side
      this.lineBox.push(this.viewBox(vecTopLeft,vectemp1));
      this.lineBox.push(this.viewBox(vecTopRight,vectemp2));
      this.lineBox.push(this.viewBox(vecDownRight,vectemp3));
      // far plane
      // its a triangle b/c missing one point
      this.lineBox.push(this.viewBox(vectemp1,vectemp2));
      this.lineBox.push(this.viewBox(vectemp2,vectemp3));
      this.lineBox.push(this.viewBox(vectemp3,vectemp1));
  	};

  	SelectionBox.prototype.searchChildInFrustum = function ( frustum, object ) {

  		if ( object.isMesh ) {

  			if ( object.material !== undefined ) {
          console.log(frustum);

  				object.geometry.computeBoundingSphere();

  				center.copy( object.geometry.boundingSphere.center );


  				center.applyMatrix4( object.matrixWorld );
          console.log(center);

  				if ( frustum.containsPoint( center ) ) {

  					this.collection.push( object );

  				}

  			}

  		}

  		if ( object.children.length > 0 ) {

  			for ( var x = 0; x < object.children.length; x ++ ) {

  				this.searchChildInFrustum( frustum, object.children[ x ] );

  			}

  		}

  	};

  	return SelectionBox;

  } )();

THREE.SelectionBox = SelectionBox;
return THREE.SelectionBox;
});
