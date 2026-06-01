package com.supplychain.supplychain_ai.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class WeatherService {

    private final RestTemplate restTemplate;
    private final String apiKey;

    public WeatherService(RestTemplate restTemplate,
                          @Value("${openweather.api.key:}") String apiKey) {
        this.restTemplate = restTemplate;
        this.apiKey = apiKey;
    }

    public String getWeatherData() {
        if (apiKey == null || apiKey.isBlank()) {
            return "{\"error\":\"OPENWEATHER_API_KEY is not configured\"}";
        }

        String url = "https://api.openweathermap.org/data/2.5/weather?q=Mumbai&appid="
                + apiKey
                + "&units=metric";

        return restTemplate.getForObject(url, String.class);
    }
}