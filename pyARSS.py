from subprocess import run, PIPE
from pydub import AudioSegment
from platform import system
from os import path as pth
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
	cmd = moddir + "\\bin_linux\\arss"
else:
	cmd = "arss" # MacOS requires ARSS to be directly installed via the installer.


def Encode(filepath : str, output_path : str,
		   min_frequency = 27,
		   max_frequency = 20000,
		   pps = 100,
		   bpo = 48):
		
	filepath = pth.abspath(filepath)
	output_path = pth.abspath(output_path)

	tempwav = False
	if not filepath.endswith(".wav"):
		# Assume we need to convert the file.
		if not filepath.endswith(".mp3"):
			raise ValueError("The filepath should either contain a .wav file or an .mp3 file.")
		new = AudioSegment.from_mp3(filepath)
		new.export("temp.wav", format="wav")
		tempwav = True
	
	if not output_path.endswith(".bmp"):
		if output_path[-1] not in ["\\", "/"]:
			if "\\" in output_path:
				output_path += "\\"
			else:
				output_path += "/"
		output_path += "out.bmp"
	
	result = run([
		cmd, "-q",
		pth.abspath("temp.wav") if tempwav \
			else filepath, 					 # ^ Input file
		output_path,						 # Output file
		"--analysis",	 					 # Type
		"--min-freq", str(min_frequency),	 # Minimum frequency
		"--max-freq", str(max_frequency),	 # Maximum frequency
		"--pps", str(pps),					 # Time resolution (pixels per second)
		"--bpo", str(bpo)					 # Frequency resolution (bands per octave)
	], stderr=PIPE, universal_newlines=True)

	remove("temp.wav")

	if result.returncode != 0:
		raise RuntimeError(result.stderr)

def Decode(filepath : str, output_path : str,
		   min_frequency = 27,
		   max_frequency = 20000,
		   sample_rate = 44100,
		   sine = True,
		   pps = 100,
		   bpo = 48):
		
	filepath = pth.abspath(filepath)
	output_path = pth.abspath(output_path)

	if not output_path.endswith(".wav") and not output_path.endswith(".mp3"):
		if output_path[-1] not in ["\\", "/"]:
			if "\\" in output_path:
				output_path += "\\"
			else:
				output_path += "/"
		output_path += "out.wav"
	
	if not output_path.endswith(".wav"):
		temp = True
	else:
		temp = False
	
	result = run([
		cmd, "-q",
		filepath, 					 		 # Input file
		pth.abspath("temp.wav") if temp \
			else output_path, 				 # Output file
		"--sine" if sine else "--noise",	 # Type
		"--sample-rate", str(sample_rate),   # Sample rate
		"--min-freq", str(min_frequency),	 # Minimum frequency
		# "--max-freq", str(max_frequency),	 # Maximum frequency -- TODO: ARSS: "You have set one parameter too many"
		"--pps", str(pps),					 # Time resolution (pixels per second)
		"--bpo", str(bpo)					 # Frequency resolution (bands per octave)
	], stderr=PIPE, universal_newlines=True)

	if result.returncode != 0:
		try:
			remove("temp.wav")
		except:
			pass
		raise RuntimeError(result.stderr)
	
	if temp:
		# We need to convert the file.
		if not output_path.endswith(".mp3"):
			remove("temp.wav")
			raise ValueError("The output_path must be a .wav file or an .mp3 file.")
		new = AudioSegment.from_wav("temp.wav")
		new.export(output_path, format="mp3")
		remove("temp.wav")