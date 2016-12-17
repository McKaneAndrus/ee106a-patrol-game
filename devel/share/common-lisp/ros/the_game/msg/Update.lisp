; Auto-generated. Do not edit!


(cl:in-package the_game-msg)


;//! \htmlinclude Update.msg.html

(cl:defclass <Update> (roslisp-msg-protocol:ros-message)
  ((vectors
    :reader vectors
    :initarg :vectors
    :type (cl:vector geometry_msgs-msg:Vector3)
   :initform (cl:make-array 0 :element-type 'geometry_msgs-msg:Vector3 :initial-element (cl:make-instance 'geometry_msgs-msg:Vector3))))
)

(cl:defclass Update (<Update>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Update>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Update)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name the_game-msg:<Update> is deprecated: use the_game-msg:Update instead.")))

(cl:ensure-generic-function 'vectors-val :lambda-list '(m))
(cl:defmethod vectors-val ((m <Update>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader the_game-msg:vectors-val is deprecated.  Use the_game-msg:vectors instead.")
  (vectors m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Update>) ostream)
  "Serializes a message object of type '<Update>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'vectors))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'vectors))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Update>) istream)
  "Deserializes a message object of type '<Update>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'vectors) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'vectors)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'geometry_msgs-msg:Vector3))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Update>)))
  "Returns string type for a message object of type '<Update>"
  "the_game/Update")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Update)))
  "Returns string type for a message object of type 'Update"
  "the_game/Update")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Update>)))
  "Returns md5sum for a message object of type '<Update>"
  "0e70d69b80b6619295db7fb48376314f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Update)))
  "Returns md5sum for a message object of type 'Update"
  "0e70d69b80b6619295db7fb48376314f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Update>)))
  "Returns full string definition for message of type '<Update>"
  (cl:format cl:nil "geometry_msgs/Vector3[] vectors~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Update)))
  "Returns full string definition for message of type 'Update"
  (cl:format cl:nil "geometry_msgs/Vector3[] vectors~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Update>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'vectors) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Update>))
  "Converts a ROS message object to a list"
  (cl:list 'Update
    (cl:cons ':vectors (vectors msg))
))
