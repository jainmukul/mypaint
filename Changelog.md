Version 1.1.0:
* geometry tools: sequence of lines, curved lines, ellipses
* new brush and layer blending modes; different layer merging
* new color dialog: palette and gamut mapping
* improved document frame, can be resized on canvas
* symmetric drawing mode
* old color changer ("washed") from 0.6 is available again
* toolbar improvements, e.g. move layer mode, pan/zoom
* revised cursor and on-canvas color picker
* better separation of mypaint's brush library; json brush file format
* translations, performance improvements, bugfixes, and more

Version 1.0.0:
* toolbar with color, brush selector and brush settings dropdown
* tool windows can be docked instead of floating
* locked alpha brush mode
* basic layer compositing modes
* new scratchpad area
* lots of other improvements (about 500 commits)

Version 0.9.1:
* several fixes for non-ascii file names, directories, layer names
* workaround for tablets reporting invalid tilt values
* rotation: fix direction while mirrored, change steps to 22.5 degrees
* store freedesktop thumbnails also when saving (for preview in other apps)
* reduce the minimal cursor size
* brush selector: remember state of the expander at the bottom
* fix glitch when changing the brush/color with a different input device
* osx: fix compile error
* windows: use AppData folder for settings
* some other minor fixes

Version 0.9.0:
* brush collection: updated better and smaller collection
* brushset import and export
* improvement for jaggy lines on Windows (might also fix saving problems)
* fixes for non-ascii brush- and filenames (for Windows mainly)
* sharper image for some zoom levels
* stylus tilt support
* persistence of selected brush and group
* file preview in open dialog
* configurable default save format and zoom level
* optimizations: faster startup, much faster saving
* lots of small improvements, bug fixes, optimizations
* updated translations: hu,es,ru,sv,nb,nn_NO,sl,ko,it
* improved exception dialog
* added GIMP-style subwindow toggle
* added GIMP-style cursor-menu
* usability improvements for brush selector and brush settings dialog
* added file->export action

Version 0.8.2:
* fix regression in 0.8.1 causing temporary layers to stick
* complain about unsupported pygtk version

Version 0.8.1:
* fixed memory leak: layer data was never freed, eg. when opening a new image
* fixed loading of layer names
* respect layer visibility when saving to PNG
* fixed a freeze in the exception dialog
* added empty "favorites" brushgroup
* Korean translation
* some minor gui fixes

Version 0.8.0:
* many new brushes contributed by various artists
* brushes organized into groups
* straight lines are possible (hold shift)
* basic layer dialog
* select brush from a stroke on the canvas
* improved color picker, show color while picking
* tools stay at top, only one taskbar entry (depending on your wm)
* faster zoomed-out view (30x speedup in some cases)
* i18n support added, translations in several languages
* new and revised color selectors
* big background patterns are possible (with limitations)
* can save all layers as numbered PNGs
* some drag&drop support
* many other minor enhancements and bugfixes
	
Version 0.7.1:
* bugfixes for win32 build
* limit the cursor size (problem on Windows, and X11 with Compiz)
* fixed brushes that lead to save problems (Windows only?)
* show filename in titlebar
* zoom on scrollwheel
* new brushes: splatter and marker
* other minor fixes

Version 0.7.0:
* color history popup
* merge layer down
* layer solo
* color changer can operate clickless (hold key down, release key to select)
* can save flattened transparent PNG
* recognize eraser end of the stylus
* elliptical dabs are possible now (aspect ratio)
* new brushes and background patterns
* save/load improved
  * fixed bugs that caused overwrite without asking
  * made OpenRaster the default file format
  * made "save scrap" more consistent (always save to scrap directory)
  * faster saving and loading (about factor two)
  * do dithering when converting from 16bit to 8bit (only when saving with transparency)
* fixed build problem with some distributions
* many other GUI tweaks and bugfixes

Version 0.6.0:
* Layers, transparency and eraser mode
* Background color and pattterns
* Save OpenRaster
* Very fast undo, limited number of steps
* Canvas rotation (via keyboard shortcuts) and mirroring
* A few great new brushes

Version 0.5.1:
* Fullscreen mode was implemented.
* Streamlined "Save" and "Save As". Also added error handling.
* Added "Save Next" as a dialog-free non-destructive alternative.
* If undo would take a lot of time, show a confirmation dialog.
* Reduced maximum zoom-out to 1/4 to avoid out of memory.
* Added settings dialog with global pressure mapping.
* New desktop icon by Sebastian Kraft (needcoffee).
* Fixed "ghost strokes" seen on internet tablets.
* Fixed startup crash where the mouse was wrongly recognized as a tablet.
* Fixed compilation for some systems.
* New brushes were added (and some removed).

Before 0.5.0:
* no changelog available

