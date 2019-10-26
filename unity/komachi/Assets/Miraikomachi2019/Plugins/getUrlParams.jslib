mergeInto(LibraryManager.library, {
  GetUrlParams: function() {
    searchParams = new URLSearchParams(location.search);
    return searchParams.getAll();
  },

  GiveJs2Unity: function(data) {
    console.log("TestJs2");
    console.log("data: " + data);
    return data;
  },

  InitWS: function() {
    var ws = new WebSocket("ws://localhost:3001");
    console.log(ws);
    ws.onopen = function(event) {
      console.log("open: " + event);
    };

    ws.onclose = function(event) {
      console.log("close: " + event);
    };

    ws.onmessage = function(event) {
      console.log("msg: " + event.data);
      _GiveJs2Unity(parseFloat(event.data));
    };
  },

  ReadAnimationValue: function() {
    var value = document.getElementById("animationValue").value;
    console.log(value);
    return value;
  }
});
