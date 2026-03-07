package com.supplychain.supplychain_ai.repository;

import com.supplychain.supplychain_ai.entity.Supplier;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SupplierRepository extends JpaRepository<Supplier, Long> {
}