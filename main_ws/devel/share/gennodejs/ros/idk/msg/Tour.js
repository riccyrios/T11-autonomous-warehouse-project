// Auto-generated. Do not edit!

// (in-package idk.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Tour {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.nodes = null;
    }
    else {
      if (initObj.hasOwnProperty('nodes')) {
        this.nodes = initObj.nodes
      }
      else {
        this.nodes = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Tour
    // Serialize message field [nodes]
    bufferOffset = _arraySerializer.int32(obj.nodes, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Tour
    let len;
    let data = new Tour(null);
    // Deserialize message field [nodes]
    data.nodes = _arrayDeserializer.int32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 4 * object.nodes.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'idk/Tour';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '81a3f490b90e9559507f416ae312dc21';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32[] nodes
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Tour(null);
    if (msg.nodes !== undefined) {
      resolved.nodes = msg.nodes;
    }
    else {
      resolved.nodes = []
    }

    return resolved;
    }
};

module.exports = Tour;
