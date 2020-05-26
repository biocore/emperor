define(['three'], function(THREE){

/**
 * @author HypnosNova / https://www.threejs.org.cn/gallery
 */

var Vector2 = THREE.Vector2;

var SelectionHelper = ( function () {

	function SelectionHelper( selectionBox, renderer, cssClassName ) {

		this.element = document.createElement( 'div' );
		this.element.classList.add( cssClassName );
		this.element.style.pointerEvents = 'none';

		this.renderer = renderer;

		this.startPoint = new Vector2();
		this.pointTopLeft = new Vector2();
		this.pointBottomRight = new Vector2();

		this.isDown = false;
    this.enabled = true;

		this.renderer.domElement.addEventListener( 'mousedown', function ( event ) {

			this.isDown = true;
			this.onSelectStart( event );

		}.bind( this ), false );

		this.renderer.domElement.addEventListener( 'mousemove', function ( event ) {

			if ( this.isDown ) {

				this.onSelectMove( event );

			}

		}.bind( this ), false );

		this.renderer.domElement.addEventListener( 'mouseup', function ( event ) {

			this.isDown = false;
			this.onSelectOver( event );

		}.bind( this ), false );

	}

	SelectionHelper.prototype.onSelectStart = function ( event ) {
    if (!this.enabled) {
      return;
    }

		this.renderer.domElement.parentElement.appendChild( this.element );

		this.element.style.left = event.clientX + 'px';
		this.element.style.top = event.clientY + 'px';
		this.element.style.width = '0px';
		this.element.style.height = '0px';

		this.startPoint.x = event.clientX;
		this.startPoint.y = event.clientY;

	};

	SelectionHelper.prototype.onSelectMove = function ( event ) {
    if (!this.enabled) {
      return;
    }

		this.pointBottomRight.x = Math.max( this.startPoint.x, event.clientX );
		this.pointBottomRight.y = Math.max( this.startPoint.y, event.clientY );
		this.pointTopLeft.x = Math.min( this.startPoint.x, event.clientX );
		this.pointTopLeft.y = Math.min( this.startPoint.y, event.clientY );

		this.element.style.left = this.pointTopLeft.x + 'px';
		this.element.style.top = this.pointTopLeft.y + 'px';
		this.element.style.width = ( this.pointBottomRight.x - this.pointTopLeft.x ) + 'px';
		this.element.style.height = ( this.pointBottomRight.y - this.pointTopLeft.y ) + 'px';

	};

	SelectionHelper.prototype.onSelectOver = function () {
    // prevent partial selection box creations
    if (this.element.parentElement) {
		  this.element.parentElement.removeChild( this.element );
    }

	};

	return SelectionHelper;
} )();

THREE.SelectionHelper = SelectionHelper;
return THREE.SelectionHelper;
});
