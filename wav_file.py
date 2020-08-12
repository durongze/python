import numpy
import scipy
import pandas
from scipy import signal
from ctypes import windll

fa_resample = windll.LoadLibrary(r'E:\\webdown\\libresample.dll')

opt_downfactor= 147
opt_upfactor  = 160

sourcefile = fa_resample.fa_fopen(b'Ring08.wav')
fa_resample.fa_wavfmt_readheader(sourcefile)
samplerate_in = 0 # fmt.samplerate
#fmt.fa_fseek(sourcefile, 44, 0)

h_resflt = fa_resample.fa_resample_filter_init(opt_upfactor, opt_downfactor, 1, 2)
samplerate_out = (samplerate_in * opt_upfactor)/opt_downfactor

in_len_bytes = fa_resample.fa_get_resample_framelen_bytes(h_resflt)

while 1:
    if is_last:
        break
    p_wavin = []
    p_wavout = []
    out_len_bytes = 0
    read_len = fa_resample.fa_fread(p_wavin, 1, in_len_bytes, sourcefile)
    if read_len < in_len_bytes:
        is_last = 1
    fa_resample.fa_resample(h_resflt, p_wavin, in_len_bytes, p_wavout, windll.POINTER(out_len_bytes))
