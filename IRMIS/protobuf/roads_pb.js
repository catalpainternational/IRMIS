/**
 * @fileoverview
 * @enhanceable
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
  proto.assets.Road.displayName = 'proto.assets.Road';
}


if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.assets.Road.prototype.toObject = function(opt_includeInstance) {
  return proto.assets.Road.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.assets.Road} msg The msg instance to transform.
 * @return {!Object}
 */
proto.assets.Road.toObject = function(includeInstance, msg) {
  var f, obj = {
    id: jspb.Message.getField(msg, 1),
    geojsonId: jspb.Message.getField(msg, 2),
    roadCode: jspb.Message.getField(msg, 3),
    roadName: jspb.Message.getField(msg, 4),
    linkCode: jspb.Message.getField(msg, 5),
    linkName: jspb.Message.getField(msg, 6),
    linkLength: jspb.Message.getOptionalFloatingPointField(msg, 7),
    surfaceType: jspb.Message.getField(msg, 8),
    surfaceCondition: jspb.Message.getField(msg, 9),
    roadType: jspb.Message.getField(msg, 10)
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
    case 5:
      var value = /** @type {string} */ (reader.readString());
      msg.setLinkCode(value);
      break;
    case 6:
      var value = /** @type {string} */ (reader.readString());
      msg.setLinkName(value);
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
    case 10:
      var value = /** @type {string} */ (reader.readString());
      msg.setRoadType(value);
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
 */
proto.assets.Road.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = /** @type {number} */ (jspb.Message.getField(message, 1));
  if (f != null) {
    writer.writeUint32(
      1,
      f
    );
  }
  f = /** @type {number} */ (jspb.Message.getField(message, 2));
  if (f != null) {
    writer.writeUint32(
      2,
      f
    );
  }
  f = /** @type {string} */ (jspb.Message.getField(message, 3));
  if (f != null) {
    writer.writeString(
      3,
      f
    );
  }
  f = /** @type {string} */ (jspb.Message.getField(message, 4));
  if (f != null) {
    writer.writeString(
      4,
      f
    );
  }
  f = /** @type {string} */ (jspb.Message.getField(message, 5));
  if (f != null) {
    writer.writeString(
      5,
      f
    );
  }
  f = /** @type {string} */ (jspb.Message.getField(message, 6));
  if (f != null) {
    writer.writeString(
      6,
      f
    );
  }
  f = /** @type {number} */ (jspb.Message.getField(message, 7));
  if (f != null) {
    writer.writeFloat(
      7,
      f
    );
  }
  f = /** @type {string} */ (jspb.Message.getField(message, 8));
  if (f != null) {
    writer.writeString(
      8,
      f
    );
  }
  f = /** @type {string} */ (jspb.Message.getField(message, 9));
  if (f != null) {
    writer.writeString(
      9,
      f
    );
  }
  f = /** @type {string} */ (jspb.Message.getField(message, 10));
  if (f != null) {
    writer.writeString(
      10,
      f
    );
  }
};


/**
 * required uint32 id = 1;
 * @return {number}
 */
proto.assets.Road.prototype.getId = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 1, 0));
};


/** @param {number} value */
proto.assets.Road.prototype.setId = function(value) {
  jspb.Message.setField(this, 1, value);
};


proto.assets.Road.prototype.clearId = function() {
  jspb.Message.setField(this, 1, undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.assets.Road.prototype.hasId = function() {
  return jspb.Message.getField(this, 1) != null;
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
  jspb.Message.setField(this, 2, value);
};


proto.assets.Road.prototype.clearGeojsonId = function() {
  jspb.Message.setField(this, 2, undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.assets.Road.prototype.hasGeojsonId = function() {
  return jspb.Message.getField(this, 2) != null;
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
  jspb.Message.setField(this, 3, value);
};


proto.assets.Road.prototype.clearRoadCode = function() {
  jspb.Message.setField(this, 3, undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.assets.Road.prototype.hasRoadCode = function() {
  return jspb.Message.getField(this, 3) != null;
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
  jspb.Message.setField(this, 4, value);
};


proto.assets.Road.prototype.clearRoadName = function() {
  jspb.Message.setField(this, 4, undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.assets.Road.prototype.hasRoadName = function() {
  return jspb.Message.getField(this, 4) != null;
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
  jspb.Message.setField(this, 5, value);
};


proto.assets.Road.prototype.clearLinkCode = function() {
  jspb.Message.setField(this, 5, undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.assets.Road.prototype.hasLinkCode = function() {
  return jspb.Message.getField(this, 5) != null;
};


/**
 * optional string link_name = 6;
 * @return {string}
 */
proto.assets.Road.prototype.getLinkName = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 6, ""));
};


/** @param {string} value */
proto.assets.Road.prototype.setLinkName = function(value) {
  jspb.Message.setField(this, 6, value);
};


proto.assets.Road.prototype.clearLinkName = function() {
  jspb.Message.setField(this, 6, undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.assets.Road.prototype.hasLinkName = function() {
  return jspb.Message.getField(this, 6) != null;
};


/**
 * optional float link_length = 7;
 * @return {number}
 */
proto.assets.Road.prototype.getLinkLength = function() {
  return /** @type {number} */ (+jspb.Message.getFieldWithDefault(this, 7, 0.0));
};


/** @param {number} value */
proto.assets.Road.prototype.setLinkLength = function(value) {
  jspb.Message.setField(this, 7, value);
};


proto.assets.Road.prototype.clearLinkLength = function() {
  jspb.Message.setField(this, 7, undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.assets.Road.prototype.hasLinkLength = function() {
  return jspb.Message.getField(this, 7) != null;
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
  jspb.Message.setField(this, 8, value);
};


proto.assets.Road.prototype.clearSurfaceType = function() {
  jspb.Message.setField(this, 8, undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.assets.Road.prototype.hasSurfaceType = function() {
  return jspb.Message.getField(this, 8) != null;
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
  jspb.Message.setField(this, 9, value);
};


proto.assets.Road.prototype.clearSurfaceCondition = function() {
  jspb.Message.setField(this, 9, undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.assets.Road.prototype.hasSurfaceCondition = function() {
  return jspb.Message.getField(this, 9) != null;
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
  jspb.Message.setField(this, 10, value);
};


proto.assets.Road.prototype.clearRoadType = function() {
  jspb.Message.setField(this, 10, undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.assets.Road.prototype.hasRoadType = function() {
  return jspb.Message.getField(this, 10) != null;
};



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
  proto.assets.Roads.displayName = 'proto.assets.Roads';
}
/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.assets.Roads.repeatedFields_ = [1];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.assets.Roads.prototype.toObject = function(opt_includeInstance) {
  return proto.assets.Roads.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.assets.Roads} msg The msg instance to transform.
 * @return {!Object}
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
 * If you change this array by adding, removing or replacing elements, or if you
 * replace the array itself, then you must call the setter to update it.
 * @return {!Array.<!proto.assets.Road>}
 */
proto.assets.Roads.prototype.getRoadsList = function() {
  return /** @type{!Array.<!proto.assets.Road>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.assets.Road, 1));
};


/** @param {!Array.<!proto.assets.Road>} value */
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


proto.assets.Roads.prototype.clearRoadsList = function() {
  this.setRoadsList([]);
};


goog.object.extend(exports, proto.assets);
