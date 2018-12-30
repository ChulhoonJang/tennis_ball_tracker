import numpy as np

class track:
    def __init__(self, pos):
        self.pos = pos
        self.traj = []
        self.traj.append(pos)
        self.pos_bounce = None
        
        self.age = 0
        self.time_count = 0
    
    def refresh(self):
        self.time_count += 1
        
        # calculate traj_grad
        if len(self.traj) >= 3:
            traj = np.array(self.traj)
            self.traj_grad = traj[1:,:] - traj[:-1,:]
            
            for i in range(len(self.traj_grad)-1):
                prev_traj_grad = self.traj_grad[i]
                curr_traj_grad = self.traj_grad[i+1]
                
                # find the change of the sign of the y_grad
                if prev_traj_grad[1] * curr_traj_grad[1] < 0 and prev_traj_grad[1] > curr_traj_grad[1]:                        
                    self.pos_bounce = self.traj[i+1]
                    break
                else:
                    self.pos_bounce = None
            
        else:
            self.traj_grad = None
            self.pos_bounce = None
    
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