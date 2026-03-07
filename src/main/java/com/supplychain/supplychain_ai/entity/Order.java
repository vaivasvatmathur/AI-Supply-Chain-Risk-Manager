package com.supplychain.supplychain_ai.entity;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name="orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long productId;
    private Long supplierId;

    private int quantity;

    private LocalDate orderDate;
    private LocalDate expectedDelivery;

    private String status;

    public Order(){}

    public Long getId(){ return id; }
    public Long getProductId(){ return productId; }
    public Long getSupplierId(){ return supplierId; }
    public int getQuantity(){ return quantity; }
    public LocalDate getOrderDate(){ return orderDate; }
    public LocalDate getExpectedDelivery(){ return expectedDelivery; }
    public String getStatus(){ return status; }

    public void setId(Long id){ this.id = id; }
    public void setProductId(Long productId){ this.productId = productId; }
    public void setSupplierId(Long supplierId){ this.supplierId = supplierId; }
    public void setQuantity(int quantity){ this.quantity = quantity; }
    public void setOrderDate(LocalDate orderDate){ this.orderDate = orderDate; }
    public void setExpectedDelivery(LocalDate expectedDelivery){ this.expectedDelivery = expectedDelivery; }
    public void setStatus(String status){ this.status = status; }
}