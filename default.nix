{ nixpkgs ? <nixpkgs> }:

let pkgs = import nixpkgs { config = {}; };
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    python36Packages.numpy python36Packages.pyyaml python36Packages.matplotlib python36Packages.jupyterlab
    wineFull winetricks
  ];

  shellHook = ''
  # Development environment
  export NIX_PATH="nixpkgs=nixpkgs:."

  # Install wine tricks and srim
  winetricks vb5run comdlg32ocx msflxgrd
  bash install.sh

  # Assumes that nix-shell is run in directory
  export PYTHONPATH=$PWD:$PYTHONPATH
  '';
}
