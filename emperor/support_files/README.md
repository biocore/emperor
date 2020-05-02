# Emperor's resources

The organization of this directory should be as follows:

- `js/` should contain only JavaScript source code from Emperor.
- `css/` should contain only CSS source code from Emperor.
- `img/` should contain images that are only by Emperor.
- `vendor/` should contain any third party code used in the project. If it is a JavaScript file the files should live in `vendor/js/` and if it is a CSS file the files should live in `vendor/css/`.

## THREE.js

One note on THREE.js, all the plugins that emperor relies on (anything under `emperor/support_files/vendor/js/three.js-plugins/`), are not AMD/require.js compatible, as such they have been modified from the original source to be defined as modules that depend on THREE and that export themselves. The discussion in [this issue](https://github.com/mrdoob/three.js/issues/9602) points out that you either encapsulate dependencies, or make THREE.js global.
