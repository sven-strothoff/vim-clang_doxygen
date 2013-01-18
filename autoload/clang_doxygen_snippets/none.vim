" Vim plugin for generating Doxygen comments
" Last Change:  2013 Jan 18
" Maintainer:   Sven Strothoff <sven.strothoff@googlemail.com>
" License:      See documentation (clang_doxygen.txt)
" 
" Copyright (c) 2013, Sven Strothoff
" All rights reserved.

function! clang_doxygen_snippets#none#trigger(snippet)
  let l:snippet = substitute(a:snippet, "\\${[1-9][0-9]*:\\([^}]*\\)}", "", "g")
  let l:snippet = substitute(l:snippet, "\\$0\\|\\${0:[^}]*}", "", "")
  let l:snippet = substitute(l:snippet, "\\\\\\\\", "\\\\", "g")
  let l:line = line('.')
  execute l:line 'delete _'
  call append(l:line - 1, split(l:snippet, "\n"))
  call setpos('.', [0, l:line, 0, 0])
  startinsert!
endfunction
