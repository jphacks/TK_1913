mergeInto(LibraryManager.library, {
  GetUrlParams: function() {
    searchParams = new URLSearchParams(location.search);
    return searchParams.getAll();
  },

  TestJs2: function(data) {
    console.log("TestJs2");
    return data;
  },

  TestJs: function() {
    console.log("hoge");
    var ws = new WebSocket("ws://localhost:3001");
    console.log(ws);
    ws.onopen = function(event) {
      console.log("open: " + event);
    };

    ws.onclose = function(event) {
      console.log("close: " + event);
    };

    ws.onmessage = function(event) {
      console.log("msg: " + event);
      _TestJs2(event);
    };
  },

  ReadAnimationValue: function() {
    var value = document.getElementById("animationValue").value;
    console.log(value);
    return value;
  }
});
