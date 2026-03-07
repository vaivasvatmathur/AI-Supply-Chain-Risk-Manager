package com.supplychain.supplychain_ai.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
public class RiskAlert {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long orderId;

    private double riskScore;

    private String reason;

    private LocalDateTime timestamp;

    public RiskAlert() {}

    public Long getId() { return id; }
    public Long getOrderId() { return orderId; }
    public double getRiskScore() { return riskScore; }
    public String getReason() { return reason; }
    public LocalDateTime getTimestamp() { return timestamp; }

    public void setId(Long id) { this.id = id; }
    public void setOrderId(Long orderId) { this.orderId = orderId; }
    public void setRiskScore(double riskScore) { this.riskScore = riskScore; }
    public void setReason(String reason) { this.reason = reason; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
}