# vim-clang_doxygen

Generate Doxygen comments for your C/C++ code.

## Requirements

You need to have libClang (Version 3.0 or higher) installed on your system for
this plugin to work.
This plugin uses Python to interface with libClang, so make sure that your Vim
version was compiled with Python support. If `:version` includes `+python` you
are good to go.
Currently this plugin requires the
[XPTemplate][https://github.com/drmingdrmer/xptemplate] plugin to be
installed. In the future this will be configurable and it will be possible to
insert basic, i.e. without place-holders, Doxygen comments without XPTemplate.

## Installation

Install to your `~/.vim` (`~\vimfiles` on Windows) folder or better use a
plugin manager like [pathogen.vim][https://github.com/tpope/vim-pathogen].

## Usage

Move the cursor onto a function declaration and run `:GenerateDoxygen`. This
will parse your source file and create and insert an XPTemplate, so that you
just have to replace the place-holders with your documentation.

For more information see `:help clang_doxygen`.

## License

Copyright (c) 2013, Sven Strothoff
All rights reserved.

For full license see `:help clang_doxygen-license`.
