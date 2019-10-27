mergeInto(LibraryManager.library, {
  GetBowId: function() {
    var bow_id = window.location.search.substring(1).split("=")[1];
    console.log("bow_id: " + bow_id);
    var bufferSize = lengthBytesUTF8(bow_id) + 1;
    var buffer = _malloc(bufferSize);
    stringToUTF8(bow_id, buffer, bufferSize);
    return buffer;
  },
});
