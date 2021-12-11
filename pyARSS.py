from subprocess import run, PIPE
from pydub import AudioSegment
from platform import system
from os import path as pth
from uuid import uuid4
from os import remove

sys = system()
supported = ["Windows", "Linux", "Darwin"]

if sys not in supported:
    raise RuntimeError("Invalid operating system. pyARSS only supports Windows, MacOS and Linux")


# Set ARSS run command for the correct platform
modpth = pth.abspath(__file__)
moddir = pth.dirname(modpth)
if sys == "Windows":
    cmd = moddir + "\\bin_windows\\arss"
elif sys == "Linux":
    cmd = moddir + "/bin_linux/arss"
else:
    cmd = "arss" # MacOS requires ARSS to be directly installed via the installer.


# Encodes audio file `input_path` into image file `output_path` using ARSS.
def Encode(input_path : str, output_path : str,
           min_frequency = 27,
           max_frequency = 20000,
           pps = 100,
           bpo = 48):
    
    # Change paths to absolute paths to avoid errors with ARSS.
    input_path = pth.abspath(input_path)
    output_path = pth.abspath(output_path)

    uuid = None
    if not input_path.endswith(".wav"):
        # Assume we need to convert the file.
        if not input_path.endswith(".mp3"):
            # Validate input_path input.
            
            # Raise an error if the user inputted an invalid file type.
            if "." in input_path:
                raise ValueError("The input_path must be a WAV file or an MP3 file.")

            # Raise an error if the user inputted a directory.
            elif input_path[-1] in ["\\", "/"]:
                raise ValueError("The input_path must be a file path, not a directory.")

            # Raise generic error.
            else:
                raise ValueError("The input_path must contain a path to an MP3 or WAV file.")
        
        # Generate temporary WAV file from MP3.
        new = AudioSegment.from_mp3(input_path)
        uuid = "_pyARSS_temp_" + uuid4().hex + ".wav"
        new.export(uuid, format="wav")
    
    # Validate output_path input.
    if not output_path.endswith(".bmp"):
        # Raise an error if the user inputted an invalid file type.
        if "." in output_path:
            raise ValueError("The output_path must be a BMP file.")

        # Raise an error if the user inputted a directory.
        elif output_path[-1] in ["\\", "/"]:
            raise ValueError("The output_path must be a file path, not a directory.")

        # Raise generic error.
        else:
            raise ValueError("The output_path must contain a path to the new BMP file.")
    
    # Run the main ARSS executable.
    result = run([
        cmd, "-q",
        pth.abspath(uuid) if uuid is not None \
            else input_path,                 # Input file     
        output_path,                         # Output file
        "--analysis",                        # Type
        "--min-freq", str(min_frequency),    # Minimum frequency
        "--max-freq", str(max_frequency),    # Maximum frequency
        "--pps", str(pps),                   # Time resolution (pixels per second)
        "--bpo", str(bpo)                    # Frequency resolution (bands per octave)
    ], stderr=PIPE, universal_newlines=True)

    # Remove temporary WAV file.
    if uuid is not None:
        remove(uuid)
        
    # Check and raise ARSS errors.
    if result.returncode != 0:
        raise RuntimeError(result.stderr)

        
# Decodes image file `input_path` into audio file `output_path` using ARSS.
def Decode(input_path : str, output_path : str,
           min_frequency = 27,
           max_frequency = 20000,
           sample_rate = 44100,
           sine = True,
           pps = 100,
           bpo = 48):
        
    # Change paths to absolute paths to avoid errors with ARSS.
    input_path = pth.abspath(input_path)
    output_path = pth.abspath(output_path)
    
    # Validate input_path input.
    if not input_path.endswith(".bmp"):
        # Raise an error if the user inputted an invalid file type.
        if "." in input_path:
            raise ValueError("The input_path must be a BMP file.")

        # Raise an error if the user inputted a directory.
        elif input_path[-1] in ["\\", "/"]:
            raise ValueError("The input_path must be a file path, not a directory.")

        # Raise generic error.
        else:
            raise ValueError("The input_path must contain a path to the BMP file.")

    # Validate output_path input.
    if not output_path.endswith(".wav") and not output_path.endswith(".mp3"):
        # Raise an error if the user inputted an invalid file type.
        if "." in output_path:
            raise ValueError("The output_path must be a WAV file or an MP3 file.")
        
        # Raise an error if the user inputted a directory.
        elif output_path[-1] in ["\\", "/"]:
            raise ValueError("The output_path must be a file path, not a directory.")
        
        # Raise generic error.
        else:
            raise ValueError("The output_path must contain a path to an MP3 or WAV file.")
    
    # Should pyARSS create a temporary WAV file?
    # ARSS only supports waveform files.
    if not output_path.endswith(".wav"):
        uuid = "_pyARSS_temp_" + uuid4().hex + ".wav"
    else:
        uuid = None
    
    # Run the main ARSS executable.
    result = run([
        cmd, "-q",
        input_path,                          # Input file
        pth.abspath(uuid) if uuid is not None \
            else output_path,                # Output file
        "--sine" if sine else "--noise",     # Type
        "--sample-rate", str(sample_rate),   # Sample rate
        "--min-freq", str(min_frequency),    # Minimum frequency
        # "--max-freq", str(max_frequency),  # Maximum frequency -- TODO: ARSS: "You have set one parameter too many"
        "--pps", str(pps),                   # Time resolution (pixels per second)
        "--bpo", str(bpo)                    # Frequency resolution (bands per octave)
    ], stderr=PIPE, universal_newlines=True)

    # Raise error if ARSS failed.
    if result.returncode != 0:
        try:
            # Attempt to remove the temporary WAV file if it was generated.
            remove(uuid)
        except:
            pass
        raise RuntimeError(result.stderr)
    
    # Convert the file if required.
    if uuid is not None:
        # Load WAV and convert MP3.
        new = AudioSegment.from_wav(uuid)
        new.export(output_path, format="mp3")
        
        # Remove temporary WAV file.
        remove(uuid)
