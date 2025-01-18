if {[file isdirectory [file join $dir BlueElegance]]} {
    package ifneeded ttk::theme::BlueElegance 0.1 \
        [list source [file join $dir BlueElegance.tcl]]
}
