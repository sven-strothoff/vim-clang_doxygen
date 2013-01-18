" Vim plugin for generating Doxygen comments
" Last Change:  2013 Jan 18
" Maintainer:   Sven Strothoff <sven.strothoff@googlemail.com>
" License:      See documentation (clang_doxygen.txt)
" 
" Copyright (c) 2013, Sven Strothoff
" All rights reserved.

function! clang_doxygen_snippets#xptemplate#trigger(snippet)
  let l:snippet = substitute(a:snippet, "\\${[1-9][0-9]*:\\([^}]*\\)}", "`\\1^", "g")
  let l:snippet = substitute(l:snippet, "\\$0\\|\\${0:[^}]*}", "`cursor^", "")
  call XPTemplate("clang_doxygen_template", l:snippet)
  call XPTtgr("clang_doxygen_template")
endfunction
