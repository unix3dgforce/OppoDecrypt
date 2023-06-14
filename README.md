# OppoDecrypt
Oppo .ofp Firmware decrypter

Installation:
-------------
- Install >= python 3.10 and poetry

In the console, run
```bash
poetry install
```

Usage:
-------- 
* Extract oppo ofp file:

```
python3 OppoDecrypt [file.ofp] [directory to extract]
```


* Merge super images:

The .ofp may contain super firmware from multiple carriers, check the super_map.csv.txt outside .ofp first.

```
sudo apt install simg2img # If you have already installed, skip this step.
simg2img [super.0.xxxxxxxx.img] [super.1.xxxxxxxx.img] [super.1.xxxxxxxx.img] [filename to merge] # All split super imgs must be the same carrier
```

Thanks:
-------- 
- [Bjoern Kerler](https://github.com/bkerler)