## setup my rofi`
#!/bin/zsh
[[ ! -d ~/.config/rofi/ ]] && mkdir -p ~/.config/rofi/
[[ ! -f ~/.config/rofi/config.rasi ]] && echo "~/.config/rofi/config.rasi exist;\n Please Remove Manually!" && ln -s ~/scripts/1-shell/dwm/config/rofi.rasi ~/.config/rofi/config.rasi
[[ ! -d ~/Github/rofi-themes-collection/ ]] && git clone https://github.com/lr-tech/rofi-themes-collection.git ~/Github/rofi-themes-collection
[[ ! -d ~/.local/share/rofi/themes ]] && mkdir -p ~/.local/share/rofi/themes/
cd ~/Github/rofi-themes-collection
[[ ! -f ~/.local/share/rofi/themes/rounded-common.rasi && ! -f ~/.local/share/rofi/themes/rounded-nord-dark.rasi ]] && ln -s ~/Github/rofi-themes-collection/themes/rounded-common.rasi ~/Github/rofi-themes-collection/themes/rounded-nord-dark.rasi ~/.local/share/rofi/themes/
echo "rounded-nord-dark" 
rofi-theme-selector
