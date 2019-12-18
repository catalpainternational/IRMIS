// source: report.proto
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
goog.exportSymbol('proto.assets.AttributeEntry', null, global);
goog.exportSymbol('proto.assets.AttributeTable', null, global);
goog.exportSymbol('proto.assets.Report', null, global);
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
proto.assets.Report = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.assets.Report.repeatedFields_, null);
};
goog.inherits(proto.assets.Report, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.assets.Report.displayName = 'proto.assets.Report';
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
proto.assets.AttributeTable = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.assets.AttributeTable.repeatedFields_, null);
};
goog.inherits(proto.assets.AttributeTable, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.assets.AttributeTable.displayName = 'proto.assets.AttributeTable';
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
proto.assets.AttributeEntry = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.assets.AttributeEntry, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.assets.AttributeEntry.displayName = 'proto.assets.AttributeEntry';
}

/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.assets.Report.repeatedFields_ = [3];



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
proto.assets.Report.prototype.toObject = function(opt_includeInstance) {
  return proto.assets.Report.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.assets.Report} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.Report.toObject = function(includeInstance, msg) {
  var f, obj = {
    filter: jspb.Message.getFieldWithDefault(msg, 1, ""),
    lengths: jspb.Message.getFieldWithDefault(msg, 2, ""),
    attributeTablesList: jspb.Message.toObjectList(msg.getAttributeTablesList(),
    proto.assets.AttributeTable.toObject, includeInstance)
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
 * @return {!proto.assets.Report}
 */
proto.assets.Report.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.assets.Report;
  return proto.assets.Report.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.assets.Report} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.assets.Report}
 */
proto.assets.Report.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setFilter(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.setLengths(value);
      break;
    case 3:
      var value = new proto.assets.AttributeTable;
      reader.readMessage(value,proto.assets.AttributeTable.deserializeBinaryFromReader);
      msg.addAttributeTables(value);
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
proto.assets.Report.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.assets.Report.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.assets.Report} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.Report.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getFilter();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getLengths();
  if (f.length > 0) {
    writer.writeString(
      2,
      f
    );
  }
  f = message.getAttributeTablesList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      3,
      f,
      proto.assets.AttributeTable.serializeBinaryToWriter
    );
  }
};


/**
 * optional string filter = 1;
 * @return {string}
 */
proto.assets.Report.prototype.getFilter = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/** @param {string} value */
proto.assets.Report.prototype.setFilter = function(value) {
  jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional string lengths = 2;
 * @return {string}
 */
proto.assets.Report.prototype.getLengths = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 2, ""));
};


/** @param {string} value */
proto.assets.Report.prototype.setLengths = function(value) {
  jspb.Message.setProto3StringField(this, 2, value);
};


/**
 * repeated AttributeTable attribute_tables = 3;
 * @return {!Array<!proto.assets.AttributeTable>}
 */
proto.assets.Report.prototype.getAttributeTablesList = function() {
  return /** @type{!Array<!proto.assets.AttributeTable>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.assets.AttributeTable, 3));
};


/** @param {!Array<!proto.assets.AttributeTable>} value */
proto.assets.Report.prototype.setAttributeTablesList = function(value) {
  jspb.Message.setRepeatedWrapperField(this, 3, value);
};


/**
 * @param {!proto.assets.AttributeTable=} opt_value
 * @param {number=} opt_index
 * @return {!proto.assets.AttributeTable}
 */
proto.assets.Report.prototype.addAttributeTables = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 3, opt_value, proto.assets.AttributeTable, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 */
proto.assets.Report.prototype.clearAttributeTablesList = function() {
  this.setAttributeTablesList([]);
};



/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.assets.AttributeTable.repeatedFields_ = [2,3];



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
proto.assets.AttributeTable.prototype.toObject = function(opt_includeInstance) {
  return proto.assets.AttributeTable.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.assets.AttributeTable} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.AttributeTable.toObject = function(includeInstance, msg) {
  var f, obj = {
    primaryAttribute: jspb.Message.getFieldWithDefault(msg, 1, ""),
    dateSurveyed: (f = msg.getDateSurveyed()) && google_protobuf_timestamp_pb.Timestamp.toObject(includeInstance, f),
    secondaryAttributeList: (f = jspb.Message.getRepeatedField(msg, 2)) == null ? undefined : f,
    attributeEntriesList: jspb.Message.toObjectList(msg.getAttributeEntriesList(),
    proto.assets.AttributeEntry.toObject, includeInstance)
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
 * @return {!proto.assets.AttributeTable}
 */
proto.assets.AttributeTable.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.assets.AttributeTable;
  return proto.assets.AttributeTable.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.assets.AttributeTable} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.assets.AttributeTable}
 */
proto.assets.AttributeTable.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setPrimaryAttribute(value);
      break;
    case 4:
      var value = new google_protobuf_timestamp_pb.Timestamp;
      reader.readMessage(value,google_protobuf_timestamp_pb.Timestamp.deserializeBinaryFromReader);
      msg.setDateSurveyed(value);
      break;
    case 2:
      var value = /** @type {string} */ (reader.readString());
      msg.addSecondaryAttribute(value);
      break;
    case 3:
      var value = new proto.assets.AttributeEntry;
      reader.readMessage(value,proto.assets.AttributeEntry.deserializeBinaryFromReader);
      msg.addAttributeEntries(value);
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
proto.assets.AttributeTable.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.assets.AttributeTable.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.assets.AttributeTable} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.AttributeTable.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getPrimaryAttribute();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getDateSurveyed();
  if (f != null) {
    writer.writeMessage(
      4,
      f,
      google_protobuf_timestamp_pb.Timestamp.serializeBinaryToWriter
    );
  }
  f = message.getSecondaryAttributeList();
  if (f.length > 0) {
    writer.writeRepeatedString(
      2,
      f
    );
  }
  f = message.getAttributeEntriesList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      3,
      f,
      proto.assets.AttributeEntry.serializeBinaryToWriter
    );
  }
};


/**
 * optional string primary_attribute = 1;
 * @return {string}
 */
proto.assets.AttributeTable.prototype.getPrimaryAttribute = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/** @param {string} value */
proto.assets.AttributeTable.prototype.setPrimaryAttribute = function(value) {
  jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional google.protobuf.Timestamp date_surveyed = 4;
 * @return {?proto.google.protobuf.Timestamp}
 */
proto.assets.AttributeTable.prototype.getDateSurveyed = function() {
  return /** @type{?proto.google.protobuf.Timestamp} */ (
    jspb.Message.getWrapperField(this, google_protobuf_timestamp_pb.Timestamp, 4));
};


/** @param {?proto.google.protobuf.Timestamp|undefined} value */
proto.assets.AttributeTable.prototype.setDateSurveyed = function(value) {
  jspb.Message.setWrapperField(this, 4, value);
};


/**
 * Clears the message field making it undefined.
 */
proto.assets.AttributeTable.prototype.clearDateSurveyed = function() {
  this.setDateSurveyed(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.assets.AttributeTable.prototype.hasDateSurveyed = function() {
  return jspb.Message.getField(this, 4) != null;
};


/**
 * repeated string secondary_attribute = 2;
 * @return {!Array<string>}
 */
proto.assets.AttributeTable.prototype.getSecondaryAttributeList = function() {
  return /** @type {!Array<string>} */ (jspb.Message.getRepeatedField(this, 2));
};


/** @param {!Array<string>} value */
proto.assets.AttributeTable.prototype.setSecondaryAttributeList = function(value) {
  jspb.Message.setField(this, 2, value || []);
};


/**
 * @param {string} value
 * @param {number=} opt_index
 */
proto.assets.AttributeTable.prototype.addSecondaryAttribute = function(value, opt_index) {
  jspb.Message.addToRepeatedField(this, 2, value, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 */
proto.assets.AttributeTable.prototype.clearSecondaryAttributeList = function() {
  this.setSecondaryAttributeList([]);
};


/**
 * repeated AttributeEntry attribute_entries = 3;
 * @return {!Array<!proto.assets.AttributeEntry>}
 */
proto.assets.AttributeTable.prototype.getAttributeEntriesList = function() {
  return /** @type{!Array<!proto.assets.AttributeEntry>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.assets.AttributeEntry, 3));
};


/** @param {!Array<!proto.assets.AttributeEntry>} value */
proto.assets.AttributeTable.prototype.setAttributeEntriesList = function(value) {
  jspb.Message.setRepeatedWrapperField(this, 3, value);
};


/**
 * @param {!proto.assets.AttributeEntry=} opt_value
 * @param {number=} opt_index
 * @return {!proto.assets.AttributeEntry}
 */
proto.assets.AttributeTable.prototype.addAttributeEntries = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 3, opt_value, proto.assets.AttributeEntry, opt_index);
};


/**
 * Clears the list making it empty but non-null.
 */
proto.assets.AttributeTable.prototype.clearAttributeEntriesList = function() {
  this.setAttributeEntriesList([]);
};





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
proto.assets.AttributeEntry.prototype.toObject = function(opt_includeInstance) {
  return proto.assets.AttributeEntry.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.assets.AttributeEntry} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.AttributeEntry.toObject = function(includeInstance, msg) {
  var f, obj = {
    chainageStart: jspb.Message.getFloatingPointFieldWithDefault(msg, 1, 0.0),
    chainageEnd: jspb.Message.getFloatingPointFieldWithDefault(msg, 2, 0.0),
    values: jspb.Message.getFieldWithDefault(msg, 3, ""),
    surveyId: jspb.Message.getFieldWithDefault(msg, 4, 0),
    dateSurveyed: (f = msg.getDateSurveyed()) && google_protobuf_timestamp_pb.Timestamp.toObject(includeInstance, f),
    addedBy: jspb.Message.getFieldWithDefault(msg, 6, ""),
    primaryAttribute: jspb.Message.getFieldWithDefault(msg, 7, "")
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
 * @return {!proto.assets.AttributeEntry}
 */
proto.assets.AttributeEntry.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.assets.AttributeEntry;
  return proto.assets.AttributeEntry.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.assets.AttributeEntry} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.assets.AttributeEntry}
 */
proto.assets.AttributeEntry.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setChainageStart(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setChainageEnd(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setValues(value);
      break;
    case 4:
      var value = /** @type {number} */ (reader.readUint32());
      msg.setSurveyId(value);
      break;
    case 5:
      var value = new google_protobuf_timestamp_pb.Timestamp;
      reader.readMessage(value,google_protobuf_timestamp_pb.Timestamp.deserializeBinaryFromReader);
      msg.setDateSurveyed(value);
      break;
    case 6:
      var value = /** @type {string} */ (reader.readString());
      msg.setAddedBy(value);
      break;
    case 7:
      var value = /** @type {string} */ (reader.readString());
      msg.setPrimaryAttribute(value);
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
proto.assets.AttributeEntry.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.assets.AttributeEntry.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.assets.AttributeEntry} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.assets.AttributeEntry.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getChainageStart();
  if (f !== 0.0) {
    writer.writeFloat(
      1,
      f
    );
  }
  f = message.getChainageEnd();
  if (f !== 0.0) {
    writer.writeFloat(
      2,
      f
    );
  }
  f = message.getValues();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getSurveyId();
  if (f !== 0) {
    writer.writeUint32(
      4,
      f
    );
  }
  f = message.getDateSurveyed();
  if (f != null) {
    writer.writeMessage(
      5,
      f,
      google_protobuf_timestamp_pb.Timestamp.serializeBinaryToWriter
    );
  }
  f = message.getAddedBy();
  if (f.length > 0) {
    writer.writeString(
      6,
      f
    );
  }
  f = message.getPrimaryAttribute();
  if (f.length > 0) {
    writer.writeString(
      7,
      f
    );
  }
};


/**
 * optional float chainage_start = 1;
 * @return {number}
 */
proto.assets.AttributeEntry.prototype.getChainageStart = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 1, 0.0));
};


/** @param {number} value */
proto.assets.AttributeEntry.prototype.setChainageStart = function(value) {
  jspb.Message.setProto3FloatField(this, 1, value);
};


/**
 * optional float chainage_end = 2;
 * @return {number}
 */
proto.assets.AttributeEntry.prototype.getChainageEnd = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 2, 0.0));
};


/** @param {number} value */
proto.assets.AttributeEntry.prototype.setChainageEnd = function(value) {
  jspb.Message.setProto3FloatField(this, 2, value);
};


/**
 * optional string values = 3;
 * @return {string}
 */
proto.assets.AttributeEntry.prototype.getValues = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/** @param {string} value */
proto.assets.AttributeEntry.prototype.setValues = function(value) {
  jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional uint32 survey_id = 4;
 * @return {number}
 */
proto.assets.AttributeEntry.prototype.getSurveyId = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 4, 0));
};


/** @param {number} value */
proto.assets.AttributeEntry.prototype.setSurveyId = function(value) {
  jspb.Message.setProto3IntField(this, 4, value);
};


/**
 * optional google.protobuf.Timestamp date_surveyed = 5;
 * @return {?proto.google.protobuf.Timestamp}
 */
proto.assets.AttributeEntry.prototype.getDateSurveyed = function() {
  return /** @type{?proto.google.protobuf.Timestamp} */ (
    jspb.Message.getWrapperField(this, google_protobuf_timestamp_pb.Timestamp, 5));
};


/** @param {?proto.google.protobuf.Timestamp|undefined} value */
proto.assets.AttributeEntry.prototype.setDateSurveyed = function(value) {
  jspb.Message.setWrapperField(this, 5, value);
};


/**
 * Clears the message field making it undefined.
 */
proto.assets.AttributeEntry.prototype.clearDateSurveyed = function() {
  this.setDateSurveyed(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.assets.AttributeEntry.prototype.hasDateSurveyed = function() {
  return jspb.Message.getField(this, 5) != null;
};


/**
 * optional string added_by = 6;
 * @return {string}
 */
proto.assets.AttributeEntry.prototype.getAddedBy = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 6, ""));
};


/** @param {string} value */
proto.assets.AttributeEntry.prototype.setAddedBy = function(value) {
  jspb.Message.setProto3StringField(this, 6, value);
};


/**
 * optional string primary_attribute = 7;
 * @return {string}
 */
proto.assets.AttributeEntry.prototype.getPrimaryAttribute = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 7, ""));
};


/** @param {string} value */
proto.assets.AttributeEntry.prototype.setPrimaryAttribute = function(value) {
  jspb.Message.setProto3StringField(this, 7, value);
};


goog.object.extend(exports, proto.assets);
