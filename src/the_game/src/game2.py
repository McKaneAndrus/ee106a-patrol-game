import tf
import numpy as np
import os
from std_msgs.msg import Bool
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker



# ar_tags = {'origin':'ar_marker_0', 'ref': 'ar_marker_1'}
# listener = tf.TransformListener()

# grid_x = 9
# grid_y = 6

# Rechecks the camera for step size, then calculates coordinate relative to origin
# def get_player_coord(player):
#     step_x, step_y = get_steps()

#     done = False
#     while not done: 
#         try:
#             (trans, rot) = listener.lookupTransform(ar_tags['origin'], "ar_marker_" + player, rospy.Time(0))
#             done = True
#         except:
#             continue
#         x_coord = int(round(trans[0]/step_x))
#         y_coord = int(round(trans[1]/step_y))
#     return x_coord, y_coord

# def get_orientation(tag):
#     done = False
#     while not done: 
#         try:
#             (trans, rot) = listener.lookupTransform(ar_tags['origin'], tag, rospy.Time(0))
#             done = True
#         except:
#             continue
#         orientation = np.dot(rot, np.array([[1],[0]]))

# def get_steps():
#     av_step_x = .13
#     av_step_y = .13
#     iterations = 1
    
#     done = False
#     while not done: 
#         try:
#             (trans, rot) = listener.lookupTransform(ar_tags['origin'], ar_tags['ref'], rospy.Time(0))
#             done = True
#         except:
#             continue

#         step_x, step_y = trans[0]/grid_x, trans[1]/grid_y

#     # TODO: Figure out av_step_x
#     if abs(step_x/av_step_x - 1) < 0.15 and abs(step_y/av_step_y - 1) < 0.15:
#         av_step_x = (av_step_x * iterations + step_x) / (iterations + 1)
#         av_step_y = (av_step_y * iterations + step_y) / (iterations + 1)
#         iterations += 1

#     return av_step_x, av_step_y

# Callback for patrols getting line of sight on the player
# def cam_callback(msg, patrol, player_tag, observations):
#     global game_status
#     observation = False
#     for marker in msg.markers:
#         if marker.id == player_tag:
#             observation = True
#     observations.append(observation)
#     if len(observations) > 100:
#         if sum(observations) > 50:
#             print "Patrols won!"
#             game_status = True
#         else:
#             observations[patrol] = []

# def player_state_callback(msg):
#     global game_status
#     if msg.data:
#         print "Player won!"
#         game_status = True

def get_map():
    # CHANGE THIS
    return np.loadtxt("map.txt", dtype=int).T.tolist()

def get_map_dims():
    return np.loadtxt('map.txt', dtype=int).T.shape

def reveal(x, y):
    game_map = get_map()
    locs = []
    for i in range(x - 1, x + 2):
        if i >= 0 and i < len(game_map):
            for j in range(y - 1, y + 2):
                if j >= 0 and j < len(game_map[0]):
                    locs.append((i, j, game_map[i][j]))
    return locs

# if __name__=='__main__':
#     if len(sys.argv) < 5 or len(sys.argv) % 2 != 1:
#         print('Use: game2.py [ player tag ] [ p1 zumy ] [ p2 zumy ]')
#         sys.exit()

#     rospy.init_node('game')

#     game_state = rospy.Publisher("game_state", Bool, queue_size = 1)
#     game_status = False


#     observation1 = []
#     observation2 = []
#     self.cam_checker1 = rospy.Subscriber(sys.argv[2] + "/ar_pose_marker", AlvarMarkers, cam_callback, (0, player_tag, observation1))
#     self.cam_checker2 = rospy.Subscriber(sys.argv[3] + "/ar_pose_marker", AlvarMarkers, cam_callback, (1, player_tag, observation2))
#     self.player_checker = rospy.Subscriber("player_won", Bool, player_state_callback)
#     while not rospy.is_shutdown():
#         game_state.publish(Bool(game_status))


    # ar_tags = {}
    # ar_tags[sys.argv[1]] = "ar_marker_" + sys.argv[2]
    # rospy.Subscriber("player_pos", Vector2, player_pos_callback)

    # patrols = []
    # for index in range((len(sys.argv)-3)/2):
    #     i = index*2+3
    #     patrols.append(sys.argv[i])
    #     ar_tags[sys.argv[i]] = "ar_marker_" + sys.argv[i+1]
    #     update = rospy.Publisher(sys.argv[i] + "_update", Updatee, queue_size = 1)
    #     rospy.Subscriber(sys.argv[i] + "_state", State, lambda msg: pos_callback(msg, update))  

    """
    patrols = [sys.argv[3]]
    ar_tags[sys.argv[3]] = "ar_marker_" + sys.argv[4]
    patrol1_update = rospy.Publisher(sys.argv[3] + "_update", Update, queue_size = 1)
    rospy.Subscriber(sys.argv[3] + "_pos", Vector2, lambda msg: pos_callback(msg, patrol1_update))
    
    if len(sys.argv) > 5:
        patrols += [sys.argv[5]]
        ar_tags[sys.argv[5]] = "ar_marker_" + sys.argv[6]
        patrol2_update = rospy.Publisher(sys.argv[5] + "_update", Update, queue_size = 1)
        rospy.Subscriber(sys.argv[5] + "_pos", Vector2, lambda msg: pos_callback(msg, patrol2_update))
        
        if len(sys.argv) > 7:
            patrols += [sys.argv[7]]
            ar_tags[sys.argv[7]] = "ar_marker_" + sys.argv[8]
            patrol3_update = rospy.Publisher(sys.argv[7] + "_update", Update, queue_size = 1)
            rospy.Subscriber(sys.argv[7] + "_pos", Vector2, lambda msg: pos_callback(msg, patrol3_update))
    """

    # for i in range(len(patrols)):
    #     observations.append([])
    #     rospy.Subscriber(patrols[i] + "/ar_pose_marker", AlvarMarkers, lambda msg: seen_callback(msg, i))
        
    # rospy.spin()