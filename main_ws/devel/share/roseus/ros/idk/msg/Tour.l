;; Auto-generated. Do not edit!


(when (boundp 'idk::Tour)
  (if (not (find-package "IDK"))
    (make-package "IDK"))
  (shadow 'Tour (find-package "IDK")))
(unless (find-package "IDK::TOUR")
  (make-package "IDK::TOUR"))

(in-package "ROS")
;;//! \htmlinclude Tour.msg.html


(defclass idk::Tour
  :super ros::object
  :slots (_nodes ))

(defmethod idk::Tour
  (:init
   (&key
    ((:nodes __nodes) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _nodes __nodes)
   self)
  (:nodes
   (&optional __nodes)
   (if __nodes (setq _nodes __nodes)) _nodes)
  (:serialization-length
   ()
   (+
    ;; int32[] _nodes
    (* 4    (length _nodes)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32[] _nodes
     (write-long (length _nodes) s)
     (dotimes (i (length _nodes))
       (write-long (elt _nodes i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32[] _nodes
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _nodes (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _nodes i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get idk::Tour :md5sum-) "81a3f490b90e9559507f416ae312dc21")
(setf (get idk::Tour :datatype-) "idk/Tour")
(setf (get idk::Tour :definition-)
      "int32[] nodes

")



(provide :idk/Tour "81a3f490b90e9559507f416ae312dc21")


