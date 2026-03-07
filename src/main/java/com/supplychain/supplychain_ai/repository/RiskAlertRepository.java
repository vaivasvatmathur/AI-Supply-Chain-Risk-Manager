package com.supplychain.supplychain_ai.repository;

import com.supplychain.supplychain_ai.entity.RiskAlert;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RiskAlertRepository extends JpaRepository<RiskAlert, Long> {
}