/*
 *
 * QtWebKit-powered headless test runner using PhantomJS
 *
 * PhantomJS binaries: http://phantomjs.org/download.html
 * Requires PhantomJS 1.6+ (1.7+ recommended)
 *
 * Run with:
 *   phantomjs runner.js [url-of-your-qunit-testsuite]
 *
 * e.g.
 *   phantomjs runner.js http://localhost/qunit/test/index.html
 *
 * Originally taken from underscore.js https://github.com/jashkenas/underscore
 * SHA-1 b5f074ff72f949c2548605354e6c739df7ba73aa
 *
 */

/*jshint latedef:false */
/*global phantom:false, require:false, console:false, window:false,
  QUnit:false */

(function() {
    'use strict';

    var args = require('system').args;

    // arg[0]: scriptName, args[1...]: arguments
    if (args.length !== 2) {
        console.error('Usage:\n  phantomjs runner.js ' +
                      '[url-of-your-qunit-testsuite]');
        exit(1);
    }

    var url = args[1],
        page = require('webpage').create();

    // Route `console.log()` calls from within the Page context to the main
    // Phantom context (i.e. current `this`)
    page.onConsoleMessage = function(msg) {
        console.log(msg);
    };

    page.onInitialized = function() {
        page.evaluate(addLogging);

        // https://stackoverflow.com/a/29506120/379593
        page.evaluate(function() {
            Math.log2 = Math.log2 || function(x) {
                return Math.log(x) / Math.LOG2E;
            };
        });

        page.evaluate(addPolyfillsForPhantomJS);
    };

    page.onCallback = function(message) {
        var result,
            failed;

        if (message) {
            if (message.name === 'QUnit.done') {
                result = message.data;
                failed = !result || result.failed;

                exit(failed ? 1 : 0);
            }
        }
    };

    page.open(url, function(status) {
        if (status !== 'success') {
            console.error('Unable to access network: ' + status);
            exit(1);
        } else {
            // Cannot do this verification with the 'DOMContentLoaded' handler
            // because it will be too late to attach it if a page does not have
            // any script tags.
            var qunitMissing = page.evaluate(function() {
                return (typeof QUnit === 'undefined' || !QUnit);
            });
            if (qunitMissing) {
                console.error('The `QUnit` object is not present.');
                exit(1);
            }

            // Do nothing... the callback mechanism will handle everything!
        }
    });

    function addLogging() {
        window.document.addEventListener('DOMContentLoaded', function() {
            var cur_test_asserts = [];

            QUnit.log(function(details) {
                var response;

                // Ignore passing assertions
                if (details.result) {
                    return;
                }

                response = details.message || '';

                if (typeof details.expected !== 'undefined') {
                    if (response) {
                        response += ', ';
                    }

                    response += 'expected: ' + details.expected +
                    ', but was: ' + details.actual;
                    if (details.source) {
                        response += '\n' + details.source;
                    }
                }

                cur_test_asserts.push('Failed assertion: ' + response);
            });

            QUnit.testDone(function(result) {
                var i,
                    len,
                    name = result.module + ': ' + result.name;

                if (result.failed) {
                    console.log('Test failed: ' + name);

                    for (i = 0, len = cur_test_asserts.length; i < len; i++) {
                        console.log('    ' + cur_test_asserts[i]);
                    }
                }
                else {
                    console.log(name + ' (' + result.duration + ' ms) ... ok');
                }

                cur_test_asserts.length = 0;
            });

            QUnit.moduleDone(function(result) {
                console.log('');
            });

            QUnit.done(function(result) {
                console.log('Took ' + result.runtime + 'ms to run ' +
                            result.total + ' tests. ' + result.passed +
                            ' passed, ' + result.failed + ' failed.');

                if (typeof window.callPhantom === 'function') {
                    window.callPhantom({
                        'name': 'QUnit.done',
                        'data': result
                    });
                }
            });
        }, false);
    }

    /*
     * A number of methods are not available in phantom.js, we took
     * these implementations from Mozilla's documentation
     */
    function addPolyfillsForPhantomJS() {
        // https://github.com/uxitten/polyfill/blob/master/string.polyfill.js
        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/padEnd
        String.prototype.padEnd = function padEnd(targetLength, padString) {
            //floor if number or convert non-number to 0;
            targetLength = targetLength >> 0;
            padString = String((typeof padString !== 'undefined' ?
                                padString : ' '));
            if (this.length > targetLength) {
                return String(this);
            }
            else {
                targetLength = targetLength - this.length;
                if (targetLength > padString.length) {
                    //append to original to ensure we are longer than needed
                    padString += padString.repeat(targetLength /
                                                  padString.length);
                }
                return String(this) + padString.slice(0, targetLength);
            }
        };

        // https://github.com/uxitten/polyfill/blob/master/string.polyfill.js
        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/padStart
        String.prototype.padStart = function padStart(targetLength, padString) {
            // truncate if number or convert non-number to 0;
            targetLength = targetLength >> 0;
            padString = String((typeof padString !== 'undefined' ?
                                padString : ' '));
            if (this.length > targetLength) {
                return String(this);
            }
            else {
                targetLength = targetLength - this.length;
                if (targetLength > padString.length) {
                    //append to original to ensure we are longer than needed
                    padString += padString.repeat(targetLength /
                                                  padString.length);
                }
                return padString.slice(0, targetLength) + String(this);
            }
        };

        String.prototype.repeat = function(count) {
            if (this == null) {
                throw new TypeError('can\'t convert ' + this + ' to object');
            }
            var str = '' + this;
            count = +count;
            if (count != count) {
                count = 0;
            }
            if (count < 0) {
                throw new RangeError('repeat count must be non-negative');
            }
            if (count == Infinity) {
                throw new RangeError('repeat count must be less than infinity');
            }
            count = Math.floor(count);
            if (str.length == 0 || count == 0) {
                return '';
            }
            // Ensuring count is a 31-bit integer allows us to heavily optimize
            // the main part. But anyway, most current (August 2014) browsers
            // can't handle strings 1 << 28 chars or longer, so:
            if (str.length * count >= 1 << 28) {
                throw new RangeError('repeat count must not overflow maximum' +
                                     ' string size');
            }
            var rpt = '';
            for (var i = 0; i < count; i++) {
                rpt += str;
            }
            return rpt;
        };

      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/startsWith
      if (!String.prototype.startsWith) {
        Object.defineProperty(String.prototype, 'startsWith', {
          value: function(search, rawPos) {
            var pos = rawPos > 0 ? rawPos | 0 : 0;
            return this.substring(pos, pos + search.length) === search;
          }
        });
      }

      // Production steps of ECMA-262, Edition 6, 22.1.2.1
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from
      if (!Array.from) {
        Array.from = (function() {
          var toStr = Object.prototype.toString;
          var isCallable = function(fn) {
            return (typeof fn === 'function' ||
                    toStr.call(fn) === '[object Function]');
          };
          var toInteger = function(value) {
            var number = Number(value);
            if (isNaN(number)) { return 0; }
            if (number === 0 || !isFinite(number)) { return number; }
            return (number > 0 ? 1 : -1) * Math.floor(Math.abs(number));
          };
          var maxSafeInteger = Math.pow(2, 53) - 1;
          var toLength = function(value) {
            var len = toInteger(value);
            return Math.min(Math.max(len, 0), maxSafeInteger);
          };

          // The length property of the from method is 1.
          return function from(arrayLike/*, mapFn, thisArg */) {
            // 1. Let C be the this value.
            var C = this;

            // 2. Let items be ToObject(arrayLike).
            var items = Object(arrayLike);

            // 3. ReturnIfAbrupt(items).
            if (arrayLike == null) {
              throw new TypeError('Array.from requires an array-like object ' +
                                  '- not null or undefined');
            }

            // 4. If mapfn is undefined, then let mapping be false.
            var mapFn = arguments.length > 1 ? arguments[1] : void undefined;
            var T;
            if (typeof mapFn !== 'undefined') {
              // 5. else
              // 5. a If IsCallable(mapfn) is false, throw a TypeError
              // exception.
              if (!isCallable(mapFn)) {
                throw new TypeError('Array.from: when provided, the second ' +
                                    'argument must be a function');
              }

              // 5. b. If thisArg was supplied, let T be thisArg; else let T be
              // undefined.
              if (arguments.length > 2) {
                T = arguments[2];
              }
            }

            // 10. Let lenValue be Get(items, "length").
            // 11. Let len be ToLength(lenValue).
            var len = toLength(items.length);

            // 13. If IsConstructor(C) is true, then
            // 13. a. Let A be the result of calling the [[Construct]] internal
            // method of C with an argument list containing the single item len.
            // 14. a. Else, Let A be ArrayCreate(len).
            var A = isCallable(C) ? Object(new C(len)) : new Array(len);

            // 16. Let k be 0.
            var k = 0;
            // 17. Repeat, while k < len… (also steps a - h)
            var kValue;
            while (k < len) {
              kValue = items[k];
              if (mapFn) {
                A[k] = (typeof T === 'undefined' ?
                        mapFn(kValue, k) : mapFn.call(T, kValue, k));
              } else {
                A[k] = kValue;
              }
              k += 1;
            }
            // 18. Let putStatus be Put(A, "length", len, true).
            A.length = len;
            // 20. Return A.
            return A;
          };
        }());
      }
    }

    /*
     This function was taken from:
     https://github.com/jonkemp/qunit-phantomjs-runner

     It helps prevent some problems with the output produced by this script.
     */
    function exit(code) {
        if (page) {
            page.close();
        }
        setTimeout(function() {
            phantom.exit(code);
        }, 0);
    }


})();
