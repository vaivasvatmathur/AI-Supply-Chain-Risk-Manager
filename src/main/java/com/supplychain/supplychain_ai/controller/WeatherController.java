package com.supplychain.supplychain_ai.controller;

import com.supplychain.supplychain_ai.service.WeatherService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/weather")
public class WeatherController {

    private final WeatherService weatherService;

    public WeatherController(WeatherService weatherService) {
        this.weatherService = weatherService;
    }

    @GetMapping("/mumbai")
    public String getMumbaiWeather() {
        return weatherService.getWeatherData();
    }
}