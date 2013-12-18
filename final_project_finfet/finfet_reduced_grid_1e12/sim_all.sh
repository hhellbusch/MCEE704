#!/bin/bash

echo "deckbuild -run -ascii atlas_idvg_low.in -outfile sim_log_idvg.txt && ./notify.py" | at -m now
echo "deckbuild -run -ascii atlas_idvg_high.in -outfile sim_log_idvg.txt && ./notify.py" | at -m now
echo "deckbuild -run -ascii atlas_family.in -outfile sim_log_family.txt && ./notify.py" | at -m now