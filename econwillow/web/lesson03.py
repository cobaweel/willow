from willow.willow import *

def session(me):
    add("<style type='text/css'>.important { font-weight: bold; }</style>")
    add("<p>The <span class='important' id='a'>division</span> of "
        "<span class='b'>labor</span> is limited "
        "by the extent of the "
        "<a href='http://ebay.ocm'>market</a>.")
    add(" and subdivision", "#a")
    let("labour", ".b")
    poke("href", "http://ebay.com", "a")
    pop("important","#a")
    push("important",".b")    
    add("<p class='elusive'>Microfoundations.</p>")
    add("<p class='hidden'>Prices.</p>")    
    hide(".elusive")
    show(".hidden")
    
run(session)        
 
