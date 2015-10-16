# i21 beamline profile

if [ ! -n "$BEAMLINE" ]; then
  echo "ERROR: BEAMLINE not set" 1>&2
  exit 1
fi

export PATH=/dls_sw/$BEAMLINE/software/gda/workspace_git/gda-dls-beamlines-i21.git/i21-config/bin:${PATH}
export GDA_MODE=live