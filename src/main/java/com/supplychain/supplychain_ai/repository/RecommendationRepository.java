package com.supplychain.supplychain_ai.repository;

import com.supplychain.supplychain_ai.entity.Recommendation;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RecommendationRepository extends JpaRepository<Recommendation, Long> {
}