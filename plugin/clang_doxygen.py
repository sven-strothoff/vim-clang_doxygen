# Vim plugin for generating Doxygen comments
# Last Change:  2013 Jan 18
# Maintainer:   Sven Strothoff <sven.strothoff@googlemail.com>
# License:      See documentation (clang_doxygen.txt)
# 
# Copyright (c) 2013, Sven Strothoff
# All rights reserved.

import vim
from clang.cindex import Index, SourceLocation, Cursor, File, CursorKind, TypeKind

# Generate doxygen comments for a function declaration.
# Also generates XPTemplate placeholders.
def handleFunctionDecl(c):
  tabStopCounter = 1
  doxygenLines = []
  functionName = c.spelling
  doxygenLines.append("/// \\brief ${" + str(tabStopCounter) + ":" + functionName + "}")
  tabStopCounter += 1
  doxygenLines.append("/// ")
  doxygenLines.append("/// $0")

  # Extract parameters.
  # Only supported by libClang >= 3.1
  #n = c.get_num_arguments()
  #for i in xrange(0, n):
  #  print "  Argument: %s" % c.get_argument(i).spelling
  paramLines = []
  children = c.get_children()
  for arg in children:
    if arg.kind != CursorKind.PARM_DECL:
      continue
    paramLines.append("/// \\param " + arg.spelling + " ${" + str(tabStopCounter) + ":" + arg.spelling + "}")
    tabStopCounter += 1
  if len(paramLines) > 0:
    doxygenLines.append("/// ")
  doxygenLines += paramLines

  # Check result type.
  if (c.type.get_result().kind != TypeKind.VOID):
    doxygenLines.append("/// ")
    doxygenLines.append("/// \\return ${" + str(tabStopCounter) + ":" + c.type.get_result().kind.spelling + "}")
    tabStopCounter += 1

  # Add indentation.
  # Comment indentation should match the indentation of the line containing the
  # declaration name, however clang_getSpellingLocation() ist note exposed by
  # the Python bindings.
  tabCount = vim.current.buffer[c.location.line - 1][:c.location.column - 1].count('\t')
  indent = (c.extent.start.column - 1 - tabCount) + tabCount * int(vim.eval("&tabstop"))
  indentString = indent * " "
  for l in xrange(0, len(doxygenLines)):
    doxygenLines[l] = indentString + doxygenLines[l]

  return (c.extent.start.line, doxygenLines)

# Return buffer contents between the specified source locations. Returns lines
# in an array.
def getBufferContent(startLine, startCol, endLine, endCol):
  resultLines = vim.current.buffer[startLine - 1:endLine]
  if startLine == endLine:
    resultLines[0] = resultLines[0][startCol - 1:endCol]
  else:
    resultLines[0] = resultLines[0][startCol - 1:]
    resultLines[-1] = resultLines[-1][:endCol]
  return resultLines

# Generate doxygen comments for a function template.
# Also generates XPTemplate placeholders.
def handleFunctionTemplate(c):
  tabStopCounter = 1
  doxygenLines = []
  functionName = c.spelling
  doxygenLines.append("/// \\brief ${" + str(tabStopCounter) + ":" + functionName + "}")
  tabStopCounter += 1
  doxygenLines.append("/// ")
  doxygenLines.append("/// $0")

  # Extract parameters.
  paramLines = []
  children = c.get_children()
  for arg in children:
    if arg.kind != CursorKind.PARM_DECL:
      continue
    paramLines.append("/// \\param " + arg.spelling + " ${" + str(tabStopCounter) + ":" + arg.spelling + "}")
    tabStopCounter += 1
  if len(paramLines) > 0:
    doxygenLines.append("/// ")
  doxygenLines += paramLines

  # Find TemplateTypeParameter to determine result type.
  templateTypeParameterCursor = None
  for child in c.get_children():
    if child.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
      templateTypeParameterCursor = child
      break
  if templateTypeParameterCursor is None:
    print "Unable to find TemplateTypeParameter."
    return (None, None)
  
  # Get result type string(s).
  startLine = templateTypeParameterCursor.extent.end.line
  startCol = templateTypeParameterCursor.extent.end.column + 1
  endLine, endCol = previousSourceLocation(c.location.line, c.location.column)
  resultLines = getBufferContent(startLine, startCol, endLine, endCol)

  # Check if the result type is void; if not extract result type string.
  blockCommentRegex = re.compile(r"/\*.*?\*/", re.DOTALL)
  resultString = re.sub(blockCommentRegex, "", "\n".join(resultLines))
  if re.search(r"void", resultString) is None:
    doxygenLines.append("/// ")
    doxygenLines.append("/// \\return ${" + str(tabStopCounter) + ":" + c.type.get_result().kind.spelling + "}")
    tabStopCounter += 1

  # Add indentation.
  # Comment indentation should match the indentation of the line containing the
  # declaration name, however clang_getSpellingLocation() ist note exposed by
  # the Python bindings.
  tabCount = vim.current.buffer[c.location.line - 1][:c.location.column - 1].count('\t')
  indent = (c.extent.start.column - 1 - tabCount) + tabCount * int(vim.eval("&tabstop"))
  indentString = indent * " "
  for l in xrange(0, len(doxygenLines)):
    doxygenLines[l] = indentString + doxygenLines[l]

  return (c.extent.start.line, doxygenLines)

# Returns the previous source location or None if already at the beginning of
# the buffer.
def previousSourceLocation(line, col):
  if col > 1:
    return (line, col - 1)
  if line == 1:
    return None
  return (line - 1, len(vim.current.buffer[line - 2]))

# Returns the next source location or None if already at the end of
# the buffer.
def nextSourceLocation(line, col):
  if col < len(vim.current.buffer[line - 1]):
    return (line, col + 1)
  if line == len(vim.current.buffer):
    return None
  return (line + 1, 1)

# Generate doxygen for declaration at specified source location.
# Returns a tuple consisting of the line number at which the doxygen comment
# should be inserted and the doxygen comment as an array (one line per element).
def generateDoxygenForSourceLocation(line, col):
  filename = vim.current.buffer.name

  index = Index.create()
  tu = index.parse(filename, vim.eval("g:clang_doxygen_clang_args"), [(filename, "\n".join(vim.current.buffer[:]))])

  # Skip whitespace at beginning of line
  indent = re.match(r'^\s*', vim.current.buffer[line - 1]).span()[1]
  col = max(col, indent + 1)

  c = Cursor.from_location(tu, SourceLocation.from_position(tu, File.from_name(tu, filename), line, col))

  # If there is no declaration at the source location try to find the nearest one.
  while c is not None and c.kind != CursorKind.FUNCTION_DECL and c.kind != CursorKind.FUNCTION_TEMPLATE:
    # If cursor is on a TypeRef in a FunctionTemplate manually go backwards in the source.
    if c.kind == CursorKind.TYPE_REF:
      pLine, pCol = previousSourceLocation(c.extent.start.line, c.extent.start.column)
      c = Cursor.from_location(tu, SourceLocation.from_position(tu, File.from_name(tu, filename), pLine, pCol))
      continue
    c = c.lexical_parent

  if c is None:
    print "Error: No function decl found at %s:%i,%i.\n" % (filename, line, col)
    return (None, None)
  elif c.kind == CursorKind.FUNCTION_DECL:
    return handleFunctionDecl(c)
  elif c.kind == CursorKind.FUNCTION_TEMPLATE:
    return handleFunctionTemplate(c)

# Generate Doxygen comments for the current source location.
def generateDoxygen():
  # First line is 1, first column is 0
  (line, col) = vim.current.window.cursor

  (insertLine, doxygenLines) = generateDoxygenForSourceLocation(line, col + 1)
  if doxygenLines is None:
    return
  vim.current.buffer.append("", insertLine - 1)
  vim.current.window.cursor = (insertLine, 0)
  # Call snippet plugin
  vim.command('call clang_doxygen_snippets#' + vim.eval("g:clang_doxygen_snippet_plugin") + '#trigger(\'' + "\n".join(doxygenLines).replace("\\", "\\\\") + '\')')
