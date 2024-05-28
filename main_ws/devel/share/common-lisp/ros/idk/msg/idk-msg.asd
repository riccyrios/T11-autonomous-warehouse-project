
(cl:in-package :asdf)

(defsystem "idk-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Tour" :depends-on ("_package_Tour"))
    (:file "_package_Tour" :depends-on ("_package"))
  ))