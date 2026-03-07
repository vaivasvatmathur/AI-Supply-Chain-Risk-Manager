package com.supplychain.supplychain_ai.entity;

import jakarta.persistence.*;

@Entity
public class Recommendation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long orderId;

    private Long recommendedSupplierId;

    private double estimatedCost;

    private int estimatedDelivery;

    private String agentReason;

    public Recommendation() {}

    public Long getId() {
        return id;
    }

    public Long getOrderId() {
        return orderId;
    }

    public Long getRecommendedSupplierId() {
        return recommendedSupplierId;
    }

    public double getEstimatedCost() {
        return estimatedCost;
    }

    public int getEstimatedDelivery() {
        return estimatedDelivery;
    }

    public String getAgentReason() {
        return agentReason;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setOrderId(Long orderId) {
        this.orderId = orderId;
    }

    public void setRecommendedSupplierId(Long recommendedSupplierId) {
        this.recommendedSupplierId = recommendedSupplierId;
    }

    public void setEstimatedCost(double estimatedCost) {
        this.estimatedCost = estimatedCost;
    }

    public void setEstimatedDelivery(int estimatedDelivery) {
        this.estimatedDelivery = estimatedDelivery;
    }

    public void setAgentReason(String agentReason) {
        this.agentReason = agentReason;
    }
}