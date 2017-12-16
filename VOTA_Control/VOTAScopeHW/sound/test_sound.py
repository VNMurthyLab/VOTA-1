import simpleaudio as sa

wave_obj = sa.WaveObject.from_wave_file("beep_start.wav")
play_obj = wave_obj.play()