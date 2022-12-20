{ pkgs ? import <nixpkgs> {} }:
let
  pythonPackages = (p: with p; [
    selenium
    beautifulsoup4
  ]);
  customPython310 = pkgs.python310.withPackages pythonPackages;
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    customPython310
    geckodriver
    libxml2
  ];
  packages = with pkgs; [
    starship
  ];
  shellHook = ''
    set -o vi
    tmp=$(mktemp)
    starship init bash > $tmp
    source $tmp
    export LANG=pt_BR.UTF-8
    export LOCALE=pt_BR.UTF-8
    export LC_ALL=pt_BR.UTF-8
    alias xml='xmllint --format '
  '';
}
