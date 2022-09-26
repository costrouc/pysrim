{ pkgs ? import <nixpkgs> {}, pythonPackages ? "python3Packages" }:

rec {
  package = pythonPackages.buildPythonPackage rec {
    pname = "pysrim";
    version = "master";
    disabled = pythonPackages.isPy27;

    src = ./.;

    buildInputs = with pythonPackages; [
      pytestrunner
    ];

    checkInputs = with pythonPackages; [
      pytest
      pytestcov
      pytest-mock
     ];

    propagatedBuildInputs = with pythonPackages; [
      numpy
      pyyaml
    ];

    checkPhase = ''
      pytest
    '';
  };

  docs = pkgs.stdenv.mkDerivation {
    name = "docs";
    version = "master";

    src = ./.;

    buildInputs = with pythonPackages; [
      package
      sphinx
      sphinx_rtd_theme
    ];

    buildPhase = ''
      cd docs;
      sphinx-apidoc -o source/ ../srim
      sphinx-build -b html -d build/doctrees . build/html
    '';

    installPhase = ''
     mkdir -p $out
     cp -r build/html/* $out
    '';
  };
}
