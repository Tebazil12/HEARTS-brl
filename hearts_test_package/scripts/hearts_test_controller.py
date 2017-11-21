#!/usr/bin/env python
''' 
This is a test script for a test package, it makes sure that the node is communicating with the refbox
'''

import rospy
import time
from std_msgs.msg import Empty, String
from roah_rsbb_comm_ros.msg import BenchmarkState
import std_srvs.srv

class Controller():
    def __init__(self):
        #Publishers#
        self.pub_bench_message = rospy.Publisher('roah_rsbb/messages_saved', String, queue_size = 10)

        #Subscribers
        rospy.Subscriber("roah_rsbb/benchmark/state", BenchmarkState, self.benchmark_state_callback)
    
        #Services
        self.prepare = rospy.ServiceProxy('/roah_rsbb/end_prepare', std_srvs.srv.Empty)
        self.execute = rospy.ServiceProxy('/roah_rsbb/end_execute', std_srvs.srv.Empty)
    
    ### When receiving a message from the "roah_rsbb/benchmark/state" topic, will then publish the corresponding state to "roah_rsbb/messages_save"
    def benchmark_state_callback(self, data):
                     
        if data.benchmark_state == BenchmarkState.STOP:
            rospy.loginfo("STOP")
            self.pub_bench_message.publish("Stopping")
        elif data.benchmark_state == BenchmarkState.PREPARE:
            rospy.loginfo("PREPARE")
            self.pub_bench_message.publish("Preparing")
            try:
                time.sleep(5)
                self.prepare()
            except:
                rospy.loginfo("Failed to reply PREPARE")
        elif data.benchmark_state == BenchmarkState.EXECUTE:
            rospy.loginfo("EXECUTE")
            self.pub_bench_message.publish("Starting")
            
if __name__ == '__main__':
     rospy.init_node('hearts_test', anonymous=True)
     rospy.loginfo("hearts test controller has started")
     controller = Controller()
     rospy.spin()
