# Add nano as default editor
export EDITOR=nano
export TERMINAL=terminator
export BROWSER=google-chrome
export ANDROID_HOME=/opt/android-sdk
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk
export USE_CCACHE=1
export ANDROID_CCACHE_DIR=/home/xnn/.ccache
export ANDROID_CCACHE_SIZE="40G"
# Gtk themes
export GTK2_RC_FILES="$HOME/.gtkrc-2.0"

#alias ls='ls -la --color=auto'
alias df='df -h'

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

