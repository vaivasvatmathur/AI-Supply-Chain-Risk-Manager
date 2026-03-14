package com.supplychain.supplychain_ai.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class WeatherService {

    private final String API_KEY = "8a1db6e978cc9a38edbe3d1391e178e3";

    public String getWeatherData() {

        String city = "Mumbai";

        String url = "https://api.openweathermap.org/data/2.5/weather?q="
                + city +
                "&appid=" + API_KEY +
                "&units=metric";

        RestTemplate restTemplate = new RestTemplate();

        String response = restTemplate.getForObject(url, String.class);

        return response;
    }
}