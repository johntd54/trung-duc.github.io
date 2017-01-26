---
layout: post
title: "170117 - Vim cheatsheet"
date: 2017-01-17 23:45:06
categories: vim
---

To remember:
- `operator [number] motion`: perform the operation [number] of times. If [number] is not specified, then perform 1 time. Example: `dd` deletes a line, `d2d` or `2dd` deletes 2 lines; `j` moves the cursor down 1 line, `10j` moves the cursor down 10 lines


Move around:

- `h` to move left
- `j` to move down
- `k` to move up
- `l` to move right
- `0` to move to the begin of line
- `^` to move to the first non-space character of line
- `$` to move to the end of line
- `gg` to move to the first line of file
- `G` to move to the last line of file
- `w` to move to the beginning of next word
- `e` to move to the end of next word
- `[number]G` to move to the specified line number
- `%` to move/alternate between beginning and ending '( )', '[ ]' and '{ }' characters, if the cursor is currently in/on those characters
- Ctrl-O to move the cursor back to where you were, repeat to go further
- Ctrl-I to is the reverse of Ctrl-0


File operations:

- `:q!` to quit without change
- `:wq` to write/save and quit
- `:w [filename]` to write the text to that file
- `vim [filename]` to open a file with vim
- Ctrl-G to show location of the file and file status
- `/[term]` to search the term from the begin of file, use `n` and `N` to search forward, backward respectively
- `?[term]` to search the term from the end of file, use `N` and `n` to search forward, backward respectively
    + `:set ic` to ignore case-sensitivity and `:set noic` to turn it off
    + `:set hls` to set highlight search and `:set nohls` to turn it off, `:nohlsearch` to temporarily turn the color off
    + `:set is` to set incremental search and `:set nois` to turn it off
- `:![command]` to execute any terminal command. Example `:!cd ..`, `:!pwd``, `:!ls`,...
- `v` to start visual mode
- `y` to yank (copy), (to paste it, move the cursor to desired location and `p`)
- `y` is an operator, and can work with motion like ("Move around" section above)


Delete operations:

- `x` to delete the character at cursor
- `dw` to delete a word, and the spaces leading to the next word (the cursor must be at the first character of the word to delete)
- `de` to delete a word only (the cursor must be at the first character of the word to delete)
- `d$` to delete from the cursor to the end of line
- `dd` to delete line


Add texts:

- `i` to insert before the cursor
- `a` to insert after the cursor (basically to append to a line)
- `A` to append at the end of the line
- `p` to put the previously deleted texts
- `:r [filename]` to insert the content of the file below the current cursor
- `:r ![command]` to insert output of the command below the current cursor
- `o` to make and move to a new line under the cursor
- `O` to make and move to a new line above the cursor


Edit texts:

- `u` to undo the last change
- `U` to undo the last changes in the whole line
- Ctrl-R to undo the undo
- `r[character]` to replace the character at the cursor
- `R` to replace multiple characters
- `ce` to change until the end of the word (kind of a shorthand for `de` then `i`, without having to have the cursor at the beginning of the word)
- `c$` to change until the end of line (kind of a shorthand for `d$` then `i`)
- `:s/[old]/[new]` to substitute the first occurence of old word with new word *in the current line*
- `:s/[old]/[new]/g` to substitute all old words with new word *in the current line*
- `:[number_small],[number_large]s/[old]/[new]/g` to substitute all old words with new word between line [number_small] and line [number_large]
- `:%s/old/new/g` to substitute all old words with new word *in the file*
- `:%s/old/new/gc` to substitue all old words with new word *in the file* but with notifying prompt for each change occurence
    + `y` to replace
    + `n` to skip
    + `a` to replace and end all substitution there
    + `q` to abort
    + `l`: like `a` but will also move the cursor to begin of line


Efficiency:

- `:ab [abbreviated] [term]` to create an abbreviation of term

