from __future__ import division
import gpt_getFromTo as ChatGPT
import route
import re
import sys
import api_key
import weather
# import GPT_TTS
import GCP_TTS
from google.cloud import speech
from gtts import gTTS
import playsound as ps
import pyaudio
from six.moves import queue
import msg
from gpt_inferYesOrNo import Yes_or_No
import time 
# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms / 10x

audio_input = []

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get() 
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None: #org
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

def listen_print_loop(responses): 
    global audio_input 
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """


    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))
        
        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            # audio_input.append(transcript + overwrite_chars) # exp1
            # audio_input = transcript + overwrite_chars ## minse change
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            audio_input.append(transcript.strip()) # exp1
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(고마워|고마오)\b", transcript, re.I): #2음절 이상
                print("Exiting..")
                break

            num_chars_printed = 0

def STT():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = "ko-KR"  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_word_time_offsets=True
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    GCP_TTS.TTS("삐이") #change later 
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses) 

if __name__ == "__main__":
    #개인정보 동의 + 출발지/목적지 질문 + break word 말해주기
    GCP_TTS.TTS(msg.welcome_text)

    # checkpoint
    while True:
        GCP_TTS.TTS(msg.location_q_text)
        STT() # STT : audio_input = "" 에 저장
        print(audio_input)
        final_input = str(' '.join(audio_input))#exp1
        # final_input = max(audio_input, key=len) #longest string ; need to fix here too
        print("\n\n\nFinal Audio Input :::: ", final_input, "\n\n\n") # del later
        extracted_loc = ChatGPT.Extract_loc(final_input) 
        print("\n\n\nExtraxted locations :::: ", extracted_loc, "\n\n\n") # del later

        origin, destination = extracted_loc[0], extracted_loc[1]

        GCP_TTS.TTS(f"{origin}에서, {destination}, 까지 가는 게 맞으신가요? 말씀 후 고마워라고 말씀해 주세요")

        # yes_no api part
        audio_input = []
        STT() # 음성 입력 받기
        print("audio input :::",audio_input)
        final_input = str(' '.join(audio_input))
        print(f'line202: final input: {final_input}') # delete later
        # final_input = max(audio_input, key=len) #longest string ; need to fix here too # 텍스트 추출
        print("final input after max:::",final_input)
        print("Is it yes or no???:::",Yes_or_No(final_input)) # del later
        if Yes_or_No(final_input) == "No":
            audio_input = []
            continue #go back to checkpoint
        else: #if yes : escape the loop
            break

    transit_message, arrival_message, first_step_message, transit_directions, total_duration, fare, other_message = route.get_transit_directions(api_key.API_googlemap, origin, destination)

    weather_txt = weather.weather_api(weather.api_url)
    final_route_txt = transit_message + "\n" + arrival_message + "\n" + first_step_message + "\n" + other_message 
    print(final_route_txt)
    GCP_TTS.TTS(final_route_txt)
    GCP_TTS.TTS(weather.weather_api(weather.api_url))

