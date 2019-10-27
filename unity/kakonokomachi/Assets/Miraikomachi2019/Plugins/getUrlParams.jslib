mergeInto(LibraryManager.library, {
  GetBowId: function() {
    var params_dict = window.location.search.substring(1).split('&').reduce((result, query) => {
    const [k, v] = query.split('=');
    result[k] = decodeURI(v);
    return result;
    }, {});
    var bow_id = params_dict["bow_id"];
    console.log(bow_id);
    alert(bow_id);
    var bufferSize = lengthBytesUTF8(bow_id) + 1;
    var buffer = _malloc(bufferSize);
    stringToUTF8(bow_id, buffer, bufferSize);
    return buffer;
  },
});
