; Auto-generated. Do not edit!


(cl:in-package idk-msg)


;//! \htmlinclude Tour.msg.html

(cl:defclass <Tour> (roslisp-msg-protocol:ros-message)
  ((nodes
    :reader nodes
    :initarg :nodes
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0)))
)

(cl:defclass Tour (<Tour>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Tour>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Tour)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name idk-msg:<Tour> is deprecated: use idk-msg:Tour instead.")))

(cl:ensure-generic-function 'nodes-val :lambda-list '(m))
(cl:defmethod nodes-val ((m <Tour>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader idk-msg:nodes-val is deprecated.  Use idk-msg:nodes instead.")
  (nodes m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Tour>) ostream)
  "Serializes a message object of type '<Tour>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'nodes))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    ))
   (cl:slot-value msg 'nodes))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Tour>) istream)
  "Deserializes a message object of type '<Tour>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'nodes) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'nodes)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296)))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Tour>)))
  "Returns string type for a message object of type '<Tour>"
  "idk/Tour")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Tour)))
  "Returns string type for a message object of type 'Tour"
  "idk/Tour")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Tour>)))
  "Returns md5sum for a message object of type '<Tour>"
  "81a3f490b90e9559507f416ae312dc21")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Tour)))
  "Returns md5sum for a message object of type 'Tour"
  "81a3f490b90e9559507f416ae312dc21")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Tour>)))
  "Returns full string definition for message of type '<Tour>"
  (cl:format cl:nil "int32[] nodes~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Tour)))
  "Returns full string definition for message of type 'Tour"
  (cl:format cl:nil "int32[] nodes~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Tour>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'nodes) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Tour>))
  "Converts a ROS message object to a list"
  (cl:list 'Tour
    (cl:cons ':nodes (nodes msg))
))
