# custom middleware
require 'faye/websocket'
require 'json'
require 'erb'

class WebsocketBackend
  KEEPALIVE_TIME = 15 # in seconds

  def initialize(app)
    @app     = app
    @clients = []
  end

  def call(env)
    if Faye::WebSocket.websocket?(env)
      ws = Faye::WebSocket.new(env, nil, {ping: KEEPALIVE_TIME })

      ws.on :open do |event|
        p [:open, ws.object_id]
        @clients << ws
      end

      # this echos back the message received from the client
      # event.data can be sent as text (String) or binary (Array)
      ws.on :message do |event|
        @parsed_msg = JSON.parse(event.data)
        # parse the message
        if @parsed_msg['requester'] == "robot" ##broadcast to all clients
          # -> UPDATE DATABASE
          # -> send message to all clients
          @clients.each {|client| client.send(event.data)}
        elsif @parsed_msg['requester'] == "user" ##broadcast to all robots

        end

      end

      ws.on :close do |event|
        p [:close, ws.object_id, event.code, event.reason]
        @clients.delete(ws)
        ws = nil
      end

      # Return async Rack response
      ws.rack_response

    else
      @app.call(env)
    end
  end

  ## this is used to escape unsafe HTML content
  # private
  # def sanitize(message)
  #   json = JSON.parse(message)
  #   json.each {|key, value| json[key] = ERB::Util.html_escape(value) }
  #   JSON.generate(json)
  # end
end
# end
