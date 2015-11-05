class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  protect_from_forgery with: :exception
  helper_method :fetch_sensor_image, :authenticate, :current_user, :logged_in?, :user_authenticate, :user_as_requester, :get_path, :fetch_sensor_guide

  def fetch_sensor_image(sensorType)
    sensorArray = {
      light: "light.png",
      temperature: "temp.png",
      airquality: "airquality.png",
      gas: "gas.png",
      sound: "sound.png",
      ultrasonic: "ultrasonic.png",
      humidity: "humidity.png"
    }
    sensorArray[sensorType.to_sym]
  end

  def fetch_sensor_guide(sensorType)
    sensorArray = {
      light: "tells you if it is bright or dark",
      temperature: "gives a value in celcius for you",
      airquality: "airquality.png",
      gas: "gas.png",
      sound: "sound.png",
      ultrasonic: "ultrasonic.png",
      humidity: "humidity.png"
    }
    sensorArray[sensorType.to_sym]
  end

  def authenticate
    unless logged_in?
      flash[:error] = "You must be logged in to access this section of the site"
      redirect_to login_path
    end
  end

  def user_authenticate
    unless current_user.id == user_as_requester.to_i
      flash[:error] = "no access right"
      redirect_to login_path
    end
  end

  # def get_path
  #   route_hash = Hash.new
  #   route_info = Rails.application.routes.recognize_path(request.env['PATH_INFO'])
  #   if route_info[:controller] == 'readings'
  #     route_info[:user_id]
  #   elsif route_info[:controller] == 'sensors'
  #     levels = 2
  #   end
  #   # Rails.application.routes.recognize_path(request.env['PATH_INFO'])
  # end

  def user_as_requester
    route_info = Rails.application.routes.recognize_path(request.env['PATH_INFO'])
    if route_info[:controller] == 'sensors'
      route_info[:user_id]
    elsif route_info[:controller] == 'users'
      route_info[:id]
    end
  end

  def current_user
    @current_user ||= User.find(session[:user_id]) if session[:user_id]
  end

  def logged_in?
    !!current_user
  end
end
