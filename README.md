# sublime-less2css


Sublime Text 2 Plugin to compile less files to css on save
Requires lessc installed on PATH

On a side note give big thanks to [timdouglas](https://github.com/timdouglas/sublime-less2css) for his work on this plugin
This is work in process, have added new features do to my workflow. Hope someone find this helpful.


## Features

 * Automatically compile less -> css on save when editing a .less file in sublime
 * Reports compilation errors
 * Compile all less files in a directory to css files
 
 * Compile one file with less '@import'
 * Multi project support
 
 
NB This plugin requires lessc to be in your execution path 

# Installation


## Install The Plugin

***With Git:*** Clone the repository in your Sublime Text 2 "Packages" directory:

    git clone git://github.com/tikot/sublime-less2css.git

The "Packages" directory is located at:

* OS X:

        ~/Library/Application Support/Sublime Text 2/Packages/

* Linux:

        ~/.config/sublime-text-2/Packages/

* Windows:

        %APPDATA%/Sublime Text 2/Packages/


## Install Requirements

Less2Css requires lessc to compile less to css.

#### Windows / Mac OS X / Linux(Ubuntu/Debian…)

1. Install [NodeJS](http://nodejs.org)
2. Install npm([NodeJS Package Manager](https://npmjs.org/doc/README.html))
3. Install less

## 
    npm install less -gd
    