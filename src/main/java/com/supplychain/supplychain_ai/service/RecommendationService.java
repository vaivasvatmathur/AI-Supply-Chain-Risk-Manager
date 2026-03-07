package com.supplychain.supplychain_ai.service;

import com.supplychain.supplychain_ai.entity.Supplier;
import com.supplychain.supplychain_ai.entity.Recommendation;
import com.supplychain.supplychain_ai.repository.SupplierRepository;
import com.supplychain.supplychain_ai.repository.RecommendationRepository;

import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RecommendationService {

    private final SupplierRepository supplierRepository;
    private final RecommendationRepository recommendationRepository;

    public RecommendationService(SupplierRepository supplierRepository,
                                 RecommendationRepository recommendationRepository) {
        this.supplierRepository = supplierRepository;
        this.recommendationRepository = recommendationRepository;
    }

    public Recommendation recommendBestSupplier(Long orderId) {

        List<Supplier> suppliers = supplierRepository.findAll();

        Supplier bestSupplier = suppliers.stream()
                .max((s1, s2) -> Double.compare(
                        s1.getReliabilityScore(),
                        s2.getReliabilityScore()))
                .orElse(null);

        Recommendation recommendation = new Recommendation();

        recommendation.setOrderId(orderId);
        recommendation.setRecommendedSupplierId(bestSupplier.getId());
        recommendation.setEstimatedCost(bestSupplier.getCostIndex());
        recommendation.setEstimatedDelivery(bestSupplier.getAvgDeliveryTime());
        recommendation.setAgentReason("Selected highest reliability supplier");

        return recommendationRepository.save(recommendation);
    }
}