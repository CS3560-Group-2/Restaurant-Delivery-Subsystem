{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = [
    pkgs.libgcc
    pkgs.pkg-config
    pkgs.git
    pkgs.neovim
    pkgs.nodejs
    pkgs.ripgrep
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.python3Packages.virtualenv
    pkgs.python3Packages.tkinter
    pkgs.python3Packages.mysql-connector
    pkgs.rustc
    pkgs.cargo
    pkgs.vimPlugins.nvchad
    pkgs.mysql84
  ];
  
  shellHook = ''
    if [ ! -d .venv ]; then
      python -m venv .venv
    fi
    source .venv/bin/activate
  '';
}  
