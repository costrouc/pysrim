{ pkgs ? import <nixpkgs> { } }:

let build = import ./build.nix {
      inherit pkgs;
      pythonPackages = pkgs.python3Packages;
    };
in {
  pysrim = build.package;
  pysrim-docs = build.docs;
}
