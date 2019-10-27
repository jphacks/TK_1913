mergeInto(LibraryManager.library, {
  GetBowId: function() {
    var searchParams = new URLSearchParams(location.search);
    var bow_id = searchParams.get("bow_id");
    console.log(bow_id);
    alert(bow_id);
    var bufferSize = lengthBytesUTF8(bow_id) + 1;
    var buffer = _malloc(bufferSize);
    stringToUTF8(bow_id, buffer, bufferSize);
    return buffer;
  },
});
