""""""""""""""""""""""""""""""""""""""""""""""""""
" Description:
"   This is the .vimrc file
"
" Maintainer:
"   Cédric FARINAZZO
"   <cedric.farinazzo@gmail.com>
""""""""""""""""""""""""""""""""""""""""""""""""""


""" Base

" Enable filetype detection for plugins and indentation options
filetype indent plugin on

" Force encoding to utf-8
set encoding=utf-8 fileencodings=

" This changes the values of a LOT of options, enabling
" features which are not Vi compatible but really really nice.
set nocompatible

set term=rxvt-unicode-256color

" Mouse integration
set mouse=a

" Enables syntax highlighting
syntax on

" Show command being executed
set showcmd

" Show line number
set number

" Hide buffers instead of closing them
set hidden

" Prevent the cursor from changing the current column
" when jumping to other lines within the window
set nostartofline

set ruler

" Highlight current line
set cursorline

" Reload a file when it is changed from the outside
set autoread

" Write the file when we leave the buffer
set autowrite

" The length of time Vim waits after you stop typing before it triggers
" the plugin is governed
set updatetime=500

" Always show status line
set laststatus=2

" Disable swapfiles too
set noswapfile

""" Search

" Move cursor to the matched string
set incsearch

" Highlight matched strings
set hlsearch

" Ignore case on search
set ignorecase

" Ignore case unless there is an uppercase letter in the pattern
set smartcase

" Briefly show matching braces, parens, etc
set showmatch

" Disable preview window on completion
set completeopt=menu,longest

" Enhance command line completion
set wildmenu

" Set completion behavior, see :help wildmode for details
set wildmode=longest:full,list:full

set confirm

""" Indent && Coding Style

" Make backspace behave as expected
set backspace=indent,eol,start

" Wrap on column 80
"set textwidth=79

" Color the column after textwidth, usually the 80th
if version >= 703
    set colorcolumn=+1
endif
set colorcolumn=80

" Enable line wrapping
" set wrap

" The length of a tab
" This is for documentation purposes only,
" do not change the default value of 8, ever.
set tabstop=4

" The number of spaces inserted/removed when using < or >
set shiftwidth=4

" The number of spaces inserted when you press tab.
" -1 means the same value as shiftwidth
set softtabstop=-1

" Insert spaces instead of tabs
set expandtab

" When tabbing manually, use shiftwidth instead of tabstop and softtabstop
set smarttab

" Automatically inserts one extra level of indentation
set smartindent

" Set basic indenting (i.e. copy the indentation of the previous line)
" When filetype detection didn't find a fancy indentation scheme
set autoindent

" Indentation options. See :help cinoptions for details
set cinoptions=(0,u0,U0,t0,g0,N-s

" Display whitespace characters
set list
set listchars=tab:>-,eol:¬,trail:\ ,nbsp:¤

" Remove all trailing whitespace by pressing F5
nnoremap <F5> :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar><CR>

" Highligh all trailing whitespace
highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$\| \+\ze\t/

" Remove all trailing whitespace before saving file for C/C++ files, Headers
" and Makefile
autocmd BufWritePre *.c %s/\s\+$//e
autocmd BufWritePre *.h %s/\s\+$//e
autocmd BufWritePre *.cc %s/\s\+$//e
autocmd BufWritePre *.hh %s/\s\+$//e
autocmd BufWritePre *.hxx %s/\s\+$//e
autocmd BufWritePre *.py %s/\s\+$//e
autocmd BufWritePre Makefile %s/\s\+$//e

" enable syntax highlighting for code in markdown file
let g:markdown_fenced_languages = ['html', 'vim', 'php', 'python', 'bash=sh', 'c', 'cpp', 'md']

""" Persistence

" Set location of the viminfo file
set viminfo='20,\"50,<100,n~/.vimtmp/viminfo

" See :h last-position-jump
augroup last_position_jump
    au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g`\"" | endif
augroup END

" Persistent undo
if version >= 703
    set undofile
    set undodir=~/.vimtmp/undo
    silent !mkdir -p ~/.vimtmp/undo
endif


""" Mappings

" in normal mode F2 will save the file
nmap <F2> :w<CR>
" in edit mode F2 will exit insert, save the file, enters insert again
imap <F2> <ESC>:w<CR>i<right>

" build using make with <F5>
map <F5> :make<CR>
" make clean with <F6>
map <F6> :make clean<CR>
" make _check with <F7>
map <F7> :make _check<CR>
" open the quickfixlist with <F8>
map <F8> :cope<CR>

" switch between header/source with F4
map <F4> :e %:p:s,.h$,.X123X,:s,.c$,.h,:s,.X123X$,.c,<CR>

" clang format
map <C-K> :pyf /usr/share/clang/clang-format.py<CR>
imap <C-K> <c-o>:pyf /usr/share/clang/clang-format.py<CR>

""" Functions

function! PlugLoaded(name)
    return (
                \ has_key(g:plugs, a:name) &&
                \ isdirectory(g:plugs[a:name].dir))
endfunction

""" Plugins

" Add the termdebug built-in plugin
if version >= 801
    packadd termdebug
endif

" Install vim-plug if we don't already have it
" Credit to github.com/captbaritone
if empty(glob("~/.vim/autoload/plug.vim"))
    " Ensure all needed directories exist  (Thanks @kapadiamush)
    silent execute '!mkdir -p ~/.vim/plugged'
    silent execute '!mkdir -p ~/.vim/autoload'
    " Download the actual plugin manager
    silent execute '!curl -fLo ~/.vim/autoload/plug.vim https://raw.github.com/junegunn/vim-plug/master/plug.vim'
endif

call plug#begin('~/.vim/plugged')

" airline theme
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'

" files tree
Plug 'scrooloose/nerdtree'
Plug 'Xuyuanp/nerdtree-git-plugin'

" check
Plug 'scrooloose/syntastic'

" comment helper
Plug 'scrooloose/nerdcommenter'

" git
Plug 'tpope/vim-fugitive'
Plug 'airblade/vim-gitgutter'

" tags
Plug 'ludovicchabant/vim-gutentags'
Plug 'majutsushi/tagbar'

" snippets
Plug 'MarcWeber/vim-addon-mw-utils'
Plug 'tomtom/tlib_vim'
Plug 'garbas/vim-snipmate'
Plug 'honza/vim-snippets'

" Tiger
Plug 'CohenArthur/tiger-vim'

" Fun
Plug 'johngrib/vim-game-code-break'

call plug#end()


""" Plugins config

"" NerdTree
if PlugLoaded('nerdtree')

    " Add spaces after comment delimiters by default
    let g:NERDSpaceDelims = 1

    " Use compact syntax for prettified multi-line comments
    let g:NERDCompactSexyComs = 1

    " Align line-wise comment delimiters flush left instead of following code indentation
    let g:NERDDefaultAlign = 'left'

    " Set a language to use its alternate delimiters by default
    let g:NERDAltDelims_java = 1

    " Add your own custom formats or override the defaults
    let g:NERDCustomDelimiters = { 'c': { 'left': '/**','right': '*/' } }

    " Allow commenting and inverting empty lines (useful when commenting a region)
    let g:NERDCommentEmptyLines = 1

    " Enable trimming of trailing whitespace when uncommenting
    let g:NERDTrimTrailingWhitespace = 1

    " Enable NERDCommenterToggle to check all selected lines is commented or not
    let g:NERDToggleCheckAllLines = 1

    autocmd StdinReadPre * let s:std_in=1
    autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif

    autocmd StdinReadPre * let s:std_in=1
    autocmd VimEnter * if argc() == 1 && isdirectory(argv()[0]) && !exists("s:std_in") | exe 'NERDTree' argv()[0] | wincmd p | ene | endif

    map <C-t> :NERDTreeToggle<CR>

    autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif

    let g:NERDTreeDirArrowExpandable = '▸'
    let g:NERDTreeDirArrowCollapsible = '▾'
    let NERDTreeShowHidden=1
endif

"" Airline

if PlugLoaded('vim-airline')

    set noshowmode

    let g:airline_left_sep = ''
    let g:airline_left_alt_sep = ''
    let g:airline_right_sep = ''
    let g:airline_right_alt_sep = ''
    let g:airline_symbols = {
                \ 'paste': 'PASTE',
                \ 'spell': 'SPELL',
                \ 'readonly': 'RO',
                \ 'whitespace': '!',
                \ 'linenr': 'ln',
                \ 'maxlinenr': ':',
                \ 'branch': '',
                \ 'notexists': '?',
                \ 'modified': '+',
                \ 'space': ' ',
                \ 'crypt': 'cr',
                \ }


    let g:airline#extensions#tabline#enabled = 1

    let g:airline#extensions#tagbar#flags = 'f'

    let g:airline#extensions#tabline#formatter = 'default'

    let g:airline_theme='dark_minimal'

endif

"" Syntastic

if PlugLoaded('syntastic')

    let g:syntastic_always_populate_loc_list = 0
    let g:syntastic_auto_loc_list = 0
    let g:syntastic_check_on_open = 1
    let g:syntastic_check_on_wq = 1
    let g:syntastic_c_include_dirs = [ '.', '../include', 'include', 'src', '../src' ]
    " let g:loaded_syntastic_cmake_cmakelint_checker = 1
    let g:syntastic_c_check_header = 1
    let g:syntastic_cpp_compiler = 'clang++'
    let g:syntastic_cpp_compiler_options = ' -Wall -Wextra -std=c++17'

endif

"" vim-gitgutter

if PlugLoaded('vim-gitgutter')

    highlight GitGutterAdd    guifg=#009900 guibg=#00151B ctermfg=2 ctermbg=0
    highlight GitGutterChange guifg=#bbbb00 guibg=#00151B ctermfg=3 ctermbg=0
    highlight GitGutterDelete guifg=#ff2222 guibg=#00151B ctermfg=1 ctermbg=0

    let g:gitgutter_sign_added = '+'
    let g:gitgutter_sign_modified = '~'
    let g:gitgutter_sign_removed = '-'
    let g:gitgutter_sign_removed_first_line = '-'
    let g:gitgutter_sign_modified_removed = '~~'

endif


"" tagbar

if PlugLoaded('tagbar')

    map <F9> :TagbarToggle<CR>

endif
