package com.supplychain.supplychain_ai.repository;

import com.supplychain.supplychain_ai.entity.Inventory;
import org.springframework.data.jpa.repository.JpaRepository;

public interface InventoryRepository extends JpaRepository<Inventory, Long> {
}