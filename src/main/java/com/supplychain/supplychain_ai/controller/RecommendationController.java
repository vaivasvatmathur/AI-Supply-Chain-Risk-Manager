package com.supplychain.supplychain_ai.controller;

import com.supplychain.supplychain_ai.entity.Recommendation;
import com.supplychain.supplychain_ai.repository.RecommendationRepository;
import com.supplychain.supplychain_ai.service.RecommendationService;

import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/recommendations")
public class RecommendationController {

    private final RecommendationRepository recommendationRepository;
    private final RecommendationService recommendationService;

    public RecommendationController(RecommendationRepository recommendationRepository,
                                    RecommendationService recommendationService) {
        this.recommendationRepository = recommendationRepository;
        this.recommendationService = recommendationService;
    }

    @GetMapping
    public List<Recommendation> getAllRecommendations() {
        return recommendationRepository.findAll();
    }

    @PostMapping("/generate/{orderId}")
    public Recommendation generateRecommendation(@PathVariable Long orderId) {
        return recommendationService.recommendBestSupplier(orderId);
    }
}