// create a websocket connection to the Rails webserver
  var uri = "ws://" + window.document.location.host + "/",
  ws = ws || new WebSocket(uri);

  // Define ws event handlers
  ws.onmessage = function (message){
    var command = JSON.parse(message.data);
    fetchStatus = $("#attribute_tracker").data();
    my_user_id = fetchStatus.userId;
    my_sensor_id = fetchStatus.sensorId;
    if (command.requester === "robot" && command.user_id === my_user_id) {
      var uriString = "/users/" + my_user_id + "/sensors/" + my_sensor_id
        + "/readings/";
      uriString = encodeURI(uriString);
      $.ajax({
        url: uriString,
        method: 'POST',
        data: {
          result: command.reading
        },
        success: function(response, status){
          // render the reading in the view
          var dom_target = response.sensor_type + '-' + response.sensor_id;
          $("#" + dom_target + '-reading').html(response.reading_value);
          $("#" + dom_target + '-time').html(response.time);
        },
        error: function(response, status){
          var dom_target = response.sensor_type + '-' + response.sensor_id;
          $("#" + dom_target + '-reading').html("UNABLE TO FETCH PLEASE RETRY");
          $("#" + dom_target + '-time').html(response.time);        }
      });
    }
  };
  ws.onopen = function (){
    console.log('connected to websocket on ' + uri);
  };

$(function(){
  // this event sends the JSON request to Rails over WebSocket
  $(".dashboard-btn").on("click", function() {
    // $("#realtime_value").show();
    var fetchStatus = $("#attribute_tracker").data();
    var dom_target = this.id.split('-')
    fetchStatus.sensorType = dom_target[0]
    fetchStatus.sensorId = dom_target[1]

    flash_target_dom(dom_target[0] + '-' + dom_target[1])

    ws.send(JSON.stringify(
      {
        user_id: fetchStatus.userId,
        sensor_type: fetchStatus.sensorType,
        sensor_id: fetchStatus.sensorId,
        requester: "user",
        reading: null,
        time: null
      })
    );
  });
})
