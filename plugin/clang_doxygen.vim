" Vim plugin for generating Doxygen comments
" Last Change:  2013 Jan 14
" Maintainer:   Sven Strothoff <sven.strothoff@googlemail.com>
" License:      See documentation (clang_doxygen.txt)
" 
" Copyright (c) 2013, Sven Strothoff
" All rights reserved.

if exists("g:loaded_clang_doxygen")
  finish
endif
let g:loaded_clang_doxygen = 1

let s:has_XPTemplate = 1

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')

function! s:GenerateDoxygen()
	python import sys
	exe 'python sys.path = ["' . s:plugin_path . '"] + sys.path'
	exe 'pyfile ' . s:plugin_path . '/clang_doxygen.py'

	if s:has_XPTemplate
		python generateDoxygen(True)
	else
		python generateDoxygen(False)
	endif
endfunction

command! GenerateDoxygen call s:GenerateDoxygen()
