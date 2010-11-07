/*
 *  Willow, a Python framework for experimental economics. Copyright
 * (c) 2009, George Mason University. All rights reserved. Redistribution
 * allowed under certain conditions; see file COPYING.txt.
 */

$(document).ready(function(){
  /*
   * The preferred client ID is the URL if that is an integer, or else
   * 0. We will not know the actual ID until after we haved logged in.
   */
  var url = window.location.pathname.slice(1);
  var preferred_client = url ? Math.round(url - 0) + "" : "-1";
  /*
   * Now log in.
   */
  $.post("new", preferred_client, function(client) {

    /* At this point we are logged in, and we know the actual client
     * number. First, we will define a few helper functions, and then
     * we will start listening for server requests.*/

    /*
     * This function makes a call back to the server to post a
     * dictionary on the board. It is used both for requested (tag=peek)
     * and automatic (tag=click, tag=key) dictionaries. It decorates the
     * dictionary with two additional entries that indicate (i) client
     * number and (ii) a time stamp; these are used in all dictionaries
     * posted by the client, so we might as well just code them once.
     */
    function put(obj){
      /*
       * Keep in mind that client is a string and we want an integer
       * here, so subtract 0.
       */
      obj.client = client - 0;
      obj.time = (new Date()).getTime();
      $.post("put", JSON.stringify(obj));
    }

    /*
     * Catch keypresses no matter what is in focus and post them to
     * the board. We can do this once and for all, because all keypresses
     * accrue to the document object, and there is only one such
     * object. (Other event handlers are adjusted every time the page
     * content changes.)
     */
    $(document).keypress(function(e) {
      if (e.which)
	put({"tag": "key", "value": String.fromCharCode(e.which)});
    });

    /*
     * This function is to be called on newly inserted or modified
     * HTML elements. It makes sure that the correct event handlers are
     * bound. This works better than trying to use the jQuery system of
     * live events.
     */
    function decorate(elt) {
      /*
       * Key presses that happen when a text field is in focus
       * should be processed the normal way and should not result in
       * events being reported to the server.
       */
      var text_fields = elt.find("input:text,textarea");
      text_fields.keypress(function(e) {
        e.stopPropagation();
      });

      /*
       * When somebody clicks a button, or a "clickable" element, we
       * catch the click and report it.
       */
      var buttons = elt.find(":submit,:button,.clickable");
      buttons.unbind("click");
      buttons.click(function (e) {
        put({ "tag": "click",  "id": e.currentTarget.id});
      });

      /*
       * When an element is marked with class "bait", we want to
       * turn on class "mouse" whenever the mouse is over it. (This
       * is for implementing "hover" effects.)
       */
      var mousetraps = elt.find(".bait");
      mousetraps.unbind("mouseenter");
      mousetraps.unbind("mouseleave");
      mousetraps.bind("mouseenter mouseleave", function(e) {
        $(e.target).closest(".bait").toggleClass("mouse");
      });
    }

    /*
     * This function processes a list of commands received from the
     * server, and then immediately asks for more commands.
     */
    function action(cmds) {
      /*
       * Process each command.
       */
      for (i in cmds) {
        (function () {
          var cmd = cmds[i];
          function thunk() {
            switch(cmd.action) {
            /*
             * Most of the commands correspond directly to jQuery
             * methods; we call decorate() on the result to make sure that
             * new/modified HTML elements have the right event handlers
             * bound.
             */
            case "add":
              decorate($(cmd.selector).append(cmd.content));
              break;
            case "let":
              decorate($(cmd.selector).html(cmd.content));
              break;
            case "poke":
              decorate($(cmd.selector).attr(cmd.attribute, cmd.value));
              break;
            case "push":
              decorate($(cmd.selector).addClass(cmd.css_class));
              break;
            case "pop":
              decorate($(cmd.selector).removeClass(cmd.css_class));
              break;
            case "hide":
              $(cmd.selector).hide();
              break;
            case "show":
              $(cmd.selector).show();
              break;

            /*
             * The "peek" command is a request for the contents of
             * some input element to be posted to the tuple space.
             * jQuery has a method .val() that will get the content
             *  of all sorts input elements; quite convenient!
             */
            case "peek":
              var elt = $(cmd.selector);  
	      if (elt.size() > 0) {
		  var val = elt.eq(0).val() || "";
	      } else {
		  var val = "";
	      }
              put({"tag": "peek", "ticket": cmd.ticket, "value": val});
              break;
            }

            /*
             * All commands can come with an optional request for a
             * timestamp to be posted; the put() function puts on the actual
             * timestamp.
             */
            if (cmd.timestamp)
              put({ "tag":"timestamp" });
          }
          /*
           * If cmd.delay > 0, the request is for the command to be
           * scheduled rather than executed immediately; that's easy
           * enough to handle using window.setTimeout.
           */
          if (cmd.delay > 0) {
            window.setTimeout(thunk, 1000 * cmd.delay);
          } else {
            thunk();
          }

          /*
           * The use of an anonymous function that immediately gets
           * called may seem strange, but it's a workaround for Javascript's
           * dyslexical scoping (pun intended).
           */
        })();
      }

      /*
       * Request more commands. (At your service!) Note how the loop
       * works: we the action() function registers itself as a
       * callback. This is NOT recursion and will NOT overflow the stack.
       * This here trick, BTW, is known under various highfalutin names such
       * as "Comet" and "reverse AJAX".
       */
      $.post("do", client, action, "json");
    }

    /*
     * Request some commands to set the ball rolling.
     */
    action([]);
  });
});

