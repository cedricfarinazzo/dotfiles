# If you come from bash you might have to change your $PATH.
 export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="/home/$USER/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="zeroastro"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in ~/.oh-my-zsh/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to automatically update without prompting.
# DISABLE_UPDATE_PROMPT="true"

# Uncomment the following line to change how often to auto-update (in days).
export UPDATE_ZSH_DAYS=30

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS=true

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
    archlinux
    git
    command-not-found
    python
    web-search
    colored-man-pages
    docker
    ssh-agent
    thefuck
    timer
    zsh-interactive-cd
)

source $ZSH/oh-my-zsh.sh

ZSH_AUTOSUG=/usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
if [ -f $ZSH_AUTOSUG ]; then
    source $ZSH_AUTOSUG
fi
ZSH_AUTOSUG=

ZSH_SYNTAX_HGL=/usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
if [ -f $ZSH_SYNTAX_HGL ]; then
    source $ZSH_SYNTAX_HGL
fi
ZSH_SYNTAX_HGL=

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
export EDITOR='vim'

# Compilation flags
export CC=gcc
export ARCHFLAGS="-arch x86_64"
export CFLAGS="-Wall -Wextra -Werror -pedantic -std=c99"
export _DEBUG="-fsanitize=address -g3"

export CRITERION_VERBOSITY_LEVEL=1

# ssh
export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

alias gti="git"

alias ccd="${CC} ${CFLAGS}"
alias ccdd="${CC} ${_DEBUG} ${CFLAGS}"
alias mkd="make DEBUG=\"${_DEBUG}\""
alias scmk="scan-build -analyze-headers -v -V -stats -maxloop 64 -o report make -j4"

alias cppd="g++ -Wall -Wextra -Werror -pedantic -std=c++17"
alias cppdd="g++ -fsanitize=address -g3 -Wall -Wextra -Werror -pedantic -std=c++17"

if [ -f $HOME/.zshrc.local ]; then
    . $HOME/.zshrc.local
fi

kcn () {
    if [[ "${#}" -ne 1 ]]
    then
        echo "USAGE: kcn <namespace>"
        return 1
    fi
    kubectl config set-context "$(kubectl config current-context)" --namespace="${1}"
}
alias k="kubectl"
[[ $commands[kubectl] ]] && source <(kubectl completion zsh)

zsh -c 'screenfetch -D arch'
