// source: roads.proto
/**
 * @fileoverview
 * @enhanceable
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!

var jspb = require('google-protobuf');
var goog = jspb;
var global = Function('return this')();

goog.exportSymbol('proto.assets.Road', null, global);
goog.exportSymbol('proto.assets.Roads', null, global);
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.assets.Road = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.assets.Road, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.assets.Road.displayName = 'proto.assets.Road';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.assets.Roads = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.assets.Roads.repeatedFields_, null);
};
goog.inherits(proto.assets.Roads, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.assets.Roads.displayName = 'proto.assets.Roads';
}



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.assets.Road.prototype.toObject = function(opt_includeInstance) {
  return proto.assets.Road.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.assets.Road} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.Road.toObject = function(includeInstance, msg) {
  var f, obj = {
    id: jspb.Message.getFieldWithDefault(msg, 1, 0),
    geojsonId: jspb.Message.getFieldWithDefault(msg, 2, 0),
    roadCode: jspb.Message.getFieldWithDefault(msg, 3, ""),
    roadName: jspb.Message.getFieldWithDefault(msg, 4, ""),
    roadType: jspb.Message.getFieldWithDefault(msg, 10, ""),
    roadStatus: jspb.Message.getFieldWithDefault(msg, 20, ""),
    linkCode: jspb.Message.getFieldWithDefault(msg, 5, ""),
    linkStartName: jspb.Message.getFieldWithDefault(msg, 16, ""),
    linkStartChainage: jspb.Message.getFloatingPointFieldWithDefault(msg, 11, 0.0),
    linkEndName: jspb.Message.getFieldWithDefault(msg, 17, ""),
    linkEndChainage: jspb.Message.getFloatingPointFieldWithDefault(msg, 12, 0.0),
    linkLength: jspb.Message.getFloatingPointFieldWithDefault(msg, 7, 0.0),
    surfaceType: jspb.Message.getFieldWithDefault(msg, 8, ""),
    surfaceCondition: jspb.Message.getFieldWithDefault(msg, 9, ""),
    pavementClass: jspb.Message.getFieldWithDefault(msg, 13, ""),
    carriagewayWidth: jspb.Message.getFloatingPointFieldWithDefault(msg, 14, 0.0),
    administrativeArea: jspb.Message.getFieldWithDefault(msg, 15, ""),
    project: jspb.Message.getFieldWithDefault(msg, 18, ""),
    fundingSource: jspb.Message.getFieldWithDefault(msg, 19, ""),
    technicalClass: jspb.Message.getFieldWithDefault(msg, 21, ""),
    maintenanceNeed: jspb.Message.getFieldWithDefault(msg, 22, ""),
    trafficLevel: jspb.Message.getFieldWithDefault(msg, 23, ""),
    lastRevisionId: jspb.Message.getFieldWithDefault(msg, 24, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.assets.Road}
 */
proto.assets.Road.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.assets.Road;
  return proto.assets.Road.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.assets.Road} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.assets.Road}
 */
proto.assets.Road.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {number} */ (reader.readUint32());
      msg.setId(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readUint32());
      msg.setGeojsonId(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setRoadCode(value);
      break;
    case 4:
      var value = /** @type {string} */ (reader.readString());
      msg.setRoadName(value);
      break;
    case 10:
      var value = /** @type {string} */ (reader.readString());
      msg.setRoadType(value);
      break;
    case 20:
      var value = /** @type {string} */ (reader.readString());
      msg.setRoadStatus(value);
      break;
    case 5:
      var value = /** @type {string} */ (reader.readString());
      msg.setLinkCode(value);
      break;
    case 16:
      var value = /** @type {string} */ (reader.readString());
      msg.setLinkStartName(value);
      break;
    case 11:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setLinkStartChainage(value);
      break;
    case 17:
      var value = /** @type {string} */ (reader.readString());
      msg.setLinkEndName(value);
      break;
    case 12:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setLinkEndChainage(value);
      break;
    case 7:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setLinkLength(value);
      break;
    case 8:
      var value = /** @type {string} */ (reader.readString());
      msg.setSurfaceType(value);
      break;
    case 9:
      var value = /** @type {string} */ (reader.readString());
      msg.setSurfaceCondition(value);
      break;
    case 13:
      var value = /** @type {string} */ (reader.readString());
      msg.setPavementClass(value);
      break;
    case 14:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setCarriagewayWidth(value);
      break;
    case 15:
      var value = /** @type {string} */ (reader.readString());
      msg.setAdministrativeArea(value);
      break;
    case 18:
      var value = /** @type {string} */ (reader.readString());
      msg.setProject(value);
      break;
    case 19:
      var value = /** @type {string} */ (reader.readString());
      msg.setFundingSource(value);
      break;
    case 21:
      var value = /** @type {string} */ (reader.readString());
      msg.setTechnicalClass(value);
      break;
    case 22:
      var value = /** @type {string} */ (reader.readString());
      msg.setMaintenanceNeed(value);
      break;
    case 23:
      var value = /** @type {string} */ (reader.readString());
      msg.setTrafficLevel(value);
      break;
    case 24:
      var value = /** @type {number} */ (reader.readUint32());
      msg.setLastRevisionId(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.assets.Road.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.assets.Road.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.assets.Road} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.Road.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getId();
  if (f !== 0) {
    writer.writeUint32(
      1,
      f
    );
  }
  f = message.getGeojsonId();
  if (f !== 0) {
    writer.writeUint32(
      2,
      f
    );
  }
  f = message.getRoadCode();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getRoadName();
  if (f.length > 0) {
    writer.writeString(
      4,
      f
    );
  }
  f = message.getRoadType();
  if (f.length > 0) {
    writer.writeString(
      10,
      f
    );
  }
  f = message.getRoadStatus();
  if (f.length > 0) {
    writer.writeString(
      20,
      f
    );
  }
  f = message.getLinkCode();
  if (f.length > 0) {
    writer.writeString(
      5,
      f
    );
  }
  f = message.getLinkStartName();
  if (f.length > 0) {
    writer.writeString(
      16,
      f
    );
  }
  f = message.getLinkStartChainage();
  if (f !== 0.0) {
    writer.writeFloat(
      11,
      f
    );
  }
  f = message.getLinkEndName();
  if (f.length > 0) {
    writer.writeString(
      17,
      f
    );
  }
  f = message.getLinkEndChainage();
  if (f !== 0.0) {
    writer.writeFloat(
      12,
      f
    );
  }
  f = message.getLinkLength();
  if (f !== 0.0) {
    writer.writeFloat(
      7,
      f
    );
  }
  f = message.getSurfaceType();
  if (f.length > 0) {
    writer.writeString(
      8,
      f
    );
  }
  f = message.getSurfaceCondition();
  if (f.length > 0) {
    writer.writeString(
      9,
      f
    );
  }
  f = message.getPavementClass();
  if (f.length > 0) {
    writer.writeString(
      13,
      f
    );
  }
  f = message.getCarriagewayWidth();
  if (f !== 0.0) {
    writer.writeFloat(
      14,
      f
    );
  }
  f = message.getAdministrativeArea();
  if (f.length > 0) {
    writer.writeString(
      15,
      f
    );
  }
  f = message.getProject();
  if (f.length > 0) {
    writer.writeString(
      18,
      f
    );
  }
  f = message.getFundingSource();
  if (f.length > 0) {
    writer.writeString(
      19,
      f
    );
  }
  f = message.getTechnicalClass();
  if (f.length > 0) {
    writer.writeString(
      21,
      f
    );
  }
  f = message.getMaintenanceNeed();
  if (f.length > 0) {
    writer.writeString(
      22,
      f
    );
  }
  f = message.getTrafficLevel();
  if (f.length > 0) {
    writer.writeString(
      23,
      f
    );
  }
  f = message.getLastRevisionId();
  if (f !== 0) {
    writer.writeUint32(
      24,
      f
    );
  }
};


/**
 * optional uint32 id = 1;
 * @return {number}
 */
proto.assets.Road.prototype.getId = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 1, 0));
};


/** @param {number} value */
proto.assets.Road.prototype.setId = function(value) {
  jspb.Message.setProto3IntField(this, 1, value);
};


/**
 * optional uint32 geojson_id = 2;
 * @return {number}
 */
proto.assets.Road.prototype.getGeojsonId = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/** @param {number} value */
proto.assets.Road.prototype.setGeojsonId = function(value) {
  jspb.Message.setProto3IntField(this, 2, value);
};


/**
 * optional string road_code = 3;
 * @return {string}
 */
proto.assets.Road.prototype.getRoadCode = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setRoadCode = function(value) {
  jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional string road_name = 4;
 * @return {string}
 */
proto.assets.Road.prototype.getRoadName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 4, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setRoadName = function(value) {
  jspb.Message.setProto3StringField(this, 4, value);
};


/**
 * optional string road_type = 10;
 * @return {string}
 */
proto.assets.Road.prototype.getRoadType = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 10, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setRoadType = function(value) {
  jspb.Message.setProto3StringField(this, 10, value);
};


/**
 * optional string road_status = 20;
 * @return {string}
 */
proto.assets.Road.prototype.getRoadStatus = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 20, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setRoadStatus = function(value) {
  jspb.Message.setProto3StringField(this, 20, value);
};


/**
 * optional string link_code = 5;
 * @return {string}
 */
proto.assets.Road.prototype.getLinkCode = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 5, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setLinkCode = function(value) {
  jspb.Message.setProto3StringField(this, 5, value);
};


/**
 * optional string link_start_name = 16;
 * @return {string}
 */
proto.assets.Road.prototype.getLinkStartName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 16, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setLinkStartName = function(value) {
  jspb.Message.setProto3StringField(this, 16, value);
};


/**
 * optional float link_start_chainage = 11;
 * @return {number}
 */
proto.assets.Road.prototype.getLinkStartChainage = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 11, 0.0));
};


/** @param {number} value */
proto.assets.Road.prototype.setLinkStartChainage = function(value) {
  jspb.Message.setProto3FloatField(this, 11, value);
};


/**
 * optional string link_end_name = 17;
 * @return {string}
 */
proto.assets.Road.prototype.getLinkEndName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 17, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setLinkEndName = function(value) {
  jspb.Message.setProto3StringField(this, 17, value);
};


/**
 * optional float link_end_chainage = 12;
 * @return {number}
 */
proto.assets.Road.prototype.getLinkEndChainage = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 12, 0.0));
};


/** @param {number} value */
proto.assets.Road.prototype.setLinkEndChainage = function(value) {
  jspb.Message.setProto3FloatField(this, 12, value);
};


/**
 * optional float link_length = 7;
 * @return {number}
 */
proto.assets.Road.prototype.getLinkLength = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 7, 0.0));
};


/** @param {number} value */
proto.assets.Road.prototype.setLinkLength = function(value) {
  jspb.Message.setProto3FloatField(this, 7, value);
};


/**
 * optional string surface_type = 8;
 * @return {string}
 */
proto.assets.Road.prototype.getSurfaceType = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 8, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setSurfaceType = function(value) {
  jspb.Message.setProto3StringField(this, 8, value);
};


/**
 * optional string surface_condition = 9;
 * @return {string}
 */
proto.assets.Road.prototype.getSurfaceCondition = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 9, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setSurfaceCondition = function(value) {
  jspb.Message.setProto3StringField(this, 9, value);
};


/**
 * optional string pavement_class = 13;
 * @return {string}
 */
proto.assets.Road.prototype.getPavementClass = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 13, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setPavementClass = function(value) {
  jspb.Message.setProto3StringField(this, 13, value);
};


/**
 * optional float carriageway_width = 14;
 * @return {number}
 */
proto.assets.Road.prototype.getCarriagewayWidth = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 14, 0.0));
};


/** @param {number} value */
proto.assets.Road.prototype.setCarriagewayWidth = function(value) {
  jspb.Message.setProto3FloatField(this, 14, value);
};


/**
 * optional string administrative_area = 15;
 * @return {string}
 */
proto.assets.Road.prototype.getAdministrativeArea = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 15, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setAdministrativeArea = function(value) {
  jspb.Message.setProto3StringField(this, 15, value);
};


/**
 * optional string project = 18;
 * @return {string}
 */
proto.assets.Road.prototype.getProject = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 18, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setProject = function(value) {
  jspb.Message.setProto3StringField(this, 18, value);
};


/**
 * optional string funding_source = 19;
 * @return {string}
 */
proto.assets.Road.prototype.getFundingSource = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 19, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setFundingSource = function(value) {
  jspb.Message.setProto3StringField(this, 19, value);
};


/**
 * optional string technical_class = 21;
 * @return {string}
 */
proto.assets.Road.prototype.getTechnicalClass = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 21, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setTechnicalClass = function(value) {
  jspb.Message.setProto3StringField(this, 21, value);
};


/**
 * optional string maintenance_need = 22;
 * @return {string}
 */
proto.assets.Road.prototype.getMaintenanceNeed = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 22, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setMaintenanceNeed = function(value) {
  jspb.Message.setProto3StringField(this, 22, value);
};


/**
 * optional string traffic_level = 23;
 * @return {string}
 */
proto.assets.Road.prototype.getTrafficLevel = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 23, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setTrafficLevel = function(value) {
  jspb.Message.setProto3StringField(this, 23, value);
};


/**
 * optional uint32 last_revision_id = 24;
 * @return {number}
 */
proto.assets.Road.prototype.getLastRevisionId = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 24, 0));
};


/** @param {number} value */
proto.assets.Road.prototype.setLastRevisionId = function(value) {
  jspb.Message.setProto3IntField(this, 24, value);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.assets.Roads.repeatedFields_ = [1];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.assets.Roads.prototype.toObject = function(opt_includeInstance) {
  return proto.assets.Roads.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.assets.Roads} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.Roads.toObject = function(includeInstance, msg) {
  var f, obj = {
    roadsList: jspb.Message.toObjectList(msg.getRoadsList(),
    proto.assets.Road.toObject, includeInstance)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.assets.Roads}
 */
proto.assets.Roads.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.assets.Roads;
  return proto.assets.Roads.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.assets.Roads} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.assets.Roads}
 */
proto.assets.Roads.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new proto.assets.Road;
      reader.readMessage(value,proto.assets.Road.deserializeBinaryFromReader);
      msg.addRoads(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.assets.Roads.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.assets.Roads.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.assets.Roads} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.Roads.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getRoadsList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      1,
      f,
      proto.assets.Road.serializeBinaryToWriter
    );
  }
};


/**
 * repeated Road roads = 1;
 * @return {!Array<!proto.assets.Road>}
 */
proto.assets.Roads.prototype.getRoadsList = function() {
  return /** @type{!Array<!proto.assets.Road>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.assets.Road, 1));
};


/** @param {!Array<!proto.assets.Road>} value */
proto.assets.Roads.prototype.setRoadsList = function(value) {
  jspb.Message.setRepeatedWrapperField(this, 1, value);
};


/**
 * @param {!proto.assets.Road=} opt_value
 * @param {number=} opt_index
 * @return {!proto.assets.Road}
 */
proto.assets.Roads.prototype.addRoads = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 1, opt_value, proto.assets.Road, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 */
proto.assets.Roads.prototype.clearRoadsList = function() {
  this.setRoadsList([]);
};


goog.object.extend(exports, proto.assets);
