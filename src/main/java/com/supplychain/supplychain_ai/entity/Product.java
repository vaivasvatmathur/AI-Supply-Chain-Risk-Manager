package com.supplychain.supplychain_ai.entity;

import jakarta.persistence.*;

@Entity
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String category;

    public Product(){}

    public Long getId(){ return id; }
    public String getName(){ return name; }
    public String getCategory(){ return category; }

    public void setId(Long id){ this.id = id; }
    public void setName(String name){ this.name = name; }
    public void setCategory(String category){ this.category = category; }
}