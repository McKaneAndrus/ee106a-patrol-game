
(cl:in-package :asdf)

(defsystem "the_game-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "Vector2" :depends-on ("_package_Vector2"))
    (:file "_package_Vector2" :depends-on ("_package"))
    (:file "Update" :depends-on ("_package_Update"))
    (:file "_package_Update" :depends-on ("_package"))
  ))