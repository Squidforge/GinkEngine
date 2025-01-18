# Package index for tile demo pixmap themes.

if {[file isdirectory [file join $dir aquablue]]} {
    if {![catch {package require Ttk}]} {
        package ifneeded ttk::theme::aquablue 0.1 \
            [list source [file join $dir aquablue8.5.tcl]]
    } elseif {![catch {package require tile}]} {
        package ifneeded tile::theme::aquablue 0.1 \
            [list source [file join $dir aquablue8.4.tcl]]
    } else {
	return
    }
}

