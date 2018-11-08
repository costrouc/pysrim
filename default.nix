{ nixpkgs ? <nixpkgs> }:

let pkgs = import nixpkgs { config = {}; };
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    python36Packages.numpy
    python36Packages.pyyaml
    python36Packages.matplotlib
    python36Packages.jupyterlab

    # testing
    python36Packages.pytest
    python36Packages.pytest-mock

    # Required for running srim
    wineFull winetricks
  ];

  shellHook = ''
  # Development environment
  export NIX_PATH="nixpkgs=nixpkgs:."

  # Install wine tricks and srim
  winetricks vb5run comdlg32ocx msflxgrd
  if [ ! -d /tmp/srim ]; then
    bash install.sh
  fi

  # Assumes that nix-shell is run in directory
  export PYTHONPATH=$PWD:$PYTHONPATH
  '';
}
