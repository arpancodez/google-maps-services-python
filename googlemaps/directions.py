# Copyright 2014 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions.

"""Wrapper for Google Maps Directions API requests."""

from googlemaps import convert


def directions(
    client,
    origin,
    destination,
    mode=None,
    waypoints=None,
    alternatives=False,
    avoid=None,
    language=None,
    units=None,
    region=None,
    departure_time=None,
    arrival_time=None,
    optimize_waypoints=False,
    transit_mode=None,
    transit_routing_preference=None,
    traffic_model=None,
):
    """Request directions between an origin and a destination."""

    params = {
        "origin": convert.latlng(origin),
        "destination": convert.latlng(destination),
    }

    # travel mode
    if mode:
        valid_modes = {"driving", "walking", "bicycling", "transit"}
        if mode not in valid_modes:
            raise ValueError(f"Invalid travel mode: {mode}")
        params["mode"] = mode

    # waypoints
    if waypoints:
        wp = convert.location_list(waypoints)
        if optimize_waypoints:
            wp = f"optimize:true|{wp}"
        params["waypoints"] = wp

    if alternatives:
        params["alternatives"] = "true"

    if avoid:
        params["avoid"] = convert.join_list("|", avoid)

    if language:
        params["language"] = language

    if units:
        params["units"] = units

    if region:
        params["region"] = region

    if departure_time and arrival_time:
        raise ValueError("Specify only one of departure_time or arrival_time.")

    if departure_time:
        params["departure_time"] = convert.time(departure_time)

    if arrival_time:
        params["arrival_time"] = convert.time(arrival_time)

    if transit_mode:
        params["transit_mode"] = convert.join_list("|", transit_mode)

    if transit_routing_preference:
        params["transit_routing_preference"] = transit_routing_preference

    if traffic_model:
        params["traffic_model"] = traffic_model

    # return only routes
    response = client._request("/maps/api/directions/json", params)
    return response.get("routes", [])
