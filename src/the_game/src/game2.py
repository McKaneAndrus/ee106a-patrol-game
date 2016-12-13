import tf
import numpy as np

ar_tags = {'origin':'ar_marker_0', 'ref': 'ar_marker_1'}
listener = tf.TransformListener()

grid_x = 9
grid_y = 6

# Rechecks the camera for step size, then calculates coordinate relative to origin
def get_coord(tag):
    step_x, step_y = get_steps()

    done = False
    while not done: 
        try:
            (trans, rot) = listener.lookupTransform(ar_tags['origin'], tag, rospy.Time(0))
            done = True
        except:
            continue
        x_coord = int(round(trans[0]/step_x))
        y_coord = int(round(trans[1]/step_y))
    return x_coord, y_coord

def get_orientation(tag):
    done = False
    while not done: 
        try:
            (trans, rot) = listener.lookupTransform(ar_tags['origin'], tag, rospy.Time(0))
            done = True
        except:
            continue
        orientation = np.dot(rot, np.array([[1],[0]]))

def get_steps():
    av_step_x = .13
    av_step_y = .13
    iterations = 1
    
    done = False
    while not done: 
        try:
            (trans, rot) = listener.lookupTransform(ar_tags['origin'], ar_tags['ref'], rospy.Time(0))
            done = True
        except:
            continue

        step_x, step_y = trans[0]/grid_x, trans[1]/grid_y

    # TODO: Figure out av_step_x
    if abs(step_x/av_step_x - 1) < 0.15 and abs(step_y/av_step_y - 1) < 0.15:
        av_step_x = (av_step_x * iterations + step_x) / (iterations + 1)
        av_step_y = (av_step_y * iterations + step_y) / (iterations + 1)
        iterations += 1

    return av_step_x, av_step_y

def get_map():
    return np.loadtxt('map.txt', dtype=int).tolist()

def get_map_dims():
    return np.loadtxt('map.txt', dtype=int).shape.tolist()

def reveal(x, y):
    game_map = get_map()
    locs = []
    for i in range(x - 1, x + 2):
        if i >= 0 and i < len(game_map):
            for j in range(y - 1, y + 2):
                if j >= 0 and j < len(game_map[0]):
                    locs.append((i, j, game_map[i][j]))
    return locs