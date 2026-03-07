package com.supplychain.supplychain_ai.entity;

import jakarta.persistence.*;

@Entity
public class Supplier {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String location;
    private double reliabilityScore;
    private int avgDeliveryTime;
    private double costIndex;

    public Supplier() {}

    public Supplier(Long id, String name, String location,
                    double reliabilityScore, int avgDeliveryTime,
                    double costIndex) {
        this.id = id;
        this.name = name;
        this.location = location;
        this.reliabilityScore = reliabilityScore;
        this.avgDeliveryTime = avgDeliveryTime;
        this.costIndex = costIndex;
    }

    public Long getId() { return id; }
    public String getName() { return name; }
    public String getLocation() { return location; }
    public double getReliabilityScore() { return reliabilityScore; }
    public int getAvgDeliveryTime() { return avgDeliveryTime; }
    public double getCostIndex() { return costIndex; }

    public void setId(Long id) { this.id = id; }
    public void setName(String name) { this.name = name; }
    public void setLocation(String location) { this.location = location; }
    public void setReliabilityScore(double reliabilityScore) { this.reliabilityScore = reliabilityScore; }
    public void setAvgDeliveryTime(int avgDeliveryTime) { this.avgDeliveryTime = avgDeliveryTime; }
    public void setCostIndex(double costIndex) { this.costIndex = costIndex; }
}