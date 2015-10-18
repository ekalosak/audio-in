import sys

import pdb
import time
import numpy as np
import pyaudio, audioop
import ggplot
import pandas as pd

import utils

REFRESH_RATE = .001
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 44100

def main(log):

    log.debug('initializing app')
    p = pyaudio.PyAudio()

    # Open audio input stream
    stream = p.open(format = FORMAT,
        channels = CHANNELS,
        rate = SAMPLE_RATE,
        input = True,
        frames_per_buffer = CHUNK_SIZE)

    log.debug('opened stream <{}>'.format(stream))
    log.debug('reading audio input at rate <{}>'.format(SAMPLE_RATE))

    recorded = []

    # Start mainloop
    loops = 0
    while True:
        loops += 1
        if loops % 25 == 0: log.debug('recorded <{}> loops'.format(loops))

        # Decode chunks of audio data from the stream
        try:
            data = stream.read(CHUNK_SIZE)
            decoded = np.fromstring(data, 'Float32');
            mx = max(decoded)
            recorded.append(mx)

        # On <C-c>, plot max of recorded data
        except KeyboardInterrupt as ee:
            log.debug('closing stream and ending PyAudio')
            stream.close()
            p.terminate()
            df = pd.DataFrame(columns = ['mx', 'time'])
            df['mx'] = recorded
            df['time'] = range(len(recorded))
            plt = ggplot.ggplot(ggplot.aes(x='time', y='mx'), data=df) +\
                        ggplot.geom_line()
            pdb.set_trace()
            log.debug('quitting')
            sys.exit(1)

if __name__ == "__main__":
    log = utils.make_logger('audio-reader')
    main(log)

