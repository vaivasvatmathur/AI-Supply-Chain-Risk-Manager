package com.supplychain.supplychain_ai.repository;

import com.supplychain.supplychain_ai.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepository extends JpaRepository<Product, Long> {
}