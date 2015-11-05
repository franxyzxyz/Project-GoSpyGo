// create a websocket connection to the Rails webserver
  var uri = "ws://" + window.document.location.host + "/",
  ws = ws || new WebSocket(uri);

  // LATER CHANGE AGAIN
  // ws.onmessage = function (message){
  //   var command = JSON.parse(message.data);
  //   // fetchStatus retrieves data encoded in the url of the current page.
  //   // We use this to pass the user_id and sensor_id of the current user into the JS scope
  //   fetchStatus = $("#attribute_tracker").data();
  //   my_user_id = fetchStatus.userId;
  //   my_sensor_id = fetchStatus.sensorId;
  //   // if the command is an update from a robot and is meant for this user
  //   if (command.requester === "robot" && command.user_id === my_user_id) {
  //     // update the database
  //     var uriString = "/users/" + my_user_id + "/sensors/" + my_sensor_id
  //       + "/readings/";
  //     uriString = encodeURI(uriString);

  //     // invokes #readings#create in Rails, saves the reading into the database
  //     $.ajax({
  //       url: uriString,
  //       method: 'POST',
  //       data: {
  //         result: command.reading
  //       },
  //       success: function(response, status){
  //         // render the reading in the view
  //         $('#reading-value-box').html(command.reading)
  //         $('#reading-time-box').html(response.time)
  //         // response.sensor_id
  //         // response.sensor_type
  //       },
  //       error: function(response, status){
  //         $('#reading-box').html("Please retry")
  //       }
  //     });
  //   }
  // };

  // testing MODE
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

// LATER DELETE THIS FUCK IF BELOW WORKS
// $(function(){
//   // this event sends the JSON request to Rails over WebSocket
//   $("#fetch-data").on("click", function() {
//     $("#realtime_value").show();
//     var fetchStatus = $("#attribute_tracker").data();

//     ws.send(JSON.stringify(
//       {
//         user_id: fetchStatus.userId, // globally available id
//         sensor_type: fetchStatus.sensorType,
//         sensor_id: fetchStatus.sensorId,
//         requester: "user", // indicates this is sent by a user/frontend
//         reading: null,
//         time: null
//       })
//     );
//   });
// })

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

// function newConnection (uri){
//   ws = new WebSocket(uri);
//   console.log("Woohoo New Connection!!")
//   ws.onmessage = function(message){
//     var data = JSON.parse(message.data);
//     // $("#chat-text").append("<div class='panel panel-default'><div class='panel-heading'>" + data.handle + "</div><div class='panel-body'>" + data.text + "</div></div>");
//     // $("#chat-text").stop().animate({
//     //   scrollTop: $('#chat-text')[0].scrollHeight
//     // }, 800);
//   };
// }

// $(function(){
//     $("#start_connection").on("click", function(event){
//       newConnection(uri);
//     });

//     $("#new_reading").on("submit", function(event) {
//       // Case 1: Connection Error
//       if (typeof ws == 'undefined'){
//         console.log("Not Connceted")
//         event.preventDefault();
//       }else{
//         // Case 2: Update Database(thru form) + Send Message to All Client(in backend)
//         var value = $("#reading_value").val();
//         var fetchStatus = $("#attribute_tracker").data();
//         ws.send(JSON.stringify(
//           {
//             user_id: fetchStatus.userId,
//             sensor_type: fetchStatus.sensorType,
//             sensor_id: fetchStatus.sensorId,
//             time: fetchStatus.time,
//             requester: fetchStatus.requester,
//             reading: value
//           })
//         );
//       }
//     });

//     $("#end_connection").on("click", function(){
//       console.log("DISCONNECT")
//       ws.close();
//       delete ws;
//     })
//   // });

// });