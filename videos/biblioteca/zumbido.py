"""Steady-buzz test (the cicada bug): is there a strong 20-90 Hz modulation of the band above 6 kHz? Prints the strongest line and the 37 Hz one.
  python3 zumbido.py REEL.mp4"""
import sys, subprocess, numpy as np
x = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar","48000","-af","highpass=f=6000,highpass=f=6000","-f","f32le","-"],capture_output=True).stdout, np.float32)
hop = 240; n = len(x)//hop; e = np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))   # 200 Hz envelope
e = e - e.mean(); F = np.abs(np.fft.rfft(e*np.hanning(len(e)))); f = np.fft.rfftfreq(len(e), hop/48000)
band = (f > 20) & (f < 90); k = np.argmax(F*band); bg = np.median(F[band])
print(f"strongest envelope line 20-90 Hz: {f[k]:.1f} Hz, {F[k]/bg:.1f}x the median; 37 Hz: {F[np.argmin(abs(f-37))]/bg:.1f}x; HF rms {20*np.log10(np.sqrt((x**2).mean())+1e-9):.1f} dBFS")
