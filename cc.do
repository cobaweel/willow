clear
insheet using cc.csv
forval i = 1/40 {
  graph pie * in `i', ///
    plabel(1 "$0",  color(white) size(12)) ///
    plabel(2 "$10", color(white) size(12)) ///
    plabel(3 "$20", color(white) size(12)) ///
    plabel(4 "$30", color(white) size(12)) ///
    legend(off) 
  graph export `i'.png
}
