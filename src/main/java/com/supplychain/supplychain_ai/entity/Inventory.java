package com.supplychain.supplychain_ai.entity;

import jakarta.persistence.*;

@Entity
public class Inventory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long productId;
    private int stockLevel;
    private int reorderPoint;
    private String warehouseLocation;

    public Inventory(){}

    public Long getId(){ return id; }
    public Long getProductId(){ return productId; }
    public int getStockLevel(){ return stockLevel; }
    public int getReorderPoint(){ return reorderPoint; }
    public String getWarehouseLocation(){ return warehouseLocation; }

    public void setId(Long id){ this.id = id; }
    public void setProductId(Long productId){ this.productId = productId; }
    public void setStockLevel(int stockLevel){ this.stockLevel = stockLevel; }
    public void setReorderPoint(int reorderPoint){ this.reorderPoint = reorderPoint; }
    public void setWarehouseLocation(String warehouseLocation){ this.warehouseLocation = warehouseLocation; }
}