import numpy as np

class track:
    def __init__(self, pos):
        self.pos = pos
        self.traj = []
        self.traj.append(pos)
        self.age = 0
        self.time_count = 0
    
    def refresh(self):
        self.time_count += 1
    
    def update(self, pos):
        self.pos = pos
        self.traj.append(pos)
        self.age += 1

class track_manager:
    def __init__(self, min_dist, confirm_threshold, terminate_threshold):
        self.tracks = []
        self.min_dist = min_dist
        self.terminate_threshold = terminate_threshold
        self.confirm_threshold = confirm_threshold
    
    def get_valid_tracks(self):
        valid_tracks = []
        for t in self.tracks:
            if t.age > self.confirm_threshold:
                valid_tracks.append(t)
        return valid_tracks
    
    def manage(self, measurements):
        # refreshment
        for t in self.tracks:
            t.refresh()
        
        # find neareast tracks, update track's pos
        new_measurement = []
        for m in measurements:
            is_new = True
            for t in self.tracks:
                dist = np.sqrt(np.sum(np.square(m-t.pos)))
                if dist <= self.min_dist: # track update
                    t.update(m)
                    is_new = False
                    break
                    
            if is_new == True:
                    new_measurement.append(m)
        
        # create new tracks 
        for m in new_measurement:
            new_track = track(m)
            self.tracks.append(new_track)
       
        if len(self.tracks) == 0:
            for m in measurements:
                new_track = track(m)
                self.tracks.append(new_track)
                
        # eliminate unnecessary tracks
        for t in self.tracks:
            if np.abs(t.time_count - t.age) > self.terminate_threshold:
                self.tracks.remove(t)