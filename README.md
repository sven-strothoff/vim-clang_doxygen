# vim-clang_doxygen

Generate Doxygen comments for your C/C++ code.

This is an early development version, that I created mainly for myself. The
current version should be working quite well, if you find any bugs, please open
an issue for them. If you have any ideas or suggestions feel free to share them
with me and I _might_ include them.

## Requirements

You need to have libClang (Version 3.0 or higher) installed on your system for
this plugin to work.

This plugin uses Python to interface with libClang, so make sure that your Vim
version was compiled with Python support. If `:version` includes `+python` you
are good to go.

If you want to have clang doxygen generate placeholders, so that you can qickly
enter your documentation, you need one of the supported snippet plugins.  See
`:help g:clang_doxygen_snippet_plugin`.

## Installation

Install to your `~/.vim` (`~\vimfiles` on Windows) folder or better use a
plugin manager like [pathogen.vim](https://github.com/tpope/vim-pathogen).

## Usage

Move the cursor onto a class or (template) function declaration and run
`:GenerateDoxygen`. This will parse your source file and generate and insert a
Doxygen comment.

For more information see `:help clang_doxygen`.

## License

Copyright (c) 2013, Sven Strothoff
All rights reserved.

For full license see `:help clang_doxygen-license`.
