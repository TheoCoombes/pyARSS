# pyARSS
A Python wrapper for the Analysis &amp; Resynthesis Sound Spectrograph (ARSS)
* You can learn more about ARSS [here](http://arss.sourceforge.net/).

## Requirements
```
pip install -r requirements.txt
```
If you are using MacOS, you will need to install `ARSS` manually - [Download link](http://downloads.sourceforge.net/arss/arss-0.2.3-macosx-universal.dmg?use_mirror=osdn).
* If you initally encounter issues, try restarting your mac. If this persists, submit an issue on GitHub.

## Usage

```py
import pyARSS

# Encode 'inp.wav' into the image 'out.bmp'.
pyARSS.Encode("inp.wav", "out.bmp")

# You can then use this image for many different use cases, such as machine learning.

# Decode 'out.bmp' back into an audio file.
pyARSS.Decode("out.bmp", "new.wav")
```

pyARSS also supports custom audio file types, such as MP3:

```py
pyARSS.Encode("inp.mp3", "out.bmp")
```

You can also customise the settings used (reference):

```py
pyARSS.Encode(
    "/path/to/input.wav",
    "/path/to/output.bmp",
    min_frequency = 25, # 25 Hz; the minimum frequency until the data is discarded
    max_frequency = 20000, # 20,000 Hz; the maximum frequency until the data is discarded
    pps = 100, # Time resolution; pixels per second (PPS)
    bpo = 48   # Frequency resolution; bands per octave (BPO)
)

pyARSS.Decode(
    "/path/to/input.bmp",
    "/path/to/output.wav",
    min_frequency = 25, # 25 Hz; the minimum frequency until the data is discarded
    max_frequency = 20000, # 20,000 Hz; the maximum frequency until the data is discarded ***
    sample_rate = 44100, # The sample rate for the output audio file
    sine = True, # The synthesis method; sine is better for music whereas noise (sine=False) is better for speech etc.
    pps = 100, # Time resolution; pixels per second (PPS)
    bpo = 48   # Frequency resolution; bands per octave (BPO)
)

# *** pyARSS.Decode.max_frequency is discarded as there is a parameter limit on ARSS's executable.
```

## Licence
This repository is licenced under the [MIT licence](https://github.com/TheoCoombes/pyARSS/blob/main/LICENSE).
