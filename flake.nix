{
  description = "Dev env flake";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pre-commit-hooks.url = "github:cachix/pre-commit-hooks.nix";
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils,
    pre-commit-hooks,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
          config = {
            permittedInsecurePackages = ["wasm3-0.5.0"];
          };
        };
        checks = {
          pre-commit-check = pre-commit-hooks.lib.${system}.run {
            src = ./.;
            hooks = {
              alejandra.enable = true;
            };
          };
        };
      in {
        devShell = pkgs.mkShell {
          inherit (checks.pre-commit-check) shellHook;
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
      }
    );
}
