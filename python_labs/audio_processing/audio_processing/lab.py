"""
6.101 Lab 0:
Audio Processing
"""

import wave
import struct
# No Additional Imports Allowed!

def backwards(sound):
    """Input sound dictionary as described in the lab. 
       Output's dictionary with shared 'rate' value but with reversed list of sound's samples"""
    flipped_dictsample = {}
    flipped_dictsample['rate'], flipped_dictsample['samples'] = sound['rate'], list(reversed(sound['samples']))
    return flipped_dictsample 

def mix(sound1, sound2, p):
    """Here, two sound dictionaries having shared rates but perhaps varying sample lengths are used to return a new sound with a linearly-combined sample list from the sounds.
    p is the specified proportion between 0 and 1 that specifies sound1's proportional sample contribution and 1-p is the proportion scaling each of sound2's samples"""    
    if sound1['rate'] != sound2['rate']:
       return None
    dictmixed = {}
    #Aims to empty out the smaller sample list to combine and then dumps any remaining sample values found in the longer list onto the ultimate list
    smallest_length= min(len(sound1['samples']),len(sound2['samples']))
    dictmixed['rate'], dictmixed['samples'] = sound1['rate'], [p*sound1['samples'][i]+ (1-p)*sound2['samples'][i] for i in range(smallest_length)]
    if len(sound1['samples']) ==len(sound2['samples']):
        return dictmixed
    elif len(sound1['samples']) >len(sound2['samples']):
        dictmixed['samples'].extend([p*i for i in sound1['samples'][smallest_length:]])
        return dictmixed
    else:
        dictmixed['samples'].extend([(1-p)*j for j in sound2['samples'][smallest_length:]])
        return dictmixed
def convolve(sound, kernel):
    """Implements procedure to return the sound convoluted between the samples of sound and the kernel list.
       Determines the size of the ultimate sample list to produce and updates each element with the corresponding scaled and inputed sound values"""
    dictconvoluted= {}
    dictconvoluted['rate']= sound['rate']
    ultimate= [0]*(len(sound['samples'])+(len(kernel))-1)
    inp= [i for i in sound['samples']]
    #Here the goal is to iterativelyt update ultimate by some jth index that roots the sequential dowstream scaled values from input, which iterates through the i-indexed input values, each scaled by the jth kernel scalar.
    for j in range(len(kernel)):
        #avoids having to scale and add by 0
        if kernel[j] !=0:
            for i in range(len(inp)):
                ultimate[j+i] += kernel[j]*inp[i]
    dictconvoluted['samples']= ultimate
    return dictconvoluted

def echo(sound, num_echoes, delay, scale):
    """"From a sound object, the sample list is vector added to onto itself num_echoes times with values in array shifted downstream by some delay of zeroes, each value numerically scaled by scale"""
    zerogaps= round(delay*sound['rate'])
    repeat= num_echoes
    kern= [1,]
    #creates a kern to feed onto convolve, yielding intructions for how to combine the scaled and shifted sample values of echo.
    for i in range(repeat):  
        #semantically avoids padding kern with list of negative size
        if zerogaps>=1:
            kern.extend([0]*(zerogaps-1))
            kern.append((scale)**(i+1))
    return convolve(sound, kern)

def pan(sound):
    """Takes in a Stereo formatted sound and returns a stereo sound with samples sequentially scaled as defined in the lab. This produces an ambiatic sound that increases the scale of the samples in the right channel
    whilst complementarily scaling down the corresponding samples in the left channel """    
    dictpan= {}
    dictpan['rate']= sound['rate']
    left= []
    right=[]
    #Given that the left and right channels have sample lists of same length, with arbitrarily assign the mathematical N the size of the left channel list.
    N= len(sound['left'])
    for i in range(N):
        num= sound['right'][i]
        right.append((1/(N-1))*i*num)
    for j in range(N):
        num= sound['left'][j]
        left.append((1-((1/(N-1))*j))*num)
    dictpan['left']= left
    dictpan['right']= right
    return dictpan
        


def remove_vocals(sound):
    """Seemingly removes vocals from a stereo sound by algorithmically finding the difference between the left and right channel smaple values, producing a new muted mono sample list"""
    dictkaraoke ={}
    dictkaraoke['rate']= sound['rate']
    # list comprehension takes advantage of zip to set the proper different between left and right elements.
    dictkaraoke['samples']= [lef-rig for lef,rig in zip(sound['left'], sound['right'])]
    return dictkaraoke

def bass_boost_kernel(n_val, scale=0):
    """
    Construct a kernel that acts as a bass-boost filter.

    We start by making a low-pass filter, whose frequency response is given by
    (1/2 + 1/2cos(Omega)) ^ n_val

    Then we scale that piece up and add a copy of the original signal back in.
    """
    # make this a fake "sound" so that we can use the convolve function
    base = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    kernel = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    for i in range(n_val):
        kernel = convolve(kernel, base["samples"])
    kernel = kernel["samples"]

    # at this point, the kernel will be acting as a low-pass filter, so we
    # scale up the values by the given scale, and add in a value in the middle
    # to get a (delayed) copy of the original
    kernel = [i * scale for i in kernel]
    kernel[len(kernel) // 2] += 1

    return kernel


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds


def load_wav(filename, stereo=False):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    file = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = file.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    if stereo:
        left = []
        right = []
        for i in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left.append(struct.unpack("<h", frame[:2])[0])
                right.append(struct.unpack("<h", frame[2:])[0])
            else:
                datum = struct.unpack("<h", frame)[0]
                left.append(datum)
                right.append(datum)

        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = []
        for i in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left = struct.unpack("<h", frame[:2])[0]
                right = struct.unpack("<h", frame[2:])[0]
                samples.append((left + right) / 2)
            else:
                datum = struct.unpack("<h", frame)[0]
                samples.append(datum)

        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for left, right in zip(sound["left"], sound["right"]):
            left = int(max(-1, min(1, left)) * (2**15 - 1))
            right = int(max(-1, min(1, right)) * (2**15 - 1))
            out.append(left)
            out.append(right)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()

# if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    hello = load_wav("sounds/hello.wav")
    # mystery= load_wav('C:/Users/gava1/Downloads/audio_processing/audio_processing/sounds/mystery.wav')
    # inter_mystery= backwards(mystery)
    # sound1= load_wav('C:/Users/gava1/Downloads/audio_processing/audio_processing/sounds/synth.wav')
    # sound2= load_wav('C:/Users/gava1/Downloads/audio_processing/audio_processing/sounds/water.wav')
    # inter= mix(sound1, sound2, 0.2)
    # sound= load_wav('C:/Users/gava1/Downloads/audio_processing/audio_processing/sounds/ice_and_chilli.wav')
    # kernel = bass_boost_kernel(1000, 1.5)
    # num_echoes= 5
    # delay=0.3
    # scale= 0.6 
    # sound= load_wav('C:/Users/gava1/Downloads/audio_processing/audio_processing/sounds/lookout_mountain.wav', stereo=True)
    # inter= remove_vocals(sound) 
    # write_wav(inter, 'C:/Users/gava1/Downloads/audio_processing/audio_processing/sounds/dk_solved.wav' )
    # write_wav(backwards(hello), 'hello_reversed.wav')
