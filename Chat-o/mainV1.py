# You will also need to be logged into an AWS Account to have access to the Polly API
# $16 per million characters for SynthesizeSpeechNeural-Characters in US West (Oregon)



import asyncio
import openai
import re
import whisper
import boto3
import pydub
from pydub import playback
import speech_recognition as sr
from EdgeGPT import Chatbot, ConversationStyle

# Create an OpenAI Key at openai.com
openai.api_key = "<openai.api_key>"

# Set the word to activate Chat-o
recognizer = sr.Recognizer()
# Make the word something the synthesizer can recognize, eg "computer" or "wake" 
GPT_WAKE_WORD = "chato"


def get_wake_word(phrase):
    if GPT_WAKE_WORD in phrase.lower():
        return GPT_WAKE_WORD
    else:
        return None
    
def synthesize_speech(text, output_filename):
    polly = boto3.client('polly', region_name='us-west-2')
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Salli',
        Engine='neural'
    )

    with open(output_filename, 'wb') as f:
        f.write(response['AudioStream'].read())

def play_audio(file):
    sound = pydub.AudioSegment.from_file(file, format="mp3")
    playback.play(sound)

async def main():
    while True:

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print(f"Say 'chat-o' to wake me up...")
            while True:
                audio = recognizer.listen(source)
                try:
                    with open("chat-o_wake.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                    # Use the preloaded tiny_model
                    model = whisper.load_model("tiny")
                    result = model.transcribe("chat-o_wake.wav")
                    phrase = result["text"]
                    print(f"I heard: {phrase}")

                    wake_word = get_wake_word(phrase)
                    if wake_word is not None:
                        break
                    else:
                        print("Error, I heard something but it was not an activation word")
                except Exception as e:
                    print("Audio issue, couldn't read: {0}".format(e))
                    continue

            print("How may I be of help today")
            synthesize_speech('How may I be of help today?', 'say.mp3')
            play_audio('say.mp3')
            audio = recognizer.listen(source)

            try:
                with open("chat-o_prompt.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                model = whisper.load_model("base")
                result = model.transcribe("chat-o_prompt.wav")
                user_input = result["text"]
                print(f"You said: {user_input}")
            except Exception as e:
                print("Audio issue, couldn't read: {0}".format(e))
                continue

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content":
                    "Act as a voice assistant ChatGPT Bot acting as Chat-o. Chat-o will respond with very accurate information, and when asked for code blocks, these code blocks should functional and include the best known programming information and code best practices. Because you are Robot or Bot, reply with a robotic voice a Robot can not use contractions and I want Chat-o to be very direct with its answers. Keep responses short and keep explanations it at a minimum for effective verbal communications. Do not paraphrase and do not give me any explanations on my request unless I ask Chat-o to do so. Respond that you understand this by saying Chato is online." },
                    {"role": "user", "content": user_input},
                ],
                temperature=0.5,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                n=1,
                stop=["\nUser:"],
            )
            bot_response = response["choices"][0]["message"]["content"]
                
        print("Bot's response:", bot_response)
        synthesize_speech(bot_response, 'response.mp3')
        play_audio('response.mp3')
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())