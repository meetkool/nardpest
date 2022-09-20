# sniffpest

started writing a clone of game i never even heard of
just to shove it in the faces of two morons on EFnet

_no ragrets_

```
python -m venv .venv
source .venv/bin/activate
pip install --no-binary=Pillow -r requirements.txt
python sniffpest.py
```

### i get a "munmap" error????
you probably left out the `--no-binary=Pillow` bit above.
to fix:
```
pip uninstall Pillow
pip install --no-binary=Pillow Pillow
```
