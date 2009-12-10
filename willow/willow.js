$(document).ready(function(){
   // Generate a unique ID for this instance
   var id = (new UUID()).id;

   // Warn user if they try to leave the page
   window.onbeforeunload = function () {
     return "Are you sure you want to leave the experiment?";
   };

   // Notify server whenever a button is clicked
   function decorate(elt) {
	   elt.find("input[type=submit]").unbind().click(function (e) {
	     var rep = {"action": "click", "argument": e.target.id, "id": id };
	     $.post("willow", JSON.stringify(rep));
	   });
	   elt.find(".clickable").unbind().click(function (e) {
	     var arg = $(e.target).closest(".clickable").get(0).id;
	     var rep = {"action": "click", "argument": arg, "id": id };
	     $.post("willow", JSON.stringify(rep));
	   });
	   elt.find(".bait").unbind().bind("mouseenter mouseleave", function(e) {
	     $(e.target).closest(".bait").toggleClass("mouse");
	   });

   }



   // Process command from the server and ask for another one
   function receive_update(cmds) {
     if (cmds) {
       for (i in cmds) {
	 var cmd = cmds[i];
	 switch(cmd.action) {
	 case "add":
	   decorate($(cmd.selector).append(cmd.argument));
	   break;
	 case "push":
	   decorate($(cmd.selector).addClass(cmd.argument)); break;
	 case "pop":
	   decorate($(cmd.selector).removeClass(cmd.argument)); break;
	 case "set":
	   decorate($(cmd.selector).html(cmd.argument)); break;
	 case "hide":
	   $(cmd.selector).hide(); break;
	 case "show":
	   $(cmd.selector).show(); break;
	 case "data":
	   var arg = $(cmd.selector).attr("value");
	   if (!arg) arg = "";
	   var rep = {"action": "data", "argument": arg, "id": id };
	   $.post("willow", JSON.stringify(rep));
	   break;
	 }
       }
     }
     var cmd = {"id": id, "action": "update"};
     $.post("willow", JSON.stringify(cmd), receive_update, "json");
    }
   receive_update(null);
 });

/*
# Willow, a Python framework for experimental economics
# Copyright (c) 2009, George Mason University
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# Neither the name of the George Mason University nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission. THIS SOFTWARE
# IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */