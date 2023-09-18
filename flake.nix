{
  description = "Dev env flake";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
        config = {
          permittedInsecurePackages = ["wasm3-0.5.0"];
        };
      };
    in {
      devShell = pkgs.mkShell {
        buildInputs = [
          # Python toolchain
          pkgs.poetry
          pkgs.mypy
          # Command runner
          pkgs.just
          # CLI hex files viewer
          pkgs.hexd
          # Wasm toolchain
          pkgs.wabt
          pkgs.wasmer
          pkgs.wasm3
        ];
      };
    });
}
