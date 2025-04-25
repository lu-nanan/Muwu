# import subprocess
# import speech_recognition as sr
# from pydub import AudioSegment
# from pydub.silence import split_on_silence
# import os

# def convert_to_wav(input_file, output_file):
#     """
#     Convert audio file to WAV format (PCM 16-bit, 16kHz) using FFmpeg.
#     :param input_file: Path to the input audio file.
#     :param output_file: Path to the output WAV file.
#     """
#     command = f"ffmpeg -i {input_file} -acodec pcm_s16le -ar 16000 {output_file}"
#     subprocess.run(command, shell=True, check=True)
#     print(f"Converted {input_file} to {output_file}")

# def transcribe_audio_speech_recognition(audio_path, language="zh-CN"):
#     """
#     Transcribe the audio file using SpeechRecognition.
#     :param audio_path: Path to the WAV audio file.
#     :param language: Language code for transcription (default: Chinese).
#     :return: Transcription text.
#     """
#     r = sr.Recognizer()
#     audio = AudioSegment.from_wav(audio_path)
#     # Split audio into chunks based on silence
#     chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=audio.dBFS-14, keep_silence=500)
#     transcripts = []
#     for i, chunk in enumerate(chunks):
#         chunk_file = f"chunk{i}.wav"
#         chunk.export(chunk_file, format="wav")
#         with sr.AudioFile(chunk_file) as source:
#             audio_chunk = r.record(source)
#         try:
#             text = r.recognize_google(audio_chunk, language=language)
#             transcripts.append(text)
#         except sr.UnknownValueError:
#             transcripts.append("Could not understand audio")
#         except sr.RequestError as e:
#             transcripts.append(f"Request failed; {e}")
#         os.remove(chunk_file)  # Clean up temporary chunk file
#     return " ".join(transcripts)

# # Main program
# if __name__ == "__main__":
#     input_file = "F:\\大三下学期\\移动应用开发\\仓库\\Muwu\\文件处理\\test\\测试.mp3"
#     output_file = "F:\\大三下学期\\移动应用开发\\仓库\\Muwu\\文件处理\\test\\测试.wav"

#     # Convert to WAV format
#     convert_to_wav(input_file, output_file)

#     # Transcribe the audio (specify language as Chinese)
#     transcript = transcribe_audio_speech_recognition(output_file, language="zh-CN")
#     print("Transcription:", transcript)

#     # Optional: Delete the temporary WAV file
#     if os.path.exists(output_file):
#         os.remove(output_file)
#         print(f"Deleted temporary file {output_file}")


#进行文件语音识别
import speech_recognition as sr
 
 
def recognize_audio(wav_file_path):
    # 初始化识别器
    recognizer = sr.Recognizer()
    
    # 从WAV文件加载音频数据
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)
 
    # 尝试使用Google Web Speech API进行语音识别
    try:
        # 识别语音
        text = recognizer.recognize_google(audio_data, language='zh-CN') # 根据需要设置语言
        print(f"识别结果: {text}")
    except sr.UnknownValueError:
        print("Google Web Speech API无法理解音频")
    except sr.RequestError as e:
        print(f"无法从Google Web Speech API获得结果; {e}")
 
# 示例：转换wav文件并进行语音识别
wav_file_path = r'F:\大三下学期\移动应用开发\仓库\Muwu\文件处理\test\测试.wav'  # WAV文件的保存路径
 
recognize_audio(wav_file_path)