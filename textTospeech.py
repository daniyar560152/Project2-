import re
import wave
import pyaudio
import _thread
import time

class TextToSpeech:
    
    chars = 1024

    def __init__(self, Pronouncewithfile:str = 'cmudict-0.7b.txt'):
        self.var1 = {}
        self.constructorWords(Pronouncewithfile)

    def constructorWords(self, Pronouncewithfile:str):
        with open(Pronouncewithfile, 'r') as file:
            for x in file:
                if not x.startswith(';;;'):
                    index, val = x.split('  ',2)
                    self.var1[index] = re.findall(r"[A-Z]+",val)

    def Pronounceit(self, Entertext):
        arrayofPronounce = []
        for word in re.findall(r"[\w']+",Entertext.upper()):
            if word in self.var1:
                arrayofPronounce += self.var1[word]
        print(arrayofPronounce)
        delay=0
        for pron in arrayofPronounce:
            _thread.start_new_thread( TextToSpeech.textToSpeech, (pron,delay,))
            delay += 0.800
    
    def textToSpeech(sound, delay):
        try:
            time.sleep(delay)
            WAV = wave.open("sounds/"+sound+".wav", 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(WAV.getsampwidth()),
                            channels=WAV.getnchannels(),
                            rate=WAV.getframerate(),
                            output=True)
            
            data = WAV.readframes(TextToSpeech.chars)
            
            while data:
                stream.write(data)
                data = WAV.readframes(TextToSpeech.chars)
        
            stream.stop_stream()
            stream.close()

            p.terminate()
            return
        except:
            pass
    
 
 

if __name__ == '__main__':
    neuralSpeech = TextToSpeech()
    while True:
        neuralSpeech.Pronounceit(input('I am waiting your text) : '))
