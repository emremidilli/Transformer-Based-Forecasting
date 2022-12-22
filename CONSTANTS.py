NR_OF_BINS = 10
BACKWARD_WINDOW_LENGTH = 4
FORWARD_WINDOW_LENGTH = 3
INTERPLOATION_POINTS = 1200
EXCHANGE_RATES = ['EURUSD']

FROM_TIMESTAMP = '2022-07-01 00:00'
TO_TIMESTAMP = '2022-11-01 00:00'
FFT_AC_COEFFICIENT  = 15 
LOWER_POINT = -0.005
UPPER_POINT = 0.005
THRESHOLD = 0.10
NR_OF_PATTERNS = 4 # MUST BE AN EVEN NUMBER SO THAT MIDDLE POINT IS ZERO. CONTROL IT.


NR_OF_ENSEMBLED_MODELS = 5