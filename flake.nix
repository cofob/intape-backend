{
  description = "InTape backend";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    {
      # Nixpkgs overlay providing the application
      overlays.default = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
        (final: prev: {
          # Compose project src with migrations
          intape-src = prev.stdenv.mkDerivation {
            name = "intape-src";
            src = ./.;
            phases = [ "installPhase" ];
            installPhase = ''
              mkdir -p $out
              # main src
              cp -r $src/intape $out/intape
              chmod -R +w $out/intape
              cp $src/pyproject.toml $out/
              cp $src/poetry.lock $out/
              # migrations
              cp -r $src/migrations $out/intape/migrations
              cp $src/alembic.ini $out/intape/alembic.ini
            '';
          };
          # The application
          intape-app = prev.poetry2nix.mkPoetryApplication {
            projectDir = ./.;
            src = final.intape-src;
            python = prev.python3;
            overrides = prev.poetry2nix.overrides.withDefaults (self: super: {
              # My package dont work :(
              asyncipfscluster = super.asyncipfscluster.overridePythonAttrs (old: {
                propagatedBuildInputs = old.propagatedBuildInputs ++ [ self.poetry ];
              });

              # Watchfiles and friends
              # (watchfiles causes a build error, so we use version from nixpkgs)
              watchfiles = prev.python3Packages.watchfiles;
              idna = prev.python3Packages.idna;
              anyio = prev.python3Packages.anyio;
              sniffio = prev.python3Packages.sniffio;

              # Disable useless broken dependencies
              sqlalchemy2-stubs = null;
              mypy = null;
            });
          };
          # CLI proxy
          intape = prev.writeShellScriptBin "intape" ''
            cd ${final.intape-app}/${final.python3.sitePackages}/intape
            ${final.intape-app}/bin/intape $@
          '';
          # Docker entrypoint
          intape-entrypoint = prev.writeShellScriptBin "intape-entrypoint" ''
            # Check $MODE is set to "server"
            if [ "$MODE" = "server" ]; then
              intape run -m -w $WORKERS -p $PORT -h $HOST
            elif [ "$MODE" = "worker" ]; then
              intape worker
            else
              echo "ERROR: \$MODE is not set to \"server\" or \"worker\""
              exit 1
            fi
          '';
          # Docker healthcheck
          intape-healthcheck = prev.writeShellScriptBin "intape-healthcheck" ''
            # Check $MODE is set to "server"
            # If true, check API server is running
            if [ "$MODE" = "server" ]; then
              # curl "http://localhost:$PORT/v1/ping/"
              # check if answer is "ok"
              # if not, exit 1
              export ANSWER=$(${prev.curl}/bin/curl -s "http://localhost:$PORT/v1/ping/")
              if [ "$ANSWER" = '"ok"' ]; then
                exit 0
              else
                exit 1
              fi
            fi
          '';
          intape-docker = prev.dockerTools.buildLayeredImage {
            name = "intape";
            tag = "latest";
            contents = with final; [ intape intape-entrypoint intape-healthcheck busybox ];
            config = {
              Env = [
                "PORT=8000"
                "HOST=0.0.0.0"
                "WORKERS=1"
                "MODE=server"
              ];
              ExposedPorts = {
                "8000/tcp" = { };
              };
              Healthcheck = {
                Test = [ "CMD-SHELL" "intape-healthcheck" ];
                Interval = 3000000000;
                Timeout = 300000000;
                Retries = 3;
              };
              Cmd = [ "intape-entrypoint" ];
            };
          };
        })
      ];
    } // (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlays.default ];
        };
      in
      {
        packages = {
          default = pkgs.intape;
          app = pkgs.intape;
          docker = pkgs.intape-docker;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            poetry
            gcc
          ];
          shellHook = "source setup.sh";
        };
      }));
}
