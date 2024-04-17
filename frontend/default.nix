{ nodejs, buildNpmPackage, ... }:

buildNpmPackage {
   name = "frontend";
   inherit nodejs;
   npmDepsHash = "sha256-R6sJIGV9ywdwvYrdLP5gazImVLMGbapm9nELB9UTPQk=";
   src = ./.;
}
