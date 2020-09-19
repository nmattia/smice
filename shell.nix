let pkgs = import ./nix {}; in

pkgs.mkShell {

  buildInputs = with pkgs; [
    # System requirements.
    readline

    # Python requirements (enough to get a virtualenv going).
    python3Full
    python3Packages.virtualenv
    python3Packages.pip
    python3Packages.pysdl2
  ];

  SOURCE_DATE_EPOCH=315532800;
  LD_LIBRARY_PATH= "${pkgs.readline}/lib";

}
