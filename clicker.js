// Support for presentation clickers (wireless presenters).
//
// A clicker is just a USB keyboard: the "next" button sends Page Down (or an
// arrow key, depending on the model) and the "previous" button sends Page Up.
// Two things make the raw key events unpleasant to use directly:
//
//  * Many clickers send a single press as several key events in a row, and
//    holding a button down makes the keyboard auto-repeat it. Acting on every
//    event makes the page jump several screens at once.
//  * Page Up / Page Down scroll by whole screens, so a question can easily
//    end up cut in half between two screens.
//
// This module therefore debounces the events and lets pages move between
// meaningful positions (e.g. one quiz question at a time) instead of scrolling
// by raw screenfuls.

var Clicker = (function() {
    // Clicker buttons bounce; two presses closer than this are one press.
    var DEBOUNCE_MS = 300;

    var NEXT_KEYS = [
        "PageDown", "ArrowRight", "ArrowDown", " ", "Enter", "n", "N"];
    var PREV_KEYS = [
        "PageUp", "ArrowLeft", "ArrowUp", "Backspace", "p", "P"];

    var last_event_time = 0;

    function typing_in_a_field(event) {
        var tag = (event.target.tagName || "").toLowerCase();
        return tag === "input" || tag === "textarea" || tag === "select" ||
            event.target.isContentEditable;
    }

    // Calls on_next / on_prev at most once per DEBOUNCE_MS. A handler that
    // returns false lets the key through to the browser.
    function listen(on_next, on_prev) {
        document.addEventListener("keydown", function(event) {
            if (event.repeat || typing_in_a_field(event) ||
                    event.ctrlKey || event.altKey || event.metaKey) {
                return;
            }

            var handler = null;
            if (NEXT_KEYS.indexOf(event.key) >= 0) {
                handler = on_next;
            } else if (PREV_KEYS.indexOf(event.key) >= 0) {
                handler = on_prev;
            }
            if (!handler) {
                return;
            }

            // The default action (scrolling, clicking a focused button) would
            // fight with ours, so it is suppressed even for repeated presses
            // that are swallowed by the debouncing.
            event.preventDefault();

            var now = Date.now();
            if (now - last_event_time < DEBOUNCE_MS) {
                return;
            }
            last_event_time = now;

            handler();
        });
    }

    // Makes the clicker move the page between the elements matching
    // `selector`, one at a time. An element taller than the window is
    // scrolled through in screen-sized steps, so nothing stays unread.
    function scroll_between(selector, margin) {
        margin = margin === undefined ? 8 : margin;

        function stops() {
            return Array.prototype.slice.call(
                document.querySelectorAll(selector));
        }

        // Where the page is going to be, which is where it already is unless
        // a smooth scroll is still running.
        var pending_top = null;
        var pending_timer = null;

        function current_top() {
            return pending_top === null ? window.scrollY : pending_top;
        }

        function scroll_to(top) {
            var max_top = Math.max(
                0,
                document.documentElement.scrollHeight - window.innerHeight);
            top = Math.min(Math.max(top, 0), max_top);

            pending_top = top;
            window.clearTimeout(pending_timer);
            // Smooth scrolling takes a while; until it settles, further
            // presses have to be counted from the target, not from the
            // position the page happens to be passing through.
            pending_timer = window.setTimeout(function() {
                pending_top = null;
            }, 1000);

            window.scrollTo({top: top, behavior: "smooth"});
        }

        function step(forward) {
            var top = current_top();
            // A press never moves the page by more than one screen, so a
            // long question is read in parts instead of being skipped over.
            var screen = Math.max(window.innerHeight * 0.85, 100);
            var target = forward ? top + screen : top - screen;

            // Snap to a question boundary if there is one within the step.
            var positions = stops().map(function(element) {
                return element.getBoundingClientRect().top + window.scrollY
                    - margin;
            });
            var snapped = null;
            positions.forEach(function(position) {
                if (forward && position > top + 1 && position <= target) {
                    if (snapped === null || position < snapped) {
                        snapped = position;
                    }
                } else if (!forward && position < top - 1 && position >= target) {
                    if (snapped === null || position > snapped) {
                        snapped = position;
                    }
                }
            });

            scroll_to(snapped === null ? target : snapped);
        }

        listen(function() { step(true); }, function() { step(false); });
    }

    return {listen: listen, scroll_between: scroll_between};
})();
