{ pkgs, nodejs, ... }: (pkgs.callPackage ./frontend { inherit nodejs; })
