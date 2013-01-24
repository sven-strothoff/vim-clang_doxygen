" Vim plugin for generating Doxygen comments
" Last Change:  2013 Jan 24
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

" Configuration of Doxygen tags
if !exists("g:clang_doxygen_tag_brief")
  let g:clang_doxygen_tag_brief = "\\brief "
endif

if !exists("g:clang_doxygen_tag_param")
  let g:clang_doxygen_tag_param = "\\param "
endif

if !exists("g:clang_doxygen_tag_return")
  let g:clang_doxygen_tag_return = "\\return "
endif

if !exists("g:clang_doxygen_block_no_newline")
  let g:clang_doxygen_block_no_newline = 0
endif

if !exists("g:clang_doxygen_comment_style")
  let g:clang_doxygen_comment_style = "c++"
endif

" Configuration of comment style
if g:clang_doxygen_comment_style ==# "c++"
  if !exists("g:clang_doxygen_use_block")
    let g:clang_doxygen_use_block = 0
  endif

  if !exists("g:clang_doxygen_comment_middle")
    let g:clang_doxygen_comment_middle = "/// "
  endif

  if !exists("g:clang_doxygen_block_start")
    let g:clang_doxygen_block_start = "/// "
  endif

  if !exists("g:clang_doxygen_block_end")
    let g:clang_doxygen_block_end = "/// "
  endif
else
  if !exists("g:clang_doxygen_use_block")
    let g:clang_doxygen_use_block = 1
  endif

  if !exists("g:clang_doxgen_comment_middle")
    let g:clang_doxygen_comment_middle = "  * "
  endif

  if !exists("g:clang_doxygen_block_start")
    let g:clang_doxygen_block_start = "/** "
  endif

  if !exists("g:clang_doxygen_block_end")
    let g:clang_doxygen_block_end = "  */"
  endif
endif

function! s:GenerateDoxygen()
	python import sys
	exe 'python sys.path = ["' . s:plugin_path . '"] + sys.path'
	exe 'pyfile ' . s:plugin_path . '/clang_doxygen.py'

  python generateDoxygen()
endfunction

command! GenerateDoxygen call s:GenerateDoxygen()
