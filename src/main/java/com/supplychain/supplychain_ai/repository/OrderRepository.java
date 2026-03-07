package com.supplychain.supplychain_ai.repository;

import com.supplychain.supplychain_ai.entity.Order;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<Order, Long> {
}