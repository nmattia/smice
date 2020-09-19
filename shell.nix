let pkgs = import ./nix {}; in

pkgs.mkShell {

  buildInputs = with pkgs; [
    # System requirements.
    readline

    # Python requirements (enough to get a virtualenv going).
    python3Full
    python3Packages.virtualenv
    python3Packages.pip
    cmake
    x11
  ];

  SOURCE_DATE_EPOCH=315532800;
  LD_LIBRARY_PATH= "${pkgs.readline}/lib:${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.glib.out}/lib:${pkgs.xorg.libSM.out}/lib:${pkgs.xorg.libICE.out}/lib:${pkgs.xorg.libXrender}/lib:${pkgs.xorg.libXext}/lib:${pkgs.xorg.libX11}/lib";

}
