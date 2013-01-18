" Vim plugin for generating Doxygen comments
" Last Change:  2013 Jan 18
" Maintainer:   Sven Strothoff <sven.strothoff@googlemail.com>
" License:      See documentation (clang_doxygen.txt)
" 
" Copyright (c) 2013, Sven Strothoff
" All rights reserved.

if exists("g:loaded_clang_doxygen")
  finish
endif
let g:loaded_clang_doxygen = 1

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')

" A list of command line args to clang
if !exists("g:clang_doxygen_clang_args")
	let g:clang_doxygen_clang_args = []
endif

" Choose a snippet plugin
if !exists("g:clang_doxygen_snippet_plugin")
  let g:clang_doxygen_snippet_plugin = "none"
endif

function! s:GenerateDoxygen()
	python import sys
	exe 'python sys.path = ["' . s:plugin_path . '"] + sys.path'
	exe 'pyfile ' . s:plugin_path . '/clang_doxygen.py'

  python generateDoxygen()
endfunction

command! GenerateDoxygen call s:GenerateDoxygen()
