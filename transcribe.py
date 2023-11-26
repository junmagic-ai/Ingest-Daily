# Fast whisper transcription

def transcribe_audio ():
# Fast whisper transcription
    import textwrap

    wrapper = textwrap.TextWrapper(width=80,
        initial_indent=" " * 8,
        subsequent_indent=" " * 8,
        break_long_words=False,
        break_on_hyphens=False)

    import torch
    from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
    from optimum.bettertransformer import BetterTransformer


    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "distil-whisper/distil-medium.en"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True#, use_flash_attention_2=True
    )
    model.to(device)
    model = model.to_bettertransformer() # we are using optimum BetterTransformer since Flash Attention 2 isn't supported on Colab

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=15, #long form transcription
        batch_size=16,
        torch_dtype=torch_dtype,
        device=device,
    )

    import os
    from pydub import AudioSegment

    audio_dir = 'Audio'
    transcripts_dir = 'Texts'

    for filename in os.listdir(audio_dir):
        if filename.endswith(('.mp3', '.mp4', '.m4a', '.wav')):
            audio_file = os.path.join(audio_dir, filename)
            transcript_file = os.path.join(transcripts_dir, os.path.splitext(filename)[0] + '.txt')

            # Convert audio file to wav format if it's not
            if not filename.endswith('.wav'):
                audio = AudioSegment.from_file(audio_file)
                audio.export(audio_file, format='wav')

            # Transcribe the audio file
            result = pipe(audio_file)

            # Save the transcript to a txt file
            with open(transcript_file, 'w') as f:
                f.write(result["text"])
