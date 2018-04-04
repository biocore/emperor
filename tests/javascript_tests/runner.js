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

        page.evaluate(addStringOperations);
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
     * A number of string operations are not available in phantom.js, we took
     * these implementations from Mozilla's documentation
     */
    function addStringOperations() {
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
