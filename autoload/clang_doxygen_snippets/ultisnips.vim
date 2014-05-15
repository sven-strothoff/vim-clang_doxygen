" Vim plugin for generating Doxygen comments
" Last Change:  2013 Jan 18
" Maintainer:   Sven Strothoff <sven.strothoff@googlemail.com>
" License:      See documentation (clang_doxygen.txt)
" 
" Copyright (c) 2013, Sven Strothoff
" All rights reserved.

function! clang_doxygen_snippets#ultisnips#trigger(snippet)
  call UltiSnips#Anon(a:snippet)
endfunction
