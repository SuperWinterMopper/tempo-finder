import librosa
import csv

# Write relative filenames of music tracks HERE
track_file_names = [

]

def extractBeatTimes(filename):
    y, sr = librosa.load(filename)
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return [round(i, 2) for i in beat_times]

def extractTempo(beat_times):
    tempo_each_beat = []
    for i in range(1, len(beat_times)):
        tempo_each_beat.append(60 / (beat_times[i] - beat_times[i - 1]))
    return round(sum(tempo_each_beat) / len(tempo_each_beat), 2)

def extractTempoShifts(beat_times):    
    tempo_changes = 0
    tempos = []
    for i in range(1, len(beat_times)):
        tempos.append(60 / (beat_times[i] - beat_times[i - 1]))

    for i in range(5, len(tempos)):
        if abs(tempos[i] - tempos[i - 1]) >= 30:
            temp, shifted = i - 1, True
            for j in range(1, 5):  
                if abs(tempos[temp] - tempos[temp - j]) >= 15:
                    shifted = False
            if shifted:
                tempo_changes += 1
    return tempo_changes

def main():    
    output = []
    for i in range(len(track_file_names)):
        beat_times = extractBeatTimes(track_file_names[i])
        output.append([track_file_names[i], extractTempo(beat_times), extractTempoShifts(beat_times)])
        
    with open("feature_extraction.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Track", "Tempo", "Number of Tempo Shifts"])
        writer.writerows(output)

if __name__ == '__main__':
    main()