// source: survey.proto
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

var google_protobuf_timestamp_pb = require('google-protobuf/google/protobuf/timestamp_pb.js');
goog.object.extend(proto, google_protobuf_timestamp_pb);
goog.exportSymbol('proto.assets.Survey', null, global);
goog.exportSymbol('proto.assets.Surveys', null, global);
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
proto.assets.Survey = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.assets.Survey, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.assets.Survey.displayName = 'proto.assets.Survey';
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
proto.assets.Surveys = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.assets.Surveys.repeatedFields_, null);
};
goog.inherits(proto.assets.Surveys, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.assets.Surveys.displayName = 'proto.assets.Surveys';
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
proto.assets.Survey.prototype.toObject = function(opt_includeInstance) {
  return proto.assets.Survey.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.assets.Survey} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.Survey.toObject = function(includeInstance, msg) {
  var f, obj = {
    id: jspb.Message.getFieldWithDefault(msg, 1, 0),
    roadId: jspb.Message.getFieldWithDefault(msg, 12, 0),
    roadCode: jspb.Message.getFieldWithDefault(msg, 2, ""),
    user: jspb.Message.getFieldWithDefault(msg, 3, 0),
    source: jspb.Message.getFieldWithDefault(msg, 9, ""),
    dateUpdated: (f = msg.getDateUpdated()) && google_protobuf_timestamp_pb.Timestamp.toObject(includeInstance, f),
    dateSurveyed: (f = msg.getDateSurveyed()) && google_protobuf_timestamp_pb.Timestamp.toObject(includeInstance, f),
    chainageStart: jspb.Message.getFloatingPointFieldWithDefault(msg, 5, 0.0),
    chainageEnd: jspb.Message.getFloatingPointFieldWithDefault(msg, 6, 0.0),
    values: jspb.Message.getFieldWithDefault(msg, 7, ""),
    addedBy: jspb.Message.getFieldWithDefault(msg, 11, "")
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
 * @return {!proto.assets.Survey}
 */
proto.assets.Survey.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.assets.Survey;
  return proto.assets.Survey.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.assets.Survey} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.assets.Survey}
 */
proto.assets.Survey.deserializeBinaryFromReader = function(msg, reader) {
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
    case 12:
      var value = /** @type {number} */ (reader.readUint32());
      msg.setRoadId(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setRoadCode(value);
      break;
    case 3:
      var value = /** @type {number} */ (reader.readUint32());
      msg.setUser(value);
      break;
    case 9:
      var value = /** @type {string} */ (reader.readString());
      msg.setSource(value);
      break;
    case 4:
      var value = new google_protobuf_timestamp_pb.Timestamp;
      reader.readMessage(value,google_protobuf_timestamp_pb.Timestamp.deserializeBinaryFromReader);
      msg.setDateUpdated(value);
      break;
    case 8:
      var value = new google_protobuf_timestamp_pb.Timestamp;
      reader.readMessage(value,google_protobuf_timestamp_pb.Timestamp.deserializeBinaryFromReader);
      msg.setDateSurveyed(value);
      break;
    case 5:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setChainageStart(value);
      break;
    case 6:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setChainageEnd(value);
      break;
    case 7:
      var value = /** @type {string} */ (reader.readString());
      msg.setValues(value);
      break;
    case 11:
      var value = /** @type {string} */ (reader.readString());
      msg.setAddedBy(value);
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
proto.assets.Survey.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.assets.Survey.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.assets.Survey} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.Survey.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getId();
  if (f !== 0) {
    writer.writeUint32(
      1,
      f
    );
  }
  f = message.getRoadId();
  if (f !== 0) {
    writer.writeUint32(
      12,
      f
    );
  }
  f = message.getRoadCode();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getUser();
  if (f !== 0) {
    writer.writeUint32(
      3,
      f
    );
  }
  f = message.getSource();
  if (f.length > 0) {
    writer.writeString(
      9,
      f
    );
  }
  f = message.getDateUpdated();
  if (f != null) {
    writer.writeMessage(
      4,
      f,
      google_protobuf_timestamp_pb.Timestamp.serializeBinaryToWriter
    );
  }
  f = message.getDateSurveyed();
  if (f != null) {
    writer.writeMessage(
      8,
      f,
      google_protobuf_timestamp_pb.Timestamp.serializeBinaryToWriter
    );
  }
  f = message.getChainageStart();
  if (f !== 0.0) {
    writer.writeFloat(
      5,
      f
    );
  }
  f = message.getChainageEnd();
  if (f !== 0.0) {
    writer.writeFloat(
      6,
      f
    );
  }
  f = message.getValues();
  if (f.length > 0) {
    writer.writeString(
      7,
      f
    );
  }
  f = message.getAddedBy();
  if (f.length > 0) {
    writer.writeString(
      11,
      f
    );
  }
};


/**
 * optional uint32 id = 1;
 * @return {number}
 */
proto.assets.Survey.prototype.getId = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 1, 0));
};


/**
 * @param {number} value
 * @return {!proto.assets.Survey} returns this
 */
proto.assets.Survey.prototype.setId = function(value) {
  return jspb.Message.setProto3IntField(this, 1, value);
};


/**
 * optional uint32 road_id = 12;
 * @return {number}
 */
proto.assets.Survey.prototype.getRoadId = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 12, 0));
};


/**
 * @param {number} value
 * @return {!proto.assets.Survey} returns this
 */
proto.assets.Survey.prototype.setRoadId = function(value) {
  return jspb.Message.setProto3IntField(this, 12, value);
};


/**
 * optional string road_code = 2;
 * @return {string}
 */
proto.assets.Survey.prototype.getRoadCode = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/**
 * @param {string} value
 * @return {!proto.assets.Survey} returns this
 */
proto.assets.Survey.prototype.setRoadCode = function(value) {
  return jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * optional uint32 user = 3;
 * @return {number}
 */
proto.assets.Survey.prototype.getUser = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 3, 0));
};


/**
 * @param {number} value
 * @return {!proto.assets.Survey} returns this
 */
proto.assets.Survey.prototype.setUser = function(value) {
  return jspb.Message.setProto3IntField(this, 3, value);
};


/**
 * optional string source = 9;
 * @return {string}
 */
proto.assets.Survey.prototype.getSource = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 9, ""));
};


/**
 * @param {string} value
 * @return {!proto.assets.Survey} returns this
 */
proto.assets.Survey.prototype.setSource = function(value) {
  return jspb.Message.setProto3StringField(this, 9, value);
};


/**
 * optional google.protobuf.Timestamp date_updated = 4;
 * @return {?proto.google.protobuf.Timestamp}
 */
proto.assets.Survey.prototype.getDateUpdated = function() {
  return /** @type{?proto.google.protobuf.Timestamp} */ (
    jspb.Message.getWrapperField(this, google_protobuf_timestamp_pb.Timestamp, 4));
};


/**
 * @param {?proto.google.protobuf.Timestamp|undefined} value
 * @return {!proto.assets.Survey} returns this
*/
proto.assets.Survey.prototype.setDateUpdated = function(value) {
  return jspb.Message.setWrapperField(this, 4, value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.assets.Survey} returns this
 */
proto.assets.Survey.prototype.clearDateUpdated = function() {
  return this.setDateUpdated(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.assets.Survey.prototype.hasDateUpdated = function() {
  return jspb.Message.getField(this, 4) != null;
};


/**
 * optional google.protobuf.Timestamp date_surveyed = 8;
 * @return {?proto.google.protobuf.Timestamp}
 */
proto.assets.Survey.prototype.getDateSurveyed = function() {
  return /** @type{?proto.google.protobuf.Timestamp} */ (
    jspb.Message.getWrapperField(this, google_protobuf_timestamp_pb.Timestamp, 8));
};


/**
 * @param {?proto.google.protobuf.Timestamp|undefined} value
 * @return {!proto.assets.Survey} returns this
*/
proto.assets.Survey.prototype.setDateSurveyed = function(value) {
  return jspb.Message.setWrapperField(this, 8, value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.assets.Survey} returns this
 */
proto.assets.Survey.prototype.clearDateSurveyed = function() {
  return this.setDateSurveyed(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.assets.Survey.prototype.hasDateSurveyed = function() {
  return jspb.Message.getField(this, 8) != null;
};


/**
 * optional float chainage_start = 5;
 * @return {number}
 */
proto.assets.Survey.prototype.getChainageStart = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 5, 0.0));
};


/**
 * @param {number} value
 * @return {!proto.assets.Survey} returns this
 */
proto.assets.Survey.prototype.setChainageStart = function(value) {
  return jspb.Message.setProto3FloatField(this, 5, value);
};


/**
 * optional float chainage_end = 6;
 * @return {number}
 */
proto.assets.Survey.prototype.getChainageEnd = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 6, 0.0));
};


/**
 * @param {number} value
 * @return {!proto.assets.Survey} returns this
 */
proto.assets.Survey.prototype.setChainageEnd = function(value) {
  return jspb.Message.setProto3FloatField(this, 6, value);
};


/**
 * optional string values = 7;
 * @return {string}
 */
proto.assets.Survey.prototype.getValues = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 7, ""));
};


/**
 * @param {string} value
 * @return {!proto.assets.Survey} returns this
 */
proto.assets.Survey.prototype.setValues = function(value) {
  return jspb.Message.setProto3StringField(this, 7, value);
};


/**
 * optional string added_by = 11;
 * @return {string}
 */
proto.assets.Survey.prototype.getAddedBy = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 11, ""));
};


/**
 * @param {string} value
 * @return {!proto.assets.Survey} returns this
 */
proto.assets.Survey.prototype.setAddedBy = function(value) {
  return jspb.Message.setProto3StringField(this, 11, value);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.assets.Surveys.repeatedFields_ = [1];



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
proto.assets.Surveys.prototype.toObject = function(opt_includeInstance) {
  return proto.assets.Surveys.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.assets.Surveys} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.Surveys.toObject = function(includeInstance, msg) {
  var f, obj = {
    surveysList: jspb.Message.toObjectList(msg.getSurveysList(),
    proto.assets.Survey.toObject, includeInstance)
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
 * @return {!proto.assets.Surveys}
 */
proto.assets.Surveys.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.assets.Surveys;
  return proto.assets.Surveys.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.assets.Surveys} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.assets.Surveys}
 */
proto.assets.Surveys.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new proto.assets.Survey;
      reader.readMessage(value,proto.assets.Survey.deserializeBinaryFromReader);
      msg.addSurveys(value);
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
proto.assets.Surveys.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.assets.Surveys.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.assets.Surveys} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.Surveys.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getSurveysList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      1,
      f,
      proto.assets.Survey.serializeBinaryToWriter
    );
  }
};


/**
 * repeated Survey surveys = 1;
 * @return {!Array<!proto.assets.Survey>}
 */
proto.assets.Surveys.prototype.getSurveysList = function() {
  return /** @type{!Array<!proto.assets.Survey>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.assets.Survey, 1));
};


/**
 * @param {!Array<!proto.assets.Survey>} value
 * @return {!proto.assets.Surveys} returns this
*/
proto.assets.Surveys.prototype.setSurveysList = function(value) {
  return jspb.Message.setRepeatedWrapperField(this, 1, value);
};


/**
 * @param {!proto.assets.Survey=} opt_value
 * @param {number=} opt_index
 * @return {!proto.assets.Survey}
 */
proto.assets.Surveys.prototype.addSurveys = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 1, opt_value, proto.assets.Survey, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 * @return {!proto.assets.Surveys} returns this
 */
proto.assets.Surveys.prototype.clearSurveysList = function() {
  return this.setSurveysList([]);
};


goog.object.extend(exports, proto.assets);
